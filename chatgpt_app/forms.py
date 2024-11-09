from django.contrib.auth.forms import UserCreationForm
from django import forms

# Import ReCaptchaField correctly
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox, ReCaptchaV3

from .models import User

# Create your forms here.

class MyUserCreationForm(UserCreationForm):
    # Use reCAPTCHA v3 for registration
    #captcha = ReCaptchaField(widget=ReCaptchaV3())
    class Meta:
        model = User
        fields =  ['name', 'username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'e.g. siisiAi@gmail.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))
    
    # Use reCAPTCHA v2 for login
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(
        attrs={
            'data-theme': 'dark',
            'data-size': 'compact'
            }
        )
    )
