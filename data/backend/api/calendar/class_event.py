from datetime import datetime
from zoneinfo import ZoneInfo
from data.backend.modules.DateTime import DateTime


def to_compare(date_1, date_2):
    if date_1.year == date_2.year:
        if date_1.month == date_2.month:
            if date_1.day == date_2.day:
                if date_1.hour == date_2.hour:
                    if date_1.minute == date_2.minute:
                        if date_1.second == date_2.second:
                            return True, True
                        return False, date_1.second < date_2.second
                    return False, date_1.minute < date_2.minute
                return False, date_1.hour < date_2.hour
            return False, date_1.day < date_2.day
        return False, date_1.month < date_2.month
    return False, date_1.year < date_2.year


class EventCalendar:
    def __init__(self, summary, init_date: DateTime = None, end_date: DateTime = None) -> None:
        super().__init__()
        self.summary = summary
        self.init_date: DateTime = init_date
        self.end_date: DateTime = end_date

    def __str__(self) -> str:
        return f"- Summary: {self.summary} - \n    - Initial Date:{self.init_date}\n    - End Date:{self.end_date}"

    def get_init_date(self) -> DateTime:
        return self.init_date

    def get_end_date(self) -> DateTime:
        return self.end_date

    def to_json(self):
        return {
            'summary': self.summary,
            'start': {
                'dateTime': self.init_date.__str__()
            },
            'end': {
                'dateTime': self.end_date.__str__()
            }
        }

    def conflicts_date(self, evt: 'EventCalendar'):
        equals_init, less_init = to_compare(self.get_init_date().get_date(), evt.get_init_date().get_date())
        equals_end, less_end = to_compare(self.end_date.get_date(), evt.get_end_date().get_date())
        if not (equals_init or equals_end):
            return less_init and not less_end
        return True
