# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

### Endpoints'
<!-- GET /categories -->
-An endpoint to get a dictionary of all available categories.

-Example of JSON  response:

```
{
'success':True,
categories:{
 '1'	Science
 '2'	Art
 '3'	Geography
 '4'	History
 '5'	Entertainment
 '6'	Sports
}
}
```

<!-- GET /categories/<int:category_id>questions-->
-An endpoint that gets a dictionary of questions based on a specific category
-Request Arguments:category_id
-Example of JSON Response:
```
{
'success':True,
'questions':[
  {
    'answer': 'Lisbon', 
    'category': 2, 
    'difficulty': 1, 
    'id': 29, 
    'question': 'What is the capital of Portugal?'
  }
],
'total_questions':2,
'current_category':'Sports'
}
```

<!-- GET /questions -->
-An endpoint that gets a list of questions(including pagination every 10 questions),number of total questions, current category, categories.
-Request parameters:question_id
-Example of JSON Response:
```
{
  'success' :True,
  'questions' :[
    {
      'answer': 'Escher', 
      'category': 2, 
      'difficulty': 1, 
      'id': 16, 
      'question': 'Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?'      
    }
  ],
  'total_questions':2
  'categories': {
    '1': 'Science', 
    '2': 'Art', 
    '3': 'Geography', 
    '4': 'History', 
    '5': 'Entertainment', 
    '6': 'Sports'
  },
  'current_category': None  
}
```

<!-- DELETE /questions/<int:question_id>-->
-An endpoint that deletes a question from existing questions.
-Request arguments:question_id
-Example of JSON Response:
```
{
  'success': True,
  'deleted' :10
}
```

<!-- POST /questions -->
-An endpoint to create a new question.
-Request parameters:question,answer,difficulty,category
-Example of JSON Response:
```
{
  'success':True,
  'created':30,
  'category':'art'
}
```

<!-- POST /questions/search -->
-An endpoint to get questions based on a search term.
-Request arguments:searchTerm
-Example of JSON Response:
```
{
  'success':True,
  'questions':[
    {
      'answer': 'The Liver', 
      'category': 1, 
      'difficulty': 4, 
      'id': 20, 
      'question': 'What is the heaviest organ in the human body?'      
    }
  ],
  'total_questions':1,
  'current_category':None
}
```

<!-- GET /categories/<int:category_id>/questions-->
-An endpoint to get a dictionary of questions based on a category,
-Request argument:category_id
-Example of JSON Response:
```
{
  'success':True,
  'questions':[
    {
     'answer': 'Maya Angelou', 
     'category': 4, 
     'difficulty': 2, 
     'id': 5, 
     'question': 'Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?'
    },
    {
      'answer': 'Muhammad Ali', 
      'category': 4, 
      'difficulty': 1, 
      'id': 9, 
      'question': 'What boxer's original name is Cassius Clay?'
     }, 
    }
  ],
  'total_questions':2
  'current_category':2
}
```

<!-- POST /quizzes -->
-An endpoint to get questions using question id to avoid repetitions.
-Request argument:{past_questions,category,category_id}
-Example of JSON Response:
```
{
  'succcess':True,
  'question':{
    'answer': 'The Liver', 
    'category': 1, 
    'difficulty': 4, 
    'id': 20, 
    'question': 'What is the heaviest organ in the human body?'    
  }
}
```
## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
