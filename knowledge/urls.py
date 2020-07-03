from django.urls import path, include
from .views import KnowledgeArticleListView, KnowledgeArticleView, ArticleCommentsView, ArticleCommentPostView

urlpatterns = [
    path('articles/', KnowledgeArticleListView.as_view()),
    path('articles/<str:id>/', KnowledgeArticleView.as_view()),
    path('articles/<str:articleid>/comments/', ArticleCommentsView.as_view()),
    path('articles/<str:articleid>/comments/new', ArticleCommentPostView.as_view())
]