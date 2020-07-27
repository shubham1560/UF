from .models import KbKnowledge, KbFeedback, m2m_knowledge_feedback_likes, BookmarkUserArticle,\
     KbUse, KbKnowledgeBase, KbCategory
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from sys_user.models import SysUser
from django.db.models import F
from decouple import config
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
            article["featured_image_thumbnail"] = str(config('S3URL'))+article["featured_image_thumbnail"]
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


def get_single_article(id):
    try:
        article = KbKnowledge.objects.get(id=id)
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
            KbKnowledge.objects.filter(id=request.data['article']).update(view_count=F('view_count')+1)
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


def add_article(request, articleid=0):
    uid = request.data["title"].lower().replace(" ", "-") + "-" + binascii.hexlify(os.urandom(4)).decode()
    if articleid == 0:
        a = KbKnowledge()
        a.id = uid
    else:
        a = KbKnowledge.objects.get(id=articleid)
    a.title = request.data["title"]
    a.article_body = request.data["article_body"]
    a.featured_image = request.data["featured_image"]
    a.description = request.data["description"]
    a.author = request.user
    a.workflow = "draft"
    a.knowledge_base = KbKnowledgeBase.objects.get(id="testing")
    a.save()
    print(request)


def get_course_section_and_articles(category, request):
    anonymous = request.user.is_anonymous
    if not anonymous:
        views = KbUse.objects.filter(user=request.user).values("viewed", "useful", "article")
    try:
        course = KbCategory.objects.get(id=category)
        sections = course.parent_of_category.all().values("id", "label", "order").order_by('order')
        results = list(sections)
        for result in results:
            result["articles"] = []
        for section in sections:
            children = KbCategory.objects.get(id=section["id"]).article_category.all().values("id",
                                                                                              "title",
                                                                                              'category'
                                                                                              ).order_by('order')
            for child in children:
                for section in sections:
                    if section["id"] == child["category"]:
                        if not anonymous:
                            child["viewed"] = False
                            for view in views:
                                if child["id"] == view["article"]:
                                    child["viewed"] = True
                        section["articles"].append(child)
    except ObjectDoesNotExist:
        return False
        # breakpoint()
    return sections, course.label


# def get_course_section_and_articles_for_logged_in_user(category, request):
    # breakpoint()
    # sections, course = get_course_section_and_articles(category)
    # views = KbUse.objects.filter(user=request.user).values("viewed", "useful", "article")
    # return sections, course

def adding_recursive_category(category: KbCategory, label_array, id_array):
    # breakpoint()
    label_array.append(category.label)
    id_array.append(category.id)
    if not category.parent_category:
        return
    # breakpoint()
    if category.parent_category:
        parent = KbCategory.objects.get(id=category.parent_category.id)
        adding_recursive_category(parent, label_array, id_array)


def get_breadcrumb_category(category):
    crumb_label = []
    crumb_id = []
    adding_recursive_category(category, crumb_label, crumb_id)
    # breakpoint()
    crumb_id.reverse()
    crumb_label.reverse()
    result = {"crumb_id": crumb_id, "crumb_label": crumb_label}
    # breakpoint()
    return result


def set_progress_course_kbuse(request):
    progress = request.data['progress']
    try:
        course = KbCategory.objects.get(id=request.data['course'])
        use, boolean = KbUse.objects.get_or_create(course=course, user=request.user)
        use.percentage_completed = progress
        use.save()
        return True
    except ObjectDoesNotExist:
        return False
    # pass
