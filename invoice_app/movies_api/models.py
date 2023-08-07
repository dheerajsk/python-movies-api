from django.db import models
from django.db import models
from djongo import models as djongo_models

class Movie(models.Model):
    _id = djongo_models.ObjectIdField()
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    starring_actors = models.CharField(max_length=255)
    runtime = models.IntegerField()
    genre = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    rating = models.CharField(max_length=10)

    def __str__(self):
        return self.title

class User(models.Model):
    _id = djongo_models.ObjectIdField()
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    name=models.CharField(max_length=100)

# class Item(models.Model):
#     _id = djongo_models.ObjectIdField()
#     invoice = models.ForeignKey('Invoice', related_name='items', on_delete=models.CASCADE)
#     desc = models.CharField(max_length=255)
#     quantity = models.IntegerField()
#     rate = models.DecimalField(max_digits=10, decimal_places=2)

# class Invoice(models.Model):
#     _id = djongo_models.ObjectIdField()
#     client_name = models.CharField(max_length=255)
#     date = models.DateField()