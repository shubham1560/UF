from rest_framework.permissions import IsAuthenticated

from sys_user.models import SysUser
from .models import KbKnowledge, BookmarkUserArticle, KbFeedback, KbKnowledgeBase, KbCategory, Tag, ArticleTag, KbUse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from django.conf import settings
from django.core.cache import cache
from uFraudApi.settings.base import CACHE_KEY
from .services import get_all_articles, get_single_article, get_comments, get_paginated_articles, \
    bookmark_the_article, get_articles_for_logged_in_user_with_bookmark, kb_use,\
    if_bookmarked_and_found_useful_by_user, add_feedback, add_article, get_course_section_and_articles, \
    get_breadcrumb_category, set_progress_course_kbuse, get_categories_tree, get_courses, get_articles, \
    add_article_to_course, add_path_or_branch, edit_path_or_branch, build_path, course_owner, delete_sections, \
    delete_article, get_profanity_matrix, add_order_to_courses
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from services.cacheservice import del_key, get_key, set_key, has_key, delete_many
from logs.services import log_random

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
                      'workflow',
                      'description',
                      "getAuthor",
                      "get_category",
                      "get_knowledge_base",
                      'sys_updated_on',
                      'sys_created_by',
                      'article_url'
                      )

    # @log_request
    def get(self, request, id, format=None):
        key = cache_key+"."+id
        if has_key(key):
            article = get_key(key)
        else:
            article = get_single_article(id, request)
            set_key(key, article)
        owner = False
        if not request.user.is_anonymous:
            if request.user == article.author:
                owner = True
        if article:
            response = {"data": self.KnowledgeArticleSerializer(article, many=False).data, "owner": owner}
            status_code = status.HTTP_200_OK
        else:
            response = {"message": "the article with this id doesn't exist"}
            status_code = status.HTTP_404_NOT_FOUND
        result = {"response": response, "status": status_code}
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
            fields = ('id', 'article', 'user', 'get_article',)

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
        # breakpoint()
        if request.user.groups.filter(name="Authors").exists():
            publish_ready = request.data['publish_ready']
            article_id = request.data['id']
            key = cache_key + "." + article_id
            del_key(key)
            print(key, "  deleted from cache")
            result = add_article(request, publish_ready, article_id)
            return Response(result, status=status.HTTP_201_CREATED)
        else:
            return Response('', status=status.HTTP_401_UNAUTHORIZED)


class UpdateArticleInsertView(APIView):

    def post(self, request, articleid, format=None):
        # breakpoint()
        result = add_article(request, articleid)
        return Response("Updated", status=status.HTTP_201_CREATED)


class GetKnowledgeBaseView(APIView):

    class KnowledgeBaseViewSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbKnowledgeBase
            fields = ('id', 'description', 'title', 'real_image', 'compressed_image', 'order', 'question_count')

    # @log_request
    def get(self, request, format=None):
        key = cache_key+"."+"kb_bases"
        if key in cache:
            bases = cache.get(key)
        else:
            bases = KbKnowledgeBase.objects.filter(active=True).order_by('order')
            cache.set(key, bases, timeout=None)
        result = self.KnowledgeBaseViewSerializer(bases, many=True)
        return Response({"bases": result.data}, status=status.HTTP_200_OK)


class GetKnowledgeCategory(APIView):
    class KnowledgeCategoryModeratorViewSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbCategory
            fields = ('id', 'label', 'parent_kb_base', 'parent_category', 'real_image', 'compressed_image', "course",
                      "section", "order", "get_parent_category", "get_parent_knowledgebase", "description",
                      'get_created_by', "active", 'get_first_article', 'question_count')

    class KnowledgeCategoryViewSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbCategory
            fields = ('id', 'label', 'parent_kb_base', 'parent_category', 'real_image', 'compressed_image', "course",
                      "section", "order", "get_parent_category", "get_parent_knowledgebase", "get_first_article",
                      "description", 'question_count')

    def get(self, request, kb_base, kb_category, courses, format=None):
        root_admin = False
        if request.user.groups.filter(name="Moderators").exists():
            moderator = True
        else:
            moderator = False
        if request.user.groups.filter(name="Root Admin").exists():
            root_admin = True

        # breakpoint()
        # If courses is true, then all the courses in the database is sent in response
        # key = cache_key+"."+kb_base+"."+kb_category
        # if key in cache:
        #     categories = cache.get(key)
        # else:
        # if request.user.groups.filter(name="Moderators"):
        if kb_category != "root":
            try:
                category = KbCategory.objects.get(id=kb_category)
                if moderator:
                    categories = KbCategory.objects.filter(parent_category=category).order_by('order')
                else:
                    categories = KbCategory.objects.filter(parent_category=category,
                                                           course=True,
                                                           active=True).order_by('order')
            except ObjectDoesNotExist:
                categories = []
        # categories = KbCategory.parent_of_category()
        # pass
        else:
            try:
                kb = KbKnowledgeBase.objects.get(id=kb_base)
                if courses == "courses":
                    if root_admin:
                        categories = KbCategory.objects.filter(course=True, parent_kb_base=kb).order_by('order')
                    elif moderator:
                        categories = KbCategory.objects.filter(Q(active=True) | Q(sys_created_by=request.user),
                                                               course=True, parent_kb_base=kb,
                                                               ).order_by('order')
                    else:
                        categories = KbCategory.objects.filter(course=True, parent_kb_base=kb,
                                                               active=True).order_by('order')
                else:
                    if moderator:
                        categories = KbCategory.objects.filter(parent_category=None,
                                                               parent_kb_base=kb
                                                               ).order_by('order')
                    else:
                        categories = KbCategory.objects.filter(active=True,
                                                               course=True,
                                                               parent_category=None,
                                                               parent_kb_base=kb
                                                               ).order_by('order')
            except ObjectDoesNotExist:
                categories = []
        if request.user.groups.filter(name="Moderators"):
            result = self.KnowledgeCategoryModeratorViewSerializer(categories, many=True)
        else:
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
        result = {}
        if key in cache:
            result = cache.get(key)
        else:
            category = KbCategory.objects.get(id=categoryId)
            result = get_breadcrumb_category(category)
            result["kb_base"] = category.parent_kb_base.id
            # breakpoint()
            cache.set(key, result, timeout=None)
        return Response({"labels": result["crumb_label"], "id": result["crumb_id"], "desc": result["crumb_desc"],
                        "kb_base": result["kb_base"]}, status=status.HTTP_200_OK)


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


class GetKnowledgeCategories(APIView):
    class KnowledgeCategoryAllViewSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbCategory
            fields = ('id', 'label', 'parent_kb_base', 'parent_category', 'real_image', 'compressed_image', "course",
                      "section", "order", "get_parent_category", "get_parent_knowledgebase", "description")

    def get(self, request, kb_base, format=None):
        key = cache_key+".branch."+kb_base+".normal"
        moderator = False
        if request.user.groups.filter(name="Moderators").exists():
            moderator = True
            key = cache_key+".branch."+kb_base+".moderator"
        if has_key(key):
            result = get_key(key)
        else:
            result = get_categories_tree(kb_base, request, moderator)
            set_key(key, result)
        return Response(result, status=status.HTTP_200_OK)


class GetSearchResults(APIView):
    class KnowledgeArticlesSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbKnowledge
            fields = ('title', 'id', 'category', 'get_category', 'description', 'article_url')

    class KnowledgeCourseSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbCategory
            fields = ('id', 'label', 'description', 'get_parent_knowledgebase')

    def get(self, request, query_keyword, format=None):
        articles = KbKnowledge.objects.filter(Q(title__icontains=query_keyword, workflow='published') |
                                              Q(article_body__icontains=query_keyword, workflow='published'
                                                )).order_by('-sys_updated_on')
        result_articles = self.KnowledgeArticlesSerializer(articles, many=True)
        courses = KbCategory.objects.filter(course=True, label__icontains=query_keyword,
                                            active=True).order_by('-sys_updated_on')
        result_courses = self.KnowledgeCourseSerializer(courses, many=True)
        result = {
            'courses': result_courses.data,
            'articles': result_articles.data
        }
        return Response(result, status=status.HTTP_200_OK)


class GetCoursesForAddingArticle(APIView):
    class KnowledgeCourseSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbCategory
            fields = ('id', 'label', 'description', 'get_parent_knowledgebase')

    def get(self, request, format=None):
        key = cache_key + "." + "path_to_add"
        if request.user.groups.filter(name="Moderators").exists():
            mod_key = key+"moderator"
            if has_key(mod_key):
                courses = get_key(mod_key)
            else:
                courses = KbCategory.objects.filter(course=True)
                set_key(mod_key, courses)
        else:
            if has_key(key):
                courses = get_key(key)
            else:
                courses = KbCategory.objects.filter(course=True, active=True)
                set_key(key, courses)
        result = self.KnowledgeCourseSerializer(courses, many=True)
        return Response(result.data, status=status.HTTP_200_OK)


class AddArticleToCourse(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        if request.user.groups.filter(name__in=["Moderators", "Authors"]).exists():
            add_article_to_course(request)
        else:
            return Response("Invalid Request", status=status.HTTP_401_UNAUTHORIZED)
        return Response("", status=status.HTTP_200_OK)


class AddPathOrBranch(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        key = cache_key + "." + "path_to_add"
        mod_key = key+"moderator"
        delete_many([key, mod_key])
        if request.data['type']['add'] == 'branch':
            key = cache_key + ".branch." + request.data['type']['kb_base']+".normal"
            del_key(key)
            key_m = cache_key + ".branch." + request.data['type']['kb_base'] + ".moderator"
            del_key(key_m)
        # breakpoint()
        if request.user.groups.filter(name="Moderators").exists():
            if request.data["action"] == 'edit':
                if request.user.id_name == request.data["type"]["product"]["get_created_by"]["id"]:
                    try:
                        if request.data["type"]["product"]:
                            edit_path_or_branch(request)
                    except KeyError:
                        add_path_or_branch(request)
                else:
                    return Response('', status=status.HTTP_401_UNAUTHORIZED)
            else:
                try:
                    if request.data["type"]["product"]:
                        edit_path_or_branch(request)
                except KeyError:
                    add_path_or_branch(request)
        else:
            return Response("invalid request", status=status.HTTP_401_UNAUTHORIZED)
        return Response("", status=status.HTTP_201_CREATED)


class BuildPathViewSet(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        response = build_path(request)
        delete_sections(request.data['deleteSections'])
        return Response(response["message"], status=response["status"])


class CourseOwner(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, course, format=None):
        response = course_owner(course, request)
        return Response(response, status=response["status"])


class DeleteArticleId(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        # breakpoint()
        if request.user.groups.filter(name="Authors").exists():
            article_id = request.data['article_id']
            key = cache_key + "." + article_id
            del_key(key)
            # print(key, "  deleted from cache")
            response = delete_article(article_id, request)
        else:
            return Response('', status=status.HTTP_401_UNAUTHORIZED)
        return Response(response, status=response["status"])


class TagsViewSet(APIView):
    permission_classes = (IsAuthenticated, )

    class GetTagsSerializer(serializers.ModelSerializer):
        class Meta:
            model = Tag
            fields = ('id', 'label')

    # def post(self, request, format=None):
    #     pass
    def get(self, request, format=None):
        # pass
        key = cache_key+"."+"tags_all"
        if has_key(key):
            tags = get_key(key)
        else:
            tags = Tag.objects.all()
            set_key(key, tags)
        result = self.GetTagsSerializer(tags, many=True)
        return Response(result.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        key = cache_key+"."+"tags_all"
        del_key(key)
        tag = Tag()
        tag.label = request.data['label']
        tag.save()
        result = {"id": tag.id, "label": tag.label}
        return Response(result, status=status.HTTP_201_CREATED)


class ArticleTags(APIView):
    permission_classes = (IsAuthenticated, )

    class GetArticleTagsSerializer(serializers.ModelSerializer):
        class Meta:
            model = ArticleTag
            fields = ('id', 'get_tag')

    def get(self, request, article_id, format=None):
        try:
            article = KbKnowledge.objects.get(id=article_id)
        except ObjectDoesNotExist:
            return Response('not found', status=status.HTTP_404_NOT_FOUND)
        try:
            article_tags = ArticleTag.objects.filter(article=article)
        except ObjectDoesNotExist:
            return Response('', status=status.HTTP_404_NOT_FOUND)
        result = self.GetArticleTagsSerializer(article_tags, many=True)
        return Response(result.data, status=status.HTTP_200_OK)

    def post(self, request, article_id, format=None):
        try:
            article = KbKnowledge.objects.get(id=article_id)
            tag = Tag.objects.get(id=request.data['tag_id'])
        except ObjectDoesNotExist:
            return Response('not found', status=status.HTTP_404_NOT_FOUND)
        if request.data['action'] == 'insert':
            try:
                article_tag = ArticleTag()
                article_tag.article = article
                article_tag.tag = tag
                article_tag.save()
            except KeyError:
                return Response('', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response('inserted', status=status.HTTP_201_CREATED)
        if request.data['action'] == 'delete':
            try:
                ArticleTag.objects.get(article=article, tag=tag).delete()
            except ObjectDoesNotExist:
                return Response('', status=status.HTTP_404_NOT_FOUND)
            return Response('deleted', status=status.HTTP_200_OK)
        if request.data['action'] == 'edit':
            try:
                atag = ArticleTag.objects.get(article=article, tag=tag)
                atag.relevance = request.data['relevance']
                atag.save()
            except ObjectDoesNotExist:
                return Response('', status=status.HTTP_404_NOT_FOUND)
            return Response('edited', status=status.HTTP_200_OK)
        return Response('', status=status.HTTP_406_NOT_ACCEPTABLE)


class CheckProfanity(APIView):

    def post(self, request, format=None):
        # breakpoint()
        result = get_profanity_matrix(request)
        return Response(result, status=status.HTTP_200_OK)


class GetArticlesInPath(APIView):
    class KnowledgeArticleListSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbKnowledge
            fields = ('id', 'title', 'featured_image_thumbnail', 'author', 'article_body', 'getAuthor')

    # @log_request
    def get(self, request, category, format=None):
        path = KbCategory.objects.get(id=category)
        articles = KbKnowledge.objects.filter(category=path, workflow='published', active=True)
        result = self.KnowledgeArticleListSerializer(articles, many=True)
        response = {'data': result.data, 'message': "ok"}
        return Response(response, status=status.HTTP_200_OK)


class OrderCourseCategory(APIView):

    def post(self, request, format=None):
        if request.user.is_staff:
            add_order_to_courses(request)
            return Response("working", status=status.HTTP_200_OK)
        return Response("unauthorized", status=status.HTTP_401_UNAUTHORIZED)


class ChangeModerator(APIView):

    def post(self, request, format=None):
        if request.user.groups.filter(name="Root Admin").exists():
            # breakpoint()
            try:
                course = KbCategory.objects.get(id=request.data['course']['id'])
                course.sys_created_by = SysUser.objects.get(email=request.data['user']['email'])
                course.save()
            except ObjectDoesNotExist:
                return Response('', status=status.HTTP_404_NOT_FOUND)
            return Response('', status=status.HTTP_200_OK)
        else:
            return Response('', status=status.HTTP_401_UNAUTHORIZED)


class GetArticleAnalysis(APIView):
    class KnowledgeArticleListSerializer(serializers.ModelSerializer):
        class Meta:
            model = KbUse
            fields = ('id', 'useful', 'viewed', 'feedback', 'get_user', 'sys_created_on')

    def get(self, request, article_id, format=None):
        kb_article = KbKnowledge.objects.get(id=article_id)
        kb_use_article = KbUse.objects.filter(article=kb_article).order_by("-sys_created_on")
        result = self.KnowledgeArticleListSerializer(kb_use_article, many=True)
        return Response(result.data, status=status.HTTP_200_OK)



