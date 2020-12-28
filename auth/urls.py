from django.urls import path, include
from .views import UserViewSet, UserListViewSet, CreateUserViewSet, CreateGoogleUserViewSet, ActivateAccountViewSet, \
    UserPasswordResetViewSet, UserPasswordResetLinkViewSet, ObtainAuthTokenViewSet, \
    UserTokenValidViewSet, GetUserDetailFromTokenViewSet, FacebookUserViewSet, SendActivationLinkAgain, \
    ResetLoggedInUserPassword, GetUserTokenImpersonation, GetModeratorsToAssign, GetUserGroups

urlpatterns = [
    path('get_token/', ObtainAuthTokenViewSet.as_view()),
    path('users/', UserListViewSet.as_view()),
    path('create_user_sys/', CreateUserViewSet.as_view()),
    path('create_user_google/', CreateGoogleUserViewSet.as_view()),
    path('create_user_facebook/', FacebookUserViewSet.as_view()),
    path('activate_account/<str:token>', ActivateAccountViewSet.as_view()),
    path('reset_password/<str:token>', UserPasswordResetViewSet.as_view()),
    path('send_password_reset_link/', UserPasswordResetLinkViewSet.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
    path('token_valid/<str:token>/', UserTokenValidViewSet.as_view()),
    path('token_get_user/', GetUserDetailFromTokenViewSet.as_view()),
    path('resend_activation_link/<str:email>/', SendActivationLinkAgain.as_view()),
    path('sys_user/reset_password_logged_in/', ResetLoggedInUserPassword.as_view()),
    path('get_impersonation_token/', GetUserTokenImpersonation.as_view()),
    path('sys_user/moderators/', GetModeratorsToAssign.as_view()),
    path('sys_user/groups/user/', GetUserGroups.as_view())
]
