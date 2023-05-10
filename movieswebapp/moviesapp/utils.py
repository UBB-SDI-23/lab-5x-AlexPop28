import os


def run_sql_script(path: str) -> None:
    os.environ["PGPASSWORD"] = os.environ["DB_PASSWORD"]
    command = os.environ["DB_CLIENT_CONNECTION_STRING"] % (path,)
    os.system(command)
    print(command)
