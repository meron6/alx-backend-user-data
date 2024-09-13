#!/usr/bin/env python3
"""
Combined DB and User model with main testing script
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError, NoResultFound

Base = declarative_base()


class User(Base):
    """User model for storing user data in the database"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(128), nullable=False)
    hashed_password = Column(String(128), nullable=False)
    session_id = Column(String(128), nullable=True)
    reset_token = Column(String(128), nullable=True)


class DB:
    """DB class to interact with the SQLite database"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)  # Drop and create all tables
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database"""
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments"""
        if not kwargs:
            raise InvalidRequestError
        for key in kwargs:
            if key not in ['id', 'email', 'hashed_password', 'session_id', 'reset_token']:
                raise InvalidRequestError
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes and commit changes"""
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if key not in ['id', 'email', 'hashed_password', 'session_id', 'reset_token']:
                raise ValueError(f"Invalid field: {key}")
            setattr(user, key, value)
        session = self._session
        session.commit()


# Main testing code
if __name__ == "__main__":
    my_db = DB()

    # Add users
    user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
    print(f"User 1 ID: {user_1.id}")

    user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
    print(f"User 2 ID: {user_2.id}")

    # Find user by email
    try:
        found_user = my_db.find_user_by(email="test@test.com")
        print(f"Found User ID: {found_user.id}")
    except NoResultFound:
        print("User not found")

    # Try to find a non-existent user
    try:
        not_found_user = my_db.find_user_by(email="notexist@test.com")
        print(f"Found User ID: {not_found_user.id}")
    except NoResultFound:
        print("User not found")

    # Update user password
    try:
        my_db.update_user(user_1.id, hashed_password="NewSuperHashedPwd")
        print("Password updated for User 1")
    except ValueError as e:
        print(f"Error: {e}")
