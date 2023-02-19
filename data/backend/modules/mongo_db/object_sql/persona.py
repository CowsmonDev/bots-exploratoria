from data.backend.modules.mongo_db.object_sql.object_sql import ObjectSQL


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
