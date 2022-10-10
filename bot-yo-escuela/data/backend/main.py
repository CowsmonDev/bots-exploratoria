from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionAhSi(Action):
	def name(self)-> Text:
		return "action_ah_si"
	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		profesion = tracker.get_slot("slot_profesion")
		if(profesion == "Profesor"):
			dispatcher.utter_message(text="que pasa profe?")
		else:
			nombre = tracker.get_slot("slot_nombre")
			if(nombre is None):
				dispatcher.utter_message(text="que pasa?")
			else: dispatcher.utter_message(text=f"ahh... si que pasa {nombre}")
	
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

class ActionDespedir(Action):
	def name(self)-> Text:
		return "action_como_estas"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		return [SlotSet('slot_como_estas', 'nombre')]
