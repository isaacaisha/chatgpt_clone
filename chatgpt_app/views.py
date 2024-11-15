import os

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse

from django.urls import reverse
from django_otp.decorators import otp_required
from django_otp.plugins.otp_static.models import StaticDevice
from django_otp.plugins.otp_totp.models import TOTPDevice

from openai import OpenAI
from .forms import LoginForm, MyUserCreationForm
from .models import ChatData
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def registerPage(request):
    page = 'register'
    form = MyUserCreationForm(request.POST or None)
    hide_navbar = True
    hide_edit_user = True

    if request.method == 'POST':
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.email = user.email.lower()
                user.save()
                messages.success(request, 'Registration successful! Please log in.')
                #return redirect('two_factor:setup')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Sorry, an error occurred: {e}')
        else:
            error_messages = form.errors.as_text()
            messages.error(request, f'Sorry, something went wrong during registration. Details: {error_messages}😝.')

    context = {
        'page': page,
        'form': form,
        'hide_navbar': hide_navbar,
        'hide_edit_user': hide_edit_user,
        'date': timezone.now().strftime("%a %d %B %Y"),
    }
    return render(request, 'login_register.html', context)


def loginPage(request):
    page = 'login'
    form = LoginForm()
    hide_navbar = True
    hide_edit_user = True

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user:
                login(request, user)
                return redirect('index')
                ## Redirect to two_factor login
                #return redirect('two_factor:login')
            else:
                messages.error(request, "Invalid email or password 😝.")
        else:
            messages.error(request, "Invalid reCAPTCHA. Please try again 😝.")

    context = {
        'page': page,
        'form': form,
        'hide_navbar': hide_navbar,
        'hide_edit_user': hide_edit_user,
        'date': timezone.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


#@otp_required
@login_required
def index(request):
    
    context = {
        'date': timezone.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'index.html', context)

def response(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')

        # Check if the message was correctly retrieved
        print(f"Message received: {message}")

        completion = client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )

        answer = completion.choices[0].message.content

        # Check the generated answer
        print(f"Answer generated: {answer}")

        # Associate ChatData with the logged-in user
        new_chat = ChatData(user=request.user, message=message, response=answer)
        
        # Check the ChatData object before saving
        print(f"ChatData to be saved: {new_chat}")

        new_chat.save()

        # Confirm the save operation
        print(f"ChatData saved with id: {new_chat.id}")

        return JsonResponse({'response': answer})
    return JsonResponse({'response': 'Invalid request'}, status=401)


# Function to check if the user is a superuser
def superuser_required(user):
    return user.is_superuser

# View for the superuser page, requiring 2FA and superuser status
@login_required
#@otp_required
#@user_passes_test(superuser_required)
def superuser_page(request):
    # Check if the user has any OTP device enabled
    has_otp_device = StaticDevice.objects.filter(user=request.user).exists() or \
                     TOTPDevice.objects.filter(user=request.user).exists()
    
    # If the user has an OTP device but hasn't completed 2FA, enforce 2FA
    if has_otp_device and not request.user.is_verified():
        messages.warning(request, "Please complete two-factor authentication.")
        return redirect(f"{reverse('two_factor:login')}?next={request.path}")
    
    if not has_otp_device:
        messages.warning(request, "Please set up two-factor authentication.")
        return redirect('two_factor:setup')
    
    context = {
        'date': timezone.now().strftime("%a %d %B %Y"),
        'message': 'Welcome to the Superuser Page!',
    }
    return render(request, 'superuser_page.html', context)
