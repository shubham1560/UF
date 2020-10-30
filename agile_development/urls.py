from django.urls import path, include
from .views import CreateFeatureViewSet, GetSupportRecords, GetSupportRowDetail

urlpatterns = [
    path('feature/post/', CreateFeatureViewSet.as_view()),
    path('tickets/get/', GetSupportRecords.as_view()),
    path('ticket/<int:record_id>/<str:record_type>', GetSupportRowDetail.as_view())
]
