import os
from re import search
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category
from sqlalchemy import func

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs

    CORS(app)

    #@TODO: Use the after_request decorator to set Access-Control-Allow

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')

        return response

    # @TODO:Create an endpoint to handle GET requests for all available categories.
    @app.route('/categories')
    def retrieve_categories():
        available_categories = Category.query.order_by(Category.type).all()

        #throw an error if category does not exist
        if len(available_categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in available_categories},
            'total_categories' : len(Category.query.all())
        })
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        categories = Category.query.order_by(Category.id).all()
        questions = Question.query.order_by(Question.id).all()

        # Trying to paginate 
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        paginated_questions = [question.format() for question in questions]
        retrieved_questions = paginated_questions[start:end]

        temp_categories = {}

        for category in categories:
            temp_categories.update({
                category.id: category.type
            })
        
        categories = temp_categories

        if len(categories) == 0:
            abort(404)

        if len(retrieved_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories,
            'questions' : retrieved_questions,
            'total_questions' :len(Question.query.all())
        })


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            if question is None:
                abort(404)

            question.delete()
            questions = Question.query.order_by(Question.id).all()
            retrieved_questions = paginate_questions (request,questions)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions' : retrieved_questions,
                'total_questions' :len(Question.query.all())                
            })

        except:
            abort(422)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    def create_question():

        data= request.get_json()
        if not ('question' in data and 'answer' in data and 'difficulty' in data and 'category' in data):
            abort(422)

        new_difficulty = data.get('difficulty',None)
        new_category = data.get('category',None)
        new_question = data.get('question',None)
        new_answer = data.get('answer',None)


        try:
            question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
            question.insert()


            return jsonify({
                'success': True,
                'created': question.id,
                'question': question.question,
                'answer': question.answer,
                'difficulty': question.difficulty,
                'category': question.category             
            })

        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        data = request.get_json()
        search_term = data.get('searchTerm', None)


        if search_term:
            search_results = Question.query.filter(
                func.lower(Question.question).contains(func.lower(search_term)))

            searched_questions = [question.format() for question in search_results]

            return jsonify({
                'success': True,
                'questions': searched_questions,
                'total_questions': len(searched_questions),
                'current_category': None
            })
        abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            # checking the category for the category_id
            questions = Question.query.filter(Question.category == str(category_id)).all()

            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'total_questions': len(questions),
                'current_category': category_id
            })
        except:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        
        try:
            data = request.get_json()
            previous_questions =data.get('previous_questions', None)
            quiz_category =data.get('quiz_category', None)
            category_id = quiz_category['id']

            if category_id == 0:
                questions = Question.query.filter(Question.id.notin_(previous_questions)).all()

            else:
                questions = Question.query.filter(Question.id.notin_(previous_questions),Question.category == category_id).all()

            if questions:
                selected_question = random.choice(questions)

            else:
                selected_question = None

            formatted_questions = selected_question.format()
            
            print(formatted_questions)

            return jsonify({
                'success': True,
                'question': formatted_questions
            })

        except:
            return jsonify({}), 209

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable resource'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Server Error'
        }), 500

    return app

