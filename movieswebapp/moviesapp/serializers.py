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
        fields = "__all__"


class MovieSerializerWithAverageAge(MovieSerializer):
    average_age = serializers.FloatField()

    class Meta:
        model = Movie
        fields = (
            "id",
            "name",
            "rating",
            "release_date",
            "length_in_minutes",
            "director",
            "actors",
            "average_age",
        )


class DirectorSerializer(serializers.ModelSerializer[Director]):
    def validate_height_in_cm(self, height_in_cm: int) -> int:
        if height_in_cm <= 0:
            raise serializers.ValidationError("Height should be positive.")
        return height_in_cm

    class Meta:
        model = Director
        fields = "__all__"


class SingleMovieSerializer(MovieSerializer):
    director = DirectorSerializer()


class SingleDirectorSerializer(DirectorSerializer):
    movies = serializers.SerializerMethodField("get_movies")

    def get_movies(self, obj: Director) -> list[ReturnDict]:
        return [
            MovieSerializer(movie).data
            for movie in Movie.objects.all().filter(director=obj.id)  # type: ignore
        ]

    class Meta:
        model = Director
        fields = [
            "id",
            "name",
            "alternative_name",
            "date_of_birth",
            "birthplace",
            "height_in_cm",
            "movies",
        ]


class DirectorSerializerWithLastReleaseDate(DirectorSerializer):
    last_movie_release_date = serializers.IntegerField()

    class Meta:
        model = Director
        fields = [
            "id",
            "name",
            "alternative_name",
            "date_of_birth",
            "birthplace",
            "height_in_cm",
            "last_movie_release_date",
        ]


class ActorSerializer(serializers.ModelSerializer[Actor]):
    def validate_height_in_cm(self, height_in_cm: int) -> int:
        if height_in_cm <= 0:
            raise serializers.ValidationError("Height should be positive.")
        return height_in_cm

    class Meta:
        model = Actor
        fields = "__all__"


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
