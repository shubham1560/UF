from rest_framework import status

from .models import KbKnowledge, KbFeedback, m2m_knowledge_feedback_likes, BookmarkUserArticle, \
    KbUse, KbKnowledgeBase, KbCategory, KnowledgeSection
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from sys_user.models import SysUser
from django.db.models import F
from decouple import config
# from services.profanityservice import profanity_array
import binascii, os


def nest_comment(comments):
    # breakpoint()
    queue = []
    final = []
    counter = 0
    for i in comments:
        count = m2m_knowledge_feedback_likes.objects.filter(comment=i["id"]).count()
        i["likes"] = count
        i["visited"] = False
        if i["parent_comment_id"] is None:
            counter += 1
            queue.append(i)
    while queue:
        s = queue.pop(0)
        final.append(s)
        counter += 1
        final[-1]["child"] = []
        for j in comments:
            if j["parent_comment_id"] == s['id']:
                final[-1]["child"].append(j)
                queue.append(j)
    return final


def nest_categories(categories, moderator):
    queue = []
    final = []
    len_fin = 0
    # breakpoint()
    for category in categories:
        category["children"] = []
        if moderator:
            courses = KbCategory.objects.filter(parent_category=category['id'], course=True).count()
        else:
            courses = KbCategory.objects.filter(parent_category=category['id'], active=True, course=True).count()
        category["course_count"] = courses
        if category["parent_category"] is None:
            queue.append(category)
            len_fin += 1
    while queue:
        s = queue.pop(0)
        final.append(s)
        for category in categories:
            if category["parent_category"] == s['id']:
                final[-1]["children"].append(category)
                queue.append(category)
    final = final[:len_fin]
    return final


def if_bookmarked_by_user(article_id, user):
    article = KbKnowledge.objects.get(id=article_id)
    exist = BookmarkUserArticle.objects.filter(user=user, article=article)
    if exist.count() == 1:
        # Exist
        return True
    else:
        # doesn't exist
        return False


def bookmark_status(articles, user):
    fin_articles = []
    for article in articles:
        if article["featured_image_thumbnail"]:
            article["featured_image_thumbnail"] = str(config('S3URL')) + article["featured_image_thumbnail"]
        article["bookmarked"] = False

        a = KbKnowledge.objects.select_related('author', 'category', 'knowledge_base').get(id=article['id'])
        try:
            article["get_category"] = {
                'category_label': a.category.label,
                'id': a.category.id
            }
        except ObjectDoesNotExist:
            pass

        try:
            article["get_knowledge_base"] = {
                'knowledge_base': a.knowledge_base.title,
                'description': a.knowledge_base.description,
                'id': a.knowledge_base.id,
            }
        except ObjectDoesNotExist:
            pass

        try:
            article["getAuthor"] = {
                'first_name': a.author.first_name,
                "id": a.author.id_name,
                'last_name': a.author.last_name,
            }
        except ObjectDoesNotExist:
            pass
        if if_bookmarked_by_user(article["id"], user):
            article["bookmarked"] = True
        fin_articles.append(article)


def get_all_articles():
    articles = KbKnowledge.objects.all()
    return articles


def get_single_article(id, request):
    try:
        if request.user.groups.filter(name='Authors').exists():
            article = KbKnowledge.objects.get(id=id)
        else:
            article = KbKnowledge.objects.get(id=id, workflow='published')
        return article
    except ObjectDoesNotExist:
        pass


def get_comments(articleid: str):
    comments = KbFeedback.objects.filter(article=articleid).values('id', 'parent_comment_id', 'flagged', 'comments')
    # comments = KbFeedback.objects.filter(article=articleid).values()
    q = list(comments)
    a = nest_comment(q)
    result = {"model": list(a)}
    return result


def get_paginated_articles(start: int, end: int):
    articles = KbKnowledge.objects.all().order_by('-sys_created_on')[start:end]
    return articles


def get_articles_for_logged_in_user_with_bookmark(start: int, end: int, user):
    articles = KbKnowledge.objects.all().values('id',
                                                'title',
                                                'featured_image_thumbnail',
                                                'description',
                                                'author_id',
                                                'category',
                                                'knowledge_base'
                                                ).order_by('-sys_created_on')[start:end]

    a = list(articles)
    bookmark_status(a, user)
    result = {"data": list(a)}
    return result


# def get_user_bookmarked_articles_for_activity_tab(start, end):
#     result = get_articles_for_logged_in_user_with_bookmark(start, end)


def get_bookmarked_articles(user) -> BookmarkUserArticle:
    bookmarked_articles = BookmarkUserArticle.objects.filter(user=user)
    return bookmarked_articles


def bookmark_the_article(user, article_id):
    article = KbKnowledge.objects.get(id=article_id)
    exist = BookmarkUserArticle.objects.filter(user=user, article=article)
    if exist.count() == 1:
        exist.delete()
        return False
    else:
        a = BookmarkUserArticle()
        a.user = user
        a.article = article
        a.save()
        return True


def if_bookmarked_and_found_useful_by_user(user, article_id):
    article = KbKnowledge.objects.get(id=article_id)
    exist = BookmarkUserArticle.objects.filter(user=user, article=article)
    useful = KbUse.objects.get(article=article, user=user)
    if exist.count() == 1:
        return {"bookmarked": True, "found_useful": useful.useful}
    else:
        return {"bookmarked": False, "found_useful": useful.useful}


def kb_use(request):
    """
    Only concerned with the view
    """
    if request.data['useful'] == 'no_response':
        if request.user.is_anonymous:
            KbKnowledge.objects.filter(id=request.data['article']).update(view_count=F('view_count') + 1)
            return "viewed by anonymous user"
        else:
            article = KbKnowledge.objects.filter(id=request.data['article'])
            a = KbUse.objects.filter(
                user=request.user,
                article=article[0],
                viewed=True
            ).count()
            if a == 0:
                article.update(view_count_logged_in=F('view_count_logged_in') + 1)
                view = KbUse.objects.get_or_create(
                    user=request.user,
                    article=article[0],
                    course=article[0].section.course,
                    viewed=True,
                )
            return "viewed by logged in user"
    elif not request.user.is_anonymous:
        """
            Only when the user responds whether useful or not
        """
        if request.data['useful'] == 'true':
            article = KbKnowledge.objects.get(id=request.data['article'])
            view = KbUse.objects.get(
                user=request.user,
                article=article,
            )
            view.useful = True
            view.save()
            return "found useful by logged in user"
        elif request.data['useful'] == 'false':
            article = KbKnowledge.objects.get(id=request.data['article'])
            view = KbUse.objects.get(
                user=request.user,
                article=article,
            )
            view.useful = False
            view.save()
            return "didn't find it useful"
    else:
        return "non logged in user can't comment on the usefulness of the data"


def add_feedback(request, article_id):
    # breakpoint()
    try:
        KbUse.objects.update_or_create(
            article=KbKnowledge.objects.get(id=article_id),
            user=request.user,
            defaults={'feedback': request.data['feedback']}
        )
        return True
    except ObjectDoesNotExist:
        return False


def add_article(request, publish_ready, article_id=0):
    # breakpoint()
    try:
        # title = request.data['article']['blocks'][0]["data"]["text"]
        title = request.data['title']
        uid = binascii.hexlify(os.urandom(3)).decode()
        if article_id == '':
            a = KbKnowledge()
            a.id = uid
            a.knowledge_base, created = KbKnowledgeBase.objects.get_or_create(id="testing", active=False)
            a.category, created = KbCategory.objects.get_or_create(id="testing", active=False)
        else:
            try:
                a = KbKnowledge.objects.get(id=article_id)
            except ObjectDoesNotExist:
                return '1'
            if a.sys_created_by != request.user:
                return
        if not a.knowledge_base:
            a.knowledge_base, created = KbKnowledgeBase.objects.get_or_create(id="testing", active=False)
        if not a.category:
            a.category, created = KbCategory.objects.get_or_create(id="testing", active=False)
        if not a.workflow:
            a.workflow = "draft"
        a.article_url = title.lower().replace(" ", "-")
        a.description = request.data['description']
        a.title = title
        a.article_body = request.data['body_data']
        a.author = request.user
        a.sys_created_by = request.user
        if publish_ready:
            a.workflow = 'review'
        a.save()
    except ValidationError:
        return "Please add the heading to the article"
    return a.id


def get_course_section_and_articles(category, request):
    anonymous = request.user.is_anonymous
    if not anonymous:
        views = KbUse.objects.filter(user=request.user).values("viewed", "useful", "article")
    try:
        course = KbCategory.objects.get(id=category)
        sections = course.related_sections.all().values('id', 'label', 'order').order_by('order')
        results = list(sections)
        for result in results:
            result["articles"] = []
        for section in sections:
            children = KnowledgeSection.objects.get(id=section['id']).related_articles.filter \
                (workflow='published').values('id',
                                              'title', 'category', 'knowledge_base', 'section',
                                              'order', 'article_url').order_by('order')

            for child in children:
                for section in sections:
                    if section["id"] == child["section"]:
                        if not anonymous:
                            child["viewed"] = False
                            for view in views:
                                if child["id"] == view["article"]:
                                    child["viewed"] = True
                        section["articles"].append(child)
    except ObjectDoesNotExist:
        return False
    return sections, {"label": course.label, "description": course.description}

    # Previously Working code

    # anonymous = request.user.is_anonymous
    # if not anonymous:
    #     views = KbUse.objects.filter(user=request.user).values("viewed", "useful", "article")
    # # breakpoint()
    # try:
    #     # breakpoint()
    #     course = KbCategory.objects.get(id=category)
    #     sections = course.parent_of_category.all().values("id", "label", "order").order_by('order')
    #     results = list(sections)
    #     for result in results:
    #         result["articles"] = []
    #     for section in sections:
    #         children = KbCategory.objects.get(id=section["id"]).article_category.all().values("id",
    #                                                                                           "title",
    #                                                                                           'category',
    #                                                                                           'knowledge_base',
    #                                                                                           ).order_by('order')
    #         for child in children:
    #             for section in sections:
    #                 if section["id"] == child["category"]:
    #                     if not anonymous:
    #                         child["viewed"] = False
    #                         for view in views:
    #                             if child["id"] == view["article"]:
    #                                 child["viewed"] = True
    #                     section["articles"].append(child)
    # except ObjectDoesNotExist:
    #     return False
    #     # breakpoint()
    # # breakpoint()
    # return sections, course.label


# def get_course_section_and_articles_for_logged_in_user(category, request):
# breakpoint()
# sections, course = get_course_section_and_articles(category)
# views = KbUse.objects.filter(user=request.user).values("viewed", "useful", "article")
# return sections, course

def adding_recursive_category(category: KbCategory, label_array, id_array, description_array):
    # breakpoint()
    label_array.append(category.label)
    id_array.append(category.id)
    description_array.append(category.description)
    if not category.parent_category:
        return
    # breakpoint()
    if category.parent_category:
        parent = KbCategory.objects.get(id=category.parent_category.id)
        adding_recursive_category(parent, label_array, id_array, description_array)


def get_breadcrumb_category(category):
    crumb_label = []
    crumb_id = []
    crumb_desc = []
    adding_recursive_category(category, crumb_label, crumb_id, crumb_desc)
    # breakpoint()
    crumb_id.reverse()
    crumb_label.reverse()
    crumb_desc.reverse()
    result = {"crumb_id": crumb_id, "crumb_label": crumb_label, "crumb_desc": crumb_desc}
    # breakpoint()
    return result


def set_progress_course_kbuse(request):
    progress = request.data['progress']
    try:
        course = KbCategory.objects.get(id=request.data['course'], active=True)
        use, boolean = KbUse.objects.get_or_create(course=course, user=request.user, article__isnull=True)
        use.percentage_completed = progress
        use.save()
        return True
    except ObjectDoesNotExist:
        return False


def get_categories_tree(kb_base, request):
    moderator = False
    if request.user.groups.filter(name="Moderators").exists():
        moderator = True
    if moderator:
        categories = KbKnowledgeBase.objects.get(id=kb_base).related_categories. \
            filter(course=False, section=False).values('id',
                                                       'parent_kb_base',
                                                       'parent_category',
                                                       'label').order_by('order')
    else:
        categories = KbKnowledgeBase.objects.get(id=kb_base).related_categories. \
            filter(course=False, section=False, active=True).values('id',
                                                                    'parent_kb_base',
                                                                    'parent_category',
                                                                    'label').order_by('order')

    nested_categories = nest_categories(list(categories), moderator)
    return list(nested_categories)
    # breakpoint()


def get_articles(query):
    return


def get_courses(query):
    return


def add_article_to_course(request):
    article_id = request.data['article_id']
    course_id = request.data['course_id']
    # breakpoint()
    try:
        course = KbCategory.objects.get(id=course_id, course=True, active=True)
        section, created = KnowledgeSection.objects.get_or_create(
            label="Individual Articles",
            course=course,
            order=100000
        )
        article = KbKnowledge.objects.get(id=article_id)
        article.workflow = "published"
        article.section = section
        article.category = course
        article.knowledge_base = course.parent_kb_base
        article.save()
        return True
    except ObjectDoesNotExist:
        return False
    # pass


def add_path_or_branch(request):
    # breakpoint()
    a = KbCategory()

    a.label = request.data["form_data"]["title"]
    a.id = a.label.lower().replace(" ", "-") + "-" + binascii.hexlify(os.urandom(2)).decode()
    a.description = request.data["form_data"]["description"]
    a.active = request.data["form_data"]["active"]
    # a.parent_kb_base =
    if request.data['type']['add'] == 'course':
        a.course = True
    a.parent_kb_base = KbKnowledgeBase.objects.get(id=request.data["type"]["kb_base"])
    if request.data['type']['kb_category'] != 'root':
        a.parent_category = KbCategory.objects.get(id=request.data['type']['kb_category'])
    # breakpoint()
    a.sys_created_by = request.user
    a.save()
    return a
    # pass


def edit_path_or_branch(request):
    try:
        category = KbCategory.objects.get(id=request.data["type"]["product"]["id"])
        category.label = request.data["form_data"]["title"]
        category.description = request.data["form_data"]["description"]
        category.active = request.data["form_data"]["active"]
        category.save()

        if not category.active:
            KbUse.objects.filter(course=category).update(active=False)

        if category.active:
            KbUse.objects.filter(course=category).update(active=True)

    except KeyError:
        pass
    # breakpoint()


def build_path(request):
    try:
        course = KbCategory.objects.get(id=request.data["course"])
        if course.sys_created_by == request.user:
            path = request.data["path"]
            for section in path:
                try:
                    if section["id"]:
                        change_section = KnowledgeSection.objects.get(id=section["id"])
                except KeyError:
                    change_section = KnowledgeSection()
                change_section.label = section["label"]
                if section["label"] != "Individual Articles":
                    change_section.order = section["order"]
                change_section.course = course
                change_section.save()

                for article in section["articles"]:
                    get_article = KbKnowledge.objects.get(id=article["id"])
                    get_article.order = article["order"]
                    get_article.section = change_section
                    get_article.save()
                    # articles.append(article)
            return {"message": "Path created successfully!", "status": status.HTTP_201_CREATED}
        else:
            return {"message": "The user is not the owner of the course!", "status": status.HTTP_401_UNAUTHORIZED}
    except ObjectDoesNotExist:
        return {"message": "The path does not exist", "status": status.HTTP_404_NOT_FOUND}
    # breakpoint()
    # pass


def delete_sections(section_ids_to_delete):
    for del_id in section_ids_to_delete:
        section = KnowledgeSection.objects.get(id=del_id)
        section.delete()
    # pass


def course_owner(course, request):
    # breakpoint()
    try:
        course = KbCategory.objects.get(id=course)
        if request.user == course.sys_created_by:
            return {"owner": True, "course": course.label, "status": status.HTTP_200_OK}
        else:
            return {"owner": False, "course": "", "status": status.HTTP_200_OK}
    except ObjectDoesNotExist:
        return {"owner": False, "status": status.HTTP_404_NOT_FOUND}


def delete_article(article_id, request):
    try:
        article = KbKnowledge.objects.get(id=article_id)
        if article.author == request.user:
            article.delete()
            response = {
                "message": 'article deleted succesfully',
                "status": status.HTTP_200_OK,
                "deleted": True
            }
        else:
            response = {
                "message": 'the user is not the owner of the article',
                "status": status.HTTP_401_UNAUTHORIZED,
                "deleted": False
            }
    except ObjectDoesNotExist:
        response = {
            "message": 'Article with this id does not exist',
            "status": status.HTTP_404_NOT_FOUND,
            "deleted": False
        }
    return response


def get_profanity_matrix(request):
    text_array = extract_array_from_article_body_json(request.data['data'])
    # result, profane = profanity_array(text_array)

    # call the profanity service
    return {"result": "", "profane": False}


def extract_array_from_article_body_json(article_body):
    text_array = []
    for text in article_body:
        if text['type'] == 'header':
            text_array.append(text['data']['text'])
        if text['type'] == 'list':
            text_array.append(text['data']['items'][0])
        if text['type'] == 'paragraph':
            text_array.append(text['data']['text'])
    return text_array


def add_order_to_courses(request):
    # breakpoint()
    for course in request.data:
        try:
            category = KbCategory.objects.get(id=course['id'])
            category.order = course["order"]
            category.save()
        except ObjectDoesNotExist:
            pass
    # pass