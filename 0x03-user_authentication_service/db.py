#!/usr/bin/env python3
"""DB module."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User
from typing import TypeVar

VALID_FIELDS = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']

class DB:
    """DB class."""

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database."""
        if not email or not hashed_password:
            return None
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user in the database."""
        if not kwargs or any(field not in VALID_FIELDS for field in kwargs):
            raise InvalidRequestError
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user in the database."""
        if not user_id or not kwargs:
            raise ValueError("Missing user_id or fields to update.")
        if any(key not in VALID_FIELDS for key in kwargs):
            raise InvalidRequestError
        session = self._session
        user = session.query(User).get(user_id)
        if user is None:
            raise NoResultFound
        for key, value in kwargs.items():
            setattr(user, key, value)
        session.commit()
