from fastapi import APIRouter

from app.schemas.product_schema import ProductPublic
from app.services.product_service import (
    product_create as create_product_service,
    product_get as get_product_service,
    product_get_all as get_all_products_service,
)

product_router = APIRouter()


@product_router.post("/product/create", response_model=ProductPublic)
def create(product: ProductPublic) -> ProductPublic:
    return create_product_service(product)


@product_router.get("/product/get/{product_id}", response_model=ProductPublic)
def get(product_id: str) -> ProductPublic:
    return get_product_service(product_id)


@product_router.get("/product/getall", response_model=list[ProductPublic])
def get_all_products() -> list[ProductPublic]:
    return get_all_products_service()
