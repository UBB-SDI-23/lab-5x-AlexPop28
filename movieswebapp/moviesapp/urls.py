from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from movieswebapp.moviesapp import views
from movieswebapp.moviesapp.views.authentication import (
    UserActivationView,
    UserRegistrationView,
)
from movieswebapp.moviesapp.views.users import UserDetail

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
        "actors/by_total_income/",
        views.actors.ActorsOrderedByTotalIncome.as_view(),
    ),
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
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("activate/", UserActivationView.as_view(), name="activate-user"),
    path("users/<str:user_id>", UserDetail.as_view()),
] + router.urls
