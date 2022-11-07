from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from data.backend.modules.estado_actual import EstadoActual
from data.backend.modules.historia import Historia
from rasa_sdk.events import SlotSet


# TODO: Estado Actual
class ActionGetAñoActual(Action):
	def name(self)-> Text:
		return "action_consultar_año"
	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		dispatcher.utter_message(text=f"uff, bueno... ahora mismo estoy en {str(EstadoActual.getAñoActual())}\n Igual deberia estar en {str(EstadoActual.getAñoTeorico())}")

class ActionGetFinalActuales(Action):
	def name(self)-> Text:
		return "action_consulta_finales_en_curso"
	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		dispatcher.utter_message(text=EstadoActual.getFinalesEnCurso())

class ActionGetCursadas(Action):
	def name(self) -> Text:
		return "action_consulta_materias_en_curso"
	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		dispatcher.utter_message(text=EstadoActual.getCursadas())

class ActionGetFinalesPendientes(Action):
	def name(self)-> Text:
		return "action_consulta_finales_pendientes"
	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		dispatcher.utter_message(text=EstadoActual.getFinalesPendientes())

class ActionEstadoMateria(Action):
	def name(self) -> Text:
		return "action_consulta_estado_materia"
	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		valor = next(tracker.get_latest_entity_values('materia_estado'), None)
		print(valor)

class ActionGetCursoTalMateria(Action):
	def name(self):
		return "action_estas_cursando"
	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		materia = next(tracker.get_latest_entity_values('materia_estado'), None)
		if(EstadoActual.estasCursando(materia)):
			dispatcher.utter_message(text=f"Si, la estoy cursando")
			return [SlotSet('slot_materia_estado', materia)]
		else:
			dispatcher.utter_message(text=f"No... {EstadoActual.getCursadas()}")

# TODO: Historia
class ActionAprobados(Action):
	def name(self)-> Text:
		return "action_consulta_aprobados"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		res = next(tracker.get_latest_entity_values('materia_final'), None)
		if (res == "cursada"):
			dispatcher.utter_message(text=Historia.getMateriasAprobadas())
		elif (res == "final" or res == "finales"):
			dispatcher.utter_message(text=Historia.getFinalesAprobados())
		else:
			print(res)
			dispatcher.utter_message(text="perdon no te entendi... hablas de finales o materias")

class ActionGetTotalMaterias(Action):
	def name(self) -> Text:
		return "action_consulta_total_materias"
	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		dispatcher.utter_message(text=Historia.getMaterias())

