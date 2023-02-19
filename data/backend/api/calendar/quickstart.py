import json
from datetime import datetime, timedelta, date, time
import os.path
from typing import Any
from zoneinfo import ZoneInfo

import pytz as pytz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from data.backend.api.calendar.class_event import EventCalendar
from google.oauth2 import service_account

from data.backend.modules.DateTime import DateTime


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
    def get_events(calendar_id, init_date: DateTime, end_date: DateTime, time_zone):
        events_result = Authentication.get_service().events().list(calendarId=calendar_id,
                                                                   timeMin=init_date.format_date_tz(),
                                                                   timeMax=end_date.format_date_tz(),
                                                                   timeZone=time_zone).execute()
        return events_result

    @staticmethod
    def get_events_by_date(date_search: date):
        e = []
        init_date = DateTime(datetime(date_search.year, date_search.month, date_search.day, 0, 0, 1))
        end_date = DateTime(datetime(date_search.year, date_search.month, date_search.day, 23, 59, 29))

        events_result = Calendar.get_events(Calendar.CALENDAR, init_date, end_date, "UTC")

        for event in events_result['items']:
            e.append(EventCalendar(event['summary'],
                                   DateTime.string_to_datetime(event['start']['dateTime'], "%Y-%m-%dT%H:%M:%Sz"),
                                   DateTime.string_to_datetime(event['end']['dateTime'], "%Y-%m-%dT%H:%M:%Sz")
                                   ))
        return e

    @staticmethod
    def get_conflicts_events(evt: EventCalendar, day_check: date):
        e = []
        init_date = DateTime.date_to_datetime(day_check)
        end_date = DateTime.date_to_datetime(day_check, time.max)

        events_result = Calendar.get_events(Calendar.CALENDAR, init_date, end_date, "UTC")

        for event in events_result['items']:
            new_event = EventCalendar(
                event['summary'],
                DateTime.string_to_datetime(event['start']['dateTime'], "%Y-%m-%dT%H:%M:%Sz"),
                DateTime.string_to_datetime(event['end']['dateTime'], "%Y-%m-%dT%H:%M:%Sz")
            )
            if evt.conflicts_date(new_event):
                e.append(new_event)
        return e

    @staticmethod
    def get_events_week(date_now: date):
        e = []
        init_date = DateTime.date_to_datetime(date_now)
        end_date = DateTime.date_to_datetime((date_now + timedelta(days=7)), time.max)

        events_result = Calendar.get_events(Calendar.CALENDAR, init_date, end_date, "UTC")

        for event in events_result['items']:
            e.append(EventCalendar(event['summary'],
                                   DateTime.string_to_datetime(event['start']['dateTime'], "%Y-%m-%dT%H:%M:%Sz"),
                                   DateTime.string_to_datetime(event['end']['dateTime'], "%Y-%m-%dT%H:%M:%Sz")
                                   ))
        return e

    """
        si la fecha inferior del que viene, es menor que que la fecha final del que esta
        y si la fecha superior del que viene, es mayor que la fecha inicial del que esta
    """

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

    @staticmethod
    def insert_event_by_date(new_event: EventCalendar):
        if new_event.get_init_date and new_event.get_end_date:
            e = Authentication.get_service().events().insert(calendarId=Calendar.CALENDAR,
                                                             body=new_event.to_json()).execute()
            print(e)
