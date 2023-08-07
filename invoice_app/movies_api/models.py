from django.db import models
from django.db import models
from djongo import models as djongo_models

class User(models.Model):
    _id = djongo_models.ObjectIdField()
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    name=models.CharField(max_length=100)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    starring_actors = models.CharField(max_length=255)
    runtime = models.IntegerField()
    genre = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    rating = models.CharField(max_length=10)

    def __str__(self):
        return self.title

class Screening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    available_seats = models.IntegerField()

    def __str__(self):
        return f"{self.movie.title} - {self.date} {self.time}"

class Seat(models.Model):
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    seat_type = models.CharField(max_length=20)  # Regular, Premium, etc.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Screening: {self.screening}, Seat: {self.seat_number}, Type: {self.seat_type}, Price: {self.price}"

