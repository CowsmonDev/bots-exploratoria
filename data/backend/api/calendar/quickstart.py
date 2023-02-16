import datetime
import os.path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from data.backend.api.calendar.class_event import EventCalendar, Date
from google.oauth2 import service_account


class Authentication:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    FILE_PATH = '/home/agustin/Proyectos/GitProyects/bots-exploratoria/data/backend/api/calendar/authorization/bot-yo-369318-21a6102e96b7.json'

    @staticmethod
    def authorization():
        creds = service_account.Credentials.from_service_account_file(
            filename=Authentication.FILE_PATH, scopes=Authentication.SCOPES
        )
        return creds

    @staticmethod
    def get_service():
        creds = Authentication.authorization()
        try:
            service = build('calendar', 'v3', credentials=creds)
            return service
        except HttpError as error:
            print('An error occurred: %s' % error)
            return None


class Calendar:
    CALENDAR = 'd4s5ros6nltg432hsq6lmfhvlo@group.calendar.google.com'

    @staticmethod
    def insert_event_by_date(new_event: EventCalendar):
        if new_event.get_init_date and new_event.get_end_date:
            e = Authentication.get_service().events().insert(calendarId=Calendar.CALENDAR,
                                                             body=new_event.to_json()).execute()
            print(e)

    @staticmethod
    def get_events_by_date(init_date: Date):
        e = []
        if init_date.is_valid():
            events_result = Authentication.get_service().events().list(calendarId=Calendar.CALENDAR,
                                                                       timeMin=init_date.get_date(),
                                                                       timeMax=Date(init_date.day, init_date.month,
                                                                                    init_date.year, 23, 59,
                                                                                    29).get_date(),
                                                                       timeZone="UTC").execute()
            for event in events_result['items']:
                e.append(EventCalendar(event['summary'],
                                       Date.text_format_to_date(event['start']['dateTime']),
                                       Date.text_format_to_date(event['end']['dateTime'])
                                       ))
        return e

    @staticmethod
    def get_conflicts_events(evt: EventCalendar, day_check: Date):
        e = []
        if day_check.is_valid():
            events_result = Authentication.get_service().events().list(calendarId=Calendar.CALENDAR,
                                                                       timeMin=day_check.get_date(),
                                                                       timeMax=Date(day_check.day, day_check.month,
                                                                                    day_check.year, 23, 59,
                                                                                    29).get_date(),
                                                                       timeZone="UTC").execute()
            for event in events_result['items']:
                new_event = EventCalendar(event['summary'], Date.text_format_to_date(event['start']['dateTime']), Date.text_format_to_date(event['end']['dateTime']))
                if evt.conflicts_date(new_event):
                    e.append(new_event)
        return e

    """
        si la fecha inferior del que viene, es menor que que la fecha final del que esta
        y si la fecha superior del que viene, es mayor que la fecha inicial del que esta
    """

    @staticmethod
    def print_events(events):
        for event in events:
            print(event)

    @staticmethod
    def get_calendars():
        page_token = None
        calendars = []
        while True:
            service = Authentication.get_service()
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                c = calendar_list_entry
                calendars.insert(len(calendars), c)
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                return calendars
