from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from data.backend.modules.db_mongo import Persona, existe_persona, agregar_persona, existe_atributo


class ActionAfirmar(Action):
    def name(self) -> Text:
        return "action_afirmar"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return []

class ActionNegar(Action):
    def name(self) -> Text:
        return "action_negar"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return []

class ActionHumor(Action):
    def name(self) -> Text:
        return "action_humor"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        humor = tracker.get_slot("slot_humor")
        print(humor)
        id_conversacion = tracker.get_slot("slot_id_conversacion")
        if(id_conversacion == None):
            dispatcher.utter_message(response="utter_saludar")
        else:
            res = existe_atributo(id_conversacion)# TODO: establecer el codigo en mognodb.py
        return []