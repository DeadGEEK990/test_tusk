from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AddressRequestsSchemas(BaseModel):
    address: str


class AddressInfoResponseSchemas(BaseModel):
    address: str
    bandwidth: int
    energy: int
    balance: float


class AddressInfoSchemas(BaseModel):
    id: int
    address: str
    bandwidth: Optional[int]
    energy: Optional[int]
    balance: Optional[float]
    created_at: datetime

    class Config:
        orm_mode = True


class AddressInfoListResponseSchemas(BaseModel):
    records: List[AddressInfoSchemas]
    total: int
    page: int
    per_page: int