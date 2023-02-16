from abc import ABC, abstractmethod
from data.backend.api.calendar.class_event import Date


class ObjectSQL(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def get_sql_keys(self):
        pass

    @abstractmethod
    def to_array(self):
        pass

    @abstractmethod
    def to_json(self):
        pass

    @abstractmethod
    def get_collection_name(self):
        pass

    @staticmethod
    @abstractmethod
    def get_object(persona):
        pass


class Persona(ObjectSQL):
    ID_CONVERSACION: str = "id_conversacion"
    NOMBRE: str = "nombre"
    APELLIDO: str = "apellido"
    PROFESION: str = "profesion"
    CONVERSACION_ANTERIOR: str = "conversacion_anterior"
    COLLECTION_NAME = "personas"

    def __init__(self, id_conversacion, nombre="", apellido="", profesion="", conversacion_anterior=None):
        super().__init__()
        if conversacion_anterior is None:
            conversacion_anterior = {}
        self.__id_conversacion = id_conversacion
        self.__nombre = nombre
        self.__apellido = apellido
        self.__profesion = profesion
        self.__conversacion_anterior = conversacion_anterior

    def get_sql_keys(self):
        return {Persona.ID_CONVERSACION: self.__id_conversacion}

    def __str__(self) -> str:
        return f"{Persona.ID_CONVERSACION}: {self.__id_conversacion} \n{Persona.NOMBRE}: {self.__nombre} \n{Persona.APELLIDO}: {self.__apellido} \n{Persona.PROFESION}: {self.__profesion}\n{Persona.CONVERSACION_ANTERIOR}: {self.__conversacion_anterior}"

    def to_array(self):
        return [self.__id_conversacion, self.__nombre, self.__apellido, self.__profesion, self.__conversacion_anterior]

    def to_json(self):
        return {
            Persona.ID_CONVERSACION: self.__id_conversacion,
            Persona.NOMBRE: self.__nombre,
            Persona.APELLIDO: self.__apellido,
            Persona.PROFESION: self.__profesion,
            Persona.CONVERSACION_ANTERIOR: self.__conversacion_anterior
        }

    def get_collection_name(self):
        return self.COLLECTION_NAME

    @staticmethod
    def get_object(persona):
        if persona is not None:
            p = Persona(
                int(persona[Persona.ID_CONVERSACION]),
                str(persona[Persona.NOMBRE]),
                "",
                persona[Persona.PROFESION],
                persona[Persona.CONVERSACION_ANTERIOR]
            )
            return p
        return persona


class EventoGrupos(ObjectSQL):
    ID_CONVERSACION_PROPUESTA = "id_conversacion_propuesta"
    FECHA_REUNION = "fecha_reunion"
    HORA_REUNION = "hora_reunion"
    CANTIDAD_ASISTENCIAS = "cantidad_asistencias"
    PERSONAS = "personas"
    COLLECTION_NAME = "reuniones"

    def __init__(self, id_conversacion_propuesta, fecha: Date, personas=None) -> None:
        super().__init__()
        self.__id_conversacion_propuesta = str(id_conversacion_propuesta)
        self.__dia = f"{fecha.day}-{fecha.month}-{fecha.year}"
        self.__hora = f"{fecha.hour}:{fecha.minute}:{fecha.second}"
        self.__personas = personas if personas is not None else []
        self.__cantidad_asistencias = len(self.__personas)

    def __str__(self) -> str:
        return f"{EventoGrupos.ID_CONVERSACION_PROPUESTA}: {self.__id_conversacion_propuesta}\n{EventoGrupos.FECHA_REUNION}: {self.__dia} {self.__hora}\n{EventoGrupos.CANTIDAD_ASISTENCIAS}: {self.__cantidad_asistencias}\n{EventoGrupos.PERSONAS}: {self.__personas}"

    def get_sql_keys(self):
        return {EventoGrupos.ID_CONVERSACION_PROPUESTA: self.__id_conversacion_propuesta, EventoGrupos.FECHA_REUNION: self.__dia, EventoGrupos.HORA_REUNION: self.__hora}

    def to_array(self):
        return [self.__id_conversacion_propuesta, self.__dia, self.__hora, self.__cantidad_asistencias, self.__personas]

    def to_json(self):
        return {EventoGrupos.ID_CONVERSACION_PROPUESTA: self.__id_conversacion_propuesta,
                EventoGrupos.FECHA_REUNION: self.__dia,
                EventoGrupos.HORA_REUNION: self.__hora,
                EventoGrupos.CANTIDAD_ASISTENCIAS: self.__cantidad_asistencias, EventoGrupos.PERSONAS: self.__personas}

    def get_collection_name(self):
        return self.COLLECTION_NAME

    @staticmethod
    def get_object(persona):
        return EventoGrupos(
            persona[EventoGrupos.ID_CONVERSACION_PROPUESTA],
            Date.text_to_date(persona[EventoGrupos.FECHA_REUNION], persona[EventoGrupos.HORA_REUNION]),
            persona[EventoGrupos.PERSONAS]
        )

    def get_personas(self):
        return self.__personas

    def get_cantidad_asistencias(self):
        return self.__cantidad_asistencias

    def increment_personas(self, personas_id: [str]):
        self.__personas.extend(personas_id)
        self.__cantidad_asistencias = len(self.__personas)
