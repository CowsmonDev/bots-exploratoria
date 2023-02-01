import datetime
import os.path
import pytz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from data.backend.api.calendar.class_event import EventCalendar

CALENDAR = '2649d24a5118ef5faca07a5c392114919a476fec13eb1002b8c6cf2fc43ea895@group.calendar.google.com'
SCOPES = ['https://www.googleapis.com/auth/calendar']


def authorization():
    creds = None
    if os.path.exists('./authorization/token.json'):
        creds = Credentials.from_authorized_user_file('./authorization/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('authorization/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('./authorization/token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def authorization2():
    creds = None
    if os.path.exists('./authorization/token2.json'):
        creds = Credentials.from_authorized_user_file('./authorization/token2.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('authorization/credentials2.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('./authorization/token2.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def get_service():
    creds = authorization()
    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except HttpError as error:
        print('An error occurred: %s' % error)
        return None


def get_events_by_date(day, month, year):
    event_date = f"{day}/{month}/{year}"
    init_event_date_str = f'{event_date} 01:55:19'
    init_event_date = datetime.datetime.strptime(init_event_date_str, '%d/%m/%Y %H:%M:%S')
    init_event_date = pytz.UTC.localize(init_event_date).isoformat()

    end_event_date_str = f"{event_date} 23:59:59"
    end_event_date = datetime.datetime.strptime(end_event_date_str, '%d/%m/%Y %H:%M:%S')
    end_event_date = pytz.UTC.localize(end_event_date).isoformat()

    events_result = get_service().events().list(calendarId=CALENDAR, timeMin=init_event_date,
                                                timeMax=end_event_date, timeZone="UTC").execute()
    e = []
    for event in events_result['items']:
        e.append(EventCalendar(event))

    events = events_result.get('items', [])
    return e, events


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


# print(get_events_by_date(3, 2, 2022))
# get_calendars()
authorization2()
