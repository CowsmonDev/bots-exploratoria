# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from swiplserver import PrologMQI, PrologThread

class ActionConsultaMaterias(Action):
	def name(self) -> Text:
		return "action_consulta_materias"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		year = next(tracker.get_latest_entity_values('materias'), None)

		if(year != None):
			with PrologMQI(port=8000) as mqi:
				with mqi.create_thread() as prolog_thread:
					prolog_thread.query_async("consult('~/GitHub/bots-exploratoria/bot-comisiones/actions/comisiones.pl')", find_all=False)
					prolog_thread.query_async(f"materia(M,{year},Y,Z)", find_all=True)
					result = prolog_thread.query_async_result()
					impresion = "Tu Tienes disponibles las siguientes materias:\n"
					for x in result:
						impresion += f"{x['M']} - {year} - {x['Y']} - {x['Z']}\n"
					dispatcher.utter_message(text=impresion)
		return []
class ActioncomisionesMaterias(Action):
	def name(self) -> Text:
		return "action_comisiones_materias"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		with PrologMQI(port=8000) as mqi:
			with mqi.create_thread() as prolog_thread:
				prolog_thread.query_async("consult('~/GitHub/bots-exploratoria/bot-comisiones/actions/comisiones.pl')", find_all=False)
				prolog_thread.query_async(f"materia(M,X,Y,Z)", find_all=True)
				result = prolog_thread.query_async_result()
				for x in result:
					print(x['M'], " - ", x['X'], " - ", x['Y'], " - ", x['Z'])
		return []
