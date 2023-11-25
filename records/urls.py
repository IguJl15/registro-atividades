
from django.urls import path
from records.views import RecordCreateView, RecordListView

urlpatterns = [
    path("", RecordListView.as_view()),
    path("novo", RecordCreateView.as_view())
]
