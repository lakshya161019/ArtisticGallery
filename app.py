from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, Session, UserDetails

app = Flask(__name__)
app.secret_key = 'your_secret_key'

import csv

def read_csv_file(file_path):
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            artwork_data = {
                'sr_no': row['sr. no'],
                'img_path': row['img path'],
                'artwork_title': row['Artwork Title'],
                'artist_name': row['Artist Name'],
                'phone': row['Phone'],
                'email': row['Email'],
                'instagram': row['Instagram']
            }
            data.append(artwork_data)
    return data

@app.route('/contact')
def contact():
    return render_template('contact.html', username=session.get('username'))


@app.route('/services')
def services():
    return render_template('services.html', username=session.get('username'))


@app.route('/about')
def about():
    return render_template('about.html', username=session.get('username'))


@app.route('/signupconf')
def signupconf():
    return render_template('signupconf.html', username=session.get('username'))


@app.route('/')
def home():
    # Read data from CSV file
    file_path = 'your_csv_file.csv'  # Update with your CSV file path
    artwork_details = read_csv_file(file_path)

    # Pass the data to the template
    return render_template('home.html', artwork_details=artwork_details,username=session.get('username'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db_session = Session()

        user = db_session.query(User).filter_by(username=username).first()
        db_session.close()

        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials')
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
            flash('Password is required')
            return redirect(url_for('signup'))

        db_session = Session()

        existing_user = db_session.query(User).filter_by(username=username).first()
        existing_email = db_session.query(UserDetails).filter_by(email=email).first()

        if existing_user:
            flash('Username already exists')
            return redirect(url_for('signup'))

        if existing_email:
            flash('Email already exists')
            return redirect(url_for('signup'))

        new_user = User(username=username, password=generate_password_hash(password))
        db_session.add(new_user)
        db_session.commit()

        new_user_details = UserDetails(
            user_id=new_user.id,
            name=name,
            surname=surname,
            email=email,
            mobile_number=mobile_number,
            address=address
        )
        db_session.add(new_user_details)
        db_session.commit()
        db_session.close()

        return redirect(url_for('signupconf'))

    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
