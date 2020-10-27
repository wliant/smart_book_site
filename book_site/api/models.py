from django.db import models

# Create your models here.

class Book(models.Model):
    created = models.DateTimeField(auto_now_add=True)