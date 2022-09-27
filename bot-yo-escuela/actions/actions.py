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

class ActionGetAñoActual(Action):
	def name(self)-> Text:
		return "action_consultar_año"
	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		dispatcher.utter_message(text=f"uff, bueno... ahora mismo estoy en {str(EstadoActual.getAñoActual())}\n Igual deberia estar en {str(EstadoActual.getAñoTeorico())}")
class ActionGetFinalActuales(Action):
	def name(self)-> Text:
		return "action_consulta_finales"
	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		dispatcher.utter_message(text=EstadoActual.getFinales())

class ActionRamaInteres(Action):
	def name(self)-> Text:
		return "action_rama_interes"
	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		if(next(tracker.get_latest_entity_values('tiempo', "universidad"), None) != None):
			print("Presente - Universidad")
		elif(next(tracker.get_latest_entity_values('tiempo', "secundaria"), None) != None):
			print("Pasado - Secundaria")
		else:
			tiempo = next(tracker.get_latest_entity_values('tiempo', "general"), None)
			if(tiempo == "pasado"):
				print(str(tiempo))
			else:
				print(str(tiempo))