from tronpy import Tron
from tronpy.exceptions import AddressNotFound
from .db import SessionLocal
from .model import AddressInfo
from .config import settings


class TronService:
    def __init__(self):
        self.client = Tron(network=settings.TRON_NETWORK)

    def get_address_info(self, address: str) -> dict:
        try:
            account = self.client.get_account(address)
            balance = self.client.get_account_balance(address)
            return {
                "address": address,
                "bandwidth": account.get("free_net_usage", 0),
                "energy": account.get("energy_usage", 0),
                "balance": balance
            }
        except AddressNotFound:
            return {
                "address": address,
                "bandwidth": None,
                "energy": None,
                "balance": None
            }


class DatabaseService:
    def __init__(self):
        self.db = SessionLocal()

    def log_query(self, address: str, info: dict) -> AddressInfo:
        db_query = AddressInfo(
            address=address,
            bandwidth=info.get("bandwidth"),
            energy=info.get("energy"),
            balance=info.get("balance")
        )
        self.db.add(db_query)
        self.db.commit()
        self.db.refresh(db_query)
        return db_query

    def get_query_history(self, page: int = 1, per_page: int = 10) -> dict:
        offset = (page - 1) * per_page
        queries = self.db.query(AddressInfo) \
            .order_by(AddressInfo.created_at.desc()) \
            .offset(offset) \
            .limit(per_page) \
            .all()
        total = self.db.query(AddressInfo).count()
        return {
            "records": queries,
            "total": total,
            "page": page,
            "per_page": per_page
        }

    def close(self):
        self.db.close()