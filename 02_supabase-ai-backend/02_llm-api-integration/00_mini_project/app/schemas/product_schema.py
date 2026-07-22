# product_schema.py
from pydantic import BaseModel, Field


class ProductPublic(BaseModel):
    id: str
    name: str
    price: int
