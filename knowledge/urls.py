from django.urls import path, include
from .views import KnowledgeArticleListView, KnowledgeArticleView,\
    ArticleNestedCommentsView,\
    ArticleCommentPostView, \
    KnowledgeArticlePaginatedListView, \
    GetBookmarkedArticleViewSet, BookmarkArticlesViewSet, \
    ArticleCommentsView, KnowledgeUseView, KbUseExistingView

urlpatterns = [
    path('articles/', KnowledgeArticleListView.as_view()),
    path('articles/<str:id>/', KnowledgeArticleView.as_view()),
    path('articles/<str:articleid>/comments/', ArticleNestedCommentsView.as_view()),
    path('articles/<str:articleid>/comments/new', ArticleCommentPostView.as_view()),
    path('articles/<str:articleid>/flatcomments/', ArticleCommentsView.as_view()),
    path('articles/<int:start>/<int:end>/', KnowledgeArticlePaginatedListView.as_view()),
    path('bookmarked_articles/', GetBookmarkedArticleViewSet.as_view()),
    path('bookmark_this_article/', BookmarkArticlesViewSet.as_view()),
    path('knowledge_view/', KnowledgeUseView.as_view()),
    path('knowledge_view/<str:article_id>/', KbUseExistingView.as_view())
]