### Installing

Start Django server

```
pip install -f reqs.txt
django-admin makemigrations
django-admin migrate
django-admin createsuperuser
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

## Paths

### Default paths

```
localhost:8000/books/         [GET, POST]
localhost:8000/books/X        [GET,PUT,DELETE]
localhost:8000/books/genres/  [GET, POST]
localhost:8000/books/genres/X [GET,PUT,DELETE]
localhost:8000/authors/       [GET, POST]
localhost:8000/authors/X      [GET,PUT,DELETE]
```

### Filter paths

#### Books

```
localhost:8000/books/filter   [GET]
```
http params

`title` (str) - exact number of pages. Adding `*` around param will do partial search

`page` (int) - exact number of pages

`min_pages` (int) - minimum pages. This param is igrnored if `page` is provided

`max_pages` (int) - maximum pages. This param is igrnored if `page` is provided

`date` (str YYYY-MM-DD) - exact date published

`min_date` (str YYYY-MM-DD) - minimum dates. This param is igrnored if `date` is provided

`max_date` (str YYYY-MM-DD) - maximum dates. This param is igrnored if `date` is provided

`author_id` (int) - author id

`author_name` (str) - author name. This param is igrnored if `author_id` is provided

`author_lastname` (str) - author last name. This param is igrnored if `author_id` is provided

#### Authors

```
localhost:8000/authors/filter   [GET]
```
http params

`name` (str) - authors name. Adding `*` around param will do partial search

`lastname` (str) - authors name. Adding `*` around param will do partial search

`email` (str) - authors name. Adding `*` around param will do partial search

