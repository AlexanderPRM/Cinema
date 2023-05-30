class MongoManager:
    def __init__(self, client, db_name: str):
        self.client = client
        self.db = self.client[db_name]

    def create_database(self, db_name: str):
        return self.client[db_name]

    def create_collection(self, collection_name: str):
        if collection_name in self.db.list_collection_names():
            return self.get_collection(collection_name)
        return self.db.create_collection(collection_name)

    def get_collection(self, collection_name: str):
        return self.db.get_collection(collection_name)
