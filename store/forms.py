from typing import Any, Dict
from django import forms
# from django.contrib.auth.models import User
from users.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(required=True, max_length=50, min_length=4, label='Nombre de usuario',
                               widget= forms.TextInput(attrs={'class': 'form-control mb-1 mt-1',
                                'id': 'username'}))
    email = forms.EmailField(required=True, label='Correo electrónico',
                             widget= forms.EmailInput(attrs={'class': 'form-control mb-1 mt-1',
                             'id': 'email', 'placeholder': '91218@vamosriver.com'}))
    password = forms.CharField(required=True, label='Contraseña',
                               widget= forms.PasswordInput(attrs={'class': 'form-control mb-1 mt-1',
                               'id': 'password'}))
    password2 = forms.CharField(required=True, label='Confirmar contraseña',
                                widget= forms.PasswordInput(attrs={'class': 'form-control mb-1 mt-1',
                               'id': 'password2'}))
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya existe')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya existe')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            self.add_error('password2', 'La clave no coincide')
        
    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password')
        )