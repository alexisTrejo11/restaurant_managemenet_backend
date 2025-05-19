from dataclasses import dataclass, asdict
from typing import List, Optional
from datetime import datetime

@dataclass
class StockDTO:
    id: int
    ingredient_id: int
    optimal_stock_quantity: float
    total_stock: float = 0.0
    transactions: List = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.transaction_ids is None:
            self.transaction_ids = []

    def to_dict(self):
        return asdict(self)