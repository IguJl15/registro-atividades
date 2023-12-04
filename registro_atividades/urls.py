from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

from coordinator import urls as coordinator_urls
from records import urls as record_urls
from users import urls as users_urls

urlpatterns = [
    path("", RedirectView.as_view(url='/registros'), name=""),
    path("admin/", admin.site.urls),
    path("registros/", include(record_urls)),
    path("", include(users_urls)),
    path("", include(coordinator_urls)),
]
