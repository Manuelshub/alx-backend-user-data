#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User

Fields = ["id", "email", "hashed_password", "session_id", "reset_token"]


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the DB

        Args:
            email (str): The user's email address
            hashed_password (str): The user's hashed password

        Returns:
            User: The new User instance
        """
        if not email or not hashed_password:
            return
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by some criteria.

        Args:
            **kwargs: Keyword arguments where the key is the column name
                and the value is the value to search for.

        Returns:
            User: The matching user instance or None if no match is found
        """
        if not kwargs or any(x not in Fields for x in kwargs):
            raise InvalidRequestError
        session = self._session
        try:
            our_user = session.query(User).filter_by(**kwargs).one()
            return our_user
        except Exception:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user in the DB

        Args:
            user_id (int): The id of the user to update
            **kwargs: Keyword arguments where the key is the column name
                and the value is the new value to set.

        Returns:
            None
        """
        # if not kwargs or not user_id:
        #     return None
        session = self._session
        user = self.find_user_by(id=user_id)
        for key, val in kwargs.items():
            if key not in Fields:
                raise ValueError
            setattr(user, key, val)
        session.commit()
