class StockUpdateDTO:
    def __init__(self, ingredient_id: int, update_status: str, quantity: float):
        self.ingredient_id = ingredient_id
        self.update_status = update_status
        self.quantity = quantity
