from django.db.models import Count
from rest_framework import generics

from movieswebapp.moviesapp.models import Actor
from movieswebapp.moviesapp.serializers import (
    ActorSerializer,
    ActorSerializerWithMovieCount,
)
from movieswebapp.moviesapp.views.pagination import CustomPagination


class ActorList(generics.ListCreateAPIView[Actor]):
    """
    List all Actors or create a new Actor.
    """

    queryset = Actor.objects.all().annotate(movie_count=Count("movie"))
    serializer_class = ActorSerializerWithMovieCount
    pagination_class = CustomPagination


class ActorDetail(generics.RetrieveUpdateDestroyAPIView[Actor]):
    """
    Retrieve, update or delete an Actor instance.
    """

    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
