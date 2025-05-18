from ninja import Schema
from datetime import datetime

class CategorySchema(Schema):
    id: int
    name: str
    slug: str
    created_at: datetime

class CategoryCreationSchema(Schema):
    name: str