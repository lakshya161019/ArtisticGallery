from models import User, Session
from werkzeug.security import generate_password_hash


def add_user(username, password):
    # Create a new session
    session = Session()

    try:
        # Check if the user already exists
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            print(f"User with username '{username}' already exists.")
            return

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Add a new user
        new_user = User(username=username, password=hashed_password)
        session.add(new_user)
        session.commit()
        print(f"User '{username}' added successfully.")
    except Exception as e:
        session.rollback()  # Rollback in case of any error
        print(f"An error occurred: {e}")
    finally:
        # Ensure the session is closed
        session.close()


# Example usage
if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    add_user(username, password)
