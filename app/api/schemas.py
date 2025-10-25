from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AdmissionResponse(BaseModel):
    uid: str = Field(min_length=1, max_length=100, description="Webhook ID")
    allowed: bool = Field(description="Allowed")
    patch: Optional[str] = Field(default=None, description="Patch")
    patchType: Optional[str] = Field(default="JSONPatch", description="Patch type")


class AdmissionReviewRequest(BaseModel):
    uid: str = Field(min_length=1, max_length=100, description="Webhook ID")
    obj: dict = Field(description="Webhook object")
    metadata: dict = Field(description="Webhook metadata")
    annotations: Optional[dict] = Field(description="Webhook annotations")


class AdmissionReviewResponse(BaseModel):
    apiVersion: str = Field(description="API version")
    kind: str = Field(description="Kind")
    response: AdmissionResponse = Field(description="Response")


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

    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Item name"
    )
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
