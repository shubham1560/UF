from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from .views import UserViewSet, UserListViewSet, CreateUserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
#router.register('get_users', UserViewSet)

urlpatterns = [
    path('get_token/', obtain_auth_token),
    path('users', UserListViewSet.as_view()),
    path('users/<int:id>', UserViewSet.as_view()),
    path('create_user', CreateUserViewSet.as_view()),
    path('', include(router.urls))
]
