from ninja import Schema
from typing import Optional

class FAQSchema(Schema):
    id: int
    question: str
    answer: str

class FAQCreationSchema(Schema):
    question: str
    answer: str

class FAQUpdateSchema(Schema):
    question: Optional[str] = None
    answer: Optional[str] = None

class FAQDeleteSchema(Schema):
    is_deleted: bool