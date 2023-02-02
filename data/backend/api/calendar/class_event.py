import datetime
import pytz


class Date:

    def __init__(self, day, month, year, hour=0, minute=0, second=1) -> None:
        super().__init__()
        self.day = day
        self.month = month
        self.year = year
        self.hour = hour
        self.minute = minute
        self.second = second

    @staticmethod
    def text_to_date(date):
        date_split = date.split('T')
        start = date_split[0].split('-')
        end = date_split[1].split('-')[0].split(':')
        return Date(int(start[2]),int(start[1]), int(start[0]), int(end[0]) - 3, int(end[1]), int(end[2].split('Z')[0]))

    def get_date(self):
        if (1 <= int(self.day) <= 31) and (1 <= int(self.month) <= 12) and (1 <= int(self.year)):
            if (0 <= int(self.hour) <= 23) and (0 <= int(self.minute) <= 59) and (0 <= int(self.second) <= 59):
                event_date = datetime.datetime.strptime(self.__str__(), '%d/%m/%Y %H:%M:%S')
                format_date = pytz.UTC.localize(event_date).isoformat()
                return format_date
        return None

    def is_valid(self) -> bool:
        return self.get_date() is not None

    @staticmethod
    def __format_date(value: int) -> str:
        return f"0{value}" if value < 10 else str(value)

    def __str__(self):
        event_date = f"{self.__format_date(self.day)}/{self.__format_date(self.month)}/{self.__format_date(self.year)}" \
                     f" {self.__format_date(self.hour)}:{self.__format_date(self.minute)}:{self.__format_date(self.second)}"
        return event_date


class EventCalendar:
    def __init__(self, summary, init_date: Date = None, end_date: Date = None) -> None:
        super().__init__()
        self.summary = summary
        self.init_date = init_date
        self.end_date = end_date

    def __str__(self) -> str:
        return f"- Summary: {self.summary} - \n    - Initial Date:{self.init_date}\n    - End Date:{self.end_date}"

    def get_init_date(self):
        return self.init_date

    def get_end_date(self):
        return self.end_date

    def to_json(self):
        return {
            'summary': self.summary,
            'start': {
                'dateTime': self.init_date.get_date()
            },
            'end': {
                'dateTime': self.end_date.get_date()
            }
        }
