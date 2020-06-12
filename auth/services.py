from sys_user.models import SysUser


def get_all_users() -> SysUser:
    result = SysUser.objects.all()
    return result


def get_user(id:int) -> SysUser:
    result = SysUser.objects.get(id=id)
    return result



