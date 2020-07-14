"""DB worker task."""
from worker import app
from docker_logs import get_logger
from pymongo import MongoClient

logging = get_logger("mongo_db_task")
logging.propagate = False
client = MongoClient('mongodb:27017')
db = client.tweetmldb


@app.task(bind=True, name='mongo_task', queue='mongo')
def mongo_task(self, collection):
    """Saves new tweets in mongo db."""
    logging.info(f"DB ISERTION FIRED ")
    if len(collection) > 0:
        db.posts.insert_many(convert_objects_to_dicts(collection))
    logging.info(f"DB SIZE: {db.posts.count()} ")
    # client.close()


def convert_objects_to_dicts(collection):
    """Converts objects to dictionaries."""
    results = []
    for tweet in collection:
        results.append(tweet.__dict__)
    return results
