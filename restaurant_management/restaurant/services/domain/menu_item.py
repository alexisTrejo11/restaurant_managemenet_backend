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
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def __str__(self):
        return self.name

    def update_price(self, new_price: Decimal):
        if new_price <= 0:
            raise ValueError("Price must be greater than zero.")
        self.price = new_price
        self.updated_at = datetime.now()

    def update_category(self, new_category: CategoryEnum):
        if new_category not in CategoryEnum:
            raise ValueError("Invalid category.")
        self.category = new_category
        self.updated_at = datetime.now()

    def is_meal(self) -> bool:
        return self.category == CategoryEnum.MEALS
