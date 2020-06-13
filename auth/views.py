from django.shortcuts import render
from rest_framework import viewsets
from sys_user.models import SysUser
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import get_all_users, get_user, create_user
from rest_framework import serializers
from rest_framework import status
# Create your views here.


class UserListViewSet(APIView):
    class UserListSerializer(serializers.ModelSerializer):
        class Meta:
            model = SysUser
            fields = ('email','profile_pic')

    def get(self, request, format=None):
        users = get_all_users()
        serializer = self.UserListSerializer(users, many=True)
        return Response(serializer.data)


class UserViewSet(APIView):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = SysUser
            fields = ('email', 'profile_pic')

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
        # id = serializers.IntegerField()

        class Meta:
            model = SysUser
            fields = ('username', 'password')

    def post(self, request, format=None):
        serializer = self.CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_user(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


# class UserViewSet(viewsets.ModelViewSet):
#    queryset = SysUser.objects.all()
#    serializer_class = UserSerializer
