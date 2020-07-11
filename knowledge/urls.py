from django.urls import path, include
from .views import KnowledgeArticleListView, \
    KnowledgeArticleView,\
    ArticleCommentsView,\
    ArticleCommentPostView, \
    KnowledgeArticlePaginatedListView, \
    GetBookmarkedArticleViewSet, BookmarkArticlesViewSet

urlpatterns = [
    path('articles/', KnowledgeArticleListView.as_view()),
    path('articles/<str:id>/', KnowledgeArticleView.as_view()),
    path('articles/<str:articleid>/comments/', ArticleCommentsView.as_view()),
    path('articles/<str:articleid>/comments/new', ArticleCommentPostView.as_view()),
    path('articles/<int:start>/<int:end>/', KnowledgeArticlePaginatedListView.as_view()),
    path('bookmarked_articles/', GetBookmarkedArticleViewSet.as_view()),
    path('bookmark_this_article/', BookmarkArticlesViewSet.as_view()),
]