from enum import Enum
from typing import Optional
from datetime import datetime
from decimal import Decimal

class CategoryEnum(Enum):
    DRINKS = "DRINKS"
    ALCOHOL_DRINKS = "ALCOHOL_DRINKS"
    BREAKFASTS = "BREAKFASTS"
    STARTERS = "STARTERS"
    MEALS = "MEALS"
    DESSERTS = "DESSERTS"
    EXTRAS = "EXTRAS"
    

class MenuItem:
    def __init__(
        self,
        id: Optional[int],
        name: str,
        price: Decimal,
        category: CategoryEnum,
        description: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.__id = id
        self.__name = name
        self.__price = price
        self.__description = description
        self.__category = category
        self.__created_at = created_at or datetime.now()
        self.__updated_at = updated_at or datetime.now()

    def __str__(self):
        return self.__name

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value: Optional[int]):
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
    def category(self):
        return self.__category
    
    @category.setter
    def category(self, value: CategoryEnum):
        self.__category = value

    @property
    def created_at(self):
        return self.__created_at
    
    @created_at.setter
    def created_at(self, value: Optional[datetime]):
        self.__created_at = value

    @property
    def updated_at(self):
        return self.__updated_at
    
    @updated_at.setter
    def updated_at(self, value: Optional[datetime]):
        self.__updated_at = value

    def update_price(self, new_price: Decimal):
        if new_price <= 0:
            raise ValueError("Price must be greater than zero.")
        self.__price = new_price
        self.__updated_at = datetime.now()

    def update_category(self, new_category: CategoryEnum):
        if new_category not in CategoryEnum:
            raise ValueError("Invalid category.")
        self.__category = new_category
        self.__updated_at = datetime.now()

    def is_meal(self) -> bool:
        return self.__category == CategoryEnum.MEALS
