import datetime
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction
from data.backend.modules.mongo_db.connection import Connection
from data.backend.modules.mongo_db.object_sql import Persona


class ActionHumor(Action):
    def name(self) -> Text:
        return "action_humor"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        humor = tracker.get_slot("slot_humor")
        id_conversacion = tracker.get_slot("slot_id_conversacion")
        date = datetime.datetime.now()
        date = f"{date.year}/{date.month}/{date.day} {date.hour}-{date.minute}-{date.second}"

        if id_conversacion == None:
            return [FollowupAction("action_saludar")]
        else:
            Connection().update(Persona(id_conversacion), {Persona.CONVERSACION_ANTERIOR:{
                "emociones": humor,
                "fecha": date
            }})
            profesion = tracker.get_slot("slot_profesion")
            if profesion == "Compañero":
                print()
                dispatcher.utter_message(response=f"utter_{humor}_humor")
                dispatcher.utter_message(response="utter_excusa")
            else:
                dispatcher.utter_message(response="utter_por")
        return []
