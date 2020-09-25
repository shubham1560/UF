from django.urls import path, include
from .views import GetUserDetailViewSet, EditUserDetailViewSet, EditImageOnlyViewSet, GetUserActivity, \
    AddSubscriberViewSet, IsDeveloperViewSet

urlpatterns = [
    path('get_user_data/', GetUserDetailViewSet.as_view()),
    path('edit_user_data/', EditUserDetailViewSet.as_view()),
    path('edit_user_image/', EditImageOnlyViewSet.as_view()),
    path('get_user_activity/<requested_type>/<int:start>/<int:end>/',
         GetUserActivity.as_view()),  # whether article or course
    path('add_subscriber/', AddSubscriberViewSet.as_view()),
    path('developer/<str:developer_code>/', IsDeveloperViewSet.as_view()),
]
