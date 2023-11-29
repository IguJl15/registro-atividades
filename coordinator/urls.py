from django.urls import path

urlpatterns = [
    path("bolsistas/", ScholarsListView.as_view(), name="scholars_list")
]
