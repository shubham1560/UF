from django.urls import path, include
from .views import CreateSupportViewSet, GetSupportRecords, GetSupportRowDetail, EditSupportViewSet

urlpatterns = [
    path('support/post/', CreateSupportViewSet.as_view()),
    path('support/edit/', EditSupportViewSet.as_view()),
    path('tickets/get/', GetSupportRecords.as_view()),
    path('ticket/<int:record_id>/<str:record_type>/', GetSupportRowDetail.as_view())
]
