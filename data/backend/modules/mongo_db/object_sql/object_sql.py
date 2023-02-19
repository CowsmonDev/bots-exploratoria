from abc import ABC, abstractmethod


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
