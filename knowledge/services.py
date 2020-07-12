from .models import KbKnowledge, KbFeedback, m2m_knowledge_feedback_likes, BookmarkUserArticle,\
    KbCategory, KbKnowledgeBase
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from sys_user.models import SysUser
from decouple import config


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
    # breakpoint()
    fin_articles = []
    type(articles)

    counter = 0
    for article in articles:
        if article["featured_image_thumbnail"]:
            article["featured_image_thumbnail"] = str(config('S3URL'))+article["featured_image_thumbnail"]
        article["bookmarked"] = False



        try:
            category = KbCategory.objects.get(id=article["category"])
            article["get_category"] = {
                'category_label': category.label,
                'id': category.id
            }
        except ObjectDoesNotExist:
            pass

        try:
            knowledge_base = KbKnowledgeBase.objects.get(id=article["knowledge_base"])
            article["get_knowledge_base"] = {
                'knowledge_base': knowledge_base.title,
                'description': knowledge_base.description,
                'id': knowledge_base.id,
            }
        except ObjectDoesNotExist:
            pass

        try:
            author = SysUser.objects.get(id=article["author_id"])
            article["getAuthor"] = {
                'first_name': author.first_name,
                "id": author.id_name,
                'last_name': author.last_name,
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
    comments = KbFeedback.objects.filter(article=articleid).values('id', 'parent_comment_id', 'flagged')
    # comments = KbFeedback.objects.filter(article=articleid).values()
    q = list(comments)
    a = nest_comment(q)
    result = {"model": list(a)}
    return result


def get_paginated_articles(start: int, end: int):
    articles = KbKnowledge.objects.all().order_by('-sys_created_on')[start:end]
    # a = list(articles)
    # user = SysUser.objects.get(id=225)
    # bookmark_status(a, user)
    # result = {"model": list(a)}
    return articles


def get_articles_for_logged_in_user_with_bookmark(start: int, end: int, user):
    articles = KbKnowledge.objects.all().values('id',
                                                'title',
                                                'featured_image_thumbnail',
                                                'description',
                                                'author_id',
                                                'category',
                                                'knowledge_base').order_by('-sys_created_on')[start:end]
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


