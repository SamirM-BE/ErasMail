from datetime import datetime


def year_difference(date):
    if date:
        return ((datetime.now(date.tzinfo) - date).days) / 365.25
    return 0


def emailPollution(size, date):
    return 0.0000017712 * size * (year_difference(date) + 1)
