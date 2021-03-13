import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
from werkzeug.exceptions import HTTPException

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    current_index = page - 1
    items_limit = request.args.get('limit', QUESTIONS_PER_PAGE, type=int)
    #start = (page-1)*QUESTIONS_PER_PAGE
    #end = start + QUESTIONS_PER_PAGE
    paged_Selection = selection.limit(items_limit).offset(current_index * items_limit).all()
    current_questions = [question.format() for question in paged_Selection]
    # current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @Done: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={r'/*': {'origins': '*'}})

    '''
  @Done: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type , Accept ,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        return jsonify({
            'success': True,
            'total_categories': len(categories),
            'categories': {category.id: category.type for category in categories}
        })
    '''
      @Done:
      Create an endpoint to handle GET requests for questions,
      including pagination (every 10 questions).
      This endpoint should return a list of questions,
      number of total questions, current category, categories.

      TEST: At this point, when you start the application
      you should see questions and categories generated,
      ten questions per page and pagination at the bottom of the screen for three pages.
      Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions', methods=['GET'])
    def get_paginated_questions():

        selection = Question.query.order_by(Question.id)
        categories_collection = Category.query.order_by(Category.id).all()
        categories = {
            category.id: category.type for category in categories_collection
        }
        currentCategory = None
        current_questions = paginate_questions(request, selection)
        if len(current_questions) == 0:
            abort(404)
        return jsonify({
            'success':True,
            'questions': current_questions,
            'categories': categories,
            'currentCategory': currentCategory,
            'total_questions': len(selection.all())
        })

    '''
    @Done: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        success = False
        try:
            question = Question.query.get(question_id)
            print(question)
            question.delete()
            success = True
        except Exception as e:
            print(e)
            abort(422)
        if success:
            return jsonify({
                'success': True,
                'deleted': question_id
            })
    '''
    @Done: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)
        searchTerm = body.get('searchTerm', None)
        currentCategory = body.get('currentCategory', None)
        try:
            if searchTerm:
                selection = Question.query.filter(
                    Question.question.ilike('%{}%'.format(searchTerm))).order_by(Question.id)
                current_questions = paginate_questions(request, selection)
                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'totalQuestions': len(selection.all()),
                    'currentCategory': currentCategory
                })
            else:
                question = Question(question=question, answer=answer,
                                    category=category, difficulty=difficulty)
                question.insert()
                return jsonify({
                    'success': True,
                    'created': question.id
                })
        except Exception as e:
            print(e)
            abort(422)

    '''
    @Done above: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
  @Done: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_paginated_category_questions(category_id):
        currentCategory = Category.query.filter(
            Category.id == category_id).one_or_none()
        if currentCategory is None:
            abort(404)
        selection = Question.query.filter(
            Question.category == category_id).order_by(Question.id)
        categories_collection = Category.query.order_by(Category.id).all()
        current_questions = paginate_questions(request, selection)

        return jsonify({
            'success':True,
            'questions': current_questions,
            'total_questions': len(selection.all()),
            'categories': {category.id: category.type for category in categories_collection},
            'currentCategory': {currentCategory.id: currentCategory.type}
        })

    '''
  @Done: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_next_question():
        body = request.get_json()
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)
        print(quiz_category)
        #trial = Question.query.filter(~Question.id.in_(previous_questions),Question.category == quiz_category['id']).all()
        #print('total found ',len(trial))
        next_question = None
        if quiz_category == None or quiz_category['id'] == 0:
            next_question = Question.query.filter(
                ~Question.id.in_(previous_questions)).first()
            print(next_question)
        else:
            next_question = Question.query.filter(~Question.id.in_(
                previous_questions), Question.category == quiz_category['id']).first()
            print(next_question)

        if next_question is None:
            return jsonify({
                'success': True,
                'question': None
            })
        else:
            return jsonify({
                'success': True,
                'question': next_question.format()
            })

    '''
    @Done: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    @app.errorhandler(HTTPException)
    def generic_exception_Handler(e):
        return jsonify({
            'success': False,
            'code': e.code,
            'message': e.name
        }), e.code

    return app
