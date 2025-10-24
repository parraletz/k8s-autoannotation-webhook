from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """Base schema with common item fields"""

    name: str = Field(min_length=1, max_length=100, description="Item name")
    description: str = Field(
        min_length=1, max_length=100, description="Item description"
    )
    price: float = Field(gt=0, description="Item price")


class ItemCreateRequest(ItemBase):
    """Schema for creating new items (no ID required)"""

    pass


class ItemUpdateRequest(BaseModel):
    """Schema for updating items (all fields optional)"""

    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Item description"
    )
    price: Optional[float] = Field(None, gt=0, description="Item price")


class ItemRequest(ItemBase):
    """Schema for item operations requiring ID"""

    id: str = Field(min_length=1, max_length=100, description="Item ID")


class ItemResponse(ItemBase):
    """Schema for item responses"""

    id: str
    created_at: datetime
    updated_at: datetime
