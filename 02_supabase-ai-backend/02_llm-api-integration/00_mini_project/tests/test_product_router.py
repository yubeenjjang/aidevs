from fastapi.testclient import TestClient

from app.main import app
from app.routers import product_router
from app.schemas.product_schema import ProductPublic


client = TestClient(app)


def test_create_product_returns_created_product(monkeypatch):
    received = {}

    def fake_create_product(product):
        received["product"] = product
        return product

    monkeypatch.setattr(
        product_router,
        "create_product_service",
        fake_create_product,
    )

    payload = {"id": "product-1", "name": "keyboard", "price": 50000}
    response = client.post("/product/create", json=payload)

    assert response.status_code == 200
    assert response.json() == payload
    assert received["product"] == ProductPublic(**payload)


def test_create_product_rejects_invalid_payload():
    response = client.post(
        "/product/create",
        json={"id": "product-1", "name": "keyboard"},
    )

    assert response.status_code == 422


def test_get_product_returns_requested_product(monkeypatch):
    def fake_get_product(product_id):
        return ProductPublic(id=product_id, name="mouse", price=30000)

    monkeypatch.setattr(
        product_router,
        "get_product_service",
        fake_get_product,
    )

    response = client.get("/product/get/product-2")

    assert response.status_code == 200
    assert response.json() == {
        "id": "product-2",
        "name": "mouse",
        "price": 30000,
    }


def test_get_all_products_returns_product_list(monkeypatch):
    products = [
        ProductPublic(id="product-1", name="keyboard", price=50000),
        ProductPublic(id="product-2", name="mouse", price=30000),
    ]
    monkeypatch.setattr(
        product_router,
        "get_all_products_service",
        lambda: products,
    )

    response = client.get("/product/getall")

    assert response.status_code == 200
    assert response.json() == [product.model_dump() for product in products]
