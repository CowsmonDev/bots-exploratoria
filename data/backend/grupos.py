import datetime
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from datetime import datetime
from data.backend.api.calendar.class_event import EventCalendar
from data.backend.api.calendar.quickstart import get

WEEK_DAYS = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']


class ActionIniciarPlanificacion(Action):
    def name(self) -> Text:
        return "action_iniciar_planificacion"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="me va")
        return []


class ActionProponerFecha(Action):
    def name(self) -> Text:
        return "action_proponer_fecha"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        fecha_semana = next(tracker.get_latest_entity_values('fecha_semana'), None)
        if fecha_semana in WEEK_DAYS:
            fecha = WEEK_DAYS.index(fecha_semana)
            dispatcher.utter_message(fecha_semana)
            day, month, year = self.determinar_fecha(fecha)
            get()
            print(f"dia: {day} \nMes: {month} \naño: {year}")
        else:
            dispatcher.utter_message(text="Perdon, que dia?")
        return []

    def determinar_fecha(self, fecha_semana):
        dt = datetime.now()
        day_week = dt.weekday()

        day = dt.day
        month = dt.month
        year = dt.year

        day = (day + (7 - day_week) + fecha_semana) if (fecha_semana - day_week < 0) \
            else day + (fecha_semana - day_week)

        if day > 31:
            day -= 31
            month += 1
            if month > 12:
                month -= 12
                year += 1
        return day, month, year


class ActionAceptarFecha(Action):
    def name(self) -> Text:
        return "action_aceptar_fecha"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        return []


class ActionRechazarFecha(Action):
    def name(self) -> Text:
        return "action_rechazar_fecha"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        return []
