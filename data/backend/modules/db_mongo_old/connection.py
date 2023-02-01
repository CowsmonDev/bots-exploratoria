from pymongo import MongoClient

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