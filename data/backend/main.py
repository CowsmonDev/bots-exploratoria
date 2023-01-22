from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from data.backend.modules.db_mongo import Persona, existe_persona, agregar_persona, get_emociones, modificar_emociones

class ActionSaludar(Action):
    def name(self) -> Text:
        return "action_saludar"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        from_message = tracker.latest_message["metadata"]['message']['from']
        id_conversacion = from_message["id"]
        persona = existe_persona(id_conversacion)

        if persona:
            persona = persona[0]
            return [
                FollowupAction("action_ah_si"),
                SlotSet("slot_nombre", persona.get_nombre()),
                SlotSet("slot_profesion", persona.get_profesion()),
                SlotSet('slot_id_conversacion', id_conversacion)
            ]
        else:
            dispatcher.utter_message(response="utter_saludar")
        return [SlotSet("slot_profesion", "Profesion")]

class ActionAhSi(Action):
    def name(self) -> Text:
        return "action_ah_si"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        from_message = tracker.latest_message["metadata"]['message']['from']
        id_conversacion = from_message["id"]
        res = existe_persona(id_conversacion)

        nombre = str(tracker.get_slot("slot_nombre"))
        profesion = str(tracker.get_slot("slot_profesion"))

        # TODO: si no existia el usuario en la base de datos lo registra
        if not res[0]:
            dispatcher.utter_message(text="Ah... si\n")
            agregar_persona(Persona(id_conversacion, nombre , "", profesion))

        if profesion == "Profesor":
            dispatcher.utter_message(text="hola profe, que pasa?")
        else:
            if nombre == "Null":
                dispatcher.utter_message(text="hola, que pasa?")
            else:
                dispatcher.utter_message(text=f"hola {nombre}, que pasa")
            res = get_emociones(id_conversacion)
            if res:
                res = res[0]
                dispatcher.utter_message(response=f"utter_como_estas_{res['emociones']}")
                modificar_emociones(id_conversacion, {})
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
