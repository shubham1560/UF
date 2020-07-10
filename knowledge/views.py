from rest_framework.permissions import IsAuthenticated
from .models import KbKnowledge, BookmarkUserArticle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .services import get_all_articles, get_single_article, get_comments, get_paginated_articles, \
    get_bookmarked_articles
from logs.services import log_request
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class KnowledgeArticleListView(APIView):
    class KnowledgeArticleListSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbKnowledge
            fields = ('id', 'title', 'featured_image_thumbnail', 'author', 'article_body', 'getAuthor')

    @log_request
    def get(self, request, format=None):
        articles = get_all_articles()
        result = self.KnowledgeArticleListSerializer(articles, many=True)
        response = {'data': result.data, 'message': "ok"}
        return Response(response, status=status.HTTP_200_OK)


class KnowledgeArticlePaginatedListView(APIView):
    class KnowledgeArticleListSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbKnowledge
            fields = ('id', 'title', 'featured_image_thumbnail', 'description', 'getAuthor')

    @log_request
    def get(self, request, start, end, format=None):
        articles = get_paginated_articles(start, end)
        total_articles = KbKnowledge.objects.all().count()
        result = self.KnowledgeArticleListSerializer(articles, many=True)
        response = {'data': result.data, 'message': 'ok', 'total_articles': total_articles}
        return Response(response, status=status.HTTP_200_OK)


class KnowledgeArticleView(APIView):
    class KnowledgeArticleSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbKnowledge
            fields = ('id', 'title', 'article_body')

    @log_request
    def get(self, request, id, format=None):
        article = get_single_article(id)
        if article:
            response = {"data": self.KnowledgeArticleSerializer(article, many=False).data, "message": "Ok"}
            status_code = status.HTTP_200_OK
        else:
            response = {"message": "the article with this id doesn't exist"}
            status_code = status.HTTP_404_NOT_FOUND
        return Response(response, status=status_code)


class ArticleCommentsView(APIView):
    permission_classes = (IsAuthenticated, )

    @log_request
    def get(self, request, articleid, format=None):
        try:
            KbKnowledge.objects.get(id=articleid)
            comments = get_comments(articleid)
            if comments:
                response = {
                        'article': articleid,
                        'data': comments,
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


class ArticleCommentPostView(APIView):
    pass


class GetBookmarkedArticleViewSet(APIView):
    class BookmarkedArticleListSerializer(serializers.ModelSerializer):
        class Meta:
            model = BookmarkUserArticle
            fields = ('id', 'article', 'user', 'get_article')

    @log_request
    def get(self, request, format=None):
        # breakpoint()
        articles = get_bookmarked_articles(request.user)
        result = self.BookmarkedArticleListSerializer(articles, many=True)
        response = {"bookmarked_articles": result.data}
        return Response(response, status=status.HTTP_200_OK)




