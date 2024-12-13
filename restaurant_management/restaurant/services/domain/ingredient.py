from datetime import datetime
from decimal import Decimal
from typing import Optional

class Ingredient:
    def __init__(
        self,
        id: str,
        name: str,
        unit: str,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.name = name
        self.unit = unit
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def __str__(self):
        return self.name

    def update_quantity(self, new_quantity: Decimal):
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.quantity = new_quantity
        self.updated_at = datetime.now()
