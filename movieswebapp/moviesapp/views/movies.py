from typing import Any

from django.db.models import Avg, QuerySet
from django.db.models.functions import ExtractYear
from rest_framework import generics, mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.settings import api_settings

from movieswebapp.moviesapp.models import ActorMovie, Movie
from movieswebapp.moviesapp.permissions import HasEditPermissionOrReadOnly
from movieswebapp.moviesapp.serializers import (
    ActorMovieSerializer,
    ActorMovieSerializerWithActorName,
    MovieSerializer,
    MovieSerializerWithActorCount,
    MovieSerializerWithAverageAge,
    SingleMovieSerializer,
)
from movieswebapp.moviesapp.views.generics import GenericSqlView
from movieswebapp.moviesapp.views.pagination import CustomPagination


class MovieList(generics.ListCreateAPIView[Movie]):
    """
    List all Movies or create a new Movie.
    """

    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

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

    def get_serializer_class(
        self,
    ) -> type[MovieSerializer | MovieSerializerWithActorCount]:
        if self.request.method == "GET":
            return MovieSerializerWithActorCount
        return MovieSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = request.data.copy()
        data["added_by_id"] = self.request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer: BaseSerializer[Movie]) -> None:
        serializer.save(added_by=self.request.user)


class MovieDetail(generics.RetrieveUpdateDestroyAPIView[Movie]):
    """
    Retrieve, update or delete a Movie instance.
    """

    queryset = Movie.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasEditPermissionOrReadOnly]

    def get_serializer_class(self) -> type[MovieSerializer | SingleMovieSerializer]:
        if self.request.method == "PUT":
            return MovieSerializer
        return SingleMovieSerializer


class MoviesOrderedByAverageAgeOfActors(generics.ListAPIView[Movie]):
    queryset = Movie.objects.annotate(
        average_age=Avg(
            ExtractYear("release_date") - ExtractYear("actors__date_of_birth")
        )
    ).order_by("average_age")
    serializer_class = MovieSerializerWithAverageAge
    pagination_class = CustomPagination


class ActorMovieViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet[ActorMovie],
):
    serializer_class = ActorMovieSerializer
    queryset = ActorMovie.objects.all()
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly, HasEditPermissionOrReadOnly]

    lookup_field = "actor_id"

    def create(
        self, request: Request, movie_id: str, *args: Any, **kwargs: Any
    ) -> Response:
        # Check that if a `movie` parameter was passed, it matches the movie_id from the route.
        data = request.data.copy()
        if data.get("movie", movie_id) != int(movie_id):
            return Response(
                {"message": "Bad request format. Movie does not match id from route."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data["movie"] = int(movie_id)
        data["added_by_id"] = request.user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(added_by=request.user)
        headers = ActorMovieViewSet.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def list(self, request: Request, movie_id: str) -> Response:
        get_object_or_404(Movie.objects.all(), id=movie_id)
        actor_movies = ActorMovie.objects.filter(movie=movie_id)

        # Use pagination class to paginate the queryset
        page = self.paginate_queryset(actor_movies)
        if page is not None:
            serializer = ActorMovieSerializerWithActorName(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ActorMovieSerializerWithActorName(actor_movies, many=True)
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


class MovieTruncateTable(GenericSqlView):
    def __init__(self) -> None:
        super().__init__("sql_scripts/truncate_movies.sql")


class MoviePopulateTable(GenericSqlView):
    def __init__(self) -> None:
        super().__init__("sql_scripts/gen_movies.sql")
