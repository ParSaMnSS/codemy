from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'somepassword' #dont push it to github

# create a class form :thumbsup
class NamerForm(FlaskForm):
    name = StringField('Whats your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    firstname = 'john'
    stuff = 'this is <strong>Bold</strong>'
    flash('Welcome to our website')
    fav_pizza = ['pep', 'mush', 'cheese']
    return render_template('index.html', firstname = firstname, stuff = stuff, fav_pizza = fav_pizza)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', username = name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.route('/user/add', methods = ['GET', 'POST'])
def add_user():
    return render_template('add_user.html')


@app.route('/name', methods = ['POST', 'GET'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Form Submitted!')

    return render_template('name.html', name = name, form = form)

if __name__ == '__main__':
    app.run(debug=True)