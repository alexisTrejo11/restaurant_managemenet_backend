from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Table:
    """
    Domain entity representing a table in the restaurant.
    """
    capacity: int
    is_available: bool = True
    id: int = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __str__(self):
        return f"Table {self.id} ({self.capacity} capacity)"