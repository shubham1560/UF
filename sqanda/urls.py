from django.urls import path, include
from .views import QuestionViewSet, GetQuestionAndAnswer
urlpatterns = [
    path("question/", QuestionViewSet.as_view()),
    path("question/<str:question_id>/", GetQuestionAndAnswer.as_view())
]