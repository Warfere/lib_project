from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.GetAuthors.as_view(), name="get_author"),
    path("<int:pk>/", view=views.GetAuthorDetail.as_view(), name="get_author_detail"),
    path("filter/", view=views.FilterAuthors.as_view(), name="filter_author"),
]
