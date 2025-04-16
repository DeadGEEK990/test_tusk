from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AddressRequestsSchemas(BaseModel):
    """Схема адреся, предназначеного для получения обращения"""
    address: str


class AddressInfoResponseSchemas(BaseModel):
    """Схема возврращающая инфомарцию по одному обращени."""
    address: str
    bandwidth: int
    energy: int
    balance: float


class AddressInfoSchemas(BaseModel):
    """Преобразование модели SQLAlchemy в модель Pydantic"""
    id: int
    address: str
    bandwidth: Optional[int]
    energy: Optional[int]
    balance: Optional[float]
    created_at: datetime

    class Config:
        orm_mode = True


class AddressInfoListResponseSchemas(BaseModel):
    """Схема получения списка обращений"""
    records: List[AddressInfoSchemas]
    total: int
    page: int
    per_page: int