import os


def run_sql_script(path: str) -> None:
    from dotenv import load_dotenv

    load_dotenv()
    command = os.environ["DB_CLIENT_CONNECTION_STRING"] % (path,)
    # os.system(command)
    print(command)


if __name__ == "__main__":
    run_sql_script("/root/path")
