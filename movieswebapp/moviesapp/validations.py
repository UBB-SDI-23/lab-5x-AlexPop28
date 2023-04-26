import datetime


def check_date_in_the_past(date: datetime.date) -> bool:
    return date < datetime.datetime.now().date()
