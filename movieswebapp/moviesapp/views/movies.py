from typing import Any

from django.db.models import Avg, QuerySet
from django.db.models.functions import ExtractYear
from rest_framework import generics, mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.settings import api_settings

from movieswebapp.moviesapp.models import ActorMovie, Movie
from movieswebapp.moviesapp.serializers import (
    ActorMovieSerializer,
    MovieSerializer,
    MovieSerializerWithAverageAge,
    SingleMovieSerializer,
)


class MovieList(generics.ListCreateAPIView[Movie]):
    """
    List all Movies or create a new Movie.
    """

    serializer_class = MovieSerializer

    def get_queryset(self) -> QuerySet[Movie]:
        """
        Optionally, filters the returned movies to those having a rating
        at least `min_rating` that is a query parameter in the URL.
        """
        queryset = Movie.objects.all()
        min_rating = self.request.query_params.get("min_rating")
        if min_rating is not None:
            queryset = queryset.filter(rating__gte=min_rating)
        return queryset


class MovieDetail(generics.RetrieveUpdateDestroyAPIView[Movie]):
    """
    Retrieve, update or delete a Movie instance.
    """

    queryset = Movie.objects.all()
    serializer_class = SingleMovieSerializer


class MoviesOrderedByAverageAgeOfActors(generics.ListAPIView[Movie]):
    queryset = Movie.objects.annotate(
        average_age=Avg(
            ExtractYear("release_date") - ExtractYear("actors__date_of_birth")
        )
    ).order_by("average_age")
    serializer_class = MovieSerializerWithAverageAge


class ActorMovieViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet[ActorMovie],
):
    serializer_class = ActorMovieSerializer
    queryset = ActorMovie.objects.all()

    lookup_field = "actor_id"

    def create(
        self, request: Request, movie_id: int, *args: Any, **kwargs: Any
    ) -> Response:
        # Check that if a `movie` parameter was passed, it matches the movie_id from the route.
        data = request.data.copy()
        if data.get("movie", movie_id) != movie_id:
            return Response(
                {"message": "Bad request format. Movie does not match id from route."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data["movie"] = movie_id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = ActorMovieViewSet.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def list(self, request: Request, movie_id: int) -> Response:
        get_object_or_404(Movie.objects.all(), id=movie_id)
        actor_movies = ActorMovie.objects.filter(movie=movie_id)
        serializer = ActorMovieSerializer(actor_movies, many=True)
        return Response(serializer.data)

    @staticmethod
    def get_success_headers(data: dict[str, Any]) -> dict[str, str]:
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def get_object(self) -> ActorMovie:
        queryset = self.filter_queryset(self.get_queryset())
        movie_id = self.kwargs["movie_id"]
        actor_id = self.kwargs["actor_id"]

        filter_kwargs = {
            "movie_id": movie_id,
            "actor_id": actor_id,
        }
        actor_movie = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, actor_movie)

        return actor_movie
