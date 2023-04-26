from django.db.models import F, Sum
from rest_framework import generics

from movieswebapp.moviesapp.models import Actor
from movieswebapp.moviesapp.serializers import (
    ActorSerializer,
    ActorSerializerWithMovieCount,
    ActorSerializerWithTotalIncome,
)
from movieswebapp.moviesapp.views.pagination import CustomPagination


class ActorList(generics.ListCreateAPIView[Actor]):
    """
    List all Actors or create a new Actor.
    """

    queryset = Actor.objects.all()
    serializer_class = ActorSerializerWithMovieCount
    pagination_class = CustomPagination


class ActorDetail(generics.RetrieveUpdateDestroyAPIView[Actor]):
    """
    Retrieve, update or delete an Actor instance.
    """

    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class ActorsOrderedByTotalIncome(generics.ListAPIView[Actor]):
    """
    Retrieve actors sorted by their total income from movies they played in.
    """

    queryset = (
        Actor.objects.all()
        .annotate(total_income=Sum("actormovie__salary_in_usd"))
        .order_by(F("total_income").desc(nulls_last=True))
    )
    serializer_class = ActorSerializerWithTotalIncome
    pagination_class = CustomPagination
