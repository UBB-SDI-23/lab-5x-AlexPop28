from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from .models import Actor, ActorMovie, Director, Movie
from .validations import check_date_in_the_past


class MovieSerializer(serializers.ModelSerializer[Movie]):
    def validate_rating(self, rating: float) -> float:
        if rating < 0 or rating > 10.0:
            raise serializers.ValidationError("Rating should be between 0 and 10.")
        return rating

    def validate_release_date(self, release_date: str) -> str:
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

    def get_actor_count(self, movie: Movie) -> int:
        return ActorMovie.objects.filter(movie=movie.id).count()  # type: ignore

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

    def validate_date_of_birth(self, date_of_birth: str) -> str:
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

    def get_movie_count(self, director: Director) -> int:
        return Movie.objects.filter(director=director.id).count()  # type: ignore

    class Meta:
        model = Director
        fields = DirectorSerializer.Meta.fields + ("movie_count",)


class ActorSerializer(serializers.ModelSerializer[Actor]):
    def validate_height_in_cm(self, height_in_cm: int) -> int:
        if height_in_cm <= 0:
            raise serializers.ValidationError("Height should be positive.")
        return height_in_cm

    def validate_date_of_birth(self, date_of_birth: str) -> str:
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

    def get_movie_count(self, actor: Actor) -> int:
        return ActorMovie.objects.filter(actor=actor.id).count()  # type: ignore

    class Meta:
        model = Actor
        fields = ActorSerializer.Meta.fields + ("movie_count",)


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
        fields = "__all__"


class MovieIdsSerializer(serializers.Serializer[list[int]]):
    movie_ids = serializers.ListField(child=serializers.IntegerField())
