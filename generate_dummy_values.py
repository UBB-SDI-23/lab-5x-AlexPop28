import random

from faker import Faker

ROWS = 1_000_000
PRINT_FREQ = 100
ROWS_JOIN = 10_000_000
BATCH_SIZE = 1000


fake = Faker()


def get_actors() -> list[str]:
    actors = []
    for i in range(1, ROWS + 1):
        if i % PRINT_FREQ == 0:
            print(f"actor {i}")
        name = fake.name()
        name = "".join([c if c != "'" else "''" for c in name])
        alternative_name = fake.name() if fake.random_int(0, 10) == 0 else ""
        alternative_name = "".join([c if c != "'" else "''" for c in alternative_name])
        date_of_birth = str(fake.date_of_birth(minimum_age=25, maximum_age=80))
        birthplace = fake.city() + ", " + fake.country()
        birthplace = "".join([c if c != "'" else "''" for c in birthplace])
        height_in_cm = fake.random_int(120, 200)
        actor = f"({i}, '{name}', '{alternative_name}', '{date_of_birth}', '{birthplace}', {height_in_cm})"
        actors.append(actor)
    return actors


def get_directors() -> list[str]:
    return get_actors()


def get_movies() -> list[str]:
    movies = []
    for i in range(1, ROWS + 1):
        if i % PRINT_FREQ == 0:
            print(f"movie {i}")
        name = fake.catch_phrase()
        name = "".join([c if c != "'" else "''" for c in name])
        rating = round(random.uniform(0, 10), 2)
        release_date = str(fake.date_of_birth(minimum_age=1, maximum_age=20))
        length_in_minutes = fake.random_int(100, 150)
        director = fake.random_int(1, ROWS)
        movie = f"({i}, '{name}', {rating}, '{release_date}', {length_in_minutes}, {director})"
        movies.append(movie)
    return movies


def get_actormovie() -> list[str]:
    actor_movies = []
    pairs = set()
    i = 1
    while i <= ROWS_JOIN:
        if i % PRINT_FREQ == 0:
            print(f"actor_movie {i}")
        actor_id = fake.random_int(1, ROWS)
        movie_id = fake.random_int(1, ROWS)
        if (actor_id, movie_id) in pairs:
            continue
        i += 1
        pairs.add((actor_id, movie_id))
        screen_time_in_minutes = fake.random_int(5, 100)
        salary = fake.random_int(BATCH_SIZE, 100_000_000)
        actor_movie = (
            f"({i}, {screen_time_in_minutes}, {actor_id}, {movie_id}, {salary})"
        )
        actor_movies.append(actor_movie)
    return actor_movies


def main() -> None:
    with open("gen_actormovie.sql", "w") as f:
        # Insert Actors
        actors = get_actors()
        for i in range(0, len(actors), BATCH_SIZE):
            f.write(
                "INSERT INTO public.movieswebapp_actor (id, name, alternative_name, date_of_birth, birthplace, height_in_cm) VALUES "
            )
            f.write(",\n".join(actors[i : i + BATCH_SIZE]))
            f.write(";\n\n")

        # Insert Directors
        directors = get_directors()
        for i in range(0, len(directors), BATCH_SIZE):
            f.write(
                "INSERT INTO public.movieswebapp_director (id, name, alternative_name, date_of_birth, birthplace, height_in_cm) VALUES "
            )
            f.write(",\n".join(directors[i : i + BATCH_SIZE]))
            f.write(";\n\n")

        # Insert Movies
        movies = get_movies()
        for i in range(0, len(movies), BATCH_SIZE):
            f.write(
                "INSERT INTO public.movieswebapp_movie (id, name, rating, release_date, length_in_minutes, director_id) VALUES "
            )
            f.write(",\n".join(movies[i : i + BATCH_SIZE]))
            f.write(";\n\n")

        # Insert ActorMovie
        actors_movies = get_actormovie()
        for i in range(0, len(actors_movies), BATCH_SIZE):
            f.write("INSERT INTO public.movieswebapp_actormovie VALUES ")
            f.write(",\n".join(actors_movies[i : i + BATCH_SIZE]))
            f.write(";\n\n")


if __name__ == "__main__":
    main()
