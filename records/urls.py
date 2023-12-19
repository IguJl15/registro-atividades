from django.urls import path
from records.views import (
    RecordCreateView,
    RecordListView,
    RecordReportView,
    TestePdfView,
    # EasyPdf,
)

urlpatterns = [
    path("", RecordListView.as_view(), name="records_home"),
    path("novo", RecordCreateView.as_view()),
    path("relatorio", RecordReportView.as_view(), name="report"),
    path("pdf", TestePdfView.as_view(), name="pdf"),
    # path("pdf2", EasyPdf.as_view(), name="pdf2")
]
