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
        self.id = id
        self.number = number
        self.capacity = capacity
        self.is_available = is_available
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def __str__(self):
        return f"Table {self.number} (Capacity: {self.capacity})"

    def mark_unavailable(self):
        self.is_available = False
        self.updated_at = datetime.now()

    def mark_available(self):
        self.is_available = True
        self.updated_at = datetime.now()
