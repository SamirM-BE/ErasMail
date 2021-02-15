from datetime import datetime

def year_difference(date):
    return ((datetime.now(date.tzinfo) - date).days) / 365.25

def emailPollution(size, date):
    return 0.0000017712 * size * year_difference(date)