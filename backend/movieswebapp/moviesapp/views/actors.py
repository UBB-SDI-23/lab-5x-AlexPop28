from rest_framework import generics

from movieswebapp.moviesapp.models import Actor
from movieswebapp.moviesapp.serializers import ActorSerializer


class ActorList(generics.ListCreateAPIView[Actor]):
    """
    List all Actors or create a new Actor.
    """

    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class ActorDetail(generics.RetrieveUpdateDestroyAPIView[Actor]):
    """
    Retrieve, update or delete an Actor instance.
    """

    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
