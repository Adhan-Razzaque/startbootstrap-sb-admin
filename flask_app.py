from flask import Flask, render_template, Response, redirect, url_for, flash
from flask_login import LoginManager, login_required, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from forms import LoginForm
from flask_migrate import Migrate

app = Flask(__name__)

# config class with all state variables
app.config.from_object(Config)


# MySQL database connection
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# login manager
login_manager = LoginManager()
login_manager.init_app(app)


# class User(UserMixin):

#     def __init__(self, username, password_hash):
#         self.username = username
#         self.password_hash = password_hash

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

#     def get_id(self):
#         return self.username
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

# all_users = {
#     "admin": User("admin@email.com", generate_password_hash("secret")),
#     "bob": User("bob@email.com", generate_password_hash("less-secret")),
#     "caroline": User("caroline@email.com", generate_password_hash("completely-secret")),
# }

@login_manager.user_loader
def load_user(user_id):
    return all_users.get(user_id)

class Employee(db.Model):

    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

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
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('main'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
        return render_template('register.html')

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# handle login failed
@app.errorhandler(401)
def login_failure(e):
    return Response("Login Failed")


if __name__ == '__main__':
    app.run()