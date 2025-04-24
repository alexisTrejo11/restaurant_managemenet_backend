from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Table:
    """
    Domain entity representing a table in the restaurant.
    """
    number: int
    capacity: int
    is_available: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __str__(self):
        return f"Table {self.number} ({self.capacity} capacity)"