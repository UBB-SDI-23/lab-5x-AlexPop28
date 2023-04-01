import pytest
from rest_framework.test import APIClient

from movieswebapp.moviesapp.models import Director, Movie


@pytest.fixture()
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
@pytest.fixture()
def directors(api_client: APIClient) -> list[Director]:
    directors = [
        Director(
            name="Director 1",
            alternative_name="Dir 1",
            date_of_birth="2000-01-01",
            birthplace="City 1",
            height_in_cm=180,
        ),
        Director(
            name="Director 2",
            alternative_name="Dir 2",
            date_of_birth="2001-02-01",
            birthplace="City 1",
            height_in_cm=185,
        ),
        Director(
            name="Director 3",
            alternative_name="Dir 3",
            date_of_birth="2001-02-02",
            birthplace="City 2",
            height_in_cm=160,
        ),
    ]

    for director in directors:
        director.save()
    return directors


@pytest.mark.django_db
@pytest.fixture()
def movies(directors: list[Director], api_client: APIClient) -> list[Movie]:
    movies = [
        Movie(
            name="Movie 1",
            rating=3.0,
            release_date="2023-03-28",
            length_in_minutes=100,
            director=directors[0],
        ),
        Movie(
            name="Movie 2",
            rating=4.0,
            release_date="2020-02-21",
            length_in_minutes=120,
            director=directors[1],
        ),
        Movie(
            name="Movie 3",
            rating=5.0,
            release_date="2005-09-02",
            length_in_minutes=96,
            director=directors[1],
        ),
    ]

    for movie in movies:
        movie.save()
    return movies
