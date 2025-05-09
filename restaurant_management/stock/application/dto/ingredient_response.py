from dataclasses import dataclass, asdict
from decimal import Decimal

@dataclass
class IngredientResponse:
    id = int
    name: str
    unit: str
    quantity: Decimal


    def to_dict(self) -> dict:
        return asdict(self)
