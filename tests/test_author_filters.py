from tests.test_data import *
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from authors.models import Author
from authors.views import FilterAuthors


class AuthorTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.view = FilterAuthors.as_view()
        self.url = reverse("filter_authors")
        self.authors = Author.objects.create(**AUTHOR_DATA_1), Author.objects.create(
            **AUTHOR_DATA_2
        )

    def test_author_is_populated(self):
        response = self.client.get(reverse("get_authors"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        for i, author in enumerate(AUTHOR_LIST):
            self.assertEqual(response.json()[i]["name"], author["name"])
    
    def test_filter_author_name(self):
        filter_url = self.url + "?name=Foo"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        filter_url = self.url + "?name=foo"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        filter_url = self.url + "?name=*o*"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_author_lastname(self):
        filter_url = self.url + "?last_name=Bar"
        response = self.client.get(filter_url, format="json")
        print(response.json())
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        filter_url = self.url + "?last_name=BAR"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        filter_url = self.url + "?last_name=*a*"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_filter_author_email(self):
        filter_url = self.url + "?email=mail"
        response = self.client.get(filter_url, format="json")
        print(response.json())
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        filter_url = self.url + "?email=email"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        filter_url = self.url + "?email=*il*"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    