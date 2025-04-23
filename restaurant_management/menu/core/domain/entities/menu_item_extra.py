from typing import List, Optional
from decimal import Decimal

class MenuExtra:
    """
    Represents a menu extra.
    """
    def __init__(self, 
                 id: Optional[int] = None,
                 name: Optional[str] = None,
                 price: Optional[Decimal] = None,
                 description: Optional[str] = None):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.validate()

    def validate(self):
        if not self.name:
            raise ValueError("The menu extra name is required.")
        if not self.price or self.price < 0:
            raise ValueError("The menu extra price must be greater than or equal to zero.")

    def __str__(self) -> str:
        return self.name