from django.db import models

# Create your models here.

from django.db import models

class User(models.Model):
    user_id=models.IntegerField()
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    name=models.CharField(max_length=100)