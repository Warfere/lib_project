from django.db import models
from authors.models import Author
from django.utils import timezone
from django.contrib.postgres.fields import CICharField


class Genre(models.Model):
    name = CICharField(unique=True, max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "genres"


class Book(models.Model):
    title = models.CharField(
        "Name of the book", max_length=120, db_index=True, unique=True
    )
    number_of_pages = models.IntegerField("Number of pages", db_index=True, default=0)
    pub_date = models.DateField("Date published", db_index=True, default=timezone.now)
    author = models.ManyToManyField(
        Author,
        db_index=True,
    )
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, db_index=True, default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self):
        authors = Author.objects.filter(book=self)
        if authors:
            for author in authors:
                books = Book.objects.filter(author=author)
                if books.count() == 1:
                    author.delete()
        super(Book, self).delete()


    class Meta:
        db_table = "books"
