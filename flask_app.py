from flask import Flask, render_template, Response, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user #UserMixin
from models import User, Employees
from forms import LoginForm, RegistrationForm
from config import Config
from shared import db
from socket import gethostname

# Github to check out https://github.com/itzvnl/Flask-Webapplication-with-mysql

login_manager = LoginManager()



app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# from

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
    flash('Check 1')
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('user'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        flash('User object built successfully') #Remove rem for testing
        db.session.add(user)
        flash('Object added to database') #Remove Rem for testing
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/tables', methods=['GET'])
@login_required
def tables():
    return render_template('tables.html')

@app.route('/user/<username>', methods=['GET'])
@login_required
def user(username):
    cur = db.cursor()
    cur.execute("SELECT * FROM employees")
    data = cur.fetchall()
    return render_template('index.html', data=Employees.query.all())

@app.route('/contactme', methods=['GET', 'POST'])
def contactme():
    return render_template("contact.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))

@app.route('/test', methods=['GET'])
def test():
    return render_template("test.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# handle login failed
@app.errorhandler(401)
def login_failure(e):
    return Response("Login Failed")


if __name__ == '__main__':
    db.create_all()
    if 'liveconsole' not in gethostname():
        app.run()