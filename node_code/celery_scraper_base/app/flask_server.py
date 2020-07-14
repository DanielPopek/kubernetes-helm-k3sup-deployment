"""Flask server for metrics and shared params."""
from flask import Flask, Response
from registry import REGISTRY
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)

if not hasattr(app, 'extensions'):
    app.extensions = {}


def get_current_time():
    """Current time."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


app.extensions['LAST_DATE'] = get_current_time()


@app.route('/mongo')
def get_all_tweets_from_db():
    """All tweets from db."""
    client = MongoClient('mongodb:27017')
    db = client.testdb
    _items = db.cars.find()
    items = [items for items in _items]
    return items


@app.route('/since')
def get_last_date():
    """Last remebered date."""
    return app.extensions['LAST_DATE']


@app.route('/update/<new_date>')
def update_last_date(new_date):
    """Updates date last date for scrapping."""
    app.extensions['LAST_DATE'] = new_date
    return app.extensions['LAST_DATE']


@app.route('/test/')
def test():
    """Method for test purposes."""
    return 'test response'


@app.route('/metrics')
def metrics():
    """Returns prometheus metrics."""
    return Response(generate_latest(REGISTRY), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    """Parses script arguments."""
    app.run(host='0.0.0.0', port=5000)
