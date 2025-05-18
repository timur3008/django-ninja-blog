from ninja import Schema
from typing import Optional

from datetime import datetime
from .auth import UserSchema

class CommentSchema(Schema):
    id: int
    text: str
    created_at: datetime
    author: UserSchema


class CommentShortSchema(Schema):
    id: int
    text: str
    article_id: int
    author_id: int
    created_at: datetime


class CommentPaginatedSchema(Schema):
    total: int
    limit: int = 5
    offset: int = 0
    comments: list[CommentShortSchema]


class CommentUpdateCreateSchema(Schema):
    text: str
    article_id: int
    author_id: int