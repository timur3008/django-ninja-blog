from blog_app.models import FAQ
from blog_api.schemas.faqs import (
    FAQSchema, FAQCreationSchema, FAQUpdateSchema, FAQDeleteSchema
)
from blog_api.services.faq import faq_service

from ninja import Router
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from typing import Union

router = Router(tags=['FAQs'])

@router.get('/faqs/', response=list[FAQSchema])
def get_faqs(request):
    return faq_service.get_faqs()

@router.get('/faqs/{faq_pk}/', response=FAQSchema)
def get_faq_by_id(request: HttpRequest, faq_pk: int):
    return faq_service.get_faq_by_id(faq_pk=faq_pk)

@router.post('/faqs/', response=FAQSchema)
def create_faq(request: HttpRequest, faq_data: FAQCreationSchema):
    return faq_service.create_faq(faq_data=faq_data)

@router.patch('/faqs/{faq_pk}/update/', response=FAQSchema)
def update_faq_item(request: HttpRequest, faq_pk: int, faq_data: FAQUpdateSchema):
    return faq_service.update_faq_item(faq_pk=faq_pk, faq_data=faq_data)

@router.delete('/faqs/{faq_pk}/delete/', response=Union[FAQDeleteSchema, dict[str, str]])
def delete_faq_by_id(request: HttpRequest, faq_pk: int):
    return faq_service.delete_faq_by_id(faq_pk=faq_pk)