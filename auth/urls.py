from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from .views import UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('get_users', UserViewSet)

urlpatterns = [
    path('get_token/', obtain_auth_token),
    path('', include(router.urls))
]
