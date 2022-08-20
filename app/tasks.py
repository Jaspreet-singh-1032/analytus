from celery import shared_task

# utils
from analytus.utils import MongoDBHandler


@shared_task
def capture(collection_name: str, data: dict) -> None:
    """
    Write data to mongoDB
    collection_name: name of the collection
    data: data to write
    """
    db = MongoDBHandler()
    db.insert_one(collection_name, data)
