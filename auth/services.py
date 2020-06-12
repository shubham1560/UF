from sys_user.models import SysUser


def get_users() -> SysUser:
    result = SysUser.objects.all()
    return result



