import os
from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = '11f0c9648013c9a24e29a1e3f8579585'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)

from app import routes