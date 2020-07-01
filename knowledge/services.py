from .models import KbKnowledge, KbFeedback, m2m_knowledge_feedback_likes
from django.core.exceptions import ObjectDoesNotExist


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
