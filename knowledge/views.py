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
        result = self.KnowledgeArticleSerializer(article, many=False)
        return Response(result.data, status=status.HTTP_200_OK)


class ArticleCommentsView(APIView):
    class ArticleCommentsSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbFeedback
            fields = ('id', 'parent_comment', 'comments', 'user')

    def get(self, request, articleid, format=None):
        comments = getComments(articleid)
        result = self.ArticleCommentsSerializer(comments, many=True)
        response = {'data': result.data,
                    'message': 'OK'}
        return Response(response, status=status.HTTP_200_OK)



