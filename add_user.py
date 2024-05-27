from models import User, Session

session = Session()

# Add a sample user
new_user = User(username="testuser", password="testpassword")
session.add(new_user)
session.commit()
session.close()