from .models import SysUser, SubscriptionList
from decouple import config
from django.core.exceptions import ObjectDoesNotExist
import re

def remove_user():
    pass

# Make a regular expression
# for validating an Email
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


# for custom mails use: '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

# Define a function for
# for validating an Email
def check(email):
    # pass the regular expression
    # and the string in search() method
    if re.search(regex, email):
        return True
    else:
        return False


def add_subscriber(request):
    # breakpoint()
    if check(request.data['email']):
        email_exist = SubscriptionList.objects.filter(email=request.data['email'])
        if email_exist:
            return {"status": "Email already exists", "value": False}
        try:
            email_list = SubscriptionList()
            email_list.email = request.data['email']
            email_list.save()
            return {"status": "Entered to the subscriber's list", "value": True}
        except ObjectDoesNotExist:
            return False
    else:
        return {"status": "Invalid Email Address"}


def get_user_activity(request, requested_tye, start, end):
    # print("inside-job")
    user = request.user
    # print(user)
    # breakpoint()
    # breakpoint()
    if not user.is_anonymous:
        if requested_tye == 'courses':
            activities = user.user_activity.select_related(
                'article',
                'course').exclude(course__isnull=True).order_by('-sys_updated_on')[start:end]
        if requested_tye == 'articles':
            activities = user.user_activity.select_related(
                'article',
                'course').exclude(article__isnull=True).order_by('-sys_updated_on')[start:end]
        # breakpoint()
        related_activities = [None]*len(activities)
        counter = 0
        for activity in activities:
            related_activities[counter] = {
                "id": activity.id or '',
                "viewed": activity.viewed or '',
                "useful": activity.useful or '',
                "progress": activity.percentage_completed or '',
                "created_on": activity.sys_created_on or '',
            }
            if activity.course and activity.course.active:
                related_activities[counter]["course"] = {
                    "id": activity.course.id or '',
                    "label": activity.course.label or '',
                    "description": activity.course.description or '',
                    "compressed_image": config("S3URL") + str(activity.course.compressed_image) or '',
                    "knowledge_base": activity.course.parent_kb_base.title or '',
                    # "parent_kb_base": activity.course.parent_kb_base,
                }

            elif activity.article and activity.article.active:
                related_activities[counter]["article"] = {
                    "id": activity.article.id or '',
                    "featured_image_thumbnail": config('S3URL')+str(activity.article.featured_image_thumbnail),
                    "title": activity.article.title or '',
                    "description": activity.article.description or '',
                    "view_count": activity.article.view_count or '',
                    "view_count_logged_in": activity.article.view_count_logged_in or '',
                    "course_id": activity.article.section.course.id or '',
                    "course_name": activity.article.section.course.label or '',
                    # "knowledge_base": activity.article.category.parent_kb_base.title or '',
                    # "thumbnail": activity.article.
                }
            counter += 1
        # breakpoint()
        # print(related_activities)
        return list(related_activities)


def is_developer(code, username):
    try:
        user = SysUser.objects.get(facebook_id=code, username="admin")
        if user:
            if user.groups.filter(name='Developers').exists():
                return True
    except ObjectDoesNotExist:
        return False
    return False
