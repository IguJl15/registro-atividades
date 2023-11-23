
from django.contrib import admin
from django.urls import path, include
from records import urls as record_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registros/', include(record_urls))
]
