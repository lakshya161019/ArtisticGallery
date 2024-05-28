from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, Session, UserDetails

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        session = Session()

        user = session.query(User).filter_by(username=username).first()
        session.close()

        if user and check_password_hash(user.password, password):
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        mobile_number = request.form.get('mobile_number')
        address = request.form.get('address')

        if not password:
            flash('Password is required', 'error')
            return redirect(url_for('signup'))

        session = Session()

        existing_user = session.query(User).filter_by(username=username).first()
        existing_email = session.query(UserDetails).filter_by(email=email).first()

        if existing_user:
            flash('Username already exists', 'error')
            session.close()
            return redirect(url_for('signup'))

        if existing_email:
            flash('Email already exists', 'error')
            session.close()
            return redirect(url_for('signup'))

        new_user = User(username=username, password=generate_password_hash(password))
        session.add(new_user)
        session.commit()

        new_user_details = UserDetails(
            user_id=new_user.id,
            name=name,
            surname=surname,
            email=email,
            mobile_number=mobile_number,
            address=address
        )
        session.add(new_user_details)
        session.commit()
        session.close()

        flash('User registered successfully', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
