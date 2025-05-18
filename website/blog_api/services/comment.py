from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from blog_api.schemas.comments import CommentShortSchema, CommentPaginatedSchema, CommentUpdateCreateSchema
from blog_app.models import Comment, Article

class CommentService:
    def get_comments(self, limit: int = 5, offset: int = 0) -> CommentPaginatedSchema:
        comments = Comment.objects.all()
        total_comments = comments.count()
        return CommentPaginatedSchema(total=total_comments, limit=limit, offset=offset, comments=comments[offset:limit])
    
    def get_comment_detail(self, comment_id: int) -> CommentShortSchema:
        comment = get_object_or_404(Comment, pk=comment_id)
        return comment
    
    def create_new_comment(self, comment_data: CommentUpdateCreateSchema) -> CommentShortSchema:
        comment_data = comment_data.dict()
        article_id = comment_data.pop('article_id')
        author_id = comment_data.pop('author_id')

        article = get_object_or_404(Article, pk=article_id)
        author = get_object_or_404(User, pk=author_id)

        new_comment = Comment.objects.create(text=comment_data.get('text'), article=article, author=author)
        new_comment.save()
        return new_comment
    
    def update_comment(self, comment_id: int, comment_data: CommentUpdateCreateSchema) -> CommentShortSchema:
        comment = get_object_or_404(Comment, pk=comment_id)
        
        for key, value in comment_data.dict().items():
            setattr(comment, key, value)

        comment.save()
        return comment
    
    def delete_comment(self, comment_id: int):
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()
        return {'is_deleted': True}

comments_service = CommentService()