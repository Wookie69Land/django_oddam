from django import forms
from django.forms import ModelForm
from django.core.validators import ValidationError

from oddam_app.models import *


class UserRegisterForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data.get('email')).exists():
            raise ValidationError('Ten email jest już zajęty!')
        return self.cleaned_data.get('email')

    def clean_password2(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            raise ValidationError('Hasła nie są takie same!')
        return self.cleaned_data.get('password2')


