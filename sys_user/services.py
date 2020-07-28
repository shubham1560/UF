from .models import SysUser


def remove_user():
    pass


def get_user_activity(request):
    user = request.user
    activity = user.user_activity.all().values('user', 'course', 'article', 'viewed', 'useful', 'percentage_completed')
    return list(activity)
