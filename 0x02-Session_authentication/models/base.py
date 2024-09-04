#!/usr/bin/env python3
""" Base module
"""
from datetime import datetime
from typing import TypeVar, List, Iterable
from os import path
import json
import uuid


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA = {}


class Base:
    """ Base class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a Base instance
        """
        s_class = str(self.__class__.__name__)
        if DATA.get(s_class) is None:
            DATA[s_class] = {}

        self.id = kwargs.get('id', str(uuid.uuid4()))
        if kwargs.get('created_at') is not None:
            self.created_at = datetime.strptime(kwargs['created_at'], TIMESTAMP_FORMAT)
        else:
            self.created_at = datetime.utcnow()
        if kwargs.get('updated_at') is not None:
            self.updated_at = datetime.strptime(kwargs['updated_at'], TIMESTAMP_FORMAT)
        else:
            self.updated_at = datetime.utcnow()

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """ Check equality
        """
        return isinstance(other, Base) and self.id == other.id

    def to_json(self, for_serialization: bool = False) -> dict:
        """ Convert the object to a JSON dictionary
        """
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key.startswith('_'):
                continue
            result[key] = value.strftime(TIMESTAMP_FORMAT) if isinstance(value, datetime) else value
        return result

    @classmethod
    def load_from_file(cls):
        """ Load all objects from a file
        """
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        DATA[s_class].values()))
