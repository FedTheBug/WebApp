import os
from datetime import datetime
from flask import Flask, render_template, url_for, request, jsonify, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = '11f0c9648013c9a24e29a1e3f8579585'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    sentences = db.relationship('Sentence', backref = 'author', lazy = True)

    def __repr__(self):
        return f"User('{ self.username }, '{ self.email }', '{ self.image_file }')"

class Sentence(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sentence = db.Column(db.Text, nullable = False)
    entity_1 = db.Column(db.Text, nullable = False)
    entity_2 = db.Column(db.Text, nullable = False)
    relation = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Sentence('{ self.sentence }','{ self.entity_1 }','{ self.entity_2 }','{ self.relation }')"

sentences = [
    {
        'author':'Dr. Nabeel Mohammed',
        'sentence':'He is a student',
        'entity_1': 'He',
        'entity_2' : 'student',
        'relation': 'is_a'
    },
    {
        'author':'Dr. Nur Alam',
        'sentence':'Nur won the match',
        'entity_1': 'Nur',
        'entity_2' : 'the match',
        'relation': 'job_done'
    },
    {
        'author':'Dr. Abdur Rahman',
        'sentence':'Student failed in the exam',
        'entity_1': 'Student',
        'entity_2' : 'failed in the exam',
        'relation': 'job_done'
    }
]


@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/home')
def home():
    return render_template('home.html',sentences = sentences)


@app.route('/form')
def my_form():
    return render_template('form.html')

@app.route('/form', methods = ['GET','POST'])
def my_form_get():
    
    text = request.form.get('text') 
    string =  text.split()

    return jsonify(string) 

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form = form)

@app.route("/login",methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been loggen in!','success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password','danger')
    return render_template('login.html', title = 'Login', form = form)


if __name__ == "__main__":
    app.run(debug=True) 