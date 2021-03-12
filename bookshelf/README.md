# BookShelf
This project is a virtual bookshelf for udacity.Students are able to add their books to the bookshelf, give them a rating, update the rating and search through their book lists. It's based on concept of interaction between the front end (which is react), and the back end (which is flask) using only APIs. 

The backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/)

## Getting Started
### Pre-requisites and Local Development
Developers using this project should already have Python3, pip and node installed on thier local machines.
#### Backend
From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file.  

To run the application on linux run the following commands after navigating to the backend file:
```
export Flask_App=flaskr
export FLASK_ENV=development    //only if you are not in production environment
flask run
```
These commands put the application in the development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the [Flask documentation](https://flask.palletsprojects.com/en/master/debugging/).  

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

#### Frontend
From the frontend folder, run the following commands to start the client.
```
npm install //only at the first time to install dependencies
npm start
```
By default, the frontend will run on `localhost:3000`.

### Tests
In order to run tests navigate to the backend folder and run the following commands:
```
dropdb bookshelf_test //omit this command if you are testing it for the first time
createdb bookshelf_test
psql bookshelf_test < books.psql
python API_test.py
```
For the first time you run the tests, omit the dropdb command.
All tests are kept in that file and should be maintained as updates are made to app functionality.

## API reference
### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend ishosted at the default,
`http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON object in the following format:
```
{
    "success":False,
    "error":400,
    "message":"Bad Request"
}
```

The API will return three error types when requests fail

* 400: Bad Request
* 404: Resource Not Found
* 422: Not Processable

### Endpoints

#### GET /books
* **General:**
  * Returns a list of book objects success value and total number of books
  * Results are paginated in groups of 8. Include `page` request argument to choose a page number, starting from 1.
* **Sample:**`curl http://127.0.0.1:5000/books?page=1`
```
{
  "books": [
    {
      "author": "Stephen King",
      "id": 1,
      "rating": 5,
      "title": "The Outsider: A Novel"
    },
    {
      "author": "Lisa Halliday",
      "id": 2,
      "rating": 5,
      "title": "Asymmetry: A Novel"
    },
    {
      "author": "Kristin Hannah",
      "id": 3,
      "rating": 5,
      "title": "The Great Alone"
    },
    {
      "author": "Tara Westover",
      "id": 4,
      "rating": 5,
      "title": "Educated: A Memoir"
    },
    {
      "author": "Jojo Moyes",
      "id": 5,
      "rating": 5,
      "title": "Still Me: A Novel"
    },
    {
      "author": "Leila Slimani",
      "id": 6,
      "rating": 5,
      "title": "Lullaby"
    },
    {
      "author": "Amitava Kumar",
      "id": 7,
      "rating": 5,
      "title": "Immigrant, Montana"
    },
    {
      "author": "Madeline Miller",
      "id": 8,
      "rating": 5,
      "title": "CIRCE"
    }
  ],
"success": true,
"total_books": 18
}
```
#### POST /books
* **General:**
    * Creates a new book using the submitted title, author and rating. Returns the id of the created book, success value, total books, and book list based on current page number to update the frontend.
* **Sample:** `curl http://127.0.0.1:5000/books?page=3 -X POST -H "Content-Type: application/json" -d '{"title":"Neverwhere", "author":"Neil Gaiman", "rating":"5"}'`
```
{
"books": [
  {
    "author": "Neil Gaiman",
    "id": 24,
    "rating": 5,
    "title": "Neverwhere"
  }
],
"created": 24,
"success": true,
"total_books": 17
}
```
#### DELETE /books/{book_id}
* **General:**
    * Deletes the book of the given ID if it exists. Returns the id of the deleted book, success value, total books, and book list based on current page number to update the frontend.
* **Sample:** `curl -X DELETE http://127.0.0.1:5000/books/16?page=2`
```
{
"books": [
  {
    "author": "Gina Apostol",
    "id": 9,
    "rating": 5,
    "title": "Insurrecto: A Novel"
  },
  {
    "author": "Tayari Jones",
    "id": 10,
    "rating": 5,
    "title": "An American Marriage"
  },
  {
    "author": "Jordan B. Peterson",
    "id": 11,
    "rating": 5,
    "title": "12 Rules for Life: An Antidote to Chaos"
  },
  {
    "author": "Kiese Laymon",
    "id": 12,
    "rating": 1,
    "title": "Heavy: An American Memoir"
  },
  {
    "author": "Emily Giffin",
    "id": 13,
    "rating": 4,
    "title": "All We Ever Wanted"
  },
  {
    "author": "Jose Andres",
    "id": 14,
    "rating": 4,
    "title": "We Fed an Island"
  },
  {
    "author": "Rachel Kushner",
    "id": 15,
    "rating": 1,
    "title": "The Mars Room"
  }
],
"deleted": 16,
"success": true,
"total_books": 15
}
```
#### PATCH /books/{book_id}
* **General:**
    * If provided, updates the rating of the specified book. Returns the success value and id of the modified book.
* **Sample:** `curl http://127.0.0.1:5000/books/15 -X PATCH -H "Content-Type: application/json" -d '{"rating":"1"}'`
``` 
{ 
  "id": 15,
  "success": true
}
```
# Deployment N/A
# Authors
Yours truly Mohamed Saeed, Caryn
# Acknowledgements
The awsome team at Udacity.
