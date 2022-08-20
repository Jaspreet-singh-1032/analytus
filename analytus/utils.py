from typing import (
    Tuple,
    List,
    Sequence,
)
from pymongo import MongoClient
from django.conf import settings
from django.utils import timezone

from .types import Query


def dict_to_tuple_list(data: dict) -> List[Tuple[str, any]]:
    """
    convert a dict to list of tuples
    input: {"created": -1, "username": 1}
    output: [("created", -1), ("username", 1)]
    """
    return [(key, val) for key, val in data.items()]


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
        _query = query.get("query", {})
        _sorting = query.get("sorting", {})
        _sorting = dict_to_tuple_list(_sorting)
        if len(_sorting) == 0:
            _sorting = [("_id", 1)]
        cursor = collection.find(_query, **kwargs).sort(_sorting)
        return self.format_results(cursor)

    def format_results(self, cursor):
        result = []
        for i in cursor:
            del i["_id"]
            result.append(i)
        return result
