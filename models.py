from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import sqlalchemy

# Replace 'username' and 'password' with your actual MySQL username and password
DATABASE_URL = 'mysql://root@localhost:3306/artistic_gallery'

def create_database_if_not_exists():
    # Replace 'username' and 'password' with your actual MySQL username and password
    engine = sqlalchemy.create_engine('mysql://username:password@localhost:3306')
    conn = engine.connect()
    conn.execute("CREATE DATABASE IF NOT EXISTS artistic_gallery")
    conn.close()

create_database_if_not_exists()

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    details = relationship("UserDetails", back_populates="user")

class UserDetails(Base):
    __tablename__ = 'user_details'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    mobile_number = Column(String, nullable=False)
    user_type_id = Column(Integer, ForeignKey('user_types.id'), nullable=False)
    address = Column(String, nullable=True)
    user = relationship("User", back_populates="details")
    user_type = relationship("UserTypes", back_populates="users")

class UserTypes(Base):
    __tablename__ = 'user_types'
    id = Column(Integer, primary_key=True)
    type_name = Column(String, unique=True, nullable=False)
    users = relationship("UserDetails", back_populates="user_type")

def create_tables():
    Base.metadata.create_all(engine)

create_tables()
Session = sessionmaker(bind=engine)
session = Session()




