from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash

from models import User, Session, UserTypes, UserDetails

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    session = Session()

    user = session.query(User).filter_by(username=username).first()
    session.close()

    if user and check_password_hash(user.password, password):
        return redirect(url_for('home'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('login'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    name = request.form.get('name')
    surname = request.form.get('surname')
    email = request.form.get('email')
    mobile_number = request.form.get('mobile_number')
    address = request.form.get('address')
    user_type_name = request.form.get('user_type')

    session = Session()

    existing_user = session.query(User).filter_by(username=username).first()
    existing_email = session.query(UserDetails).filter_by(email=email).first()

    if existing_user:
        flash('Username already exists')
        session.close()
        return redirect(url_for('signup'))

    if existing_email:
        flash('Email already exists')
        session.close()
        return redirect(url_for('signup'))

    user_type = session.query(UserTypes).filter_by(type_name=user_type_name).first()
    if not user_type:
        user_type = UserTypes(type_name=user_type_name)
        session.add(user_type)
        session.commit()

    new_user = User(username=username, password=generate_password_hash(password))
    session.add(new_user)
    session.commit()

    new_user_details = UserDetails(
        user_id=new_user.id,
        name=name,
        surname=surname,
        email=email,
        mobile_number=mobile_number,
        address=address,
        user_type_id=user_type.id
    )
    session.add(new_user_details)
    session.commit()
    session.close()

    flash('User registered successfully')
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
