from django.urls import path

from coordinator.views import ScholarListView, ScholarCreateView

urlpatterns = [
    path("bolsistas/", ScholarListView.as_view(), name="scholars_list"),
    path("bolsistas/novo", ScholarCreateView.as_view(), name="create_scholar"),
]
