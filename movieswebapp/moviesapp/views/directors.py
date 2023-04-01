from django.db.models import Max
from django.db.models.functions import ExtractYear
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from movieswebapp.moviesapp.models import Director, Movie
from movieswebapp.moviesapp.serializers import (
    DirectorSerializer,
    DirectorSerializerWithLastReleaseDate,
    MovieIdsSerializer,
    SingleDirectorSerializer,
)


class DirectorList(generics.ListCreateAPIView[Director]):
    """
    List all Directors or create a new Director.
    """

    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


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


class DirectorAddMovies(APIView):
    def post(self, request: Request, director_id: int) -> Response:
        serializer = MovieIdsSerializer(data=request.data)
        if serializer.is_valid():
            movie_ids = serializer.validated_data["movie_ids"]
            Movie.objects.filter(director_id__in=movie_ids).update(
                director_id=director_id
            )
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
