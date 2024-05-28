from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, Session, UserDetails
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

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signupconf')
def signupconf():
    return render_template('signupconf.html')

@app.route('/')
def home():
    # Read data from CSV file
    file_path = 'your_csv_file.csv'  # Update with your CSV file path
    artwork_details = read_csv_file(file_path)

    # Pass the data to the template
    return render_template('home.html', artwork_details=artwork_details)

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
            return redirect(url_for('login', error='invalid_credentials'))

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
            return redirect(url_for('signup', error='password_required'))

        session = Session()

        existing_user = session.query(User).filter_by(username=username).first()
        existing_email = session.query(UserDetails).filter_by(email=email).first()

        if existing_user:
            return redirect(url_for('signup', error='username_exists'))

        if existing_email:
            return redirect(url_for('signup', error='email_exists'))

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

        return redirect(url_for('signupconf'))

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
