from django.urls import path, include
from .views import KnowledgeArticleListView

urlpatterns = [
    path('articles/', KnowledgeArticleListView.as_view()),
]
