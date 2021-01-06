#!flask/bin/python

from flask import jsonify, make_response, request

from models import *
from functools import wraps
import jwt

db.create_all()


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None
        if 'Authorization' in request.headers:
            token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            token = token.split(' ')[1]
            data = jwt.decode(token, app.config.get('SECRET_KEY'))
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'token is invalid'})

    return decorator


@app.route('/user/sign_up/', methods=['POST'])
@token_required
def sign_up():
    '''
    :return:
    '''
    try:
        data = request.get_json(force=True)
        add_new_user(data)
        return make_response(jsonify({'message': 'User created successfully'}), 201)
    except Exception as e:
        return make_response(jsonify({"response": "User not created"}), 500)


@app.route('/user/sign_in/', methods=['POST'])
def sign_in():
    '''
    function of sign in with user email and hashed password
    '''
    try:
        data = request.get_json(force=True)
        response, code = authenticate_user(data.get('email'), data.get('password'))
        return make_response(jsonify(response), code)
    except Exception as e:
        print(e)
        return make_response(jsonify({"response": "User not created"}), 500)


@app.route('/user/<int:id_user>/', methods=['GET'])
@token_required
def get_user_by_id(id_user):
    '''
    :return:  Function to get all the movies in the database
    '''
    try:
        response, code = get_user(id_user)
        return make_response(jsonify(response), code)
    except Exception as e:
        return make_response(jsonify({'user': {}}), 500)


@app.route('/user/update/<int:id_user>/', methods=['PUT'])
@token_required
def update_user_data(id_user):
    '''
    :return:  Function to update user data in database
    '''
    try:
        data = request.get_json(force=True)
        status, response, status_code = update_user(id_user, data)
        if status:
            return make_response(jsonify(response), status_code)
        else:
            return make_response(jsonify(response, status_code))
    except Exception as e:
        return make_response(jsonify({'response': 'user not found'}), 404)


@app.route('/all_users/', methods=['GET'])
@token_required
def all_users():
    return make_response(jsonify({"response": get_all_users()}), 200)


@app.route('/user/delete/<int:id_user>/', methods=['DELETE'])
@token_required
def delete_user_from_id(id_user):
    try:
        delete_user(id_user)
        return make_response(jsonify({"response": 'user deleted'}), 202)
    except Exception as e:
        return make_response(jsonify({'user not deleted'}), 500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, use_reloader=True)


