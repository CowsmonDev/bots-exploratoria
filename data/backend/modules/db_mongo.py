from pymongo import MongoClient

ID_CONVERSACION: str = "id_conversacion"
NOMBRE: str = "nombre"
APELLIDO: str = "apellido"
PROFESION: str = "profesion"
CONVERSACION_ANTERIOR: str = "conversacion_anterior"
COLLECTION_NAME = "personas"


class Connection:
    def __init__(self) -> None:
        super().__init__()
        self.host = "localhost"
        self.port = "27017"
        self.db_name = "bot-yo-db"
        self.CONNECTION_STRING = f"mongodb://{self.host}:{self.port}"

    def get_db(self):
        client = MongoClient(self.CONNECTION_STRING)
        return client[self.db_name]


class Persona:

    def __init__(self, id_conversacion, nombre, apellido, profesion):
        self.__id_conversacion = int(id_conversacion)
        self.__nombre = nombre
        self.__apellido = apellido
        self.__profesion = profesion

    def to_json(self):
        return {
            ID_CONVERSACION: self.__id_conversacion,
            NOMBRE: self.__nombre,
            APELLIDO: self.__apellido,
            PROFESION: self.__profesion
        }

    def to_string(self):
        return f"ID de Conversacion: {self.__id_conversacion} \nNombre: {self.__nombre} \nApellido: {self.__apellido} \nProfesion: {self.__profesion}"

    def get_id_conversacion(self):
        return self.__id_conversacion

    def get_nombre(self):
        return self.__nombre

    def get_apellido(self):
        return self.__apellido

    def get_profesion(self):
        return self.__profesion


conn: Connection = Connection()

collection = conn.get_db()[COLLECTION_NAME]


def agregar_persona(persona: Persona):
    collection.update_one(
        {ID_CONVERSACION: persona.get_id_conversacion()},
        {"$setOnInsert": persona.to_json()},
        upsert=True
    )


def exist(busqueda: object):
    persona = collection.find_one(busqueda)
    if persona is None:
        return []
    return [persona]


def existe_persona(id_conversacion):
    persona = exist({ID_CONVERSACION: int(id_conversacion)})
    if persona:
        return [Persona(int(persona[0][ID_CONVERSACION]), str(persona[0][NOMBRE]), "", persona[0][PROFESION])]
    return []


def existe_atributo(id_conversacion):
    persona = exist({ID_CONVERSACION: int(id_conversacion), CONVERSACION_ANTERIOR: {"$exists": "true"}})
    if persona:
        return Persona(int(persona[ID_CONVERSACION]), str(persona[NOMBRE]), "", persona[PROFESION]), persona[
            CONVERSACION_ANTERIOR]
    return []