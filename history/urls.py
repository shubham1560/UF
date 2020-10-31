from django.urls import path, include
from .views import CreateHistoryRecord, GetHistoryRecords

urlpatterns = [
    path('post/', CreateHistoryRecord.as_view()),
    path('get/<str:record_id>/<str:record_type>/', GetHistoryRecords.as_view())
    # path('feature/post/', CreateFeatureViewSet.as_view()),
    # path('tickets/get/', GetSupportRecords.as_view()),
    # path('ticket/<int:record_id>/<str:record_type>/', GetSupportRowDetail.as_view())
]
