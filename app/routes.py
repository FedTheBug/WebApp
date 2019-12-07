from flask import render_template, url_for, request, jsonify, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User, Sentence
from flask_login import login_user, current_user, logout_user, login_required

sentences = [
    {
        'author':'ডঃ নাবিল মোহাম্মেদ',
        'sentence':'সে একজন ছাত্র',
        'entity_1': 'সে',
        'entity_2' : 'ছাত্র',
        'relation': 'is_a'
    },
    {
        'author':'ডঃ নুর আলম',
        'sentence':'রহিম ম্যাচটি জিতেছে',
        'entity_1': 'রহিম',
        'entity_2' : 'ম্যাচটি',
        'relation': 'job_done'
    },
    {
        'author':'আবদুল মালেক',
        'sentence':'তার একটি বাড়ি আছে',
        'entity_1': 'তার',
        'entity_2' : 'একটি বাড়ি',
        'relation': 'has_a'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',sentences = sentences)


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
    if current_user.is_authenticated:
        return redirect (url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account created has been created! You are now able to log in', 'success')
        return redirect(url_for('dashboard'))
    return render_template('register.html', title = 'Register', form = form)

@app.route("/login",methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect (url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect (next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password','danger')
    return render_template('login.html', title = 'Login', form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title = 'Account')
