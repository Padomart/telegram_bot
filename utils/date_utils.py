from datetime import datetime


def date_format(date: str) -> str:
    return date[1:] if date[0] == "0" else date

