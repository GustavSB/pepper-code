from datetime import datetime
from datetime import timedelta
"import datefinder"
import math

class TimeUtilities(object):
    """
    Class with static methods to get time in various forms and other tools.
    """

    # Gets the current time as timestamp.
    # Gets today
    @staticmethod
    def get_timestamp():
        return datetime.now()

    # Gets datetime object from timestamp string.
    @staticmethod
    def get_datetime_from_string(string):
        return datetime.strptime(string, "%Y-%m-%d %H:%M:%S.%f")

    # Gets tomorrow
    @staticmethod
    def get_tomorrow():
        return datetime.now() + timedelta(1)

    # Gets yesterday
    @staticmethod
    def get_yesterday():
        return datetime.now() - timedelta(1)

    # Gets a delta time between now and a earlier timestamp.
    @staticmethod
    def get_time_delta(then):
        now = datetime.now()
        time_delta = then - now
        seconds = time_delta.total_seconds()
        return math.sqrt(math.pow(seconds, 2))

    # Gets the current year as linguistic string.
    @staticmethod
    def get_year_string(date=None):
        if date is None:
            return datetime.now().strftime("%Y")
        else:
            return date.strftime("%Y")

    # Gets the current date as linguistic string.
    @staticmethod
    def get_date_string(date=None):
        if date is None:
            return datetime.now().strftime("%B %d")
        else:
            return date.strftime("%B %d")


    # Gets the current month as linguistic string.
    @staticmethod
    def get_month_string(date=None):
        if date is None:
            return datetime.now().strftime("%B")
        else:
            return date.strftime("%B")

    # Gets the current day as linguistic string.
    @staticmethod
    def get_day_string(date=None):
        if date is None:
            return datetime.now().strftime("%A")
        else:
            return date.strftime("%A")

    # Gets the current clock time as linguistic string.
    @staticmethod
    def get_clock_string(date=None):
        return datetime.now().strftime("%H %M")


    # Gets the time of day as linguistic string.
    @staticmethod
    def get_time_of_day():
        clock_str = str(TimeUtilities.get_clock_string())
        clock_int = int(clock_str.replace(" ", ""))
        if 0500 < clock_int and clock_int < 1200:
            return "morning"
        elif 1200 < clock_int and clock_int < 1700:
            return "afternoon"
        elif 1700 < clock_int and clock_int < 2100:
            return "evening"
        elif (2100 < clock_int and clock_int < 2400) or (0000 < clock_int and clock_int < 0500):
            return "night"

    # Finds dates in text
    @staticmethod
    def get_text_dates(text):
        dates = []
        dates_ = datefinder.find_dates(text)
        for date in dates_:
            dates.append(date)
        return dates