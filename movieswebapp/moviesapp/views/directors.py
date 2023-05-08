from typing import Any

from django.db.models import F, Max, QuerySet
from django.db.models.functions import ExtractYear
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from movieswebapp.moviesapp.models import Director, Movie
from movieswebapp.moviesapp.serializers import (
    DirectorSerializer,
    DirectorSerializerWithLastReleaseDate,
    DirectorSerializerWithMovieCount,
    MovieIdsSerializer,
    SingleDirectorSerializer,
)
from movieswebapp.moviesapp.views.pagination import CustomPagination


class DirectorList(generics.ListCreateAPIView[Director]):
    """
    List all Directors or create a new Director.
    """

    queryset = Director.objects.all()
    pagination_class = CustomPagination

    def get_queryset(self) -> QuerySet[Director]:
        name = self.request.query_params.get("name")
        queryset = Director.objects.all()
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_serializer_class(
        self,
    ) -> type[DirectorSerializer | DirectorSerializerWithMovieCount]:
        if self.request.method == "GET":
            return DirectorSerializerWithMovieCount
        return DirectorSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = request.data.copy()
        if self.request.user is None:
            return Response(
                {"error": "Please login for this action"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        data["added_by_id"] = self.request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer: BaseSerializer[Director]) -> None:
        serializer.save(added_by=self.request.user)


class DirectorDetail(generics.RetrieveUpdateDestroyAPIView[Director]):
    """
    Retrieve, update or delete a Director instance.
    """

    queryset = Director.objects.all()
    serializer_class = SingleDirectorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DirectorsOrderedByLatestMovie(generics.ListAPIView[Director]):
    queryset = Director.objects.annotate(
        last_movie_release_date=Max(ExtractYear("movie__release_date"))
    ).order_by(F("last_movie_release_date").desc(nulls_last=True))
    serializer_class = DirectorSerializerWithLastReleaseDate
    pagination_class = CustomPagination


class DirectorAddMovies(generics.UpdateAPIView[Movie]):
    queryset = Movie.objects.all()
    serializer_class = MovieIdsSerializer
    permission_classes = [IsAuthenticated]

    def update(
        self, request: Request, *args: Any, **kwargs: dict[str, Any]
    ) -> Response:
        director_id = kwargs.get("pk")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie_ids: list[int] = serializer.validated_data["movie_ids"]
        Movie.objects.filter(director_id__in=movie_ids).update(director_id=director_id)
        return Response(status=status.HTTP_200_OK)
