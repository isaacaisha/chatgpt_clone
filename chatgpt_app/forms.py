from django.contrib.auth.forms import UserCreationForm
from django import forms

# Import ReCaptchaField correctly
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox, ReCaptchaV3

from .models import User, VIPUser

# Create your forms here.

class MyUserCreationForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(
        attrs={
            'data-theme': 'dark',
            'data-size': 'compact'
            }
        )
    )

    class Meta:
        model = User
        fields =  ['name', 'email', 'password1', 'password2', 'captcha']


class VIPUserCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=199, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(
        attrs={
            'data-theme': 'dark',
            'data-size': 'compact'
            }
        )
    )

    class Meta:
        model = VIPUser
        fields = []  # No direct fields from VIPUser, handled manually.

    def save(self, commit=True):
        """Create a VIPUser linked to a User."""
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        # Check if the user already exists
        user, created = User.objects.get_or_create(email=email, defaults={'name': name})
        
        # If the user exists but is not associated with a VIPUser
        if not created:
            if hasattr(user, 'vip_profile'):
                raise forms.ValidationError("A VIPUser with this email already exists.")

        # If the user was newly created, set their password
        if created:
            user.set_password(password)
            user.save()

        # Create and associate the VIPUser
        vip_user = super().save(commit=False)
        vip_user.user = user
        if commit:
            vip_user.save()

        return vip_user

class VIPLoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    

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
