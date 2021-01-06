from settings import *
from unittest import TestCase

from models import *


class TestTestingConfig(TestCase):

    def test_app_config(self):
        self.assertTrue(app.config['SECRET_KEY'] is 'Th1s1ss3cr3tk3y')
        self.assertTrue(app.config['DEBUG'] is False)
        self.assertFalse(app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'mysql+pymysql://daad:Backend@123@localhost/test'
        )


class TestAddUser(TestCase):

    def test_user(self):
        # Add user
        data = {'email': 'test@test.com', 'password': 'test', 'first_name': 'test', 'last_name': 'test',
                'phone': '99404904', 'country': 'Tunisia', 'gender': 'Female'}
        add_new_user(data)
        user = User.query.filter_by(email='test@test.com').first()
        self.assertTrue(user.gender, 'female')
        self.assertTrue(user.email, 'test@test.com')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        # authenticate user
        response, code = authenticate_user('test@test.com', 'test')
        self.assertTrue(code, 200)
        self.assertTrue(response.get('auth_token'), auth_token)
        # Update user
        data = {'email': 'test@test.com', 'password': 'test', 'first_name': 'test2', 'last_name': 'test2',
                'phone': '99404904', 'country': 'Tunisia', 'gender': 'Female'}
        update_user(user.id, data)
        user = User.query.filter_by(email='test@test.com').first()
        self.assertTrue(user.first_name, 'test2')
        # get all user
        users = get_all_users()
        self.assertTrue(len(users), 2)
        # delete user
        response, code = delete_user(user.id)
        self.assertTrue(code, 204)
