from rest_framework import generics
from .models import Book, Genre
from .serializers import BookSerializer, GenreSerializer
from rest_framework import permissions, exceptions
import datetime
from .book_dataclass import BookDataClass


class GetBooks(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        books = Book.objects.all()
        book_id = self.request.query_params.get("book_id")
        if book_id:
            books = books.filter(id=book_id)
        return books

    def perform_create(self, serializer=GenreSerializer):
        books = Book.objects.values("title")
        for book in books:
            if self.request.POST["title"].lower() == book["title"].lower():
                raise exceptions.ValidationError("Name must be unique", code=400)
        serializer.save()


class GetBookDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class GetGenres(generics.ListCreateAPIView):
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer=GenreSerializer):
        genres = Genre.objects.values("name")
        for genre in genres:
            if self.request.POST["name"].lower() == genre["name"].lower():
                raise exceptions.ValidationError("Name must be unique", code=400)
        serializer.save()

    def get_queryset(self):
        genres = Genre.objects.all()
        author_id = self.request.query_params.get("author_id")
        if author_id:
            genres = genres.filter(id=author_id)
        return genres


class GetGenreDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class FilterBooks(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        books = Book.objects.filter()
        validate_params = self.validate_search_params(self.request.query_params)
        if not validate_params[1]:
            raise exceptions.ParseError(
                f"{validate_params[0]} is not recognized as filter", code=400
            )
        book_dataclass = BookDataClass(
            pages=self.request.query_params.get("pages"),
            min_pages=self.request.query_params.get("min_pages"),
            max_pages=self.request.query_params.get("max_pages"),
            date=self.request.query_params.get("date"),
            min_date=self.request.query_params.get("min_date"),
            max_date=self.request.query_params.get("max_date"),
            author_id=self.request.query_params.get("author_id"),
            author_name=self.request.query_params.get("author_name"),
            author_lastname=self.request.query_params.get("author_lastname"),
            title=self.request.query_params.get("title"),
        )
        try:
            if book_dataclass.pages:
                books = books.filter(number_of_pages=book_dataclass.pages)

            if (
                book_dataclass.min_pages or book_dataclass.max_pages
            ) and not book_dataclass.pages:
                min_pages = (
                    book_dataclass.min_pages if book_dataclass.min_pages else 0
                )
                max_pages = (
                    book_dataclass.max_pages if book_dataclass.max_pages else 999999
                )
                books = books.filter(number_of_pages__range=(min_pages, max_pages))

            if book_dataclass.date:
                books = books.filter(pub_date=book_dataclass.date)

            if (
                book_dataclass.min_date or book_dataclass.max_date
            ) and not book_dataclass.date:
                min_date = (
                    book_dataclass.min_date
                    if book_dataclass.min_date
                    else datetime.date(0, 1, 3)
                )
                max_date = (
                    book_dataclass.max_date
                    if book_dataclass.max_date
                    else datetime.date(9999, 12, 12)
                )
                books = books.filter(pub_date__gt=min_date, pub_date__lt=max_date)

            if book_dataclass.author_id:
                books = books.filter(author=book_dataclass.author_id)
            if book_dataclass.author_name and not book_dataclass.author_id:
                books = books.filter(author__name=book_dataclass.author_name)
            if book_dataclass.author_lastname and not book_dataclass.author_id:
                books = books.filter(author__last_name=book_dataclass.author_lastname)
            if (book_dataclass.author_lastname and book_dataclass.author_name) and not book_dataclass.author_id:
                books = books.filter(
                    author__last_name=book_dataclass.author_lastname,
                    author__name=book_dataclass.author_name,
                )
            if book_dataclass.title:
                if book_dataclass.title[0] == "*" and book_dataclass.title[-1] == "*":
                    books = books.filter(title__icontains=book_dataclass.title[1:-1])
                else:
                    books = books.filter(title=book_dataclass.title)
                
        except ValueError as e:
            raise exceptions.ParseError(e, code=400)
        return books

    def validate_search_params(self, params):
        for param in params.keys():
            if param not in BookDataClass.__dataclass_fields__.keys():
                return param, False
        return "", True
