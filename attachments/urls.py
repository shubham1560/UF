from django.urls import path, include
from .views import AttachedImageViewSet

urlpatterns = [
    path('add_image/', AttachedImageViewSet.as_view()),
]
