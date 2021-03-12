# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others. 

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
dropdb trivia_test //omit this command if you are testing it for the first time
createdb trivia_test
psql bookshelf_test < trivia.psql
python test_flaskr.py
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

The API will return one of the following error types when requests fail

* 400: Bad Request
* 404: Not Found
* 405: Method Not Allowed
* 422: Unprocessable Entity

### Endpoints

#### GET /categories
* **General:**
  * Returns a list of category objects success value and total number of books
* **Sample:**`curl http://127.0.0.1:5000/categories`
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```
#### GET /categories/{category_id}/questions
* **General:**
  * Returns a list of category objects `categories`, success value, questions array, and total number of questions
  * Results are paginated in groups of 10. Include `page` request argument to choose a page number, starting from 1.
* **Sample:**`curl http://127.0.0.1:5000/categories/1/questions`
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": {
    "1": "Science"
  },
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Apollo 13",
      "category": 1,
      "difficulty": 4,
      "id": 24,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```
#### GET /questions
* **General:**
    * Returns a list of category objects `categories`, success value, questions array, and total number of questions.
    * Results are paginated in groups of 10. Include `page` request argument to choose a page number, starting from 1.
* `curl http://127.0.0.1:5000/questions?page=1 -X POST -H "Content-Type: application/json" -d '{"title":"Neverwhere", "author":"Neil Gaiman", "rating":"5"}'`
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": null,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```
#### POST /questions
* **General:**
    * Creates a new question using the submitted question, answer, category and difficulty. 
    * Returns the id of the created question, success value.
* **Sample:** `curl -X POST -H "Content-Type:application/json" -d '{"question": "what is the current year?","answer": 2020,"difficulty": 1,"category": 4}' http://127.0.0.1:5000/questions`
```
{
  "created": 26,
  "success": true
}
```
#### DELETE /questions/{book_id}
* **General:**
    * Deletes the question of the given ID if it exists. 
    * Returns the id of the deleted book, success value, total books, and book list based on current page number to update the frontend.
* **Sample:** `curl -X DELETE http://127.0.0.1:5000/questions/26`
```
{
  "deleted": 26,
  "success": true
}
```
#### POST /quizzes
* **General:**
    * provide a random selected question based on a given category and the previous asked ones.
* **Sample:** `curl -X POST -H "Content-Type:application/json" -d '{"previous_questions": [],"quiz_category": {"id":1,"type":"Science"}}'  http://127.0.0.1:5000/quizzes`
``` 
{
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
```
# Deployment N/A
# Authors
Yours truly Mohamed Saeed, Caryn
# Acknowledgements
The awsome team at Udacity.
