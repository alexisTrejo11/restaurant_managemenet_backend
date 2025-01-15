from datetime import datetime
from decimal import Decimal
from typing import Optional

class Ingredient:
    def __init__(
        self,
        id: str,
        name: str,
        unit: str,
        quantity: Decimal = Decimal('0.00'), 
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.__id = id
        self.__name = name
        self.__unit = unit
        self.__quantity = quantity
        self.__created_at = created_at or datetime.now()
        self.__updated_at = updated_at or datetime.now()

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def unit(self) -> str:
        return self.__unit

    @property
    def quantity(self) -> Decimal:
        return self.__quantity

    @quantity.setter
    def quantity(self, new_quantity: Decimal):
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.__quantity = new_quantity
        self.__updated_at = datetime.now()

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @property
    def updated_at(self) -> datetime:
        return self.__updated_at

    def __str__(self):
        return f'{self.__name}'

    def update_quantity(self, new_quantity: Decimal):
        self.quantity = new_quantity 
