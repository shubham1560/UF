from .models import KbKnowledge, KbCategory, KbKnowledgeBase, KbFeedback, KbUse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .services import getAllArticles, getSingleArticle, getComments
import json

# Create your views here.
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class KnowledgeArticleListView(APIView):
    class KnowledgeArticleListSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbKnowledge
            fields = ('id', 'title', 'article_body')

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

    def get(self, request, articleid, format=None):
        comments = getComments(articleid)
        if comments:
            result = self.ArticleCommentsSerializer(comments, many=True)
            response = {'data': result.data,
                        'message': 'OK',
                        "comments": True}
        else:
            response = {'message': "No Comments for mentioned article", "comments": False}
        return Response(response, status=status.HTTP_200_OK)



