import os
import django
import random
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies_app.settings')
django.setup()

from movies_api.models import User, Movie, Screening, Seat, Ticket

def seed_data():
    user_data = [
        {"email": "alice@example.com", "password": "password123", "name": "Alice Smith"},
        {"email": "bob@example.com", "password": "password123", "name": "Bob Brown"}
    ]
    
    # for user in user_data:
    #     User.objects.create(**user)

    # Seed Movie with fictional details
    movie_data = [
    {"title": "Galactic Warriors", "director": "John Doe", "starring_actors": "Alice Smith, Bob Brown, Charlie Clark", "runtime": 120, "genre": "Action", "language": "English", "rating": "4.5", "imageUrl": "https://dummyimage.com/200x300"},
    {"title": "Lost in Dreams", "director": "Jane White", "starring_actors": "David Grey, Emily Stone", "runtime": 90, "genre": "Drama", "language": "English", "rating": "4.2", "imageUrl": "https://dummyimage.com/200x300"},
    {"title": "Mystical Mountains", "director": "Oliver Twist", "starring_actors": "Sarah Connor, James Bond", "runtime": 95, "genre": "Adventure", "language": "English", "rating": "4.1", "imageUrl": "https://dummyimage.com/200x300"},
    {"title": "Robot Rebellion", "director": "Anna King", "starring_actors": "Iron Man, Captain America", "runtime": 140, "genre": "Sci-Fi", "language": "English", "rating": "4.7", "imageUrl": "https://dummyimage.com/200x300"},
    {"title": "Dancing Shadows", "director": "Steve Smith", "starring_actors": "Mia Wallace, Vincent Vega", "runtime": 110, "genre": "Drama", "language": "French", "rating": "4.3", "imageUrl": "https://dummyimage.com/200x300"},
    {"title": "Ocean's Echo", "director": "Pamela Anderson", "starring_actors": "Jack Sparrow, Davy Jones", "runtime": 130, "genre": "Adventure", "language": "Spanish", "rating": "4.8", "imageUrl": "https://dummyimage.com/200x300"},
    {"title": "Golden Sand", "director": "Bob Builder", "starring_actors": "Anakin Skywalker, Obi-Wan Kenobi", "runtime": 125, "genre": "Drama", "language": "German", "rating": "4.6", "imageUrl": "https://dummyimage.com/200x300"},
    {"title": "Moon's Descent", "director": "Clark Kent", "starring_actors": "Luke Skywalker, Darth Vader", "runtime": 150, "genre": "Sci-Fi", "language": "Italian", "rating": "4.9", "imageUrl": "https://dummyimage.com/200x300"},
    {"title": "Forgotten Kingdom", "director": "Bruce Wayne", "starring_actors": "Frodo Baggins, Aragorn", "runtime": 160, "genre": "Fantasy", "language": "English", "rating": "5.0", "imageUrl": "https://dummyimage.com/200x300"},
    {"title": "Endless Night", "director": "Diana Prince", "starring_actors": "Harry Potter, Hermione Granger", "runtime": 105, "genre": "Fantasy", "language": "English", "rating": "3.8", "imageUrl": "https://dummyimage.com/200x300"}
]

    
    # for movie in movie_data:
    #     m = Movie(**movie)
    #     m.save() 

    # Seed Screening
    for movie in Movie.objects.all():
        for i in range(2):
            Screening.objects.create(
                movie=movie,
                date=(datetime.now() + timedelta(days=i)).date(),
                time=(datetime.now() + timedelta(hours=i)).time(),
                available_seats=100
            )


    print('Data seeded successfully!')

if __name__ == "__main__":
    seed_data()
