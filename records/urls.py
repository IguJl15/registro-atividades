from django.urls import path

from records.views import (
    RecordCreateView,
    RecordDeleteView,
    RecordListView,
    RecordReportView,
    TestePdfView,
)

urlpatterns = [
    path("", RecordListView.as_view(), name="records_home"),
    path("novo", RecordCreateView.as_view()),
    path("relatorio", RecordReportView.as_view(), name="report"),
    path("pdf", TestePdfView.as_view(), name="pdf"),
    path("delete/<int:pk>/", RecordDeleteView.as_view(), name="delete"),
]
