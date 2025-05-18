from typing import Optional

from ninja import Schema

class SliderSchema(Schema):
    title: str
    description: str
    image: str


class SliderCreationSchema(Schema):
    title: str
    description: str


class SliderUpdateSchema(Schema):
    title: Optional[str] = None
    description: Optional[str] = None


class SliderDeleteSchema(Schema):
    is_deleted: bool