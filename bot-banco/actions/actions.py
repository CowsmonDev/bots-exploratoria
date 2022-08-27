from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.db import dataInsert
class ActionHelloWorld(Action):

	def name(self) -> Text:
		return "prueba_base"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		dataInsert("Agustin", "Crespo")
		dispatcher.utter_message(text="Hello Worl!")
		return []
