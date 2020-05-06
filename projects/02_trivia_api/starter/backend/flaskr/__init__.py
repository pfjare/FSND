import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, exc
from flask_cors import CORS
import math
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()

        if len(categories) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in categories}
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page-1)*10
        end = start + 10
        questions = Question.query.order_by(Question.id).all()
        if len(questions[start:end]) == 0:
            abort(404)
        formatted_questions = [question.format() for question in questions]
        categories = Category.query.all()
        if len(categories) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions': len(formatted_questions),
            'categories': {category.id: category.type for category in categories}
        })

    @app.route('/questions', methods=["POST"])
    def create_question():
        data = request.get_json()
        print(data.get('question'))

        question = data.get('question', None)
        answer = data.get('answer', None)
        category = data.get('category', None)
        difficulty = data.get('difficulty', None)
        if question and answer and category and difficulty:
            try:
                question = Question(question=question,
                                    answer=answer,
                                    category=category,
                                    difficulty=difficulty)

                question.insert()
                return jsonify({
                    'success': True,
                    'created': question.id
                })
            except exc.SQLAlchemyError:
                abort(422)
        else:
            abort(400)

    @app.route('/questions/search', methods=["POST"])
    def post_search():
        page = request.args.get('page', 1, type=int)
        start = (page-1)*10
        end = start + 10
        data = request.get_json()
        search_term = data.get('search_term', None)
        if search_term is None:
            abort(400)
        questions = Question.query.filter(
            Question.question.ilike(f"%{search_term}%")).all()

        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'success': True,
            'questions': formatted_questions[start: end],
            'total_questions': len(formatted_questions)
        })

    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def delete_questions(question_id):

        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            print(question)
            if question is None:
                abort(404)
            else:
                question.delete()

                return jsonify({
                    'success': True,
                    'deleted': question.id
                })
        except exc.SQLAlchemyError:
            abort(422)

    @app.route('/categories/<int:category_id>/questions', methods=["GET"])
    def get_questions_by_category(category_id):
        page = request.args.get('page', 1, type=int)
        start = (page-1)*10
        end = start + 10
        category = Category.query.filter(
            Category.id == category_id).one_or_none()
        if category is None:
            abort(404)
        questions = Question.query.filter(
            Question.category == category_id).all()

        formatted_questions = [question.format() for question in questions]
        if len(questions[start:end]) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions': len(formatted_questions),
            'current_category': category_id
        })

    @app.route('/quizzes', methods=["POST"])
    def post_quiz_questions():
        data = request.get_json()

        previous_questions = data.get('previous_questions', [])
        quiz_category = data.get('quiz_category', None)
        if quiz_category is None:
            abort(400)
        if quiz_category == 0:
            questions = Question.query.order_by(func.random()).all()
            print(previous_questions)

        else:
            print(quiz_category)
            questions = Question.query.filter(
                Question.category == quiz_category).order_by(func.random()).all()
        print(questions)
        new_questions = [
            question for question in questions if question.id not in previous_questions]
        print(new_questions)
        if new_questions:
            formatted_question = new_questions[0].format()
        else:
            formatted_question = None

        print(formatted_question)
        return jsonify({
            'success': True,
            'question': formatted_question,

        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(500)
    def internal_server(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app
