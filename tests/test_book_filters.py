from tests.test_data import *
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from books.models import Book, Genre
from authors.models import Author

# from authors.views import GetAuthors, GetAuthorDetail
from books.views import GetBooks, GetGenres, FilterBooks


class BookFilterTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.factory = APIRequestFactory()
        self.view = FilterBooks.as_view()
        self.url = reverse("filter_books")
        self.genre = Genre.objects.create(**GENRE_DATA)
        self.authors = Author.objects.create(**AUTHOR_DATA_1), Author.objects.create(
            **AUTHOR_DATA_2
        )
        self.create_books()

    def create_books(self):
        book = Book.objects.create(**{**BOOK_DATA_1, "genre": self.genre})
        book.author.add(self.authors[0])
        book.save()

        book = Book.objects.create(**{**BOOK_DATA_2, "genre": self.genre})
        book.author.add(self.authors[1])
        book.save()

        book = Book.objects.create(**{**BOOK_DATA_3, "genre": self.genre})
        book.author.add(self.authors[0])
        book.author.add(self.authors[1])
        book.save()

    def test_book_is_populated(self):
        response = self.client.get(reverse("get_books"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)
        for i, book in enumerate(BOOK_LIST):
            self.assertEqual(response.json()[i]["title"], book["title"])

    def test_filter_book_tittle(self):
        filter_url = self.url + "?title=title"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        filter_url = self.url + "?title=*itl*"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        filter_url = self.url + "?title=*"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_book_page(self):
        filter_url = self.url + "?pages=22"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        filter_url = self.url + "?min_pages=22"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        filter_url = self.url + "?max_pages=22"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_book_pub_date(self):
        filter_url = self.url + "?min_date=1800-11-11"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        filter_url = self.url + "?max_date=1800-11-11"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        filter_url = self.url + "?max_date=1000-11-11"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_author_id(self):
        filter_url = self.url + "?author_id=1"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        filter_url = self.url + "?author_id=[1,2]"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_author_name(self):
        filter_url = self.url + "?author_name=Foo"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_author_lastname(self):
        filter_url = self.url + "?author_lastname=Bar"
        response = self.client.get(filter_url, format="json")
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
