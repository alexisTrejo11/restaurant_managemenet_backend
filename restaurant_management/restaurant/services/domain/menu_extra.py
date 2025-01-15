from decimal import Decimal
from typing import Optional

class MenuExtraDomain:
    def __init__(self, 
                 name: str, 
                 price: Decimal, 
                 id: Optional[int] = None,
                 description: Optional[str] = None, 
                 created_at: Optional[str] = None, 
                 updated_at: Optional[str] = None):
        self.__id = id
        self.__name = name
        self.__price = price
        self.__description = description
        self.__created_at = created_at
        self.__updated_at = updated_at

    def __str__(self):
        return f"{self.__name} - {self.__price} ({'No description' if not self.__description else self.__description})"

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value: int):
        self.__id = value

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def price(self):
        return self.__price
    
    @price.setter
    def price(self, value: Decimal):
        self.__price = value

    @property
    def description(self):
        return self.__description
    
    @description.setter
    def description(self, value: Optional[str]):
        self.__description = value

    @property
    def created_at(self):
        return self.__created_at
    
    @created_at.setter
    def created_at(self, value: Optional[str]):
        self.__created_at = value

    @property
    def updated_at(self):
        return self.__updated_at
    
    @updated_at.setter
    def updated_at(self, value: Optional[str]):
        self.__updated_at = value
