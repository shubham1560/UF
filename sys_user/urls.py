from django.urls import path, include
from .views import GetUserDetailViewSet, EditUserDetailViewSet, EditImageOnlyViewSet, GetUserActivity

urlpatterns = [
    path('get_user_data/', GetUserDetailViewSet.as_view()),
    path('edit_user_data/', EditUserDetailViewSet.as_view()),
    path('edit_user_image/', EditImageOnlyViewSet.as_view()),
    path('get_user_activity/', GetUserActivity.as_view()),
]
