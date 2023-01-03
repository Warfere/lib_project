## Library application (backend only – only REST API as a consumption method):


### User-Story1: 
- As a user I want to be able to list all books with their information (title, number of pages, release date, author, genre):
- same person can be an author of multiple books and a single book may be authored by multiple persons
- each book is only assigned to a single genre
- there can only be one copy of each book in the library
### User-Story2: 
- As a user I want to be able to list all authors with their information (name, surname, contact info: email, phone, facebook username if any, profile picture data field)
### User-Story3: 
- As a user I want to be able to filter books based on their title, number of pages, release date, author
- text filters should be case-insensitive
- text filters may allow for exact and partial match
- number of pages should be filtered exactly, more/less than and range (from-to)
- release date should be filtered exactly, earlier/later than and range (from date-to date)
- author filtered by author id (exactly), name, surname or the combo of name+surname
### User-Story4: 
- As a user I want to be able to filter authors based on their name, surname, email
- text filters should be case-insensitive
- text filters may allow for exact and partial match
### User-Story5:
- As a librarian want to be able to add new/update/remove books onto a library system
- only a librarian can manipulate books - users can only list them
- each book must have their title unique
- when the book is removed and any authors no longer have any books in the system - they should also be removed
### User-Story6: 
- As a librarian want to be able to add new/update/remove authors onto a library system
- only a librarian can manipulate authors - users can only list them
- author name + surname must be unique
- authors can only be removed when they don't have any books associated with them

`Non-functional:` each CRUD operation of each api endpoint should be tested with unit tests

`Non-functional:` the Django + Django Rest Framework should be used as the framework combo

`Non-functional:` the code should be stored in github as a separate remote repo


Also, please do not push to the original repository (in case you are allowed to do so in the first place) – create your own repo for your code.