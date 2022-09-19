from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.estado_actual import EstadoActual

class ActionGetCursadas(Action):
	def name(self) -> Text:
		return "action_consulta_materias_en_curso"
	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		materias = EstadoActual.getCursadas()
		dispatcher.utter_message(text=materias)
