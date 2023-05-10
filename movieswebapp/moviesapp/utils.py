import os
import subprocess


def run_sql_script(path: str) -> None:
    os.environ["PGPASSWORD"] = os.environ["DB_PASSWORD"]
    sql_command = os.environ["DB_CLIENT_CONNECTION_STRING"] % (path,)
    post_command = os.environ["DB_CLIENT_CONNECTION_STRING"] % (
        "sql_scripts/post_gen.sql",
    )
    command = f"{sql_command} && {post_command}"
    subprocess.Popen(command, shell=True)
    print(command)
