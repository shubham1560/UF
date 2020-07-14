from sys_user.models import SysUser
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import get_all_users, get_user, create_root_user, activate_account, reset_password,\
    send_reset_link
from rest_framework import serializers
from rest_framework import status
from django.conf import settings
from django.core.cache import cache
from logs.services import log_request
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache.backends.base import DEFAULT_TIMEOUT
import requests
import json
from rest_framework import parsers, renderers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from logs.services import log_random
from services.cacheservice import rate_limit


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
# Create your views here.


class UserListViewSet(APIView):
    class UserListSerializer(serializers.ModelSerializer):
        class Meta:
            model = SysUser
            fields = ('id', 'email', 'profile_pic')

    @log_request
    def get(self, request, format=None):
        # breakpoint()
        if 'allusers' in cache:
            users = cache.get('allusers')
        else:
            users = get_all_users()
            print("From db")
            log_random.delay(str(users), 'bhanu')
            cache.set('allusers', users)
        serializer = self.UserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(APIView):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = SysUser
            fields = ('id', 'email', 'profile_pic')

    @log_request
    def get(self, request, id, format=None):
        a = get_user(id)
        if a:
            serializer = self.UserSerializer(a, many=False)  # for a single result, many should be ommited or False
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        response = {'message': 'User with this id: '+str(id)+' does not exist in the database'}
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


class CreateUserViewSet(APIView):
    class CreateUserSerializer(serializers.ModelSerializer):
        username = serializers.EmailField()
        password = serializers.CharField(
            style={'input_type': 'password'}
        )
        first_name = serializers.CharField(max_length=50)
        last_name = serializers.CharField(max_length=50, required=False, allow_blank=True)

        class Meta:
            model = SysUser
            fields = ('username', 'password', 'first_name', 'last_name')

    @log_request
    def post(self, request, format=None):
        # breakpoint()
        serializer = self.CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if create_root_user(**serializer.validated_data):
            response = {'message': 'user has been created'}
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {'message': 'User Already Exists, please log in after you have activated the account', 'ue': True}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CreateGoogleUserViewSet(APIView):
    class CreateGoogleUserSerializer(serializers.ModelSerializer):
        username = serializers.EmailField()
        profile_pic = serializers.URLField()
        first_name = serializers.CharField()
        last_name = serializers.CharField()

        class Meta:
            model = SysUser
            fields = ('username', 'profile_pic', 'first_name', 'last_name',)

    @log_request
    def post(self, request, format=None):
        payload = {'access_token': request.data.get("access_token")}
        r = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            content = {'message': 'wrong google token/ this token is already expired or you may be trying to pull of an'
                                  ' attack'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            user = SysUser.objects.get(email=data['email'])
        except SysUser.DoesNotExist:
            user = SysUser()
            user.username = data['email']
            user.profile_pic = data['picture']
            user.email = data['email']
            user.first_name = data['given_name']
            user.last_name = data['family_name']
            user.user_type = "GU"
            user.id_name = data['email'].split('@')[0]
            user.save()

        token, created = Token.objects.get_or_create(user=user)
        response = {'username': user.username, 'token': str(token)}
        return Response(response, status=status.HTTP_201_CREATED)


class ActivateAccountViewSet(APIView):
    class ActivateAccountSerializer(serializers.ModelSerializer):
        token = serializers.CharField()

    class Meta:
        model = Token

    @log_request
    def get(self, request, token, format=None):
        if activate_account(token):
            response = {"Message": "The account has been activated, you can log in now"}
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {"Message": "The url is invalid"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class UserPasswordResetViewSet(APIView):
    class UserPasswordResetSerializer(serializers.ModelSerializer):
        password = serializers.CharField(
            style={'input_type': 'password'}
        )

        class Meta:
            model = SysUser
            fields = ('password',)

    @log_request
    def post(self, request, token, format=None):
        serializer = self.UserPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if reset_password(token=token, **serializer.validated_data):
            response = {"url_valid": True, "message": "The password has been reset, you can log in now"}
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {"url_valid": False, "message": "The Url is invalid"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetLinkViewSet(APIView):

    @log_request
    def post(self, request, format=None):
        email = request.data.get("email")
        try:
            user = SysUser.objects.get(email=email)
            active = user.is_active
        except ObjectDoesNotExist:
            response = {'user_exist': False, "is_active": False}
            r_status = status.HTTP_404_NOT_FOUND
            return Response(response, status=r_status)
        try:
            token = Token.objects.get(user=user)
        except ObjectDoesNotExist:
            response = {"token_exist": False, "user_exist": True, "message": "Please check for the token creation"}
            r_status = status.HTTP_404_NOT_FOUND
            return Response(response, status=r_status)
        if active:
            send_reset_link(email=email, _token=str(token))
            response = {'reset_link_sent': True, 'email': email}
            r_status = status.HTTP_200_OK
        else:
            response = {'user_exist': True, "is_active": False, "message": "User exists but is not active"}
            r_status = status.HTTP_400_BAD_REQUEST
        return Response(response, status=r_status)


class ObtainAuthTokenViewSet(APIView):
    """
    this has been re written to make the user to stop after 3 failed login attempts using
    cache
    """

    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    @log_request
    def post(self, request, *args, **kwargs):
        try:
            """
            logic for rate limiting the user on login attempt
            """
            key = 'login.'+request.data.get('username')
            login_attempt = rate_limit(key, timeout=2)
            if login_attempt > 3:
                return Response({'too many login attempts, please try again after 2 minutes'},
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except ObjectDoesNotExist:
            pass
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            try:
                token = Token.objects.get(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'message': "invalid login credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserTokenValidViewSet(APIView):

    def get(self, request, token, format=None):

        """
        :param request: gets the request
        :param token: token is passed from the url to check the validity
        :param format: None
        :return: Response if the user exists or not and is exist, whether he is active or not
        """

        try:
            user = Token.objects.get(key=token).user
            if user.is_active:
                return Response({"user_exist": True, "is_active": user.is_active}, status=status.HTTP_200_OK)
            else:
                return Response({"user_exist": True, "is_active": user.is_active}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"user_exist": False, "message": "No user with this link valid exists"},
                            status=status.HTTP_404_NOT_FOUND)


class GetUserDetailFromTokenViewSet(APIView):
    class GetUserDetailFromTokenSerializer(serializers.ModelSerializer):
        class Meta:
            model = SysUser
            fields = ('id_name', 'first_name', 'last_name', 'profile_pic', 'profile', 'header_image')

    def get(self, request, format=None):
        serializer = self.GetUserDetailFromTokenSerializer(request.user, many=False)
        response = {'user': serializer.data}
        return Response(response, status=status.HTTP_200_OK)