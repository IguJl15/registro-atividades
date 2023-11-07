from django import urls

from users import views


urlpatterns = [
    urls.path("", views.index, name="index")
]
