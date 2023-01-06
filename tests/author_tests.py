from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from authors.views import GetAuthors, GetAuthorDetail
from books.tests.tests import BOOK_DATA
from books.views import GetBooks, GetGenres

DATA = {
    "name": "aaaaa",
    "last_name": "asdasd",
    "phone": "123",
    "email": "123",
    "facebook_username": "asfas",
}


class AuthorTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        get_user_model().objects.create_user(
            email="test@uxstudio.nl", username="admin", password="testpass"
        )
        self.user = get_user_model().objects.get(username="admin")
        self.factory = APIRequestFactory()
        self.view = GetAuthorDetail.as_view()
        self.url = reverse("get_author")

    def test_post_author(self):
        request = self.factory.post(self.url, data=DATA)
        request.user = self.user
        response = GetAuthors.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], DATA["name"])

    def test_get_authors(self):
        self.populate()
        response = self.client.get(reverse("get_author"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["name"], DATA["name"])

    def populate(self):
        request = self.factory.post(self.url, data=DATA)
        request.user = self.user
        d = GetAuthors.as_view()(request)

    def test_author_update(self):
        self.populate()
        response = self.client.get(reverse("get_author"), format="json")
        id = response.json()[0]["id"]
        data = {
            "name": "333",
            "last_name": "asdasd",
            "phone": "123",
            "email": "123",
            "facebook_username": "asfas",
        }
        request = self.factory.put(self.url, data)
        request.user = self.user
        self.view(request, pk=id)
        response = self.client.get(reverse("get_author"), format="json")
        self.assertEqual(response.json()[0]["name"], "333")

    def test_author_remove(self):
        self.populate()
        response = self.client.get(reverse("get_author"), format="json")
        id = response.json()[0]["id"]
        request = self.factory.delete(self.url)
        request.user = self.user
        self.view(request, pk=id)
        response = self.client.get(reverse("get_author"), format="json")
        self.assertEqual(len(response.json()), 0)

    def test_author_book_constrain(self):
        self.populate()
        self.populate_genre()
        response = self.client.get(reverse("get_author"), format="json")
        id = response.json()[0]["id"]
        self.populate_book([id])
        request = self.factory.delete(self.url)
        request.user = self.user
        d = self.view(request, pk=id)
        response = self.client.get(reverse("get_author"), format="json")
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(d.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(d.data["protected_elements"]), 1)

    def populate_book(self, authors_id):
        request = self.factory.post(
            reverse("get_books"), data={**BOOK_DATA, "author": authors_id}
        )
        request.user = self.user
        s = GetBooks.as_view()(request)

    def populate_genre(self):
        data = {
            "name": "genre",
        }
        request = self.factory.post(reverse("get_genres"), data=data)
        request.user = self.user
        GetGenres.as_view()(request)
