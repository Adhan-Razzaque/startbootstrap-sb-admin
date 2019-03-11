from flask import Flask, request, render_template, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

db = SQLAlchemy()

#...

class User(db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)

@app.route('/', methods=['GET'])
def main():
    return render_template("index.html")

@app.route('/charts', methods=['GET'])
def charts():
    return render_template('charts.html')

@app.route('/blank', methods=['GET'])
def blank():
    return render_template('blank.html')

@app.route('/forgot-password', methods=['GET'])
def forgot_password():
    return render_template('forgot-password.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    """For GET requests, display the login form.
    For POSTS, login the current user by processing the form.

    """
    print(db)
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for("bull.reports"))
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("logout.html")


@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/tables', methods=['GET'])
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


if __name__ == '__main__':
    app.run()
