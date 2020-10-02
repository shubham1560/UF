from django.urls import path, include
from .views import AttachedImageViewSet, AddLinkForVideo

urlpatterns = [
    path('add_image/', AttachedImageViewSet.as_view()),
    path('fetch_url/', AddLinkForVideo.as_view()),
]
