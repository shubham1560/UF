from sys_user.models import SysUser
import string
import random


def get_all_users() -> SysUser:
    result = SysUser.objects.all()
    return result


def get_user(id: int) -> SysUser:
    result = SysUser.objects.get(id=id)
    return result


def create_user(**validated_data) -> SysUser:
    print(validated_data)
    res = int(''.join(random.choices(string.digits, k=100)))
    uid = validated_data['username'].split('@')[0]+res
    SysUser.objects.create_user(**validated_data, email=validated_data['username'], id=uid)




