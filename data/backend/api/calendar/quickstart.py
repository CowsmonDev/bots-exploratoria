import datetime
import os.path
import pytz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from data.backend.api.calendar.class_event import EventCalendar
from google.oauth2 import service_account

CALENDAR = 'd4s5ros6nltg432hsq6lmfhvlo@group.calendar.google.com'
SCOPES = ['https://www.googleapis.com/auth/calendar']
FILE_PATH = 'authorization/bot-yo-369318-21a6102e96b7.json'


def authorization():
    creds = service_account.Credentials.from_service_account_file(
        filename=FILE_PATH, scopes=SCOPES
    )
    return creds


def get_service():
    creds = authorization()
    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except HttpError as error:
        print('An error occurred: %s' % error)
        return None


def get_date(day: str, month: str, year: str, hour="00", minute="00", second="01"):
    event_date = f"{day}/{month}/{year}"

    if (1 <= int(day) <= 31) and (1 <= int(month) <= 12) and (1 <= int(year)):
        if (0 <= int(hour) <= 23) and (0 <= int(minute) <= 59) and (0 <= int(second) <= 59):
            init_event_date_str = f'{event_date} {hour}:{minute}:{second}'
            init_event_date = datetime.datetime.strptime(init_event_date_str, '%d/%m/%Y %H:%M:%S')
            init_event_date = pytz.UTC.localize(init_event_date).isoformat()
            return init_event_date
    return None


def insert_event_by_date(summary: str, init_date: datetime.datetime, end_date: datetime.datetime):
    if init_date and end_date:
        event = {
            'summary': summary,
            'start': {
                'dateTime': init_date
            },
            'end': {
                'dateTime': end_date
            }
        }
        e = get_service().events().insert(calendarId=CALENDAR, body=event).execute()
        print(e)


def get_events_by_date(day, month, year):
    init_event_date = get_date(day, month, year)
    if init_event_date is not None:
        end_event_date = get_date(day, month, year, "23", "59", "59")

        events_result = get_service().events().list(calendarId=CALENDAR, timeMin=init_event_date,
                                                    timeMax=end_event_date, timeZone="UTC").execute()
        e = []
        for event in events_result['items']:
            e.append(EventCalendar(event))

        events = events_result.get('items', [])
        return e, events
    return [], []


def get_calendars():
    page_token = None
    calendars = []
    while True:
        service = get_service()
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            c = calendar_list_entry
            calendars.insert(len(calendars), c)
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            return calendars

def print_calendars():
    calendars = get_calendars()
    for calendar in calendars:
        print(calendar)

e, events = get_events_by_date("07", "02", "2023")
for event in e:
    print(event)