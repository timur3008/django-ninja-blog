from blog_api.schemas.auth import UserSchema, UserLoginSchema, UserRegistrationSchema

from ninja.errors import ValidationError
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

class AuthService:
    def login_user(self, request: HttpRequest,login_data: UserLoginSchema) -> UserSchema:
        user = authenticate(request, username=login_data.username, password=login_data.password)
        if user is None:
            raise ValidationError('User not found')
        login(request, user=user)
        return user
    
    def register_user(self, registration_data: UserRegistrationSchema) -> UserSchema:
        if User.objects.filter(username=registration_data.username).exists():
            raise ValidationError('User with this username already exists')
        
        if '@' not in registration_data.email and '.' not in registration_data.email:
            raise ValidationError('Email is incorrect')
        
        data = registration_data.dict()
        password1 = data.pop('password1')
        password2 = data.pop('password2')

        if password1 != password2:
            raise ValidationError('Passwords are not similar')
        
        user = User.objects.create(**data)
        user.set_password(password1)
        user.save()
        return user
    
    def logout_user(self, request: HttpRequest):
        logout(request)
        return {'is_authenticated': request.user.is_authenticated}
    
auth_service = AuthService()