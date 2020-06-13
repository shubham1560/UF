from sys_user.models import SysUser
import string
import random
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from decouple import config


def generate_id():
    n = random.randint(3, 9)
    res = res = int(''.join(random.choices(string.digits, k=n)))
    return res


def send_confirmation_mail(email: str, token: str):
    link = config('URL')+"authorization/activate_account/"+token
    send_mail("account created",
              "Your account has been created"+
              "click this link: " + link,
              'avij1560@gmail.com',
              [email, ],
              fail_silently=False)


def get_all_users() -> SysUser:
    result = SysUser.objects.all()
    return result


def get_user(id: int) -> SysUser:
    result = SysUser.objects.get(id=id)
    return result


def create_user(**validated_data) -> SysUser:
    res = generate_id()
    user = SysUser.objects.create_user(**validated_data,
                                       email=validated_data['username'],
                                       id=res,
                                       is_active=False,
                                       user_type="RU")
    token = Token.objects.create(user=user)
    print(token)
    send_confirmation_mail(email=validated_data['username'],
                           token=str(token))


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



