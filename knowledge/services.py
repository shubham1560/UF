from .models import KbKnowledge, KbFeedback
from django.core.exceptions import ObjectDoesNotExist


def BFS(comments):
    print(comments)
    visited = [False] * len(comments)
    queue = []
    final = []
    counter = 0
    for i in comments:
        if i["parent_comment_id"] is None:
            queue.append(i)
    while queue:
        s = queue.pop(0)
        final.append(s)
        final[-1]["child"] = []
        for j in comments:
            if j["parent_comment_id"] == s:
                final[-1].child.append(j)
                j.parent = s
                queue.append(j)
    print(final)
    return final
    # print(queue)
    # print(final)
    # return final


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
    comments = KbFeedback.objects.filter(article=articleid).values('id', 'parent_comment_id', 'comments')
    q = list(comments)
    a = BFS(q)
    result = {"model": list(a)}
    return result


