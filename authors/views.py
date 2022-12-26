from rest_framework import generics
from .models import Author
from .serializers import AuthorSerializer
from rest_framework import permissions, exceptions, filters

SEARCH_FIELDS = ["name", "last_name", "email", "phone", "facebook_username"]


class GetAuthors(generics.ListCreateAPIView):
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = SEARCH_FIELDS

    def get_queryset(self):
        authors = Author.objects.all()
        author_id: int = self.request.query_params.get("author_id")
        if author_id:
            authors = authors.filter(id=author_id)
        return authors

    def perform_create(self, serializer=AuthorSerializer):
        authors = Author.objects.values("name", "last_name")
        for author in authors:
            if (
                self.request.POST.get("name", "").lower() == author["name"].lower()
                and self.request.POST.get("last_name", "").lower()
                == author["last_name"].lower()
            ):
                raise exceptions.ValidationError(
                    "Name and last name must be unique", code=400
                )
        serializer.save()


class GetAuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Author.objects.all()
