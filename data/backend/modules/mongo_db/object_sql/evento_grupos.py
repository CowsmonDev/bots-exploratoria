from data.backend.modules.DateTime import DateTime
from data.backend.modules.mongo_db.object_sql.object_sql import ObjectSQL


class EventoGrupos(ObjectSQL):
    ID_CONVERSACION_PROPUESTA = "id_conversacion_propuesta"
    FECHA_REUNION = "fecha_reunion"
    HORA_REUNION = "hora_reunion"
    CANTIDAD_ASISTENCIAS = "cantidad_asistencias"
    CANTIDAD_NO_ASISTENCIAS = "cantidad_no_asistencias"
    ASISTENCIAS = "asistencias"
    NO_ASISTENCIAS = "no_asistencias"

    COLLECTION_NAME = "reuniones"

    def __init__(self, id_conversacion_propuesta, fecha: DateTime, asistencias=None, no_asistencias=None) -> None:
        super().__init__()
        self.__id_conversacion_propuesta = str(id_conversacion_propuesta)
        self.__dia = f"{fecha.get_date().day}-{fecha.get_date().month}-{fecha.get_date().year}"
        self.__hora = f"{fecha.get_date().hour}:{fecha.get_date().minute}:{fecha.get_date().second}"
        self.__asitencias = [] if asistencias is None else asistencias
        self.__no_asistencias = [] if no_asistencias is None else no_asistencias
        self.__cantidad_asistencias = len(self.__asitencias)
        self.__cantidad_no_asistencias = len(self.__no_asistencias)

    def __str__(self) -> str:
        return f"{EventoGrupos.ID_CONVERSACION_PROPUESTA}: {self.__id_conversacion_propuesta}" \
               f"\n{EventoGrupos.FECHA_REUNION}: {self.__dia} {self.__hora}" \
               f"\n{EventoGrupos.ASISTENCIAS}: {self.__asitencias}" \
               f"\n{EventoGrupos.CANTIDAD_ASISTENCIAS}: {self.__cantidad_asistencias}" \
               f"\n{EventoGrupos.CANTIDAD_NO_ASISTENCIAS}: {self.__cantidad_no_asistencias}" \
               f"\n{EventoGrupos.NO_ASISTENCIAS}: {self.__no_asistencias}"

    def get_sql_keys(self):
        return {
            EventoGrupos.ID_CONVERSACION_PROPUESTA: self.__id_conversacion_propuesta,
            EventoGrupos.FECHA_REUNION: self.__dia,
            EventoGrupos.HORA_REUNION: self.__hora
        }

    def to_array(self):
        return [
            self.__id_conversacion_propuesta,
            self.__dia,
            self.__hora,
            self.__asitencias,
            self.__cantidad_asistencias,
            self.__no_asistencias,
            self.__cantidad_no_asistencias
        ]

    def to_json(self):
        return {
            EventoGrupos.ID_CONVERSACION_PROPUESTA: self.__id_conversacion_propuesta,
            EventoGrupos.FECHA_REUNION: self.__dia,
            EventoGrupos.HORA_REUNION: self.__hora,
            EventoGrupos.ASISTENCIAS: self.__asitencias,
            EventoGrupos.CANTIDAD_ASISTENCIAS: self.__cantidad_asistencias,
            EventoGrupos.NO_ASISTENCIAS: self.__no_asistencias,
            EventoGrupos.CANTIDAD_NO_ASISTENCIAS: self.__cantidad_no_asistencias
        }

    def get_collection_name(self):
        return self.COLLECTION_NAME

    @staticmethod
    def get_object(persona):
        return EventoGrupos(
            persona[EventoGrupos.ID_CONVERSACION_PROPUESTA],
            DateTime.string_to_datetime(f"{persona[EventoGrupos.FECHA_REUNION]} {persona[EventoGrupos.HORA_REUNION]}"),
            persona[EventoGrupos.ASISTENCIAS],
            persona[EventoGrupos.NO_ASISTENCIAS]
        )

    def get_asistencias(self):
        return self.__asitencias

    def get_cantidad_asistencias(self):
        return self.__cantidad_asistencias

    def get_no_asistencias(self):
        return self.__no_asistencias

    def get_cantidad_no_asistencias(self):
        return self.__cantidad_no_asistencias

    def get_dia(self):
        return self.__dia

    def get_hora(self):
        return self.__hora

    def incrementar_asistencias(self, personas_id: [str]):
        self.__asitencias.extend(personas_id)
        self.__cantidad_asistencias = len(self.__asitencias)

    def incrementar_no_asistencias(self, personas_id: [str]):
        self.__no_asistencias.extend(personas_id)
        self.__cantidad_no_asistencias = len(self.__no_asistencias)