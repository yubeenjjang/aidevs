from app.schemas.product_schema import ProductPublic


def product_create(product: ProductPublic) -> ProductPublic:
    print("Product saved to database.")
    return product


def product_get_all() -> list[ProductPublic]:
    return [ProductPublic(id="100", name="idd01", price=20000)]


def product_get(product_id: str) -> ProductPublic:
    return ProductPublic(id=product_id, name="registered product", price=30000)
