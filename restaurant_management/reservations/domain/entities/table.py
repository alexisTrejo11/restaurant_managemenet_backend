from datetime import datetime
from typing import Optional

class Table:
    def __init__(
        self,
        number: int,
        capacity: int,
        is_available: bool = True,
        id: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.__id = id
        self.__number = number
        self.__capacity = capacity
        self.__is_available = is_available
        self.__created_at = created_at or datetime.now()
        self.__updated_at = updated_at or datetime.now()


    @property
    def id(self):
        return self.__id

    @property
    def number(self):
        return self.__number

    @property
    def capacity(self):
        return self.__capacity

    @property
    def is_available(self):
        return self.__is_available

    @is_available.setter
    def is_available(self, value):
        self.__is_available = value
        self.__updated_at = datetime.now()

    @property
    def created_at(self):
        return self.__created_at

    @property
    def updated_at(self):
        return self.__updated_at

    def __str__(self):
        return f"Table {self.__number} (Capacity: {self.__capacity})"

    def mark_unavailable(self):
        self.is_available = False

    def mark_available(self):
        self.is_available = True
