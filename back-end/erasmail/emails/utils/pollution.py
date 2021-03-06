from datetime import datetime


def year_difference(date):
    if date:
        return ((datetime.now(date.tzinfo) - date).days) / 365.25
    return 0


def emailPollution(size, date):
    # 1 mb/3 months (ADEME) <=> 14g
    # 1 mb/6 months (ADEME) <=> 16g
    # 1 mb/year (ADEME) <=> 19g

    sizeMB = size / 1000000

    # 6.57143x+12.5 is the regression equation for carbon/time
    return (6.57143*year_difference(date)+12.5)*sizeMB

def getYearlyCarbonForecast(size, date):
    # 1e+6 b/year <=> 0.29 g
    # 1 byte/year <=> 2.9e-7 g
    return 2.9e-7 * size * (year_difference(date) + 1)
