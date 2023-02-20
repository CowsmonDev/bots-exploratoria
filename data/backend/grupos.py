from datetime import datetime, date, timedelta
import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from datetime import datetime
from data.backend.api.calendar.class_event import EventCalendar
from data.backend.api.calendar.quickstart import Calendar
from data.backend.modules.DateTime import DateTime
from data.backend.modules.mongo_db.connection import Connection
from data.backend.modules.mongo_db.object_sql.evento_grupos import EventoGrupos

WEEK_DAYS = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']


class ActionIniciarPlanificacion(Action):
    def name(self) -> Text:
        return "action_iniciar_planificacion"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="me va")
        Calendar.get_events_week(datetime.now().date())
        return []


### realizar la accion para que pueda ingresar una fecha y una hora la mismo tiempo

class ActionProponerFecha(Action):
    def name(self) -> Text:
        return "action_proponer_fecha"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        fecha_semana = next(tracker.get_latest_entity_values('fecha_semana'), None)
        if fecha_semana in WEEK_DAYS:
            fecha = WEEK_DAYS.index(fecha_semana)
            dt = self.determinar_fecha(fecha)
            date = f"{str(dt.day)}-{str(dt.month)}-{str(dt.year)}"
            if tracker.latest_message['intent']['name'] == 'consulta_proponer_fecha_semana':
                dispatcher.utter_message(text="y a que hora?")
            return [SlotSet('slot_fecha_optativa', date)]
        else:
            dispatcher.utter_message(text="Perdon, que dia?")
        return []

    def determinar_fecha(self, fecha_semana) -> datetime:
        dt = datetime.now()
        day_week = dt.weekday()
        ### calculo cuantos dias faltan para el dia de la semana a partir de hoy (consultando si el dia ya paso o esta dentro de la semana)
        day_increment = (7 - day_week) + fecha_semana if fecha_semana - day_week < 0 else fecha_semana - day_week
        return dt + timedelta(days=day_increment)


class ActionProponerHora(Action):

    def name(self) -> Text:
        return "action_proponer_hora"

    async def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[
        Dict[Text, Any]]:

        ### genera la fecha inicial y final del evento
        hours = next(tracker.get_latest_entity_values('entity_hour'), None)
        slot_date = tracker.get_slot('slot_fecha_optativa')
        init_date = DateTime.string_date_hour_to_datetime(slot_date, hours)
        end_date = DateTime.get_copy_date(init_date.get_date() + timedelta(hours=2))

        ### revisa conflictos en calendario propio
        conflicts = Calendar.get_conflicts_events(EventCalendar("", init_date, end_date), init_date.get_date().date())
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
            personas: [str] = res[0].get_asistencias()
            if str(from_message['id']) not in personas:
                res[0].incrementar_asistencias([str(from_message['id'])])
                Connection().update(res[0])

        """ esto se puede usar para verificar si se repite la solicitud de fecha
        y el actual solicitante no estaba en la lista de atendientes """
        return [SlotSet('slot_hora_optativa', hours)]


class ActionAceptarFecha(Action):
    def name(self) -> Text:
        return "action_aceptan_fecha"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        ### obtengo la fecha y datos pertinentes sobre la reunion hablada
        from_message = str(tracker.latest_message["metadata"]['message']['from']['id'])
        from_chat = str(tracker.latest_message["metadata"]['message']['chat']['id'])
        date = tracker.get_slot('slot_fecha_optativa')
        hours = tracker.get_slot('slot_hora_optativa')

        if not (date is None or hours is None):
            init_date = DateTime.string_date_hour_to_datetime(date, hours)

            ### se asume que antes paso por "action_proponer_fecha" para no tener que confirmar si existe el evento
            evt: [EventoGrupos] = Connection().exist(EventoGrupos(from_chat, init_date))
            if len(evt) != 0:
                evt = evt[0]
                if from_message not in evt.get_asistencias():
                    evt.incrementar_asistencias([from_message])
                    if from_message in evt.get_no_asistencias():
                        evt.pop_no_asistencias(from_message)
                    Connection().update(evt)
        return []


class ActionRechazarFecha(Action):
    def name(self) -> Text:
        return "action_rechazan_fecha"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        from_message = str(tracker.latest_message["metadata"]['message']['from']['id'])
        from_chat = str(tracker.latest_message["metadata"]['message']['chat']['id'])
        date = tracker.get_slot('slot_fecha_optativa')
        hours = tracker.get_slot('slot_hora_optativa')

        if not (date is None or hours is None):
            init_date = DateTime.string_date_hour_to_datetime(date, hours)

            ### se asume que antes paso por "action_proponer_fecha" para no tener que confirmar si existe el evento
            evt: [EventoGrupos] = Connection().exist(EventoGrupos(from_chat, init_date))
            if len(evt) != 0:
                evt = evt[0]
                if from_message not in evt.get_no_asistencias():
                    evt.incrementar_no_asistencias([from_message])
                    if from_message in evt.get_asistencias():
                        evt.pop_asistencias(from_message)
                    Connection().update(evt)
        return []


class ActionEstadoFecha(Action):
    def name(self) -> Text:
        return "action_estado_fecha"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        date = tracker.get_slot('slot_fecha_optativa')
        hours = tracker.get_slot('slot_hora_optativa')
        from_chat = tracker.latest_message["metadata"]['message']['chat']
        evt: [EventoGrupos] = Connection().exist(
            EventoGrupos(from_chat['id'], DateTime.string_date_hour_to_datetime(date, hours)))

        print(json.dumps(tracker.latest_message, indent=2, ))
        if len(evt) != 0:
            evt = evt[0]
            respuesta = f"Por ahora viene: \n" \
                        f"El dia: {evt.get_dia()}\n" \
                        f"La hora: {evt.get_hora()}\n" \
                        f"hay {evt.get_cantidad_asistencias()} asistencias confirmadas y " \
                        f"{evt.get_cantidad_no_asistencias()} inasistencias"
            dispatcher.utter_message(text=respuesta)
        return []
