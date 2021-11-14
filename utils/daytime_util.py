from datetime import datetime


class Datetime_helper(object):
    @staticmethod
    def if_workday(day_str, separator=""):
        """
        if a day is workday
        :param day_str: string of a day
        :param separator: separator of year, month and day, default is empty
        :return: True: is workday; False: not workday
        """
        spec = "%Y" + separator + "%m" + separator + "%d"
        day = datetime.strptime(day_str, spec).date()
        # Monday == 0 ... Sunday == 6
        if day.weekday() in [0, 1, 2, 3, 4]:
            return True
        else:
            return False

    @staticmethod
    def if_weekend(day_str, separator=""):
        """
        if a day is weekend
        :param day_str: string of a day
        :param separator: separator of year, month and day, default is empty
        :return: True: is weekend; False: not weekend
        """
        spec = "%Y" + separator + "%m" + separator + "%d"
        day = datetime.strptime(day_str, spec).date()
        # Monday == 0 ... Sunday == 6
        if day.weekday() in [5, 6]:
            return True
        else:
            return False

