from sys_user.models import SysUser
from rest_framework.authtoken.models import Token
from emails.services import send_confirmation_mail, send_password_reset_link
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from logs.services import log_random


def get_all_users() -> SysUser:
    result = SysUser.objects.all()
    return result


def get_user(id_name: str) -> SysUser:
    try:
        key = 'user.'+id_name
        if key in cache:
            result = cache.get(key)
            print("from cache")
        else:
            result = SysUser.objects.get(id_name=id_name)
            cache.set(key, result, timeout=300)
            print("from db")
    except ObjectDoesNotExist:
        result = False
    return result


def create_root_user(**validated_data) -> SysUser:
    try:
        user = SysUser.objects.create_user(**validated_data,
                                           email=validated_data['username'],
                                           is_active=False,
                                           user_type="RU",
                                           id_name='@'+validated_data['username'].split('@')[0])
        token = Token.objects.create(user=user)
        try:
            send_confirmation_mail(username=user.first_name, email=validated_data['username'], token=str(token))
        except ObjectDoesNotExist:
            log_random("The mail is not reaching, check if the mail exists or not, the mailing is failing")
            return False
        return True
    except Exception as e:
        return False


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


def send_reset_link(email: str, _token: str):
    send_password_reset_link.delay(email=email, token=_token)




