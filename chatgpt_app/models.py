from django.db import models


# Create your models here.
class ChatData(models.Model):
    message = models.CharField(max_length=999991)
    response = models.CharField(max_length=999991)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
