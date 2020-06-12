from django.shortcuts import render
from rest_framework import viewsets
from sys_user.models import SysUser
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import get_users
# Create your views here.


class UserListViewSet(APIView):
    def get(self, request, format=None):
        users = get_users()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = SysUser.objects.all()
    serializer_class = UserSerializer
