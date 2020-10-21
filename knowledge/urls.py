from django.urls import path, include
from .views import KnowledgeArticleListView, KnowledgeArticleView,\
    ArticleNestedCommentsView,\
    ArticleCommentPostView, \
    KnowledgeArticlePaginatedListView, \
    GetBookmarkedArticleViewSet, BookmarkArticlesViewSet, \
    ArticleCommentsView, KnowledgeUseView, KbUseExistingView, \
    ArticleFeedbackView, NewArticleInsertView, UpdateArticleInsertView, \
    GetKnowledgeBaseView, GetKnowledgeCategory, GetCourseSectionAndArticles, \
    GetBreadCrumbView, SetCourseProgress, GetKnowledgeCatgories, GetSearchResults, GetCoursesForAddingArticle, \
    AddArticleToCourse, AddPathOrBranch, BuildPathViewSet

urlpatterns = [
    path('kb_knowledge/article/', NewArticleInsertView.as_view()),
    path('articles/update/<str:articleid>/', UpdateArticleInsertView.as_view()),
    path('articles/', KnowledgeArticleListView.as_view()),
    path('articles/<str:id>/', KnowledgeArticleView.as_view()),
    path('articles/<str:articleid>/comments/', ArticleNestedCommentsView.as_view()),
    path('articles/<str:articleid>/comments/new', ArticleCommentPostView.as_view()),
    path('articles/<str:articleid>/flatcomments/', ArticleCommentsView.as_view()),
    path('articles/<int:start>/<int:end>/', KnowledgeArticlePaginatedListView.as_view()),
    path('bookmarked_articles/<int:start>/<int:end>/', GetBookmarkedArticleViewSet.as_view()),
    path('bookmark_this_article/', BookmarkArticlesViewSet.as_view()),
    path('knowledge_view/', KnowledgeUseView.as_view()),
    path('knowledge_view/<str:article_id>/', KbUseExistingView.as_view()),
    path('knowledge_crumb/<str:categoryId>/', GetBreadCrumbView.as_view()),
    path('articles/<str:article_id>/feedback/', ArticleFeedbackView.as_view()),
    path('knowledge_base/get_knowledge_bases/', GetKnowledgeBaseView.as_view()),
    path('<str:kb_base>/categories/<str:kb_category>/<str:courses>/', GetKnowledgeCategory.as_view()),
    path('course/<str:category>/', GetCourseSectionAndArticles.as_view()),
    path('course_progress/', SetCourseProgress.as_view()),
    path('<str:kb_base>/categories_kb_base/', GetKnowledgeCatgories.as_view()),
    path('query/<str:query_keyword>/', GetSearchResults.as_view()),
    path('kb_category/courses/', GetCoursesForAddingArticle.as_view()),
    path('kb_sections/article/insert/', AddArticleToCourse.as_view()),
    path('kb_category/add/', AddPathOrBranch.as_view()),
    path("kb_section/path/", BuildPathViewSet.as_view())
]