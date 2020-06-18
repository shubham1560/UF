from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from .views import UserViewSet, UserListViewSet, CreateUserViewSet, CreateGoogleUserViewSet, ActivateAccountViewSet, UserPasswordResetViewSet
from rest_framework import routers

router = routers.DefaultRouter()
# router.register('get_users', UserViewSet)

urlpatterns = [
    path('get_token/', obtain_auth_token),
    path('users/', UserListViewSet.as_view()),
    path('users/<int:id>', UserViewSet.as_view()),
    path('create_user_sys/', CreateUserViewSet.as_view()),
    path('create_user_google/', CreateGoogleUserViewSet.as_view()),
    path('activate_account/<str:token>', ActivateAccountViewSet.as_view()),
    path('reset_password/<str:token>', UserPasswordResetViewSet.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
    path('', include(router.urls))
]
