from django.db import models
from django.db.models.functions import Concat


class Author(models.Model):
    name = models.CharField("Authors name", max_length=120)
    last_name = models.CharField("Authors last name", max_length=120)
    email = models.CharField("Email", max_length=120, unique=True)
    phone = models.CharField("Phone", max_length=120)
    facebook_username = models.CharField("Facebook username", max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        db_table = "author"
