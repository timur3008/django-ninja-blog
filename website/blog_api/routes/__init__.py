from ninja import NinjaAPI

from .categories import router as categories_router
from .sliders import router as sliders_router
from .faqs import router as faqs_router
from .articles import router as articles_router
from .comments import router as comments_router
from .auth import router as auth_router

api_router = NinjaAPI()

API = '/api/'

api_router.add_router(prefix=API, router=categories_router)
api_router.add_router(prefix=API, router=sliders_router)
api_router.add_router(prefix=API, router=faqs_router)
api_router.add_router(prefix=API, router=articles_router)
api_router.add_router(prefix=API, router=comments_router)
api_router.add_router(prefix=API, router=auth_router)