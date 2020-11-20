from django.urls import path, include
from .views import QuestionViewSet, GetQuestionAndAnswer, CommentViewSet, EditorDataViewSet, AnswersQuestion

urlpatterns = [
    path("question/", QuestionViewSet.as_view()),
    path("question/<str:question_id>/", GetQuestionAndAnswer.as_view()),
    path('comment/', CommentViewSet.as_view()),
    path('editor/', EditorDataViewSet.as_view()),
    path('answer/question_id/', AnswersQuestion.as_view())

]