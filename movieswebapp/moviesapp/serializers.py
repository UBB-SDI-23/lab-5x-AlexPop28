import datetime
from collections import OrderedDict
from typing import Any, cast

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from .models import Actor, ActorMovie, Director, Movie, UserProfile
from .validations import check_date_in_the_past


class MovieSerializer(serializers.ModelSerializer[Movie]):
    def validate_rating(self, rating: float) -> float:
        if rating < 0 or rating > 10.0:
            raise serializers.ValidationError("Rating should be between 0 and 10.")
        return rating

    def validate_release_date(self, release_date: datetime.date) -> datetime.date:
        if not check_date_in_the_past(release_date):
            raise serializers.ValidationError("Release date should be in the past.")
        return release_date

    class Meta:
        model = Movie
        fields = (
            "id",
            "name",
            "rating",
            "release_date",
            "length_in_minutes",
            "director",
        )


class MovieSerializerWithActorCount(MovieSerializer):
    actor_count = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_actor_count(self, movie: Movie) -> int:
        return ActorMovie.objects.filter(movie=movie.id).count()  # type: ignore

    def get_username(self, movie: Movie) -> str:
        return cast(str, movie.added_by.username)

    class Meta:
        model = Movie
        fields = MovieSerializer.Meta.fields + (
            "actor_count",
            "username",
        )


class MovieSerializerWithAverageAge(MovieSerializer):
    average_age = serializers.FloatField()

    class Meta:
        model = Movie
        fields = MovieSerializer.Meta.fields + ("average_age",)


class DirectorSerializer(serializers.ModelSerializer[Director]):
    def validate_height_in_cm(self, height_in_cm: int) -> int:
        if height_in_cm <= 0:
            raise serializers.ValidationError("Height should be positive.")
        return height_in_cm

    def validate_date_of_birth(self, date_of_birth: datetime.date) -> datetime.date:
        if not check_date_in_the_past(date_of_birth):
            raise serializers.ValidationError("Date of birth should be in the past.")
        return date_of_birth

    class Meta:
        model = Director
        fields = (
            "id",
            "name",
            "alternative_name",
            "date_of_birth",
            "birthplace",
            "height_in_cm",
        )


class SingleMovieSerializer(MovieSerializer):
    director = DirectorSerializer()


class SingleDirectorSerializer(DirectorSerializer):
    movies = serializers.SerializerMethodField("get_movies")

    def get_movies(self, obj: Director) -> ReturnDict:
        return MovieSerializer(
            Movie.objects.all().filter(director=obj.id), many=True  # type: ignore
        ).data

    class Meta:
        model = Director
        fields = DirectorSerializer.Meta.fields + ("movies",)


class DirectorSerializerWithLastReleaseDate(DirectorSerializer):
    last_movie_release_date = serializers.IntegerField()

    class Meta:
        model = Director
        fields = DirectorSerializer.Meta.fields + ("last_movie_release_date",)


class DirectorSerializerWithMovieCount(DirectorSerializer):
    movie_count = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_movie_count(self, director: Director) -> int:
        return Movie.objects.filter(director=director.id).count()  # type: ignore

    def get_username(self, director: Director) -> str:
        return cast(str, director.added_by.username)

    class Meta:
        model = Director
        fields = DirectorSerializer.Meta.fields + (
            "movie_count",
            "username",
        )


class ActorSerializer(serializers.ModelSerializer[Actor]):
    def validate_height_in_cm(self, height_in_cm: int) -> int:
        if height_in_cm <= 0:
            raise serializers.ValidationError("Height should be positive.")
        return height_in_cm

    def validate_date_of_birth(self, date_of_birth: datetime.date) -> datetime.date:
        if not check_date_in_the_past(date_of_birth):
            raise serializers.ValidationError("Date of birth should be in the past.")
        return date_of_birth

    class Meta:
        model = Actor
        fields = (
            "id",
            "name",
            "alternative_name",
            "date_of_birth",
            "birthplace",
            "height_in_cm",
        )


class ActorSerializerWithMovieCount(ActorSerializer):
    movie_count = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_movie_count(self, actor: Actor) -> int:
        return ActorMovie.objects.filter(actor=actor.id).count()  # type: ignore

    def get_username(self, actor: Actor) -> str:
        return cast(str, actor.added_by.username)

    class Meta:
        model = Actor
        fields = ActorSerializer.Meta.fields + (
            "movie_count",
            "username",
        )


class ActorSerializerWithTotalIncome(ActorSerializer):
    total_income = serializers.IntegerField()

    class Meta:
        model = Actor
        fields = ActorSerializer.Meta.fields + ("total_income",)


class ActorMovieSerializer(serializers.ModelSerializer[ActorMovie]):
    def validate_screen_time_in_minutes(self, screen_time_in_minutes: int) -> int:
        if screen_time_in_minutes <= 0:
            raise serializers.ValidationError("Screen time should be positive.")
        return screen_time_in_minutes

    class Meta:
        model = ActorMovie
        fields = (
            "actor",
            "movie",
            "screen_time_in_minutes",
            "salary_in_usd",
            "character_name",
        )


class ActorMovieSerializerWithActorName(ActorMovieSerializer):
    actor_name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_actor_name(self, actor_movie: ActorMovie) -> str:
        return cast(str, actor_movie.actor.name)

    def get_username(self, actor_movie: ActorMovie) -> str:
        return cast(str, actor_movie.added_by.username)

    class Meta:
        model = ActorMovie
        fields = ActorMovieSerializer.Meta.fields + (
            "actor_name",
            "username",
        )


class MovieIdsSerializer(serializers.Serializer[list[int]]):
    movie_ids = serializers.ListField(child=serializers.IntegerField())


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )


class UserProfileSerializer(serializers.ModelSerializer[UserProfile]):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = (
            "user",
            "bio",
            "location",
            "birthday",
            "gender",
            "activation_code",
            "activation_expiry_date",
            "active",
        )

    def create(self, validated_data: OrderedDict[str, Any]) -> UserProfile:
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile


class UserProfileDetailSerializer(serializers.ModelSerializer[UserProfile]):
    username = serializers.SerializerMethodField()
    movie_count = serializers.IntegerField()
    actor_count = serializers.IntegerField()
    director_count = serializers.IntegerField()

    def get_username(self, user_profile: UserProfile) -> str:
        return user_profile.user_id  # type: ignore

    class Meta:
        model = UserProfile
        fields = (
            "username",
            "bio",
            "location",
            "birthday",
            "gender",
            "movie_count",
            "actor_count",
            "director_count",
        )
