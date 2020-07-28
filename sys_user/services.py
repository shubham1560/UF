from .models import SysUser
from decouple import config

def remove_user():
    pass


def get_user_activity(request):
    user = request.user
    activities = user.user_activity.select_related(
        'article',
        'course').all().order_by('-sys_created_on')
    # breakpoint()
    related_activities = [None]*len(activities)
    counter = 0
    for activity in activities:
        related_activities[counter] = {
            "id": activity.id,
            "viewed": activity.viewed,
            "useful": activity.useful,
            "progress": activity.percentage_completed,
            "created_on": activity.sys_created_on
        }
        if activity.course and activity.course.active:
            related_activities[counter]["course"] = {
                "id": activity.course.id,
                "label": activity.course.label,
                "description": activity.course.description,
                "compressed_image": config("S3URL") + str(activity.course.compressed_image),
                # "parent_kb_base": activity.course.parent_kb_base,
            }

        elif activity.article and activity.article.active:
            related_activities[counter]["article"] = {
                "id": activity.article.id,
                # "featured_image_thumbnail": activity.article.featured_image_thumbnail,
                "title": activity.article.title,
                "description": activity.article.description,
                "view_count": activity.article.view_count,
                "view_count_logged_in": activity.article.view_count_logged_in,
                # "category": activity.article.category,
            }
        counter += 1
    # breakpoint()
    return list(related_activities)
