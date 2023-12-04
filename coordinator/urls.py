from django.urls import path

from coordinator.views import (
    ScholarCreateView,
    ScholarCreateWithSearchView,
    ScholarListView,
)

urlpatterns = [
    path("bolsistas/", ScholarListView.as_view(), name="scholars_list"),
    path("bolsistas/novo", ScholarCreateView.as_view(), name="create_scholar"),
    path(
        "bolsistas/adicionar",
        ScholarCreateWithSearchView.as_view(),
        name="add_scholar",
    ),
]
