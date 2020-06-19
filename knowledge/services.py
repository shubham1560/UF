from .models import KbKnowledge, KbFeedback


def getAllArticles():
    articles = KbKnowledge.objects.all()
    return articles


def getSingleArticle(id):
    article = KbKnowledge.objects.get(id=id)
    return article


def getComments(articleid: str):
    comments = KbFeedback.objects.get(article=articleid)
    return comments