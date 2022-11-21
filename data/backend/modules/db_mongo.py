from pymongo import MongoClient


class SingletonDB(object):
    __hostname: str = 'localhost'
    __port: int = 27017

    def __init__(self):
        self.__client = MongoClient(self.__hostname, self.__port)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonDB, cls).__new__(cls)
        return cls.instance

    def getClient(self):
        return self.__client


class PersonasDB:

    def __init__(self):
        self.__singleton_db = SingletonDB()
        self.__db = self.__singleton_db.getClient().bot_rasa
        self.__collection = self.__db.personas

    def insertData(self, dato):
        self.__collection.update(
            {
                "name": dato[0]
            },
            {
                "$setOnInsert": dato
            },
        )

    def updateData(self, dato):
        self.__collection.findAndModify()

    def find(self, dato):
        res = self.__collection.find({
            "name": dato.name
        })
        return res
