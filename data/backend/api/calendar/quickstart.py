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
        if init_date.is_valid():
            events_result = Authentication.get_service().events().list(calendarId=Calendar.CALENDAR,
                                                                       timeMin=init_date.get_date(),
                                                                       timeMax=Date(init_date.day, init_date.month,
                                                                                    init_date.year, 23, 59,
                                                                                    29).get_date(),
                                                                       timeZone="UTC").execute()
            e = []
            for event in events_result['items']:
                e.append(EventCalendar(event['summary'],
                                       Date.text_to_date(event['start']['dateTime']),
                                       Date.text_to_date(event['end']['dateTime'])
                                       ))
            return e
        return []

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


def get():
    e = Calendar.get_events_by_date(Date(7, 2, 2023))
    Calendar.print_events(e)
