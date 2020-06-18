from sys_user.models import SysUser
import string
import random
from rest_framework.authtoken.models import Token
from decouple import config
from emails.services import send_confirmation_mail, promotion_mail


def get_all_users() -> SysUser:
    result = SysUser.objects.all()
    return result


def get_user(id: int) -> SysUser:
    result = SysUser.objects.get(id=id)
    return result


def create_user(**validated_data) -> SysUser:
    user = SysUser.objects.create_user(**validated_data,
                                       email=validated_data['username'],
                                       is_active=False,
                                       user_type="RU")
    token = Token.objects.create(user=user)
    send_confirmation_mail.delay(email=validated_data['username'], token=str(token))


def create_google_user(**validated_data) -> SysUser:
    res = generate_id()

    user_exist = SysUser.objects.get(email=validated_data['username'])

    if user_exist:
        token = Token.objects.get(user=user_exist)
        print("User Exist")

    else:
        user = SysUser.objects.create_user(**validated_data,
                                           email=validated_data['username'],
                                           id=res,
                                           is_active=True,
                                           user_type="GU")
        token, _ = Token.objects.get_or_create(user=user)
        print("User doesn't exist")
    return token


def activate_account(token: str):
    user = Token.objects.get(key=token).user
    user.is_active = True
    user.save()


def reset_password(token: str, **validated_data):
    password = validated_data["password"]
    print(password, token)
    user = Token.objects.get(key=token).user
    user.set_password(password)
    user.save()



