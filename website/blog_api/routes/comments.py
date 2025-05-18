from blog_app.models import Comment
from blog_api.schemas.comments import CommentShortSchema, CommentPaginatedSchema, CommentUpdateCreateSchema
from blog_api.services.comment import comments_service

from ninja import Router
from django.http import HttpRequest

router = Router(tags=['Comments'])

@router.get('/comments/', response=CommentPaginatedSchema)
def get_comments(request: HttpRequest, limit: int = 5, offset: int = 0):
    return comments_service.get_comments(limit=limit, offset=offset)

@router.get('/comments/{comment_id}/', response=CommentShortSchema)
def get_comment_detail(request: HttpRequest, comment_id: int):
    return comments_service.get_comment_detail(comment_id=comment_id)

@router.post('/comments/create/', response=CommentShortSchema)
def create_new_comment(request: HttpRequest, comment_data: CommentUpdateCreateSchema):
    return comments_service.create_new_comment(comment_data=comment_data)

@router.put('/comments/{comment_id}/update/', response=CommentShortSchema)
def update_comment(request: HttpRequest, comment_id: int, comment_data: CommentUpdateCreateSchema):
    return comments_service.update_comment(comment_id=comment_id, comment_data=comment_data)

@router.delete('/comments/delete/{comment_id}/')
def delete_comment(request: HttpRequest, comment_id: int):
    return comments_service.delete_comment(comment_id=comment_id)