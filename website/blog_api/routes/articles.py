import os
from typing import Optional

from ninja import Form, Router, File
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja.files import UploadedFile
from django.contrib.auth.models import User

from blog_app.models import Article, Category, ArticleImage
from blog_api.schemas.articles import (
    ArticleListSchema, ArticlePaginatedSchema, ArticleDetailSchema, ArticleCreateSchema, ArticleUpdateSchema
)
from website.settings import BASE_DIR
from blog_api.services.article import article_service

router = Router(tags=['Articles'])

@router.get('/articles/', response=ArticlePaginatedSchema)
def get_articles(request: HttpRequest, limit: int = 0, offset: int = 2):
    return article_service.get_paginated_articles(limit=limit, offset=offset)


@router.get('/articles/{article_slug}/', response=ArticleDetailSchema)
def get_article_detail(request: HttpRequest, article_slug: str):
    return article_service.get_article_detail(article_slug=article_slug)


@router.post('/articles/post/', response=ArticleDetailSchema)
def create_new_article(request: HttpRequest, data: Form[ArticleCreateSchema], preview: UploadedFile = File(None), gallery: Optional[list[UploadedFile]] = File(None)):
    return article_service.create_new_article(data=data, preview=preview, gallery=gallery)


@router.patch('articles/update/{article_id}/', response=ArticleDetailSchema)
def update_article(request: HttpRequest, article_id: int, data: ArticleUpdateSchema, preview: Optional[UploadedFile] = File(None), gallery: Optional[list[UploadedFile]] = File(None)):
    return article_service.update_article(article_id=article_id, data=data, preview=preview, gallery=gallery)

@router.delete('/articles/delete/{article_slug}/')
def delete_article(request: HttpRequest, article_slug: str):
    return article_service.delete_article(article_slug=article_slug)