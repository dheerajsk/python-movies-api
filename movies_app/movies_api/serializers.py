from rest_framework import serializers
from .models import User, Movie,Screening,Seat,Ticket
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('_id', 'email', 'password', 'name')

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('_id', 'title', 'director', 'starring_actors', 'runtime', 'genre', 'language', 'rating', 'imageUrl')

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

class TicketSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    screening = ScreeningSerializer()
    seats = SeatSerializer(many=True)

    class Meta:
        model = Ticket
        fields = ('id', 'user', 'screening', 'seats', 'total_price')
