from rest_framework.permissions import IsAuthenticated
from .models import KbKnowledge, BookmarkUserArticle, KbFeedback, KbKnowledgeBase, KbCategory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from django.conf import settings
from django.core.cache import cache
from uFraudApi.settings.base import CACHE_KEY
from .services import get_all_articles, get_single_article, get_comments, get_paginated_articles, \
    get_bookmarked_articles, bookmark_the_article, get_articles_for_logged_in_user_with_bookmark, kb_use,\
    if_bookmarked_and_found_useful_by_user, add_feedback, add_article, get_course_section_and_articles, \
    get_breadcrumb_category, set_progress_course_kbuse, get_categories_tree, get_courses, get_articles
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

# Create your views here.
CACHE_TTL = getattr(settings, 'CACHE_TTL', 0)

cache_key = CACHE_KEY


class KnowledgeArticleListView(APIView):
    class KnowledgeArticleListSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbKnowledge
            fields = ('id', 'title', 'featured_image_thumbnail', 'author', 'article_body', 'getAuthor')

    # @log_request
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

    # @log_request
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

    # @log_request
    def get(self, request, id, format=None):
        key = cache_key+"."+"singlearticle"+id
        if key in cache:
            result = cache.get(key)
        else:
            article = get_single_article(id)
            if article:
                response = {"data": self.KnowledgeArticleSerializer(article, many=False).data, "message": "Ok"}
                status_code = status.HTTP_200_OK
            else:
                response = {"message": "the article with this id doesn't exist"}
                status_code = status.HTTP_404_NOT_FOUND
            result = {"response": response, "status": status_code}
            cache.set(key, result, timeout=None)
        return Response(result["response"], status=result["status"])


class ArticleNestedCommentsView(APIView):
    permission_classes = (IsAuthenticated, )

    # @log_request
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

    # @log_request
    def get(self, request, start, end, format=None):
        # breakpoint()
        # count = BookmarkUserArticle.objects.filter(user=request.user).count()
        # articles = get_bookmarked_articles(request.user, start, end)
        if end == 0:
            articles = request.user.user_bookmark.select_related('article').all().order_by("-sys_created_on")
        else:
            articles = request.user.user_bookmark.select_related('article').order_by("-sys_created_on")[start:end]
        # print(articles[0].article)
        # count = articles.count()
        result = self.BookmarkedArticleListSerializer(articles, many=True)
        # breakpoint()
        response = {"bookmarked_articles": result.data}
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
        use = kb_use(request)
        response = {"message": use}
        return Response(response, status=status.HTTP_201_CREATED)


class KbUseExistingView(APIView):
    """
    To get the nitial state of the used and viewed
    """

    def get(self, request, article_id, format=None):
        response = {"message": "anonymous user's data can't be fetched"}
        if not request.user.is_anonymous:
            response = if_bookmarked_and_found_useful_by_user(request.user, article_id)
        return Response(response, status=status.HTTP_200_OK)


class ArticleFeedbackView(APIView):

    def post(self, request, article_id,  format=None):
        result = add_feedback(request, article_id)
        response = {"feedback added": result}
        return Response(response, status=status.HTTP_201_CREATED)


class NewArticleInsertView(APIView):

    def post(self, request, format=None):
        result = add_article(request)
        return Response("well", status=status.HTTP_201_CREATED)


class UpdateArticleInsertView(APIView):

    def post(self, request, articleid, format=None):
        # breakpoint()
        result = add_article(request, articleid)
        return Response("Updated", status=status.HTTP_201_CREATED)


class GetKnowledgeBaseView(APIView):

    class KnowledgeBaseViewSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbKnowledgeBase
            fields = ('id', 'description', 'title', 'real_image', 'compressed_image', 'order')

    # @log_request
    def get(self, request, format=None):
        # key = cache_key+"."+"kb_bases"
        # if key in cache:
        #     bases = cache.get(key)
        #     print("from cache")
        # else:
        bases = KbKnowledgeBase.objects.filter(active=True).order_by('order')
        # cache.set(key, bases, timeout=None)
        # print("from db")
        result = self.KnowledgeBaseViewSerializer(bases, many=True)
        return Response({"bases": result.data}, status=status.HTTP_200_OK)


class GetKnowledgeCategory(APIView):
    class KnowledgeCategoryViewSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbCategory
            fields = ('id', 'label', 'parent_kb_base', 'parent_category', 'real_image', 'compressed_image', "course",
                      "section", "order", "get_parent_category", "get_parent_knowledgebase", "description")

    def get(self, request, kb_base, kb_category, courses, format=None):
        # breakpoint()
        # If courses is true, then all the courses in the database is sent in response
        # key = cache_key+"."+kb_base+"."+kb_category
        # if key in cache:
        #     categories = cache.get(key)
        # else:
        if kb_category != "root":
            try:
                category = KbCategory.objects.get(id=kb_category)
                categories = KbCategory.objects.filter(parent_category=category).order_by('order')
            except ObjectDoesNotExist:
                categories = []
        # categories = KbCategory.parent_of_category()
        # pass
        else:
            try:
                # breakpoint()
                # if request.data["onlycourses"] == True:
                #     print("yolo")
                kb = KbKnowledgeBase.objects.get(id=kb_base)
                if courses == "courses":
                    # print("fetch courses only")
                    categories = KbCategory.objects.filter(course=True, active=True, parent_kb_base=kb).order_by('order')
                else:
                    categories = KbCategory.objects.filter(active=True, parent_category=None, parent_kb_base=kb).order_by('order')
            except ObjectDoesNotExist:
                categories = []
        # cache.set(key, categories, timeout=None)
        result = self.KnowledgeCategoryViewSerializer(categories, many=True)
        # breakpoint()
        return Response({"categories": result.data}, status=status.HTTP_200_OK)


class GetCourseSectionAndArticles(APIView):

    def get(self, request, category, format=None):
        result, course = get_course_section_and_articles(category, request)
        response = {"sections": result, "course": course}
        return Response(response, status=status.HTTP_200_OK)


class GetBreadCrumbView(APIView):

    def get(self, request, categoryId, format=None):
        key = cache_key+"."+"crumb"+categoryId
        if key in cache:
            result = cache.get(key)
        else:
            category = KbCategory.objects.get(id=categoryId)
            result = get_breadcrumb_category(category)
            cache.set(key, result, timeout=None)
        return Response({"labels": result["crumb_label"], "id": result["crumb_id"]}, status=status.HTTP_200_OK)


class SetCourseProgress(APIView):

    def post(self, request, format=None):
        # breakpoint()
        if 100 >= int(request.data['progress']) >= 0:
            if not request.user.is_anonymous:
                result = set_progress_course_kbuse(request)
            else:
                result = "anonymous not allowed"
        else:
            result = "arrey bhai bhai bhai bhai, ye kahaan aa gye aap"
        return Response({"progress_saved": result}, status=status.HTTP_200_OK)


class GetKnowledgeCatgories(APIView):
    class KnowledgeCategoryAllViewSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbCategory
            fields = ('id', 'label', 'parent_kb_base', 'parent_category', 'real_image', 'compressed_image', "course",
                      "section", "order", "get_parent_category", "get_parent_knowledgebase", "description")

    def get(self, request, kb_base, format=None):
        result = get_categories_tree(kb_base)
        # base = KbKnowledgeBase.objects.get(id=kb_base)
        # categories = KbCategory.objects.filter(parent_kb_base=base, course=False, section=False)
        # breakpoint()
        # result = self.KnowledgeCategoryAllViewSerializer(categories, many=True)
        return Response(result, status=status.HTTP_200_OK)


class GetSearchResults(APIView):
    class KnowledgeArticlesSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbKnowledge
            fields = ('title', 'id', 'category', 'get_category', 'description')

    class KnowledgeCourseSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbCategory
            fields = ('id', 'label', 'description', 'get_parent_knowledgebase')

    def get(self, request, query_keyword, format=None):
        articles = KbKnowledge.objects.filter(Q(title__icontains=query_keyword) |
                                              Q(article_body__icontains=query_keyword)).order_by('-sys_updated_on')
        result_articles = self.KnowledgeArticlesSerializer(articles, many=True)
        courses = KbCategory.objects.filter(course=True, label__icontains=query_keyword).order_by('-sys_updated_on')
        result_courses = self.KnowledgeCourseSerializer(courses, many=True)

        # breakpoint()
        result = {
            'courses': result_courses.data,
            'articles': result_articles.data
        }
        # articles = get_articles(query_keyword)
        # courses = get_courses(query_keyword)
        return Response(result, status=status.HTTP_200_OK)
