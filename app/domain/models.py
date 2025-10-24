"""
Data models for the application
"""

from dataclasses import dataclass
from datetime import datetime
from typing import NewType

ItemId = NewType("ItemId", int)


@dataclass(frozen=True)
class Item:
    """
    Item domain model
    """

    id: ItemId
    name: str
    description: str
    price: float
    created_at: datetime
    updated_at: datetime

    def validate(self) -> None:
        if self.name is None or self.name.strip() == "":
            raise ValueError("Name cannot be empty")
        if self.price < 0:
            raise ValueError("Price must be positive")
