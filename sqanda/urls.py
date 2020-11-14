from django.urls import path, include
from .views import QuestionViewSet
urlpatterns = [
    path("question/get", QuestionViewSet.as_view())
]