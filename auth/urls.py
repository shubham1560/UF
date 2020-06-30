from django.urls import path, include
from .views import UserViewSet, UserListViewSet, CreateUserViewSet, CreateGoogleUserViewSet, ActivateAccountViewSet, \
    UserPasswordResetViewSet, UserPasswordResetLinkViewSet, ObtainAuthTokenViewSet

urlpatterns = [
    path('get_token/', ObtainAuthTokenViewSet.as_view()),
    path('users/', UserListViewSet.as_view()),
    path('users/<str:id>', UserViewSet.as_view()),
    path('create_user_sys/', CreateUserViewSet.as_view()),
    path('create_user_google/', CreateGoogleUserViewSet.as_view()),
    path('activate_account/<str:token>', ActivateAccountViewSet.as_view()),
    path('reset_password/<str:token>', UserPasswordResetViewSet.as_view()),
    path('send_password_reset_link/', UserPasswordResetLinkViewSet.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
]
