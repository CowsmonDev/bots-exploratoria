from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from data.backend.modules.db_sql import PersonasDB
class ActionSaludar(Action):
	def name(self)-> Text:
		return "action_saludar"
	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		from_message = tracker.latest_message["metadata"]['message']['from']
		id_conversacion = from_message["id"]
		persona = PersonasDB()
		res = persona.existe_persona(str(id_conversacion))

		if(len(res) > 0):

			return [SlotSet('slot_nombre', res[0][2]), SlotSet('slot_profesion', res[0][3]), SlotSet('slot_id_conversacion', id_conversacion)]
		else:
			dispatcher.utter_message(response = "utter_saludar")
		return []

class ActionAhSi(Action):
	def name(self)-> Text:
		return "action_ah_si"
	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		profesion = tracker.get_slot("slot_profesion")
		nombre = tracker.get_slot("slot_nombre")
		id_conversacion = tracker.get_slot("slot_id_conversacion")

		if(id_conversacion is None):
			id_conversacion = tracker.latest_message["metadata"]["message"]["from"]["id"]
			persona = PersonasDB()
			persona.agregar_persona([str(id_conversacion), '', str(nombre), str(profesion)])
			return [SlotSet('slot_id_conversacion', id_conversacion)]

		if(profesion == "Profesor"):
			dispatcher.utter_message(text="que pasa profe?")
		else:
			if(nombre is None):
				dispatcher.utter_message(text="que pasa?")
			else: 
				dispatcher.utter_message(text=f"ahh... si que pasa {nombre}")
		return []

class ActionComoEstas(Action):
	def name(self)-> Text:
		return "action_como_estas"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		return [SlotSet('slot_tema_bot', 'robot')]
class ActionDespedir(Action):
	def name(self)-> Text:
		return "action_despedir"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		profesion = tracker.get_slot("slot_profesion")
		if(profesion == "Profesor"):
			dispatcher.utter_message(text="nos vemos profe")
		else:
			nombre = tracker.get_slot("slot_nombre")
			if(nombre is None):
				dispatcher.utter_message(text="nos vemos")
			else: dispatcher.utter_message(text=f"nos vemos {nombre}")