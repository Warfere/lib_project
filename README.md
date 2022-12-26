### Installing

Start Django server

```
pip install -f reqs.txt
django-admin makemigrations
django-admin migrate
django-admin runserver
```

End with an example of getting some data out of the system or using it for a little demo.

## 🔧 Running the tests <a name = "tests"></a>

```
django-admin test
```

### Coding style tests

```
black .
```

### Paths

```
localhost:8000/books/         [GET, POST]
localhost:8000/books/X        [GET,PUT,DELETE]
localhost:8000/books/genres/  [GET, POST]
localhost:8000/books/genres/X [GET,PUT,DELETE]
localhost:8000/authors/       [GET, POST]
localhost:8000/authors/X      [GET,PUT,DELETE]
```


