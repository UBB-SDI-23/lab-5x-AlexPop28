import random

from faker import Faker

ROWS = 1_000_000
PRINT_FREQ = 2500
ROWS_JOIN = 10_000_000
BATCH_SIZE = 1000
USERS = 10000


fake = Faker()


def fix_quotes(s: str) -> str:
    return "".join([c if c != "'" else "''" for c in s])


def get_people() -> list[str]:
    people = []
    for i in range(1, ROWS + 1):
        if i % PRINT_FREQ == 0:
            print(f"actor {i}")

        name = fix_quotes(fake.name())
        alternative_name = fix_quotes(
            fake.name() if fake.random_int(0, 10) == 0 else ""
        )
        date_of_birth = str(fake.date_of_birth(minimum_age=25, maximum_age=80))
        birthplace = fix_quotes(fake.address())
        height_in_cm = fake.random_int(120, 200)
        added_by_id = fake.random_int(1, USERS)
        person = f"({i}, '{name}', '{alternative_name}', '{date_of_birth}', '{birthplace}', {height_in_cm}, {added_by_id})"
        people.append(person)
    return people


def get_actors() -> list[str]:
    return get_people()


def get_directors() -> list[str]:
    return get_actors()


def get_movies() -> list[str]:
    movies = []
    for i in range(1, ROWS + 1):
        if i % PRINT_FREQ == 0:
            print(f"movie {i}")

        name = fix_quotes(fake.catch_phrase())
        rating = round(random.uniform(0, 10), 2)
        release_date = str(fake.date_of_birth(minimum_age=1, maximum_age=20))
        length_in_minutes = fake.random_int(100, 150)
        director = fake.random_int(1, ROWS)
        added_by_id = fake.random_int(1, USERS)
        movie = f"({i}, '{name}', {rating}, '{release_date}', {length_in_minutes}, {director}, {added_by_id})"
        movies.append(movie)
    return movies


def get_actormovie() -> list[str]:
    movie_count = ROWS_JOIN / ROWS

    actor_movies = []
    i = 1
    for actor_id in range(1, ROWS):
        if actor_id % PRINT_FREQ == 0:
            print(f"actor_movie actor {i}")
        movies = set()
        i = 0
        while i < movie_count:
            movie_id = fake.random_int(1, ROWS)
            if movie_id in movies:
                continue
            i += 1
            movies.add(movie_id)

            screen_time_in_minutes = fake.random_int(5, 100)
            salary = fake.random_int(1, 100_000_000)
            character_name = fix_quotes(fake.name())
            added_by_id = fake.random_int(1, USERS)
            actor_movie = f"({i}, {screen_time_in_minutes}, {actor_id}, {movie_id}, {salary}, '{character_name}', {added_by_id})"
            actor_movies.append(actor_movie)
    return actor_movies


def main() -> None:
    with open("gen_actors.sql", "w") as f:
        actors = get_actors()
        for i in range(0, len(actors), BATCH_SIZE):
            f.write(
                "INSERT INTO public.movieswebapp_actor (id, name, alternative_name, date_of_birth, birthplace, height_in_cm, added_by_id) VALUES "
            )
            f.write(",\n".join(actors[i : i + BATCH_SIZE]))
            f.write(";\n\n")

    with open("gen_directors.sql", "w") as f:
        directors = get_directors()
        for i in range(0, len(directors), BATCH_SIZE):
            f.write(
                "INSERT INTO public.movieswebapp_director (id, name, alternative_name, date_of_birth, birthplace, height_in_cm, added_by_id) VALUES "
            )
            f.write(",\n".join(directors[i : i + BATCH_SIZE]))
            f.write(";\n\n")

    with open("gen_movies.sql", "w") as f:
        movies = get_movies()
        for i in range(0, len(movies), BATCH_SIZE):
            f.write(
                "INSERT INTO public.movieswebapp_movie (id, name, rating, release_date, length_in_minutes, director_id, added_by_id) VALUES "
            )
            f.write(",\n".join(movies[i : i + BATCH_SIZE]))
            f.write(";\n\n")

    with open("gen_actormovie.sql", "w") as f:
        actors_movies = get_actormovie()
        for i in range(0, len(actors_movies), BATCH_SIZE):
            f.write("INSERT INTO public.movieswebapp_actormovie VALUES ")
            f.write(",\n".join(actors_movies[i : i + BATCH_SIZE]))
            f.write(";\n\n")


if __name__ == "__main__":
    main()
