from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from data.backend.modules.db_mongo import Persona, existe_persona, agregar_persona


class ActionSaludar(Action):
    def name(self) -> Text:
        return "action_saludar"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        from_message = tracker.latest_message["metadata"]['message']['from']
        id_conversacion = from_message["id"]
        res = existe_persona(id_conversacion)
        print(res[0])
        if res[0]:
            res = res[1]
            print(res.get_nombre())
            return [
                FollowupAction("action_ah_si"),
                SlotSet("slot_nombre", res.get_nombre()),
                SlotSet("slot_profesion", res.get_profesion()),
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

        nombre = tracker.get_slot("slot_nombre")
        profesion = tracker.get_slot("slot_profesion")

        print("Slot Nombre: ", tracker.get_slot('slot_nombre'))
        print("Slot Profesion: ", tracker.get_slot('slot_profesion'))

        # TODO: si no existia el usuario en la base de datos lo registra
        if not res[0]:
            dispatcher.utter_message(text="Ah... si\n")
            agregar_persona(Persona(id_conversacion, "Agustin" , "", profesion))

        if profesion == "Profesor":
            dispatcher.utter_message(text="hola profe, que pasa?")
        else:
            if nombre == "Null":
                dispatcher.utter_message(text="hola, que pasa?")
            else:
                dispatcher.utter_message(text=f"hola {nombre}, que pasa")
        return [

            SlotSet("slot_profesion", profesion),
            SlotSet("slot_nombre", nombre),
            SlotSet('slot_id_conversacion', id_conversacion),
        ]


class ActionComoEstas(Action):
    def name(self) -> Text:
        return "action_como_estas"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet('slot_tema_bot', 'robot')]


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
