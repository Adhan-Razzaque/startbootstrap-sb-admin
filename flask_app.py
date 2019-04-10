from flask import Flask, render_template, request, abort, redirect, Response, url_for
from flask_login import LoginManager, login_required, UserMixin, login_user

app = Flask(__name__)

#https://github.com/shekhargulati/flask-login-example/blob/master/flask-login-example.py
#https://github.com/shekhargulati/flask-login-example/issues
app.config['SECRET_KEY'] = 'a2BxpjeRLJBOyTWluc0NqA'
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self , username , password , id , active=True):
        self.id = id
        self.username = username
        self.password = password
        self.active = active

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def get_auth_token(self):
        return make_secure_token(self.username , key='a2BxpjeRLJBOyTWluc0NqA')

class UsersRepository:

    def __init__(self):
        self.users = dict()
        self.users_id_dict = dict()
        self.identifier = 0

    def save_user(self, user):
        self.users_id_dict.setdefault(user.id, user)
        self.users.setdefault(user.username, user)

    def get_user(self, username):
        return self.users.get(username)

    def get_user_by_id(self, userid):
        return self.users_id_dict.get(userid)

    def next_index(self):
        self.identifier +=1
        return self.identifier

users_repository = UsersRepository()



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

@app.route('/login', methods=['GET', 'POST']) #add POST method for login
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remLog = request.form['remember-me']
        registeredUser = users_repository.get_user(username)
        print('Users '+ str(users_repository.users))
        print('Register user %s , password %s' % (registeredUser.username, registeredUser.password))
        if registeredUser != None and registeredUser.password == password:
            print('Logged in..')
            login_user(registeredUser, remember=remLog)
            return redirect(url_for('home'))
        else:
            return abort(401)
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username , password , users_repository.next_index())
        users_repository.save_user(new_user)
        return Response("Registered Successfully")
    else:
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
    return Response('<p>Login failed</p>')

# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return users_repository.get_user_by_id(userid)

if __name__ == '__main__':
    app.run()
