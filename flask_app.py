from flask import Flask, render_template, Response, redirect, url_for, flash
from flask_login import LoginManager, login_required, UserMixin, current_user, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

from datetime import datetime

app = Flask(__name__)

# config class with all state variables
app.config.from_object(Config)


# MySQL database connection
db = SQLAlchemy(app)

# login manager
login_manager = LoginManager()
login_manager.init_app(app)

# User Class: builds User objects for storage in MySQL database
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    employees = db.relationship('Employees', backref='manager', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Employees(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    position = db.Column(db.String(64))
    office = db.Column(db.String(64))
    age = db.Column(db.Integer)
    startdate = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Employees {}>'.format(self.body)

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=['GET'])
def main():
    return render_template('blank.html')

@app.route('/charts', methods=['GET'])
def charts():
    return render_template('charts.html')

@app.route('/blank', methods=['GET'])
def blank():
    return render_template('blank.html')

@app.route('/forgot-password', methods=['GET'])
def forgot_password():
    return render_template('forgot-password.html')

@app.route('/login', methods=['GET', 'POST']) #add POST method for login
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/tables', methods=['GET'])
@login_required
def tables():
    return render_template('tables.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/contactme', methods=['GET', 'POST'])
def contactme():
    return render_template("contact.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# handle login failed
@app.errorhandler(401)
def login_failure(e):
    return Response("Login Failed")


if __name__ == '__main__':
    app.run()