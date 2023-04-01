import pytest
from rest_framework.test import APIClient

from movieswebapp.moviesapp.models import Director, Movie
from movieswebapp.moviesapp.serializers import DirectorSerializer, MovieSerializer


@pytest.mark.django_db
def test_movies_list_empty(api_client: APIClient) -> None:
    response = api_client.get("/movies/").data
    assert response == []


@pytest.mark.django_db
def test_movies_list_min_rating(movies: list[Movie], api_client: APIClient) -> None:
    min_rating = 4.0
    response = api_client.get(f"/movies/?min_rating={min_rating}")
    movies = [movie for movie in movies if movie.rating >= min_rating]
    assert response.json() == MovieSerializer(movies, many=True).data


@pytest.mark.django_db
def test_directors_list_ordered_by_latest_movie(
    directors: list[Director], movies: list[Movie], api_client: APIClient
) -> None:
    def get_last_release_date(director: Director) -> int:
        return max(
            (movie.release_date for movie in movies if movie.director == director.id),  # type: ignore
            default=0,
        )

    directors.sort(key=get_last_release_date)
    response = api_client.get("/directors/by_last_release_date/")

    assert [director["id"] for director in response.json()] == [
        director["id"] for director in DirectorSerializer(directors, many=True).data
    ]
