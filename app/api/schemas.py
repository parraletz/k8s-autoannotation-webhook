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
