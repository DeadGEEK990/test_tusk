from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.sql import func
from .db import Base


class AddressInfo(Base):
    __tablename__ = "address_info"

    id = Column(Integer, primary_key = True, index = True)
    address = Column(String, index = True)
    bandwidth = Column(Integer, nullable = True)
    energy = Column(Integer, nullable = True)
    balance = Column(Numeric(20, 6), nullable = True)
    created_at = Column(DateTime(timezone = True), server_default = func.now())