from django.urls import path
from .views import MovieDetailAPI, MoviesAPI, SeatsAPI, TicketsAPI, UserSignIn, UserSignUp
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('user/signup', csrf_exempt(UserSignUp.as_view()), name='signup'),
    path('user/signin', csrf_exempt(UserSignIn.as_view()), name='signin'),
    path('movies', MoviesAPI.as_view(), name='movies'),
    path('movie/<int:movie_id>/', MovieDetailAPI.as_view(), name='movie-detail'),
    path('tickets', csrf_exempt(TicketsAPI.as_view()), name='tickets'),
    path('seats', csrf_exempt(SeatsAPI.as_view()), name='Seats'),
]