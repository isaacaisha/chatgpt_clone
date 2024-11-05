from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm 
from .models import User

# Create your forms here.


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields =  ['name', 'username', 'email', 'password1', 'password2']
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email']
