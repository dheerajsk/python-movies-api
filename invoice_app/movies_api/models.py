from django.db import models
from django.db import models
from djongo import models as djongo_models

class User(models.Model):
    _id = djongo_models.ObjectIdField()
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    name=models.CharField(max_length=100)

class Item(models.Model):
    _id = djongo_models.ObjectIdField()
    invoice = models.ForeignKey('Invoice', related_name='items', on_delete=models.CASCADE)
    desc = models.CharField(max_length=255)
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)

class Invoice(models.Model):
    _id = djongo_models.ObjectIdField()
    client_name = models.CharField(max_length=255)
    date = models.DateField()
