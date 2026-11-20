from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


class ItemCreate(BaseModel):
    sku: str
    name: str
    item_type: Literal["RAW_MATERIAL", "FINISHED_GOOD"]
    unit: str
    barcode: str | None = None
    category_id: int


class ItemResponse(BaseModel):
    id: int
    sku: str
    name: str
    item_type: str
    unit: str
    barcode: str | None
    category_id: int

    model_config = ConfigDict(from_attributes=True)
