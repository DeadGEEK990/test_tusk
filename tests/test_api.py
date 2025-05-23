import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.db import Base, engine
from app.model import AddressInfo

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # Создание таблиц БД
    Base.metadata.create_all(bind=engine)
    yield
    # Удаление всех таблиц
    Base.metadata.drop_all(bind=engine)


def test_get_address_info():
    """Тест запроса /address-info/"""
    test_address = "TNPeeaaFB7K9cmo4uQpcU32zGK8G1NYqeL"  # Testnet address
    response = client.post(
        "/address-info/",
        json={"address": test_address}
    )
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["address"] == test_address
    assert "bandwidth" in data
    assert "energy" in data
    assert "balance" in data


def test_get_query_history():
    """Тест запроса /query-history/"""
    # Создаем тестовую запись в БД
    test_address = "TNPeeaaFB7K9cmo4uQpcU32zGK8G1NYqeL"
    client.post("/address-info/", json={"address": test_address})
    # Получаем записи из БД
    response = client.get("/query-history/", params={"page": 1, "per_page": 5})
    assert response.status_code == 200
    data = response.json()
    assert len(data["records"]) > 0
    assert data["total"] > 0
    assert data["page"] == 1
    assert data["per_page"] == 5