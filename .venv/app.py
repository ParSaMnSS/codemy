from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:parsa123@localhost/our_users' #mysql://username:password@localhost/db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'somepassword'  # Don't push this to GitHub
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Specify length for MySQL VARCHAR
    email = db.Column(db.String(100), nullable=False)  # Specify length for MySQL VARCHAR
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self) -> str:
        return f'user id: {self.id}, name: {self.name}, email: {self.email}, date_added: {self.date_added}'

class UserForm(FlaskForm):
    name = StringField('What\'s your name?', validators=[DataRequired()])
    email = StringField('What\'s your Email?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NamerForm(FlaskForm):
    name = StringField('What\'s your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# Update database record

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = User.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash('user updated!')
            return render_template('update.html', form = form, name_to_update = name_to_update)
        except:
            flash('Error, looks like there was a problem, try again!')
            return render_template('update.html', form = form, name_to_update = name_to_update)
    else:
        return render_template('update.html', form = form, name_to_update = name_to_update)
        

@app.route('/')
def index():
    firstname = 'John'
    stuff = 'this is <strong>Bold</strong>'
    flash('Welcome to our website')
    fav_pizza = ['pep', 'mush', 'cheese']
    return render_template('index.html', firstname=firstname, stuff=stuff, fav_pizza=fav_pizza)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', username=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash('User added!')
    our_users = User.query.order_by(User.date_added)
    return render_template('add_user.html', form=form, name=name, our_users=our_users)

@app.route('/name', methods=['POST', 'GET'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Form Submitted!')
    return render_template('name.html', name=name, form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
