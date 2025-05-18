from typing import Union

from blog_api.schemas.faqs import FAQSchema, FAQCreationSchema, FAQUpdateSchema, FAQDeleteSchema
from blog_app.models import FAQ

from django.shortcuts import get_object_or_404

class FAQService:
    def get_faqs(self) -> list[FAQSchema]:
        faqs = FAQ.objects.all()
        return faqs
    
    def get_faq_by_id(self, faq_pk: int) -> FAQSchema:
        faq = get_object_or_404(FAQ, pk=faq_pk)
        return faq
    
    def create_faq(self, faq_data: FAQCreationSchema) -> FAQSchema:
        faq = FAQ.objects.create(**faq_data.dict())
        return faq
    
    def update_faq_item(self, faq_pk: int, faq_data: FAQUpdateSchema) -> FAQSchema:
        faq = get_object_or_404(FAQ, pk=faq_pk)

        for key, value in faq_data.dict().items():
            if not value:
                current_value = getattr(faq, key)
                setattr(faq, key, current_value)
            else:
                setattr(faq, key, value)

        faq.save()
        return faq
    
    def delete_faq_by_id(self, faq_pk: int) -> Union[FAQDeleteSchema, dict[str, str]]:
        faq = get_object_or_404(FAQ, pk=faq_pk)
        faq.delete()
        return {'is_deleted': True}
    

faq_service = FAQService()