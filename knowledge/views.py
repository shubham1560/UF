from rest_framework.permissions import IsAuthenticated
from .models import KbKnowledge, BookmarkUserArticle, KbFeedback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .services import get_all_articles, get_single_article, get_comments, get_paginated_articles, \
    get_bookmarked_articles, bookmark_the_article, get_articles_for_logged_in_user_with_bookmark, kb_use,\
    if_bookmarked_and_found_useful_by_user
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
            fields = ('id', 'title', 'featured_image_thumbnail', 'description', 'getAuthor',
                      'get_category', 'get_knowledge_base')

    @log_request
    def get(self, request, start, end, format=None):
        # breakpoint()
        total_articles = KbKnowledge.objects.all().count()
        if request.user.is_anonymous:
            articles = get_paginated_articles(start, end)
            result = self.KnowledgeArticleListSerializer(articles, many=True)
            response = {'data': result.data, 'message': 'ok', 'total_articles': total_articles}
            return Response(response, status=status.HTTP_200_OK)
        else:
            articles = get_articles_for_logged_in_user_with_bookmark(start, end, request.user)
            return Response({"message": "Ok", "data": articles["data"], 'total_articles': total_articles})


class KnowledgeArticleView(APIView):
    class KnowledgeArticleSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbKnowledge
            fields = ('id',
                      'title',
                      'article_body',
                      "getAuthor",
                      "get_category",
                      "get_knowledge_base",
                      'featured_image',
                      'featured_image_thumbnail'
                      )

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


class ArticleNestedCommentsView(APIView):
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
        count = BookmarkUserArticle.objects.filter(user=request.user).count()
        articles = get_bookmarked_articles(request.user)
        result = self.BookmarkedArticleListSerializer(articles, many=True)
        response = {"bookmarked_articles": result.data, "articles_count": count}
        return Response(response, status=status.HTTP_200_OK)


class BookmarkArticlesViewSet(APIView):

    def post(self, request, format=None):
        article_id = request.data['article_id']
        if bookmark_the_article(request.user, article_id):
            response = {"bookmarked": True}
        else:
            response = {'bookmarked': False}
        return Response(response, status=status.HTTP_201_CREATED)


class ArticleCommentsView(APIView):
    class ArticleCommentsViewSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbFeedback
            fields = ('id', 'comments', 'parent_comment', 'get_user')

    def get(self, request, articleid, format=None):
        comments = KbFeedback.objects.filter(article=KbKnowledge.objects.get(id=articleid))
        count = comments.count()
        result = self.ArticleCommentsViewSerializer(comments, many=True)
        response = {'count': count, 'comments': result.data}
        return Response(response, status=status.HTTP_200_OK)


class KnowledgeUseView(APIView):

    def post(self, request, format=None):
        # breakpoint()
        use = kb_use(request)
        response = {"message": use}
        return Response(response, status=status.HTTP_201_CREATED)


class KbUseExistingView(APIView):
    """
    To get the nitial state of the used and viewed
    """

    def get(self, request, article_id, format=None):
        if not request.user.is_anonymous:
            # if if_bookmarked_and_found_useful_by_user(request.user, article_id):
            #     response = {"bookmarked": True}
            # else:
            #     response = {'bookmarked': False}
            response = if_bookmarked_and_found_useful_by_user(request.user, article_id)
        return Response(response, status=status.HTTP_200_OK)
