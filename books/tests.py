from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from .views import GetBooks, GetBookDetail, GetGenres
from authors.views import GetAuthors


class BooksrTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        get_user_model().objects.create_user(
            email="test@uxstudio.nl", username="admin", password="testpass"
        )
        self.user = get_user_model().objects.get(username="admin")
        self.factory = APIRequestFactory()
        self.view = GetBooks.as_view()
        self.url = reverse("get_books")
        self.populate_author()
        self.populate_genre()

    def test_post(self):
        data = {
            "title": "1",
            "number_of_pages": 11,
            "pub_date": "1111-11-11",
            "created_at": "2022-12-22T15:16:37.367045Z",
            "updated_at": "2022-12-22T15:16:37.367045Z",
            "genre": 1,
            "author": [1],
        }
        request = self.factory.post(self.url, data=data)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])

    def test_get_bookss(self):
        self.populate()
        response = self.client.get(reverse("get_books"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["title"], "1")

    def populate(self):
        data = {
            "title": "1",
            "number_of_pages": 11,
            "pub_date": "1111-11-11",
            "created_at": "2022-12-22T15:16:37.367045Z",
            "updated_at": "2022-12-22T15:16:37.367045Z",
            "genre": 1,
            "author": [1],
        }
        request = self.factory.post(self.url, data=data)
        request.user = self.user
        self.view(request)

    def populate_author(self):
        data = {
            "name": "author",
            "last_name": "asdasd",
            "phone": "123",
            "email": "123",
            "facebook_username": "asfas",
        }
        request = self.factory.post("/authos", data=data)
        request.user = self.user

        GetAuthors.as_view()(request)
        data = {
            "name": "author1",
            "last_name": "asdasd1",
            "phone": "123",
            "email": "123",
            "facebook_username": "asfas",
        }
        request = self.factory.post("/authos", data=data)
        request.user = self.user

        GetAuthors.as_view()(request)

    def populate_genre(self):
        data = {
            "name": "genre",
        }
        request = self.factory.post("/authos", data=data)
        request.user = self.user

        GetGenres.as_view()(request)

    def test_book_update(self):
        self.populate()
        response = self.client.get(reverse("get_books"), format="json")
        id = response.json()[0]["id"]
        data = {
            "title": "333",
            "number_of_pages": 11,
            "pub_date": "1111-11-11",
            "created_at": "2022-12-22T15:16:37.367045Z",
            "updated_at": "2022-12-22T15:16:37.367045Z",
            "genre": 1,
            "author": [1, 2],
        }
        self.view = GetBookDetail.as_view()
        request = self.factory.put(self.url, data)
        request.user = self.user
        self.view(request, pk=id)
        response = self.client.get(reverse("get_books"), format="json")
        self.assertEqual(response.json()[0]["title"], "333")
        self.assertEqual(response.json()[0]["author"], [1, 2])

    def test_book_remove(self):
        self.populate()
        response = self.client.get(reverse("get_books"), format="json")
        id = response.json()[0]["id"]
        self.view = GetBookDetail.as_view()
        request = self.factory.delete(self.url)
        request.user = self.user
        self.view(request, pk=id)
        response = self.client.get(reverse("get_books"), format="json")
        self.assertEqual(len(response.json()), 0)
