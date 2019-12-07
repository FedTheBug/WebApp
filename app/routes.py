from flask import render_template, url_for, request, jsonify, flash, redirect
from app import app
from app.forms import RegistrationForm, LoginForm
from app.models import User, Sentence

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
