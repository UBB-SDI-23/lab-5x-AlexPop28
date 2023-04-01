from django.urls import path
from rest_framework import routers

from movieswebapp.moviesapp import views

router = routers.SimpleRouter()
router.register(
    r"movies/(?P<movie_id>\d+)/actors",
    views.movies.ActorMovieViewSet,
    basename="movie-actors",
)


urlpatterns = [
    path("movies/", views.movies.MovieList.as_view()),
    path("movies/<int:pk>/", views.movies.MovieDetail.as_view()),
    path("directors/", views.directors.DirectorList.as_view()),
    path("directors/<int:pk>/", views.directors.DirectorDetail.as_view()),
    path("actors/", views.actors.ActorList.as_view()),
    path("actors/<int:pk>/", views.actors.ActorDetail.as_view()),
    path(
        "movies/by_average_age_of_actors/",
        views.movies.MoviesOrderedByAverageAgeOfActors.as_view(),
    ),
    path(
        "directors/by_last_release_date/",
        views.directors.DirectorsOrderedByLatestMovie.as_view(),
    ),
    path(
        "directors/<int:director_id>/movies",
        views.directors.DirectorAddMovies.as_view(),
    ),
] + router.urls
