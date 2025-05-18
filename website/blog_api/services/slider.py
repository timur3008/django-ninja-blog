import os

from blog_app.models import Slider
from blog_api.schemas.sliders import SliderSchema, SliderCreationSchema, SliderUpdateSchema, SliderDeleteSchema
from website.settings import BASE_DIR

from django.shortcuts import get_object_or_404
from ninja import File, UploadedFile

class SliderService:
    def __save_image(self, path: str, file: UploadedFile):
        with open(path, mode='wb') as _file:
            _file.write(file)

    def get_sliders(self) -> list[SliderSchema]:
        sliders = Slider.objects.all()
        return sliders
    
    def get_slider_by_id(self, slider_id: int) -> SliderSchema:
        slider = get_object_or_404(Slider, pk=slider_id)
        return slider
    
    def create_new_slider(self, slider_data: SliderCreationSchema, image: UploadedFile = File(...)) -> SliderSchema:
        slider = Slider.objects.create(**slider_data)
        slider_path = f'{BASE_DIR}/media/slider/{image.name}'

        self.__save_image(path=slider_path, file=image.read())

        slider.image = f'slider/{image.name}'
        slider.save()
        return slider
    
    def update_slider(self, slider_id: int, slider_data: SliderUpdateSchema, image: UploadedFile = File(None)) -> SliderSchema:
        slider = get_object_or_404(Slider, pk=slider_id)

        for key, value in slider_data.dict().items():
            if not value:
                current_value = getattr(slider, key)
                setattr(slider, key, current_value)
            else:
                setattr(slider, key, value)

        if image is not None:
            if slider.image:
                os.remove(f'{BASE_DIR}/{slider.image.url}')
            image_path = f'{BASE_DIR}/media/slider/{image.name}'
            self.__save_image(path=image_path, file=image.read())
            slider.image = f'slider/{image.name}'
        
        slider.save()
        return slider
    
    def delete_slider(self, slider_id: int) -> SliderDeleteSchema:
        slider = get_object_or_404(Slider, pk=slider_id)
        slider.delete()
        return {'is_deleted': True}
    
sliders_service = SliderService()