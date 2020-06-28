from sys_user.models import SysUser
from rest_framework.authtoken.models import Token
from emails.services import send_confirmation_mail, send_password_reset_link
from django.core.exceptions import ObjectDoesNotExist


def get_all_users() -> SysUser:
    result = SysUser.objects.all()
    return result


def get_user(id: int) -> SysUser:
    result = SysUser.objects.get(id=id)
    return result


def create_root_user(**validated_data) -> SysUser:
    user = SysUser.objects.create_user(**validated_data,
                                       email=validated_data['username'],
                                       is_active=False,
                                       user_type="RU")
    token = Token.objects.create(user=user)
    send_confirmation_mail.delay(email=validated_data['username'], token=str(token))


def activate_account(token: str):
    try:
        current_token = Token.objects.get(key=token)
    except ObjectDoesNotExist:
        return False
    user = current_token.user
    user.is_active = True
    user.save()
    current_token.delete()
    Token.objects.create(user=user)
    return True


def reset_password(token: str, **validated_data):
    password = validated_data["password"]
    try:
        current_token = Token.objects.get(key=token)
    except ObjectDoesNotExist:
        return False
    user = current_token.user
    user.set_password(password)
    user.save()
    current_token.delete()
    Token.objects.create(user=user)
    return True


def send_reset_link(email: str):
    if send_password_reset_link(email) is False:
        return False
    return True



