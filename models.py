from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import sqlalchemy

# Replace 'root' and 'admin' with your actual MySQL username and password
DATABASE_URL = 'mysql+pymysql://root:root@localhost:3306/artistic_gallery'

import pymysql

def create_database_if_not_exists():
    # Replace 'root' and 'admin' with your actual MySQL username and password
    conn = pymysql.connect(host='localhost', user='root', password='root')
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS artistic_gallery")
    conn.close()

create_database_if_not_exists()

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    details = relationship("UserDetails", back_populates="user", uselist=False)

class UserDetails(Base):
    __tablename__ = 'user_details'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    mobile_number = Column(String(255), nullable=False)
    user_type_id = Column(Integer, ForeignKey('user_types.id'), nullable=False)
    address = Column(String(255), nullable=True)
    user = relationship("User", back_populates="details")
    user_type = relationship("UserTypes", back_populates="users")

class UserTypes(Base):
    __tablename__ = 'user_types'
    id = Column(Integer, primary_key=True)
    type_name = Column(String(255), unique=True, nullable=False)
    users = relationship("UserDetails", back_populates="user_type")

def create_tables():
    Base.metadata.create_all(engine)

create_tables()
Session = sessionmaker(bind=engine)
