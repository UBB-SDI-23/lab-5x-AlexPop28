from datetime import datetime


def check_date_in_the_past(date: str) -> bool:
    format_string = "%Y-%m-%d"
    date_date = datetime.strptime(date, format_string).date()
    return date_date < datetime.now()
