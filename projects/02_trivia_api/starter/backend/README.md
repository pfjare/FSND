# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

# API Documentation

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "Bad Request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Unprocessable Entity
- 500: Internal Server Error

## The question object

Contains the unique id of the question, the question itself, the answer to the question, the question category, and the question difficulty.

### Example

```
{
    'id': 22,
    'question': "What is capital of Montana?",
    'answer': "Helena",
    'category': 1
    'difficulty': 3
}
```

## Endpoints

GET /api/categories

GET /api/questions

POST /api/questions

DELETE /api/questions/:id

POST /api/questions/search

GET /api/categories/:id/questions

POST /api/quizzes

---

### GET /categories

Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.

**Query String Parameters:** None

**Returns:** An object with a single key, categories, that contains a object of id: category_string key:value pairs.

`curl http://127.0.0.1:5000/categories`

Response

```
{
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
}
```

### GET /questions

Fetches all questions in the dataset.

**Query String Parameters:**

page \[int\] (optional) - Questions are paginated in groups of 10. Include a page argument to retreive the desired page. If unspecified the page defaults to 1.

**Returns:** A dictionary with a questions property that contains an array of question objects. If there are no questions in the database, the resulting array will be empty. The dictionary also contains a categories object, a success value, and the total number of questions.

`curl http://127.0.0.1:5000/questions?page=1`

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
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
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
        }
    ],
    "success": true,
    "total_questions": 19
}
```

### POST /api/questions

Creates a new question in the database.

**Query String Parameters:**
None

**Body Parameters:**

question \[string\] (required) - The question itself.

answer \[string\] (required) - The answer to the question.

category \[int\] (required) - The question category.

difficulty \[int\] (required) - The question difficulty.

**Returns:** A success value and the id of the created question.

`curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is the capital of Montana, USA?", "answer": "Helena", "category": 3, "difficulty": 2}'`

```
{
    "created": 24,
    "success": true
}
```

### DELETE /api/questions/:id

Deletes a question in the database with the specified id.

**Query String Parameters:**
None

**Body Parameters:**
None

**Returns:** A success value and the id of the deleted question.

`curl -X DELETE http://127.0.0.1:5000/questions/24`

```
{
    "deleted": 24,
    "success": true
}
```

### POST /questions/search

Fetches questions from the database for which the search term
is a substring of the question. The search term is case insensitive.

**Query String Parameters:**

page \[int\] (optional) - Questions are paginated in groups of 10. Include a page argument to retreive the desired page. If unspecified the page defaults to 1.

**Body Parameters:**

search_term \[string\] (required) - Search term to use in query.

**Returns:** A dictionary with a questions property that contains an array of question objects. If no questions match the search term, the resulting array will be empty. The dictionary also contains a success value and the total number of questions.

`curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"search_term": "title"}'`

```
{
    "questions": [
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
        }
    ],
    "success": true,
    "total_questions": 2
}
```

### GET /categories/:id/questions

Fetches all questions in a given category.

**Query String Parameters:**

page \[int\] (optional) - Questions are paginated in groups of 10. Include a page argument to retreive the desired page. If unspecified the page defaults to 1.

**Returns:** A dictionary with a questions property that contains an array of question objects. If there are no questions in the category, the resulting array will be empty. The dictionary also contains the current category, a success value, and the total number of questions in the category.

`curl http://127.0.0.1:5000/categories/3/questions?page=1`

```
{
    "current_category": 3,
    "questions": [
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
    "total_questions": 3
}
```

### POST /quizzes

Fetches a single question from the database for the next quiz question given a category and previously answered questions. The returned question is a random selection from the remaining questions in the category.

**Query String Parameters:**

None

**Body Parameters:**

quiz_category \[int\] (required) - Quiz category. If you want the quiz to include all categories put 0 here.

previous_questions \[list\] (required) - A list of previosly answered quiz questions specified by question id.

**Returns:** A success value and a single question object.

`curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category": 4, "previous_questions": [5, 9]}'`

```
{
    "question": {
        "answer": "Scarab",
        "category": 4,
        "difficulty": 4,
        "id": 23,
        "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    "success": true
}
```

## Changes to frontend

- Altered the format of the request body sent to /quizzes endpoint
- Made changes to QuestionView.js to allow paging to work for categories and search.
- Fixed bug in quiz anwer evaluation where only single word answers were evaluated properly.

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
