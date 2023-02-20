from datetime import datetime, timedelta, tzinfo, date, time
from zoneinfo import ZoneInfo

TIME_ZONE = ZoneInfo("America/Argentina/Buenos_Aires")
TIME_ZONE_UTC = ZoneInfo("UTC")


class DateTime:

    def __init__(self, new_date: datetime, zone_info=TIME_ZONE_UTC):
        self.date = new_date
        self.zone_info = zone_info
        self.format_date = "%d-%m-%Y %H:%M:%S"

    def format_date_tz(self, tz: ZoneInfo = None):
        if tz is not None:
            self.zone_info = tz
        return self.date.astimezone(tz).isoformat()

    def get_date(self):
        return self.date

    def __str__(self) -> str:
        return DateTime.datetime_to_string(self.date, self.format_date)

    @staticmethod
    def get_copy_date(old_date: datetime) -> 'DateTime':
        return DateTime(old_date)

    @staticmethod
    def date_to_datetime(new_date: date = date.min, new_time: time = time.min) -> 'DateTime':
        return DateTime(datetime.combine(new_date, new_time))

    @staticmethod
    def datetime_to_string(datetime_date, time_format="%d-%m-%Y %H:%M:%S"):
        return datetime_date.strftime(time_format)

    @staticmethod
    def string_to_datetime(datetime_str, time_format="%d-%m-%Y %H:%M:%S") -> 'DateTime':
        return DateTime(datetime.strptime(datetime_str, time_format))

    @staticmethod
    def string_date_hour_to_datetime(date_str, hours_str=None) -> 'DateTime':
        """convierte dos valores en texto pasados por parametro a un objeto de tipo Date
        Args:
            day: fecha con el formato dd-mm-yy
            hours: hora con el formato hh:mm:ss
        Returns:
            una instancia de objeto Date con esos valores introducidos
        """
        day_split = date_str.split('-')
        new_date = date(int(day_split[2]), int(day_split[1]), int(day_split[0]))
        hour = minute = second = 0
        if hours_str is not None:
            if ":" in hours_str:
                hours_split = hours_str.split(':')
                hour = int(hours_split[0])
                minute = int(hours_split[1])
                if len(hours_split) == 3:
                    second = int(hours_split[2])
            else:
                hour = int(hours_str)
        return DateTime.date_to_datetime(new_date, time(hour, minute, second))
