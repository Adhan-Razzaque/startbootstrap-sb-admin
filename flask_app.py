from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template("login.html")

@app.route('/charts', methods=['GET'])
def charts():
    return render_template('charts.html')

@app.route('/blank', methods=['GET'])
def blank():
    return render_template('blank.html')

@app.route('/forgot-password', methods=['GET'])
def forgot_password():
    return render_template('forgot-password.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/tables', methods=['GET'])
def tables():
    return render_template('tables.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
