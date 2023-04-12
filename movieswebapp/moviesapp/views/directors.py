from typing import Any

from django.db.models import Max, QuerySet
from django.db.models.functions import ExtractYear
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from movieswebapp.moviesapp.models import Director, Movie
from movieswebapp.moviesapp.serializers import (
    DirectorSerializer,
    DirectorSerializerWithLastReleaseDate,
    MovieIdsSerializer,
    SingleDirectorSerializer,
)
from movieswebapp.moviesapp.views.pagination import CustomPagination


class DirectorList(generics.ListCreateAPIView[Director]):
    """
    List all Directors or create a new Director.
    """

    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    pagination_class = CustomPagination

    def get_queryset(self) -> QuerySet[Director]:
        name = self.request.query_params.get("name")
        queryset = Director.objects.all()
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class DirectorDetail(generics.RetrieveUpdateDestroyAPIView[Director]):
    """
    Retrieve, update or delete a Director instance.
    """

    queryset = Director.objects.all()
    serializer_class = SingleDirectorSerializer


class DirectorsOrderedByLatestMovie(generics.ListAPIView[Director]):
    queryset = Director.objects.annotate(
        last_movie_release_date=Max(ExtractYear("movie__release_date"))
    ).order_by("-last_movie_release_date")
    serializer_class = DirectorSerializerWithLastReleaseDate
    pagination_class = CustomPagination


class DirectorAddMovies(generics.UpdateAPIView[Movie]):
    queryset = Movie.objects.all()
    serializer_class = MovieIdsSerializer

    def update(
        self, request: Request, *args: Any, **kwargs: dict[str, Any]
    ) -> Response:
        director_id = kwargs.get("pk")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie_ids: list[int] = serializer.validated_data["movie_ids"]
        Movie.objects.filter(director_id__in=movie_ids).update(director_id=director_id)
        return Response(status=status.HTTP_200_OK)
