from pymongo import MongoClient
from django.conf import settings
from django.utils import timezone

from .types import Query


class MongoDBHandler:
    def __init__(self):
        client = MongoClient(settings.MONGODB_CONNECTION_STRING)
        self.db = client["analytus"]

    def insert_one(self, collection_name: str, data: dict, **kwargs):
        collection = self.db[collection_name]
        inserted = collection.insert_one(data, **kwargs)
        return inserted

    def query(self, collection_name: str, query: Query, **kwargs):
        collection = self.db[collection_name]
        filters = query.get("filters", {})
        sorting = query.get("sorting", {})
        ranges = query.get("ranges", {})
        cursor = collection.find(filters, **kwargs)
        return self.format_results(cursor)

    def format_results(self, cursor):
        result = []
        for i in cursor:
            del i["_id"]
            result.append(i)
        return result


db = MongoDBHandler()
