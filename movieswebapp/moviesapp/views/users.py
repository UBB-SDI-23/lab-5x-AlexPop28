from django.db.models import Count
from rest_framework import generics

from movieswebapp.moviesapp.models import UserProfile
from movieswebapp.moviesapp.serializers import UserProfileDetailSerializer


class UserDetail(generics.RetrieveAPIView[UserProfile]):
    queryset = UserProfile.objects.all().annotate(
        movie_count=Count("user__movie", distinct=True),
        actor_count=Count("user__actor", distinct=True),
        director_count=Count("user__director", distinct=True),
    )
    serializer_class = UserProfileDetailSerializer
    lookup_field = "user_id"
