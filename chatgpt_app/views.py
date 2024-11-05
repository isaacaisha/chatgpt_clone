import os
from django.shortcuts import render, redirect
from django.contrib import messages
from openai import OpenAI
from django.http import JsonResponse
from .forms import MyUserCreationForm
from .models import User, ChatData
from django.contrib.auth import authenticate, login, logout
from datetime import datetime


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def loginPage(request):
    page = 'login'
    hide_navbar = True
    hide_edit_user = True

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, f'User email: {email} doesn\'t exit 😝')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, f'User email: {email} or Password  doesn\'t exit 😝')

    context = {
        'page': page,
        'hide_navbar': hide_navbar,
        'hide_edit_user': hide_edit_user,
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    page = 'register'
    form = MyUserCreationForm()
    hide_navbar = True
    hide_edit_user = True

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, f'Sorry, something went wrong during registration 😝')

    context = {
        'page': page,
        'form': form,
        'hide_navbar': hide_navbar,
        'hide_edit_user': hide_edit_user,
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'login_register.html', context)


def index(request):
    return render(request, 'index.html')

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

        new_chat = ChatData(message=message, response=answer)
        
        # Check the ChatData object before saving
        print(f"ChatData to be saved: {new_chat}")

        new_chat.save()

        # Confirm the save operation
        print(f"ChatData saved with id: {new_chat.id}")

        return JsonResponse({'response': answer})
    return JsonResponse({'response': 'Invalid request'}, status=401)
