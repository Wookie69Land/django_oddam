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


class UserPasswordForm(ModelForm):
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    class Meta:
        model = User
        fields = ['password']


class EditProfileForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data.get('email')).exclude(pk=self.instance.id).exists():
            raise ValidationError('Ten email jest już zajęty!')
        return self.cleaned_data.get('email')


class UpdatePasswordForm(forms.Form):
    old_password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Stare hasło'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło'}))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz nowe hasło'}))

    def clean_password_repeat(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            raise ValidationError('Hasła nie są takie same!')
        return self.cleaned_data.get('password2')


