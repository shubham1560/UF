from .models import KbKnowledge, KbCategory, KbKnowledgeBase, KbFeedback, KbUse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .services import getAllArticles, getSingleArticle, getComments
from logs.services import log_request
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class KnowledgeArticleListView(APIView):
    class KnowledgeArticleListSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbKnowledge
            fields = ('id', 'title', 'article_body')

    @log_request
    def get(self, request, format=None):
        articles = getAllArticles()
        result = self.KnowledgeArticleListSerializer(articles, many=True)
        response = {'data': result.data, 'message': "ok"}
        return Response(response, status=status.HTTP_200_OK)


class KnowledgeArticleView(APIView):
    class KnowledgeArticleSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbKnowledge
            fields = ('id', 'title', 'article_body')

    @log_request
    def get(self, request, id, format=None):
        article = getSingleArticle(id)
        if article:
            response = {"data": self.KnowledgeArticleSerializer(article, many=False).data, "message": "Ok"}
            status_code = status.HTTP_200_OK
        else:
            response = {"message": "the article with this id doesn't exist"}
            status_code = status.HTTP_404_NOT_FOUND
        return Response(response, status=status_code)


class ArticleCommentsView(APIView):
    class ArticleCommentsSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbFeedback
            fields = ('id', 'parent_comment', 'comments', 'user', 'getLikes')

    @log_request
    def get(self, request, articleid, format=None):
        try:
            KbKnowledge.objects.get(id=articleid)
            comments = getComments(articleid)
            if comments:
                result = self.ArticleCommentsSerializer(comments, many=True)
                response = {
                        'article': articleid,
                        'data': result.data,
                        'message': 'OK',
                        "comments": True,
                    }
            else:
                response = {
                        'message': "No Comments for article",
                        "comments": False,
                        "article": articleid,
                }
            return Response(response, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            response = {'message': "the article with id: " + articleid + " doesn't exist"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)



