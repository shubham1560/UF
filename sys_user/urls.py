from django.urls import path, include
from .views import GetUserDetailViewSet

urlpatterns = [
    path('get_user_data/', GetUserDetailViewSet.as_view()),
]
