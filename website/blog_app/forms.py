from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from . import models

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }

# ModelForm - модель для работы с формами
class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment # говорим от какой модели наследоваться
        fields = ['text'] # говорим какие поля заполнить
        widgets = { # для отрисовки
            'text': forms.Textarea(
                attrs={'class': 'form-control'}
            )
        }

class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ['title', 'short_description', 'full_description', 'preview', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название статьи'
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Краткое описание'
            }),
            'full_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Полное описание'
            }),
            'preview': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            })
        }