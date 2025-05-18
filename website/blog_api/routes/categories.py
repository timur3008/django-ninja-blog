from blog_api.schemas.categories import CategorySchema, CategoryCreationSchema
from blog_app.models import Category

from ninja import Router
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from slugify import slugify

router = Router(tags=['Categories'])

@router.get('/categories/', response=list[CategorySchema])
def get_categories(request: HttpRequest):
    categories = Category.objects.all()
    return categories

@router.get('/categories/{category_pk}/', response=CategorySchema)
def get_category_by_id(request: HttpRequest, category_pk: int):
    '''Get category object by id'''
    category = get_object_or_404(Category, pk=category_pk)
    return category

# @router.get('/categories/{category_slug}/', response=CategorySchema)
# def get_category_by_slug(request: HttpRequest, category_slug: str):
#     '''Get category object by slug'''
#     category = get_object_or_404(Category, slug=category_slug)
#     return category

@router.post('/categories/', response=CategorySchema)
def create_category(request: HttpRequest, category_data: CategoryCreationSchema):
    category = Category.objects.create(name=category_data.name, slug=slugify(category_data.name))
    return category