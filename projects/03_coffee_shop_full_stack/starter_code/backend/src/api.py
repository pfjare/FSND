import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()

# ROUTES

# GET /drinks (Public)
@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()

    return jsonify({
        "success": True,
        "drinks": [drink.short() for drink in drinks]
        })


# GET /drinks - Requires get:drinks-detail permission
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail():
    drinks = Drink.query.all()

    return jsonify({
        "success": True,
        "drinks": [drink.long() for drink in drinks]
    })


# POST /drinks - Requires post:drinks permission
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks():
    data = request.get_json()
    title = data.get('title', None)
    recipe = data.get('recipe', None)
    # Request body must contain both a title and recipe
    if recipe is None or title is None:
        abort(422)
    try:
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()
    except exc.SQLAlchemyError as error:
        print(error)
        abort(422)

    return jsonify({
        "success": True,
        "drinks": [drink.long()]
        })


#PATCH /drinks/:id - Requires patch:drinks permission
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(drink_id):

    data = request.get_json()
    title = data.get('title', None)
    recipe = data.get('recipe', None)
    # Request body must contain either a title or a recipe or both
    if recipe is None and title is None:
        abort(422)

    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is None:
        abort(404)

    try:
        if title:
            drink.title = title
        if recipe:
            drink.recipe = json.dumps(recipe)
        drink.update()

    except exc.SQLAlchemyError as error:
        print(error)
        abort(422)

    return jsonify({
        "success": True,
        "drinks": [drink.long()]
    })


# DELETE /drinks/:id - Requires delete:drinks permission
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is None:
        abort(404)

    try:
        drink.delete()
    except exc.SQLAlchemyError as error:
        print(error)
        abort(422)

    return jsonify({
        "success": True,
        "delete": drink.id
    })


# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
        }), 404

#AuthError defined in auth.py
@app.errorhandler(AuthError)
def authentication(error):
    return jsonify(error.error), 401
