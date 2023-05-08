from typing import Any

from django.db.models import F, Sum
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

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
    pagination_class = CustomPagination

    def get_serializer_class(
        self,
    ) -> type[ActorSerializer | ActorSerializerWithMovieCount]:
        if self.request.method == "GET":
            return ActorSerializerWithMovieCount
        return ActorSerializer

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

    def perform_create(self, serializer: BaseSerializer[Actor]) -> None:
        serializer.save(added_by=self.request.user)


class ActorDetail(generics.RetrieveUpdateDestroyAPIView[Actor]):
    """
    Retrieve, update or delete an Actor instance.
    """

    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


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
