from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from data.backend.modules.mongo_db.object_sql import Persona
from data.backend.modules.mongo_db.connection import Connection


class ActionSaludar(Action):
    def name(self) -> Text:
        return "action_saludar"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.latest_message["metadata"]['message']['chat']['type'] != "group":
            from_message = tracker.latest_message["metadata"]['message']['from']
            id_conversacion = from_message["id"]
            persona = Connection().exist(Persona(id_conversacion))

            if persona:
                persona = persona[0]
                persona = persona.to_json()
                return [
                    FollowupAction("action_ah_si"),
                    SlotSet("slot_nombre", persona[Persona.NOMBRE]),
                    SlotSet("slot_profesion", persona[Persona.PROFESION]),
                    SlotSet('slot_id_conversacion', id_conversacion)
                ]
            else:
                dispatcher.utter_message(response="utter_saludar")
            return [SlotSet("slot_profesion", "Profesion")]
        return []


class ActionAhSi(Action):
    def name(self) -> Text:
        return "action_ah_si"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        from_message = tracker.latest_message["metadata"]['message']['from']
        id_conversacion = from_message["id"]
        res = Connection().exist(Persona(id_conversacion))

        nombre = str(tracker.get_slot("slot_nombre"))
        profesion = str(tracker.get_slot("slot_profesion"))

        # TODO: si no existia el usuario en la base de datos lo registra
        if not res[0]:
            dispatcher.utter_message(text="Ah... si\n")
            Connection().insert_one(Persona(id_conversacion, nombre, "", profesion))

        if profesion == "Profesor":
            dispatcher.utter_message(text="hola profe, que pasa?")
        else:
            if nombre == "Null":
                dispatcher.utter_message(text="hola, que pasa?")
            else:
                dispatcher.utter_message(text=f"hola {nombre}, que pasa")

            if res[0]:
                dispatcher.utter_message(response=f"utter_como_estas_{res[0].to_json()[Persona.CONVERSACION_ANTERIOR]['emociones']}")
                Connection().update_date(Persona(id_conversacion, nombre, "", profesion))
        return [
            SlotSet("slot_profesion", profesion),
            SlotSet("slot_nombre", nombre),
            SlotSet('slot_id_conversacion', id_conversacion),
        ]


class ActionDespedir(Action):
    def name(self) -> Text:
        return "action_despedir"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        profesion = tracker.get_slot("slot_profesion")
        if profesion == "Profesor":
            dispatcher.utter_message(text="nos vemos profe")
        else:
            nombre = tracker.get_slot("slot_nombre")
            if nombre is None:
                dispatcher.utter_message(text="nos vemos")
            else:
                dispatcher.utter_message(text=f"nos vemos {nombre}")
