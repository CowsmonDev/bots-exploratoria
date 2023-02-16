import datetime
import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from datetime import datetime
from data.backend.api.calendar.class_event import EventCalendar, Date
from data.backend.api.calendar.quickstart import Calendar
from data.backend.modules.mongo_db.connection import Connection
from data.backend.modules.mongo_db.object_sql import EventoGrupos

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
            day, month, year = self.determinar_fecha(fecha)
            date = f"{str(day)}-{str(month)}-{str(year)}"
            dispatcher.utter_message(text="y a que hora?")
            return [SlotSet('slot_fecha_optativa', date)]
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


class ActionProponerHora(Action):

    def name(self) -> Text:
        return "action_proponer_hora"

    async def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[
        Dict[Text, Any]]:

        ### genera la fecha inicial y final del evento
        hours = next(tracker.get_latest_entity_values('entity_hour'), None)
        date = tracker.get_slot('slot_fecha_optativa')
        init_date = Date.text_to_date(date, hours)
        end_date = Date.copy_date(init_date)
        end_date.hour += 2

        ### revisa conflictos en calendario propio
        conflicts = Calendar.get_conflicts_events(EventCalendar("", init_date, end_date), init_date)
        participantes = []
        if len(conflicts) > 0:
            dispatcher.utter_message(response="utter_rechazar_fecha")
        else:
            dispatcher.utter_message(response="utter_aceptar_fecha")
            participantes.append("0")

        ### crea el evento para mongoDB
        from_chat = tracker.latest_message["metadata"]['message']['chat']
        from_message = tracker.latest_message["metadata"]['message']['from']

        ### revisa en mongoDB si ya se trato esta fecha antes
        res: [EventoGrupos] = Connection().exist(EventoGrupos(from_chat['id'], init_date))
        if len(res) == 0:
            participantes.append(str(from_message['id']))
            evt = EventoGrupos(from_chat['id'], init_date, participantes)
            Connection().insert_one(evt)
        else:
            ### verifica si el usuario que propuso ya esta en la lista de participantes
            personas: [str] = res[0].get_personas()
            if str(from_message['id']) not in personas:
                res[0].increment_personas([str(from_message['id'])])
                Connection().update(res[0])

        """ esto se puede usar para verificar si se repite la solicitud de fecha
        y el actual solicitante no estaba en la lista de atendientes """
        return [SlotSet('slot_hora_optativa', hours)]


class ActionAceptarFecha(Action):
    def name(self) -> Text:
        return "action_aceptan_fecha"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        ### obtengo la fecha y datos pertinentes sobre la reunion hablada
        from_message = tracker.latest_message["metadata"]['message']['from']
        from_chat = tracker.latest_message["metadata"]['message']['chat']
        date = tracker.get_slot('slot_fecha_optativa')
        hours = tracker.get_slot('slot_hora_optativa')
        if not (date is None or hours is None):
            init_date = Date.text_to_date(date, hours)

            if 'reply_to_message' in from_message:
                reply = from_message['reply_to_message']
            else:
                ### se asume que antes paso por "action_proponer_fecha" para no tener que confirmar si existe el evento
                evt: [EventoGrupos] = Connection().exist(EventoGrupos(from_chat['id'], init_date))
                evt = evt[0]
                if from_message['id'] not in evt.get_personas():
                    evt.increment_personas([str(from_message['id'])])
                    print(evt)
                    Connection().update(evt)
        return []


class ActionRechazarFecha(Action):
    def name(self) -> Text:
        return "action_rechazan_fecha"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        return []
