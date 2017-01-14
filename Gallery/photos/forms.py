from django import forms
from .models import User, Images


class AuthForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
    password = forms.CharField(
        widget=forms.PasswordInput
    )


class RegForm(AuthForm):
    conf_password = forms.CharField(
        widget=forms.PasswordInput
    )


class UploadForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image']


