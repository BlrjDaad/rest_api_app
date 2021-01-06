from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Th1s1ss3cr3tk3y'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://daad:Backend@123@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

engine = create_engine(app.config.get('SQLALCHEMY_DATABASE_URI'))
