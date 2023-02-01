from abc import ABC, abstractmethod


class ObjectSQL(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def to_string(self):
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
    @abstractmethod
    def get_object(self, persona):
        pass


class Persona(ObjectSQL):
    ID_CONVERSACION: str = "id_conversacion"
    NOMBRE: str = "nombre"
    APELLIDO: str = "apellido"
    PROFESION: str = "profesion"
    CONVERSACION_ANTERIOR: str = "conversacion_anterior"
    COLLECTION_NAME = "personas"

    def __init__(self, id_conversacion, nombre="", apellido="", profesion="", conversacion_anterior={}):
        super().__init__()
        self.__id_conversacion = id_conversacion
        self.__nombre = nombre
        self.__apellido = apellido
        self.__profesion = profesion
        self.__conversacion_anterior = conversacion_anterior

    def get_sql_keys(self):
        return {Persona.ID_CONVERSACION: self.__id_conversacion}

    def to_string(self):
        return f"{Persona.ID_CONVERSACION}: {self.__id_conversacion} \n{Persona.NOMBRE}: {self.__nombre} \n{Persona.APELLIDO}: {self.__apellido} \n{Persona.PROFESION}: {self.__profesion}\n {Persona.CONVERSACION_ANTERIOR}: {self.__conversacion_anterior}"

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

    def get_object(self, persona):
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