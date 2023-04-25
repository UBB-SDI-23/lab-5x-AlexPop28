from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from .models import Actor, ActorMovie, Director, Movie


class MovieSerializer(serializers.ModelSerializer[Movie]):
    def validate_rating(self, rating: float) -> float:
        if rating < 0 or rating > 10.0:
            raise serializers.ValidationError("Rating should be between 0 and 10.")
        return rating

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
    actor_count = serializers.IntegerField(required=False)

    class Meta:
        model = Movie
        fields = MovieSerializer.Meta.fields + ("actor_count",)


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
    movie_count = serializers.IntegerField()

    class Meta:
        model = Director
        fields = DirectorSerializer.Meta.fields + ("movie_count",)


class ActorSerializer(serializers.ModelSerializer[Actor]):
    def validate_height_in_cm(self, height_in_cm: int) -> int:
        if height_in_cm <= 0:
            raise serializers.ValidationError("Height should be positive.")
        return height_in_cm

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
    movie_count = serializers.IntegerField(required=False)

    class Meta:
        model = Actor
        fields = ActorSerializer.Meta.fields + ("movie_count",)


class ActorMovieSerializer(serializers.ModelSerializer[ActorMovie]):
    def validate_screen_time_in_minutes(self, screen_time_in_minutes: int) -> int:
        if screen_time_in_minutes <= 0:
            raise serializers.ValidationError("Screen time should be positive.")
        return screen_time_in_minutes

    class Meta:
        model = ActorMovie
        fields = "__all__"


class MovieIdsSerializer(serializers.Serializer[list[int]]):
    movie_ids = serializers.ListField(child=serializers.IntegerField())
