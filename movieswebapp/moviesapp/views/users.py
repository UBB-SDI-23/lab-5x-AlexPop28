from django.db.models import Count, QuerySet
from rest_framework import generics

from movieswebapp.moviesapp.models import UserProfile
from movieswebapp.moviesapp.permissions import IsAdminOrReadOnly
from movieswebapp.moviesapp.serializers import (
    UsernameRolePageSizeSerializer,
    UserProfileDetailSerializer,
)
from movieswebapp.moviesapp.views.pagination import CustomPagination


class UserList(generics.ListAPIView[UserProfile]):
    queryset = UserProfile.objects.all()
    serializer_class = UsernameRolePageSizeSerializer
    pagination_class = CustomPagination


class UserDetail(generics.RetrieveUpdateAPIView[UserProfile]):
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "user_id"

    def get_serializer_class(
        self,
    ) -> type[UserProfileDetailSerializer | UsernameRolePageSizeSerializer]:
        if self.request.method == "GET":
            return UserProfileDetailSerializer
        return UsernameRolePageSizeSerializer

    def get_queryset(self) -> QuerySet[UserProfile]:
        queryset = UserProfile.objects.all()
        if self.request.method == "GET":
            queryset = queryset.annotate(
                movie_count=Count("user__movie", distinct=True),
                actor_count=Count("user__actor", distinct=True),
                director_count=Count("user__director", distinct=True),
            )
        return queryset
