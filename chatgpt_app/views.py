import os
from django.shortcuts import render
from openai import OpenAI
from django.http import JsonResponse
from .models import ChatData

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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
