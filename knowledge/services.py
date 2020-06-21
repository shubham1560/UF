from .models import KbKnowledge, KbFeedback
from django.core.exceptions import ObjectDoesNotExist


def BFS(comments):
    visited = [False] * len(comments)
    queue = []
    final = []
    counter = 0
    for i in comments:
        if i["parent_comment"] is None:
            queue.append(i)
    while queue:
        s = queue.pop(0)
        final.append(s)
        final[-1]["child"] = []
        for j in comments:
            if j["parent_comment"] == s:
                final[-1].child.append(j)
                j.parent = s
                queue.append(j)
    print(queue)
    print(final)
    return final


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
    comments = KbFeedback.objects.filter(article=articleid)
    return comments


