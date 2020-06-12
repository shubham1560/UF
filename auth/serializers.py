from rest_framework import serializers
from sys_user.models import SysUser
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysUser
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = SysUser.objects.create_user(**validated_data)
        token = Token.objects.create(user=user)
        return user
