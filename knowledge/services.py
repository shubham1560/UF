from .models import KbKnowledge


def getAllArticles():
    article = KbKnowledge.objects.all()
    return article