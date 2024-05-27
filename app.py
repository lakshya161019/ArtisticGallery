from flask import Flask, render_template, request, redirect, url_for, flash, render_template_string
from werkzeug.security import check_password_hash

from models import User, Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def login(users=None):
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.get(email)

        if user and check_password_hash(user['password'], password):
            return redirect(url_for('index'))
        else:
            return "Invalid credentials, please try again.", 401

    return render_template_string(open('login.htm').read())


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    session = Session()

    user = session.query(User).filter_by(username=username).first()
    session.close()

    if user and user.password == password:
        return redirect(url_for('home'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('login'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
