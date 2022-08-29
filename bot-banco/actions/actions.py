from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.db import Client, Cuenta
class ActionHelloWorld(Action):

	def name(self) -> Text:
		return "action_devolver_saldo"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		cuenta = Cuenta()
		print(cuenta.get_datos_cuenta("1"))
		texto = "Tu Saldo es: " + cuenta.get_datos_cuenta("1")[0][1] + "$"
		dispatcher.utter_message(text=texto)
		return []
