import datetime
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from data.backend.modules.db_mongo import Persona, existe_persona, agregar_persona, modificar_emociones


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
            modificar_emociones(id_conversacion, {
                "emociones": humor,
                "fecha": date
            })
            profesion = tracker.get_slot("slot_profesion")
            if profesion == "Compañero":
                print()
                dispatcher.utter_message(response=f"utter_{humor}_humor")
                dispatcher.utter_message(response="utter_excusa")
            else:
                dispatcher.utter_message(response="utter_por")
        return []
