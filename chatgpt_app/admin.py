from django.contrib import admin
from .models import ChatData


# Register your models here.
@admin.register(ChatData)
class ChatDataAdmin(admin.ModelAdmin):
    list_display = ('message', 'response', 'created_at')
