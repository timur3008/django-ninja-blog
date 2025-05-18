import os
from typing import Optional

from django.shortcuts import get_object_or_404
from ninja import UploadedFile, Form

from blog_api.schemas.articles import ArticlePaginatedSchema, ArticleCreateSchema, ArticleUpdateSchema
from blog_app.models import Article, Category, User, ArticleImage
from website.settings import BASE_DIR

class ArticleService:
    def __save_photo(self, file: UploadedFile, folder_path: str):
        file = file.read()
        with open(folder_path, mode='wb') as _file:
            _file.write(file)

    def get_paginated_articles(self, limit: int = 0, offset: int = 2) -> ArticlePaginatedSchema:
        articles = Article.objects.all()
        total = articles.count()
        articles = articles[limit:offset]

        return ArticlePaginatedSchema(total=total, limit=limit, offset=offset, articles=articles)
    
    def get_article_detail(self, article_slug: str) -> Article:
        article = get_object_or_404(Article, slug=article_slug)
        return article
    
    def create_new_article(self, data: Form[ArticleCreateSchema], preview: UploadedFile, gallery: Optional[list[UploadedFile]]):
        data = data.dict()
        category = get_object_or_404(Category, pk=data.pop('category'))
        author = get_object_or_404(User, pk=data.pop('author'))

        article = Article.objects.create(**data, category=category, author=author)

        if preview is not None:
            preview_path = f'{BASE_DIR}/media/articles/previews/{preview.name}'
            self.__save_photo(preview, preview_path)
            article.preview = f'articles/previews/{preview.name}'
            article.save()

        for photo in gallery:
            photo_path = f'{BASE_DIR}/media/articles/previews/{photo.name}'
            self.__save_photo(photo, photo_path)
            ArticleImage.objects.create(article=article, photo=f'articles/gallery/{photo.name}')

        return article
    
    def update_article(self, article_id: int, data: ArticleUpdateSchema, preview: Optional[UploadedFile], gallery: Optional[list[UploadedFile]]):
        article = get_object_or_404(Article, pk=article_id)
        for key, value in data.dict().items():
            if not value:
                current_value = getattr(article, key)
                setattr(article, key, current_value)
            else:
                if key == 'category':
                    category = get_object_or_404(Category, pk=value)
                    setattr(article, key, category)
                else:
                    setattr(article, key, value)
        article.save()

        if preview is not None:
            preview_content = preview.read()
            if article.preview:
                os.remove(f'{BASE_DIR}/{article.preview.url}')
            preview_path = f'{BASE_DIR}/media/articles/previews/{preview.name}'
            with open(preview_path, mode='wb') as _file:
                _file.write(preview_content)
            article.preview = f'articles/previews/{preview.name}'
            article.save()

        if gallery is not None:
            for gallery_photo in article.gallery.all():
                try:
                    os.remove(f'{BASE_DIR}/{gallery_photo.photo.url}')
                except Exception as exc:
                    print(exc)
                gallery_photo.delete()
            for photo in gallery:
                photo_content = photo.read()
                photo_path = f'{BASE_DIR}/media/articles/previews/{photo.name}'
                with open(photo_path, mode='wb') as photo_file:
                    photo_file.write(photo_content)
                ArticleImage.objects.create(article=article, photo=f'articles/gallery/{photo.name}')

        return article
    
    def delete_article(self, article_slug: str):
        article = get_object_or_404(Article, slug=article_slug)
        article.delete()
        return {'is_deleted': True}
    

article_service = ArticleService()