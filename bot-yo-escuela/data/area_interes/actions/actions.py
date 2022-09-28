from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

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