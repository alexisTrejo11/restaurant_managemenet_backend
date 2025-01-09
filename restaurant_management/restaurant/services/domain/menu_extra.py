from decimal import Decimal

class MenuExtraDomain:
    def __init__(self, 
                 name: str, 
                 price: Decimal, 
                 id : int = None,
                 description: str = None, 
                 created_at: str = None, 
                 updated_at: str = None):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        return f"{self.name} - {self.price} ({'No description' if not self.description else self.description})"