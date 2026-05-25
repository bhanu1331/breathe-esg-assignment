from django.urls import path
from .views import (
    RecordListView,
    SuspiciousRecordView,
    PendingRecordView,
    FailedRecordView,
    ApproveRecordView,
    RejectRecordView,
    LockRecordView,
)

urlpatterns = [
    path("records/", RecordListView.as_view()),
    path("records/pending/", PendingRecordView.as_view()),
    path("records/suspicious/", SuspiciousRecordView.as_view()),
    path("records/failed/", FailedRecordView.as_view()),
    path("records/<int:record_id>/approve/", ApproveRecordView.as_view()),
    path("records/<int:record_id>/reject/", RejectRecordView.as_view()),
    path("records/<int:record_id>/lock/", LockRecordView.as_view()),
]