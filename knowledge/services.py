from .models import KbKnowledge, KbFeedback
from django.core.exceptions import ObjectDoesNotExist


def getAllArticles():
    articles = KbKnowledge.objects.all()
    return articles


def getSingleArticle(id):
    try:
        article = KbKnowledge.objects.get(id=id)
        return article
    except ObjectDoesNotExist:
        pass


def getComments(articleid: str):
    try:
        comments = KbFeedback.objects.filter(article=articleid)
        return comments
    except ObjectDoesNotExist:
        pass


