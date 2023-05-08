import datetime
import random

from faker import Faker

ROWS = 10000
PRINT_FREQ = 1000
BATCH_SIZE = 1000
PASSWORD = "pbkdf2_sha256$600000$YroDdnnGew1msYRkM2CjRi$BP/OuN/pLGDl7ui2fQckEYfUQwZEcEg+6/1z+C3ZKBE="

fake = Faker()


def get_users() -> tuple[list[str], list[str]]:
    users = []
    profiles = []
    for i in range(1, ROWS + 1):
        if i % PRINT_FREQ == 0:
            print(f"User {i}")
        username = fake.user_name() + str(i)
        username = "".join([c if c != "'" else "''" for c in username])

        bio = fake.text()
        bio = "".join([c if c != "'" else "''" for c in bio])

        birthday = str(fake.date_of_birth(minimum_age=18, maximum_age=80))
        location = fake.address()
        location = "".join([c if c != "'" else "''" for c in location])
        gender = ["male", "female", "other"][random.randint(0, 2)]

        user = f"({i}, '{username}', '{PASSWORD}', 'F', '', '', 'T', 'F', '', '{datetime.datetime.today()}')"
        profile = f"({i}, '{i}', '{bio}', '{birthday}', '{location}', '{gender}', 'T', 'activation_code', '{datetime.datetime.now()}')"
        users.append(user)
        profiles.append(profile)
    return users, profiles


def main() -> None:
    with open("gen_users.sql", "w") as f:
        users, profiles = get_users()
        for i in range(0, len(users), BATCH_SIZE):
            f.write(
                "INSERT INTO public.auth_user (id, username, password, is_superuser, first_name, last_name, is_active, is_staff, email, date_joined) VALUES "
            )
            f.write(",\n".join(users[i : i + BATCH_SIZE]))
            f.write(";\n\n")

        for i in range(0, len(profiles), BATCH_SIZE):
            f.write(
                "INSERT INTO public.movieswebapp_userprofile (id, user_id, bio, birthday, location, gender, active, activation_code, activation_expiry_date) VALUES "
            )
            f.write(",\n".join(profiles[i : i + BATCH_SIZE]))
            f.write(";\n\n")


if __name__ == "__main__":
    main()
