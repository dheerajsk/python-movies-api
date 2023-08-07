from rest_framework import serializers
from .models import User, Item,Movie,Screening,Seat
from rest_framework import serializers


class MovieSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    director = serializers.CharField(max_length=100)
    starring_actors = serializers.CharField(max_length=255)
    runtime = serializers.IntegerField()
    genre = serializers.CharField(max_length=50)
    language = serializers.CharField(max_length=50)
    rating = serializers.CharField(max_length=10)    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('_id','desc', 'quantity', 'rate')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('_id', 'email', 'password', 'name')

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'director', 'starring_actors', 'runtime', 'genre', 'language', 'rating')

class ScreeningSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()

    class Meta:
        model = Screening
        fields = ('id', 'movie', 'date', 'time', 'available_seats')

class SeatSerializer(serializers.ModelSerializer):
    screening = ScreeningSerializer()

    class Meta:
        model = Seat
        fields = ('id', 'screening', 'seat_number', 'seat_type', 'price', 'is_available')

