from django.urls import path
from . import views

urlpatterns = [
    path("genres/", view=views.GetGenres.as_view(), name="get_genres"),
    path("genres/<int:pk>/", view=views.GetGenreDetail.as_view()),
    path("", view=views.GetBooks.as_view(), name="get_books"),
    path("<int:pk>/", view=views.GetBookDetail.as_view()),
    path("filter/", view=views.FilterBooks.as_view()),
]
