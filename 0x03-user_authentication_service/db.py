#!/usr/bin/env python3
""" DB module for managing database """

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError, SQLAlchemyError
from user import Base, User
from typing import Optional, Dict

VALID_FIELDS = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']

class DB:
    """ DB class for interacting with the database """

    def __init__(self) -> None:
        """ Initialize a new DB instance """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session: Optional[Session] = None

    @property
    def _session(self) -> Session:
        """ Memoized session object """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Adds a new user to the Database """
        if not email or not hashed_password:
            raise ValueError("Email and password cannot be empty")
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        try:
            session.add(user)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        return user

    def find_user_by(self, **kwargs) -> User:
        """ Finds a User in the Database """
        if not kwargs or any(field not in VALID_FIELDS for field in kwargs):
            raise InvalidRequestError("Invalid query parameters")
        session = self._session
        try:
            return session.query(User).filter_by(**kwargs).one()
        except SQLAlchemyError as e:
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Update a user in the database """
        session = self._session
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if key not in VALID_FIELDS:
                raise ValueError(f"Invalid field: {key}")
            setattr(user, key, value)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
