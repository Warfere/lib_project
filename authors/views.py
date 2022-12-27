from rest_framework import generics
from .models import Author
from .serializers import AuthorSerializer
from rest_framework import permissions, exceptions
from .author_dataclass import AuthorDataClass


class GetAuthors(generics.ListCreateAPIView):
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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


class FilterAuthors(generics.ListAPIView):
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        authors = Author.objects.filter()
        validate_params = self.validate_search_params(self.request.query_params)
        if not validate_params[1]:
            raise exceptions.ParseError(
                f"{validate_params[0]} is not recognized as filter", code=400
            )
        author_dataclass = AuthorDataClass(
            name=self.request.query_params.get("name"),
            lastname=self.request.query_params.get("lastname"),
            email=self.request.query_params.get("email"),
        )
        try:
            if author_dataclass.name:
                search = self.construct_search(author_dataclass.name, 'name')
                authors = authors.filter(**search)
            if author_dataclass.lastname:
                search = self.construct_search(author_dataclass.lastname, 'lastname')
                authors = authors.filter(**search)
            if author_dataclass.email:
                search = self.construct_search(author_dataclass.email, 'email')
                authors = authors.filter(**search)
        except ValueError as e:
            raise exceptions.ParseError(e, code=400)
        return authors

    def validate_search_params(self, params):
        for param in params.keys():
            if param not in AuthorDataClass.__dataclass_fields__.keys():
                return param, False
        return "", True
    pass

    def exact_search(self, filter_value):
        if filter_value[0] == "*" and filter_value[-1] == "*":
            return False
        return True

    def construct_search(self, filter_value, search_field):
        if self.exact_search(filter_value):
            return {search_field+'__iexact': filter_value}
        else:
            return {search_field+'__icontains': filter_value[1:-1]}