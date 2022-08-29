from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.db import Client
class ActionHelloWorld(Action):

	def name(self) -> Text:
		return "action_saldo"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		cliente = Client()
		print(cliente.select())
		dispatcher.utter_message(text="Hello Worl!")
		return []
