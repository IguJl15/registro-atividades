
from django.urls import path
from records.views import RecordCreateView, RecordListView, RecordReportView

urlpatterns = [
    path("", RecordListView.as_view(), name="records_home"),
    path("novo", RecordCreateView.as_view()),
    path("relatorio", RecordReportView.as_view(), name="report")
]
