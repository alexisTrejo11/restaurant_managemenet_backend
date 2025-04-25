from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime

@dataclass
class TableDTO:
    """
    Data Transfer Object for transferring Table data.
    """
    number: int
    capacity: int
    is_available: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def to_dict(self) -> dict:
        """
        Converts the TableDTO instance into a dictionary representation.
        
        Returns:
            dict: A dictionary containing all fields of the TableDTO.
        """
        return asdict(self)