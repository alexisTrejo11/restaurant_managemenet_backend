from decimal import Decimal
from typing import List, Optional

class MenuItem:
    """
    Represents a menu item with business logic.
    """
    CATEGORY_CHOICES: List[str] = ['DRINKS', 'ALCOHOL_DRINKS', 'BREAKFASTS', 'STARTERS', 'MEALS', 'DESSERTS', 'EXTRAS']

    def __init__(self, 
                 id: Optional[int] = None,
                 name: Optional[str] = None,
                 price: Optional[Decimal] = None,
                 description: Optional[str] = None,
                 category: Optional[str] = None):
        """
        Constructor for the MenuItem class.

        Args:
            id (Optional[int]): The ID of the menu item.
            name (Optional[str]): The name of the item.
            price (Optional[Decimal]): The price of the item.
            description (Optional[str]): A description of the item.
            category (Optional[str]): The category of the item.
        """
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.category = category

    def validate(self) -> None:
        """
        Validates the attributes of the menu item.
        """
        if not self.name:
            raise ValueError("The menu item name is required.")
        if not self.price or self.price < 0:
            raise ValueError("The menu item price must be greater than or equal to zero.")
        if self.category and self.category not in self.CATEGORY_CHOICES:
            raise ValueError(f"Invalid category '{self.category}'.  Must be one of: {', '.join(self.CATEGORY_CHOICES)}.")

    def __str__(self) -> str:
        return self.name
