from django.urls import path, include
from .views import KnowledgeArticleListView, KnowledgeArticleView, ArticleCommentsView

urlpatterns = [
    path('articles/', KnowledgeArticleListView.as_view()),
    path('articles/<str:id>/', KnowledgeArticleView.as_view()),
    path('comments/<str:articleid>/', ArticleCommentsView.as_view())
]