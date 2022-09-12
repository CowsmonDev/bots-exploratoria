from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionHelloWorld(Action):
	def name(self) -> Text:
		return "action_nombre"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		retorno = next(tracker.get_latest_entity_values('nombre'), None)
		print(retorno)
		dispatcher.utter_message(text="Hello World!")

		return []
