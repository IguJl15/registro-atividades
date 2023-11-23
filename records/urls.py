
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from records.views import RecordCreateView, RecordListView

urlpatterns = [
    path("", RecordListView.as_view()),
    path("novo", RecordCreateView.as_view())
]
