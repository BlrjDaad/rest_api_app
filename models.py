from datetime import datetime, timedelta
from sqlalchemy.orm.exc import NoResultFound

from settings import *

import jwt


class User(db.Model):
    __table_name__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(20), nullable=True, unique=True)
    country = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(80), nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    date_joined = db.Column(db.DateTime, default=datetime.now)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def json(self):
        return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name,
                'phone': self.phone, 'gender': self.gender, 'is_active': self.is_active, 'date_joined': self.date_joined}


def authenticate_user(email, password):
    try:
        user = User.query.filter_by(email=email, password=password).first()
        auth_token = user.encode_auth_token(user.id)
        if auth_token:
            response = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'auth_token': auth_token.decode()
            }
            return response, 200
    except Exception as e:
        response = {
            'status': 'fail',
            'message': 'Try again'
        }
        return response, 500


def get_user(_id):
    '''
    function to get user using its id as parameter
    :param _id: id of the user in database
    :return: user details
    '''
    try:
        return {'response': User.json(User.query.filter_by(id=_id).first())}, 200
    except NoResultFound:
        return {'response': 'user not found'}, 404
    except:
        return {'response': 'error getting user'}, 500


def add_new_user(_data):
    '''
    function to add new user (sign up)
    :return: True if the user is created else False
    '''
    try:
        new_user = User(email=_data.get('email'), first_name=_data.get('first_name', ''),
                        last_name=_data.get('last_name', ''), password=_data.get('password'),
                        phone=_data.get('phone'), country=_data.get('country'), gender=_data.get('gender'))
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()


def get_all_users():
    '''
    function to get all users in database
    :return: All users saved in database
    '''
    return [User.json(user) for user in User.query.all()]


def update_user(id_user, data):
    '''
    function to update the details of a user using the id, first_name, last_name,
     phone, email, gender, is_active as parameters
    '''
    try:
        user_to_update = User.query.filter_by(id=id_user).first()
        user_to_update.email = data.get('email')
        user_to_update.first_name = data.get('first_name')
        user_to_update.last_name = data.get('last_name')
        user_to_update.phone = data.get('phone')
        user_to_update.gender = data.get('gender')
        user_to_update.country = data.get('country')
        user_to_update.is_active = data.get('is_active')
        db.session.commit()
    except NoResultFound:
        return False, {'response': 'user not found'}, 404
    except Exception as e:
        db.session.rollback()
        return False, {'response': 'error in updating user'}, 500
    finally:
        return True, {'response': 'updated successfully'}, 204


def delete_user(_id):
    '''
    function to delete a movie from our database using
       the id of the movie as a parameter
    '''
    try:
        User.query.filter_by(id=_id).delete()
        db.session.commit()
        return {"response": "user deleted successfully"}, 204
    except NoResultFound:
        return {"response": "user not found"}, 404
    except Exception as e:
        db.session.rollback()
        return {"response": "Error deleting user"}, 500

