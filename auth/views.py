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
        last_name = serializers.CharField(max_length=50)

        class Meta:
            model = SysUser
            fields = ('username', 'password', 'first_name', 'last_name')

    @log_request
    def post(self, request, format=None):
        serializer = self.CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_root_user(**serializer.validated_data)
        response = {'message': 'user has been created'}
        return Response(response, status=status.HTTP_201_CREATED)


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
        if request.data.get("access_token") not in cache:
            print("executing")
            print(request.data.get('access_token'))
            cache.set(request.data.get("access_token"), 1, timeout=300)
        cache.incr(request.data.get("access_token"), delta=1)
        called = cache.get(request.data.get("access_token"))
        print(called)
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
            response = {"message": "The password has been reset, you can log in now"}
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {"message": "The Url is invalid"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetLinkViewSet(APIView):

    @log_request
    def post(self, request, format=None):
        email = request.data.get("email")
        try:
            user = SysUser.objects.get(email=email)
        except ObjectDoesNotExist:
            response = {'message': "User with this email doesn't exist"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        try:
            token = Token.objects.get(user=user)
        except ObjectDoesNotExist:
            response = {'message': "Token doesn't exist for the user"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        send_reset_link(email=email, _token=str(token))
        response = {'message': 'Reset Link has been sent'}
        return Response(response, status=status.HTTP_200_OK)


class ObtainAuthTokenViewSet(APIView):
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
        key = 'login'+request.data.get('username')
        if key not in cache:
            cache.set(key, 1)
        cache.incr(key, delta=1)
        print(cache.get(key))
        print(request)
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=False):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'message': "Wrong Credentials for logging in"}, status=status.HTTP_404_NOT_FOUND)


