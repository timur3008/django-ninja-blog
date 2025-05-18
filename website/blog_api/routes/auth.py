from blog_api.schemas.auth import UserSchema, UserLoginSchema, UserRegistrationSchema
from blog_api.services.auth import auth_service

from ninja import Router
from ninja.errors import ValidationError
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

router = Router(tags=['User'])

@router.post('/auth/login/', response=UserSchema)
def login_user(request: HttpRequest, login_data: UserLoginSchema):
    return auth_service.login_user(request=request, login_data=login_data)

@router.post('/auth/register/', response=UserSchema)
def register_user(request: HttpRequest, registration_data: UserRegistrationSchema):
    return auth_service.register_user(registration_data=registration_data)

@router.post('/auth/logout/')
def logout_user(request: HttpRequest):
    return auth_service.logout_user(request=request)