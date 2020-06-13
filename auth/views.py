from django.shortcuts import render
from rest_framework import viewsets
from sys_user.models import SysUser
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import get_all_users, get_user, create_user, create_google_user, activate_account, reset_password
from rest_framework import serializers
from rest_framework import status
# Create your views here.


class UserListViewSet(APIView):
    class UserListSerializer(serializers.ModelSerializer):
        class Meta:
            model = SysUser
            fields = ('id', 'email', 'profile_pic')

    def get(self, request, format=None):
        users = get_all_users()
        serializer = self.UserListSerializer(users, many=True)
        return Response(serializer.data)


class UserViewSet(APIView):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = SysUser
            fields = ('id', 'email', 'profile_pic')

    def get(self, request, id, format=None):
        a = get_user(id)
        serializer = self.UserSerializer(a, many=False)  # for a single result, many should be ommited or False
        return Response(serializer.data)


class CreateUserViewSet(APIView):
    class CreateUserSerializer(serializers.ModelSerializer):
        username = serializers.EmailField()
        password = serializers.CharField(
            style={'input_type': 'password'}
        )
        first_name = serializers.CharField(max_length=50)
        last_name = serializers.CharField(max_length=50)
        # id = serializers.IntegerField()

        class Meta:
            model = SysUser
            fields = ('username', 'password', 'first_name', 'last_name')

    def post(self, request, format=None):
        serializer = self.CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_user(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class CreateGoogleUserViewSet(APIView):
    class CreateGoogleUserSerializer(serializers.ModelSerializer):
        username = serializers.EmailField()
        profile_pic = serializers.URLField()
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        # id = serializers.IntegerField()

        class Meta:
            model = SysUser
            fields = ('username', 'profile_pic', 'first_name', 'last_name',)

    def post(self, request, format=None):
        serializer = self.CreateGoogleUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_google_user(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class ActivateAccountViewSet(APIView):
    class ActivateAccountSerializer(serializers.ModelSerializer):
        token = serializers.CharField()

    class Meta:
        model = Token

    def get(self, request, token, format=None):
        activate_account(token)
        return Response(status=status.HTTP_200_OK)


class UserPasswordResetViewSet(APIView):
    class UserPasswordResetSerializer(serializers.ModelSerializer):
        password = serializers.CharField(
            style={'input_type': 'password'}
        )

        class Meta:
            model = SysUser
            fields = ('password',)

    def post(self, request, token, format=None):
        serializer = self.UserPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # print(request.data)
        # print(token)
        reset_password(token=token, **serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)


# class UserViewSet(viewsets.ModelViewSet):
#    queryset = SysUser.objects.all()
#    serializer_class = UserSerializer
