"""Test worker task. Will be removed."""
import requests
from worker import app
from docker_logs import get_logger

logging = get_logger("time_log_task")
logging.propagate = False


@app.task(bind=True, name='time_task', queue='time')
def scrap_tweets_from_location(self):
    """Logs time."""
    r = requests.get('http://webapp:5000/since')
    logging.info(f"CURRENT TIME {r.text} ")
