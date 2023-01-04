from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from .views import GetAuthors, GetAuthorDetail


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
        self.view = GetAuthors.as_view()
        self.url = reverse("get_author")

    def test_post_author(self):

        request = self.factory.post(self.url, data=DATA)
        request.user = self.user
        response = self.view(request)
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
        self.view(request)

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
        self.view = GetAuthorDetail.as_view()
        request = self.factory.put(self.url, data)
        request.user = self.user
        self.view(request, pk=id)
        response = self.client.get(reverse("get_author"), format="json")
        self.assertEqual(response.json()[0]["name"], "333")

    def test_author_remove(self):
        self.populate()
        response = self.client.get(reverse("get_author"), format="json")
        id = response.json()[0]["id"]
        self.view = GetAuthorDetail.as_view()
        request = self.factory.delete(self.url)
        request.user = self.user
        self.view(request, pk=id)
        response = self.client.get(reverse("get_author"), format="json")
        self.assertEqual(len(response.json()), 0)
