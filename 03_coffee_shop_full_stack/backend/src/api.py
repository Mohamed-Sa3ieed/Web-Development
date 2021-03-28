import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

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
# db_drop_and_create_all()

# ensure that recipe follow a proper format or return None


def validate_recipe(recipe):
    drink_recipie = []
    if(not isinstance(recipe, list) and not isinstance(recipe, dict)):
        return None
    elif(isinstance(recipe, dict)):
        try:
            name = recipe['name']
            parts = recipe['parts']
            color = recipe['color']
            if((not isinstance(name, str)) or (not isinstance(color, str)) or (not isinstance(parts, (str, float, int))) or (not str(parts).isdigit())):
                return None
            drink_recipie = [
                {'color': color, 'name': name, 'parts': int(parts)}]
        except:
            return None
    else:
        for ingredient in recipe:
            name = ingredient['name']
            parts = ingredient['parts']
            color = ingredient['color']
            if((not isinstance(name, str)) or (not isinstance(color, str)) or (not isinstance(parts, (str, float, int))) or (not str(parts).isdigit())):
                return None
            drink_recipie.append(
                {'color': color, 'name': name, 'parts': int(parts)})
    return drink_recipie


# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def get_all_drinks():
    drinks = Drink.query.all()
    return jsonify({
        "success": True,
        "drinks": [drink.short() for drink in drinks]
    }), 200


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth(permission='get:drinks-detail')
def get_drinks_detailed():
    drinks = Drink.query.all()
    return jsonify({
        "success": True,
        "drinks": [drink.long() for drink in drinks]
    }), 200


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink():
    body = json.loads(request.data)
    try:
        title = body.get('title', None)
        recipe = body.get('recipe', None)
        if title is None or recipe is None:
            abort(400)
        recipe = validate_recipe(recipe)
        if recipe is None:
            abort(400)
        new_drink = Drink(title=title, recipe=json.dumps(recipe))
        new_drink.insert()
    except Exception as e:
        print(e)
        abort(422)
    return jsonify({
        "success": True,
        "drinks": [new_drink.long()]})


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth(permission='patch:drinks')
def modify_drink(id):
    target_drink = Drink.query.filter(Drink.id == id).one_or_none()
    if target_drink is None:
        abort(404)
    try:
        body = json.loads(request.data)
        title = body.get('title', None)
        recipe = body.get('recipe', None)
        if title is not None:
            target_drink.title = title
        if recipe is not None:
            target_drink.recipe = recipe

        print(json.dumps(target_drink.long()))
        target_drink.update()
        return jsonify({
            "success": True,
            "drinks": [target_drink.long()]
        }), 200
    except Exception as e:
        print(e)
        abort(422)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(id):
    target_drink = Drink.query.filter(Drink.id == id).one_or_none()
    if target_drink is None:
        abort(404)
    try:
        target_drink.delete()
        return jsonify({
            'success': True,
            'delete': id
        })
    except Exception as e:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


""" @app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422
 """

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''


""" @app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404
 """

@app.errorhandler(HTTPException)
def generic_error_handler(error):
    return jsonify({
        "success": False,
        "error": error.code,
        "message": error.name
    }), error.code


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''


@app.errorhandler(AuthError)
def unprocessable(error):
    print(error)
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code
