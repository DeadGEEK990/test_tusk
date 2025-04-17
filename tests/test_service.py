import pytest
from app.service import TronService, DatabaseService
from app.db import Base, engine
from app.model import AddressInfo
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="module")
def db_service():
    Base.metadata.create_all(bind=engine)
    service = DatabaseService()
    yield service
    service.close()
    Base.metadata.drop_all(bind=engine)


def test_log_query(db_service):
    """Тест записи запроса в БД"""
    # Создаем тестовые данные
    test_address = "TNPeeaaFB7K9cmo4uQpcU32zGK8G1NYqeL"
    test_info = {
        "address": test_address,
        "bandwidth": 100,
        "energy": 200,
        "balance": 1000
    }
    # Заносим тестовые данные в БД
    query = db_service.log_query(test_address, test_info)

    assert query.id is not None
    assert query.address == test_address
    assert query.bandwidth == 100
    assert query.energy == 200
    assert query.balance == 1000


def test_get_query_history(db_service):
    """Тест получения из БД списка обращений"""
    # Создаем 15 записей в БД
    for i in range(15):
        db_service.log_query(f"address_{i}", {"bandwidth": i, "energy": i * 2, "balance": i * 10})
    # Получаем список записей по страницам
    history = db_service.get_query_history(page=1, per_page=5)
    assert len(history["records"]) == 5
    assert history["total"] >= 15
    assert history["page"] == 1
    assert history["per_page"] == 5

    history = db_service.get_query_history(page=2, per_page=5)
    assert len(history["records"]) == 5