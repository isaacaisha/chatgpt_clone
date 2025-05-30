import os

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse

from django_otp.decorators import otp_required

from openai import OpenAI
from .forms import  MyUserCreationForm, VIPUserCreationForm, LoginForm
from .models import ChatData
from django.contrib.auth import authenticate, login, logout

from gtts import gTTS
from django.utils import timezone

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def registerPage(request):
    page = 'register'
    form = MyUserCreationForm(request.POST or None)
    hide_navbar = True

    if request.method == 'POST':
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.email = user.email.lower()
                user.save()
                messages.success(request, 'Registration successful! Please log in.')
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
        'date': timezone.now().strftime("%a %d %B %Y"),
    }
    return render(request, 'login_register.html', context)


# View for the register VIP page, requiring 2FA
@login_required
def registerVipUser(request):
    page = 'register_vip'

    if request.method == "POST":
        form = VIPUserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "VIP User registered successfully!")
                # Redirect to two_factor setup
                return redirect('two_factor:setup')
            except ValidationError as e:
                # Add the error message to the form
                messages.error(request, f'Sorry, an error occurred: {e}')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = VIPUserCreationForm()

    context = {
        'page': page,
        'form': form,
        'date': timezone.now().strftime("%a %d %B %Y"),
        'message': 'Welcome to the Superuser Page!',
    }
    return render(request, 'vip_register.html', context)


# View for the login VIP page, requiring 2FA
@login_required
def loginVipPage(request):
    page = 'login_vip'
    context = {
        'page': page,
        'date': timezone.now().strftime("%a %d %B %Y"),
        'message': 'Welcome to the Superuser Page!',
    }
    return render(request, 'vip_register.html', context)


def loginPage(request):
    page = 'login'
    form = LoginForm()
    hide_navbar = True

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Invalid email or password 😝.")
        else:
            messages.error(request, "Invalid reCAPTCHA. Please try again 😝.")

    context = {
        'page': page,
        'form': form,
        'hide_navbar': hide_navbar,
        'date': timezone.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
        'date': timezone.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'index.html', context)


def response(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')

        # Log the received message
        print(f"Message received: {message}")

        # Generate OpenAI response
        completion = client.chat.completions.create(
            model='gpt-4',
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        answer = completion.choices[0].message.content
        print(f"Answer generated: {answer}")

        # Save ChatData object
        new_chat = ChatData(user=request.user, message=message, response=answer)
        new_chat.save()
        print(f"ChatData saved with id: {new_chat.id}")

        # Convert the OpenAI response to speech
        tts = gTTS(text=answer, lang='en')
        audio_path = os.path.join(settings.MEDIA_ROOT, f'response_{new_chat.id}.mp3')
        tts.save(audio_path)
        print(f"Audio saved at: {audio_path}")

        # Return JSON response including audio URL
        audio_url = request.build_absolute_uri(settings.MEDIA_URL + f'response_{new_chat.id}.mp3')
        return JsonResponse({'response': answer, 'audio_url': audio_url})


# View for the VIP page, requiring 2FA status
@login_required
@otp_required
def vipPage(request):
    if not request.user.is_verified():
        messages.warning(request, "Please complete two-factor authentication.")
        # Redirect to two_factor login
        return redirect('two_factor:login')

    context = {
        'date': timezone.now().strftime("%a %d %B %Y"),
        'message': 'Welcome to the Superuser Page!',
    }
    return render(request, 'vip_page.html', context)
