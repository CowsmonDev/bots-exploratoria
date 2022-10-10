from os import link
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionRamaInteres(Action):
	def name(self)-> Text:
		return "action_rama_interes"
	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		if(next(tracker.get_latest_entity_values('tiempo', "universidad"), None) != None):
			dispatcher.utter_message(text="uff, bueno. me he interesado por un poco de queda cosa... he estado en haciendo aplicaciones de escritorio, web, he tenido mi interaccion con juegos, y con algoritmos complejos...\nahora mismo estoy trabajando con un bot. (espero que resulte)")
		elif(next(tracker.get_latest_entity_values('tiempo', "secundaria"), None) != None):
			dispatcher.utter_message(text="En la secundaria, en su momento (hoy parece lejano) me interesaba bastante lo que era la robotica")
			print("Pasado - Secundaria")
		else:
			tiempo = next(tracker.get_latest_entity_values('tiempo', "general"), None)
			if(tiempo == "pasado"):
				dispatcher.utter_message(text="A un nivel general, me interesaba cualquier cosa nueva... cualquier cosa que aprendiera y diera cuerda a mi mente :)")
			elif(tiempo == "presente"):
				dispatcher.utter_message(text="Ahora mismo, estoy enfocandome en la conexion entre diferentes tecnologias. como estas tecnologias se conectan a traves de mensajes... Algo asi como un FullStack.")

class ActionProyectoAparte(Action):
	def name(self)-> Text:
		return "action_proyecto_aparte"
	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		if(next(tracker.get_latest_entity_values('tiempo', "secundaria"), None) != None):
			dispatcher.utter_message(text="En su momento no trabajaba con muchos proyectos")
		else:
			tiempo = next(tracker.get_latest_entity_values('tiempo', "general"), None)
			if(tiempo == "pasado"):
				dispatcher.utter_message(text="recien tarde en la secundaria (ultimo año) recien estaba empezando mi primer proyecto. un tanto ambicioso, llamado MetricPoint.... se suponia que iba a ser un programa de administracion para el negocio de mi tia (empresa de prestamos y seguros automovilisticos)\n este proyeto lo utilizo hoy como proyecto inicial cuando quiero probar una tecnologia nueva, ya que este fue tan grande y ambicioso que toco un poco de cada cosa. por lo que aprendo bastante")
			elif(tiempo == "presente"):
				dispatcher.utter_message(text="hoy en dia estoy adaptando el proyecto en Java a Electron, un Framework basado en JavaScript de forma de poder realizar un proyecto mas mantenible con recursos limitados... ademas, asi practico nuevas tecnologias con un proyecto bastante completo")