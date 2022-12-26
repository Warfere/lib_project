from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("books/", include("books.url")),
    path("authors/", include("authors.url")),
]

urlpatterns.append(path("auth", include("rest_framework.urls")))
