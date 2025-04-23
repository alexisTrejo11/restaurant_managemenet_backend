from dataclasses import dataclass

@dataclass
class MenuItemDTO:
    id: int
    name: str
    price: str
    description: str
    category: str