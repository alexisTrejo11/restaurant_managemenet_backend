from dataclasses import dataclass

@dataclass
class MenuExtraDTO:
    id: int
    name: str
    price: str
    description: str