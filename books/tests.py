from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from .views import GetBooks, GetBookDetail, GetGenres
from authors.views import GetAuthors


BOOK_DATA = {
    "title": "1",
    "number_of_pages": 11,
    "pub_date": "1111-11-11",
    "created_at": "2022-12-22T15:16:37.367045Z",
    "updated_at": "2022-12-22T15:16:37.367045Z",
    "genre": 1,
    "author": [1],
}


AUTHOR_DATA = {
    "name": "author",
    "last_name": "author_last",
    "phone": "123",
    "email": "123",
    "facebook_username": "asfas",
}


class CustomAPITestCase(APITestCase):
    def assertHTMLStatus200(self, response) -> None:
        return super().assertEqual(response.status_code, status.HTTP_200_OK)


class BooksrTestCase(CustomAPITestCase):
    def setUp(self):
        self.client = APIClient()
        get_user_model().objects.create_user(
            email="test@uxstudio.nl", username="admin", password="admin"
        )
        self.user = get_user_model().objects.get(username="admin")
        self.factory = APIRequestFactory()
        self.view = GetBooks.as_view()
        self.url = reverse("get_books")
        self.populate_author()
        self.populate_genre()

    def test_post(self):
        request = self.factory.post(self.url, data=BOOK_DATA)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], BOOK_DATA["title"])

    def test_get_bookss(self):
        self.populate()
        response = self.client.get(reverse("get_books"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["title"], "1")

    def populate(self, data=BOOK_DATA):
        request = self.factory.post(self.url, data=data)
        request.user = self.user
        self.view(request)

    def populate_author(self):

        request = self.factory.post("/authos", data=AUTHOR_DATA)
        request.user = self.user

        GetAuthors.as_view()(request)
        
        data = {**AUTHOR_DATA, 'name': 'name2', 'last_name': 'last_name2', 'email': 'new_email'}
        request = self.factory.post("/authos", data=data)
        request.user = self.user

        GetAuthors.as_view()(request)

    def populate_genre(self):
        data = {
            "name": "genre",
        }
        request = self.factory.post(reverse("get_genres"), data=data)
        request.user = self.user

        GetGenres.as_view()(request)

    
    def test_get_genre(self):
        response = self.client.get(reverse("get_genres"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["name"], "genre")
        self.assertHTMLStatus200(response)

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
        request = self.factory.put(self.url+str(id)+'/', data)
        request.user = self.user
        self.view(request, pk=id)
        response = self.client.get(reverse("get_books")+str(id)+'/', format="json")
        self.assertEqual(response.json()["title"], "333")
        self.assertEqual(response.json()["author"], [1, 2])

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
    