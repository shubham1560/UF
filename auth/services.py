from sys_user.models import SysUser
import string
import random
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail


def generate_id():
    n = random.randint(3, 9)
    res = res = int(''.join(random.choices(string.digits, k=n)))
    return res


def send_confirmation_mail(email: str):
    send_mail("account created", "Your account has been created", 'avij1560@gmail.com', [email, ], fail_silently=False)


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
                                       is_active=False)
    Token.objects.create(user=user)
    send_confirmation_mail(email=validated_data['username'])


def create_google_user(**validated_data) -> SysUser:
    res = generate_id()

    user = SysUser.objects.create_user(**validated_data,
                                       email=validated_data['username'],
                                       id=res,
                                       is_active=True)
    token, _ = Token.objects.get_or_create(user=user)
    print(token)



