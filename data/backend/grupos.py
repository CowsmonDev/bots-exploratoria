import datetime
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction

class ActionIniciarPlanificacion(Action):
    def name(self) -> Text:
        return "action_iniciar_planificacion"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[ Dict[Text, Any]]:
        return []

class ActionProponerFecha(Action):
    def name(self) -> Text:
        return "action_proponer_fecha"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[ Dict[Text, Any]]:
        return []