from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from .service import TronService, DatabaseService
from .schemas import (
    AddressRequestsSchemas,
    AddressInfoResponseSchemas,
    AddressInfoListResponseSchemas
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tron_service = TronService()
db_service = DatabaseService()

@app.post("/address-info/", response_model=AddressInfoResponseSchemas)
async def get_address_info(request: AddressRequestsSchemas):
    """Полечение информации по адресу и занесение обращения в бд"""
    try:
        info = tron_service.get_address_info(request.address)
        db_service.log_query(request.address, info)
        return info
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/query-history/", response_model=AddressInfoListResponseSchemas)
async def get_query_history(page: int = 1, per_page: int = 10):
    """Полечние последних обращений"""
    try:
        history = db_service.get_query_history(page, per_page)
        return history
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.on_event("shutdown")
def shutdown_event():
    db_service.close()