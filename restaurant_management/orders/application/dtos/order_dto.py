from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime

@dataclass
class OrderDTO:
    """
    Data Transfer Object for transferring Order data.
    """
    id: int
    table_number: int
    status: str
    created_at: Optional[datetime]
    end_at: Optional[datetime]

    def to_dict(self) -> dict:
        """
        Converts the OrderDTO instance into a dictionary representation.
        
        Returns:
            dict: A dictionary containing all fields of the OrderDTO.
        """
        return asdict(self)

@dataclass
class OrderItemDTO:
    """
    Data Transfer Object for transferring OrderItem data.
    """
    menu_item_id: int
    order_id: int
    menu_extra_id: Optional[int]
    quantity: int
    notes: Optional[str]
    is_delivered: bool
    added_at: Optional[datetime]

    def to_dict(self) -> dict:
        """
        Converts the OrderItemDTO instance into a dictionary representation.
        
        Returns:
            dict: A dictionary containing all fields of the OrderItemDTO.
        """
        return asdict(self)