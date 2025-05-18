import os

from blog_app.models import Slider
from blog_api.schemas.sliders import SliderSchema, SliderCreationSchema, SliderUpdateSchema, SliderDeleteSchema
from website.settings import BASE_DIR

from blog_api.services.slider import sliders_service

from ninja import Router
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import File, UploadedFile

router = Router(tags=['Sliders'])

@router.get('/sliders/', response=list[SliderSchema])
def get_sliders(request: HttpRequest):
    return sliders_service.get_sliders()

@router.get('/sliders/{slider_id}/', response=SliderSchema)
def get_slider_by_id(request: HttpRequest, slider_id: int):
    return sliders_service.get_slider_by_id(slider_id=slider_id)

@router.post('slider/create/', response=SliderSchema)
def create_new_slider(request: HttpRequest, slider_data: SliderCreationSchema, image: UploadedFile = File(...)):
    return sliders_service.create_new_slider(slider_data=slider_data, image=image)

@router.put('sliders/{slider_id}/update', response=SliderSchema)
def update_slider(request: HttpRequest, slider_id: int, slider_data: SliderUpdateSchema, image: UploadedFile = File(None)):
    return sliders_service.update_slider(slider_id=slider_id, slider_data=slider_data, image=image)

@router.delete('/sliders/{slider_id}/delete', response=SliderDeleteSchema)
def delete_slider(request: HttpRequest, slider_id: int):
    return sliders_service.delete_slider(slider_id=slider_id)

