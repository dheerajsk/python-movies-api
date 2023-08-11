from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from .serializers import UserSerializer
import json
import jwt
import datetime
from bson import ObjectId
from django.conf import settings
from .models import User, Movie,Screening
from django.core.exceptions import ObjectDoesNotExist
from .models import Ticket
from .serializers import TicketSerializer
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from .models import Booking
from .serializers import BookingSerializer
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from .models import Seat
from .serializers import SeatSerializer

# Create your views here.

users=[]
movies = [
    {
        "title": "Movie A",
        "director": "Director A",
        "starring_actors": "Actor A, Actor B",
        "runtime": 120,
        "genre": "Action",
        "language": "English",
        "rating": "PG-13",
    },
    {
        "title": "Movie B",
        "director": "Director B",
        "starring_actors": "Actor C, Actor D",
        "runtime": 105,
        "genre": "Comedy",
        "language": "Spanish",
        "rating": "PG",
    },
    {
        "title": "Movie C",
        "director": "Director C",
        "starring_actors": "Actor E, Actor F",
        "runtime": 140,
        "genre": "Drama",
        "language": "German",
        "rating": "R",
    },
    {
        "title": "Movie D",
        "director": "Director D",
        "starring_actors": "Actor G, Actor H",
        "runtime": 110,
        "genre": "Thriller",
        "language": "English",
        "rating": "PG-13",
    },
    {
        "title": "Movie E",
        "director": "Director E",
        "starring_actors": "Actor I, Actor J",
        "runtime": 125,
        "genre": "Romance",
        "language": "French",
        "rating": "PG",
    },
]


class UserSignUp(View):
    def post(self, request):
        user_data=json.loads(request.body)
        
        #Validate data using serializer
        user_serialized=UserSerializer(data=user_data)
        if(user_serialized.is_valid()):
            user_instance = user_serialized.save()

            return JsonResponse(user_serialized.data, status=201)
        else:
            return HttpResponseBadRequest()

class UserSignIn(View):
    def post(self, request):
        user_data = json.loads(request.body)
        try:
            # Fetch user from database
            user = User.objects.get(email=user_data["email"])
        except User.DoesNotExist:
            # User not found in database
            return HttpResponseBadRequest()

        # Check password - this should be improved because storing and comparing passwords as plain text is not secure
        if user.password == user_data["password"]:
            # Generate a token with the user's email and an expiration time
            token = jwt.encode({
                'email': user.email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)  # Expiration time
            }, settings.SECRET_KEY, algorithm='HS256')

            return JsonResponse({"token": token}, status=200)
        else:
            # Password didn't match
            return HttpResponseBadRequest()
        

class MoviesAPI(View):
    def get(self, request):
        # Implement fetching all movies with optional filtering based on genre, language, location, and rating
        genre = request.GET.get('genre')
        language = request.GET.get('language')
        location = request.GET.get('location')
        rating = request.GET.get('rating')

        movies = Movie.objects.all()

        if genre:
            movies = movies.filter(genre=genre)

        if language:
            movies = movies.filter(language=language)

        if location:
            # Apply location filtering logic here if you have it as a field in the Movie model
            pass

        if rating:
            movies = movies.filter(rating=rating)

        movie_data = [{
            "id": movie.id,
            "title": movie.title,
            "director": movie.director,
            "starring_actors": movie.starring_actors,
            "runtime": movie.runtime,
            "genre": movie.genre,
            "language": movie.language,
            "rating": movie.rating
        } for movie in movies]

        return JsonResponse(movie_data, status=200, safe=False)

    def post(self, request):
        # Implement adding a new movie (admin-only)
        # You can add authentication and authorization checks here to ensure only admins can add new movies
        movie_data = json.loads(request.body)

        # Validate and save the movie data to the database
        # You can use serializers to validate and save the data

        return JsonResponse({"message": "Movie added successfully"}, status=201)

    def put(self, request, movie_id):
        # Implement updating an existing movie (admin-only)
        # You can add authentication and authorization checks here to ensure only admins can update movies
        movie_data = json.loads(request.body)

        # Fetch the movie by movie_id and update its fields with the new data
        # You can use serializers to validate and save the updated data

        return JsonResponse({"message": "Movie updated successfully"}, status=200)

    def delete(self, request, movie_id):
        # Implement deleting an existing movie (admin-only)
        # You can add authentication and authorization checks here to ensure only admins can delete movies

        # Fetch the movie by movie_id and delete it
        # You can use serializers to validate and delete the movie

        return JsonResponse({"message": "Movie deleted successfully"}, status=200)


class TicketsAPI(View):
    def get(self, request):
        # Implement fetching all booked tickets
        # You can add authentication and authorization checks here to ensure only authenticated users can access the tickets

        # Fetch all booked tickets from the database
        booked_tickets = Ticket.objects.all()
        
        # Serialize the data using TicketSerializer
        ticket_serializer = TicketSerializer(booked_tickets, many=True)
        tickets_data = ticket_serializer.data

        return JsonResponse(tickets_data, status=200, safe=False)

    def post(self, request):
        # Implement booking a new ticket
        # You can add authentication and authorization checks here to ensure only authenticated users can book tickets
        ticket_data = json.loads(request.body)

        # Validate the ticket data, check seat availability, and save the booking details to the database
        # You can use serializers to validate and save the data
        ticket_serializer = TicketSerializer(data=ticket_data)
        
        if ticket_serializer.is_valid():
            ticket_serializer.save()
            return JsonResponse({"message": "Ticket booked successfully"}, status=201)
        else:
            return HttpResponseBadRequest()

class SeatsAPI(View):
    def get(self, request, movie_id):
        # Implement fetching all seats for a specific movie
        # You can add authentication and authorization checks here if needed

        # Fetch all seats for the given movie from the database
        seats = Seat.objects.filter(screening__movie_id=movie_id)
        
        # Serialize the data using SeatSerializer
        seat_serializer = SeatSerializer(seats, many=True)
        seats_data = seat_serializer.data

        return JsonResponse(seats_data, status=200, safe=False)

    def post(self, request, movie_id):
        # Implement reserving seats for a specific movie
        # You can add authentication and authorization checks here if needed
        seats_data = json.loads(request.body)

        # Validate the seat reservation data, check seat availability, and save the reservation details to the database
        # You can use serializers to validate and save the data
        seat_serializer = SeatSerializer(data=seats_data)
        
        if seat_serializer.is_valid():
            seat_serializer.save()
            return JsonResponse({"message": "Seats reserved successfully"}, status=201)
        else:
            return HttpResponseBadRequest()

    def put(self, request, movie_id):
        # Implement updating seat reservations
        # You can add authentication and authorization checks here if needed
        seats_data = json.loads(request.body)

        # Validate the updated seat reservation data, check seat availability, and update the reservation details in the database
        # You can use serializers to validate and update the data
        seat_serializer = SeatSerializer(data=seats_data)
        
        if seat_serializer.is_valid():
            seat_serializer.save()
            return JsonResponse({"message": "Seat reservation updated successfully"}, status=200)
        else:
            return HttpResponseBadRequest()



class BookingAPI(View):
    def get(self, request, booking_id):
        # Implement fetching booking summary for a specific booking_id
        # You can add authentication and authorization checks here if needed

        try:
            # Fetch the booking summary from the database based on the booking_id
            booking = Booking.objects.get(pk=booking_id)
        except Booking.DoesNotExist:
            return JsonResponse({"error": "Booking not found"}, status=404)

        # Serialize the data using BookingSerializer
        booking_serializer = BookingSerializer(booking)
        booking_summary_data = booking_serializer.data

        return JsonResponse(booking_summary_data, status=200)

    def post(self, request):
        # Implement creating a new booking
        # You can add authentication and authorization checks here if needed
        booking_data = json.loads(request.body)

        # Validate the booking data, check seat availability, and save the booking details to the database
        # You can use serializers to validate and save the data
        booking_serializer = BookingSerializer(data=booking_data)

        if booking_serializer.is_valid():
            booking_serializer.save()
            return JsonResponse({"message": "Booking created successfully"}, status=201)
        else:
            return HttpResponseBadRequest()
