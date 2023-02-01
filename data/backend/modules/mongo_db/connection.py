from pymongo import MongoClient

from data.backend.modules.mongo_db.object_sql import ObjectSQL


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

    def insert_one(self, object: ObjectSQL):
        collections = self.get_db()[object.get_collection_name()]
        collections.insert_one(object.to_json())

    def update_date(self, element: ObjectSQL, date: object):
        collection = self.get_db()[element.get_collection_name()]
        collection.update_one(
            {element.get_sql_keys()},
            {"$set": date},
            upsert=True
        )

    def update(self, element: ObjectSQL):
        self.update_date(element, element.to_json())

    def exist(self, element: ObjectSQL):
        collection = self.get_db()[element.get_collection_name()]
        obj = collection.find_one(element.get_sql_keys())
        obj = element.get_object(obj)
        if obj is None:
            return []
        return [obj]
