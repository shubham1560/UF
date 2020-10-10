from django.urls import path, include
from .views import AttachedImageViewSet, AddLinkForVideo, GetEmbedLinkDetail

urlpatterns = [
    # path('fetch_url/<str:link>', GetEmbedLinkDetail.as_view()),
    path('add_image/', AttachedImageViewSet.as_view()),
    path('fetch_url/', AddLinkForVideo.as_view()),
]
