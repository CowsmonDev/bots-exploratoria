from pymongo import MongoClient

ID_CONVERSACION: str = "id_conversacion"
NOMBRE: str = "nombre"
APELLIDO: str = "apellido"
PROFESION: str = "profesion"
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

    def toJSON(self):
        return {
            ID_CONVERSACION: self.__id_conversacion,
            NOMBRE: self.__nombre,
            APELLIDO: self.__apellido,
            PROFESION: self.__profesion
        }

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


def existe_persona(id_conversacion):
    persona = collection.find_one({ID_CONVERSACION: int(id_conversacion)})
    if persona is not None:
        return True, Persona(
            int(persona[ID_CONVERSACION]), str(persona[NOMBRE]), "", persona[PROFESION]
        )
    return False, persona


def agregar_persona(persona: Persona):
    collection.update_one(
        {ID_CONVERSACION: persona.get_id_conversacion()},
        {"$setOnInsert": persona.toJSON()},
        upsert=True
    )

def existe_atributo(id_conversacion):
    persona = collection.find()
    return true