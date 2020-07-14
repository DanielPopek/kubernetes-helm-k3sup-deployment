"""Twitter scrapping task."""
import twint
import time
import requests
from worker import app
from embedding_task import embedding_task
from datamodel.tweet import Tweet
from docker_logs import get_logger
from registry import update_average_request_time, update_time_histogram, \
    increase_tweets_counter, update_tweets_histogram, \
    update_tweets_average_length
from datetime import datetime

logging = get_logger("tasks")
logging.propagate = False


@app.task(bind=True, name='scrap_tweets_of_user')
def scrap_tweets_from_location(self, city, limit):
    """Scraps tweets from location."""
    c = prepare_twint_request(limit, city)
    start = time.time()
    twint.run.Search(c)
    elapsed = time.time() - start
    data = twint.storage.panda.Tweets_df
    last_date = get_latest_scrap_date()
    logging.info(f"DATE BEFORE UPDATE:{last_date}")
    logging.info(f"SCRAPPED PORTION: {data.shape[0]} TIME ELAPSED:{elapsed}")
    filtered_data = filter_new_tweets(data, last_date)
    logging.info(f"NEW TWEETS ADDED: {filtered_data.shape[0]}")
    update_metrics(data, filtered_data, elapsed)
    # app.signature('embedding_task',
    # kwargs={'tweets': convert_pandas_df_to_model_collection(filtered_data)})
    embedding_task(convert_pandas_df_to_model_collection(filtered_data))
    update_latest_date(data, last_date)
    logging.info(f"DATE AFTER UPDATE:{get_latest_scrap_date()}")


def prepare_twint_request(limit, city):
    """Prepares twint request."""
    c = twint.Config()
    c.Near = city
    c.Limit = limit
    c.Hide_output = True
    c.Pandas = True
    return c


def get_latest_scrap_date():
    """Last saved date for scraping new portion."""
    r = requests.get('http://webapp:5000/since')
    return r.text


def set_latest_date(date):
    """Parses script arguments."""
    r = requests.get(f'http://webapp:5000/update/{date}')
    return r.text


def filter_new_tweets(tweets, current_time):
    """Filter tweets for new only."""
    if tweets.shape[0] > 0:
        return tweets[tweets['date'] >= current_time]
    else:
        return tweets


def update_latest_date(tweets, current_time):
    """Updates last rembered date basing on tweets."""
    if tweets.shape[0] > 0:
        date_from_tweets = get_latest_date_from_tweets(tweets)
        current = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
        tweets_date = datetime.strptime(date_from_tweets, '%Y-%m-%d %H:%M:%S')
        if tweets_date > current:
            set_latest_date(tweets_date)


def convert_pandas_df_to_model_collection(dataframe):
    """Converts pandas to data model."""
    result = []
    for index, row in dataframe.iterrows():
        tweet = Tweet(
            row['id'],
            row['conversation_id'],
            row['username'],
            row['date'],
            row['tweet'], '',
            row['nlikes'],
            row['nretweets'],
            row['nreplies'],
            row['hashtags']
        )
        result.append(tweet)
    return result


def get_latest_date_from_tweets(tweets):
    """Latest date from tweets."""
    return tweets.sort_values(by=['date'], ascending=False)['date'][0]


def update_metrics(data, filtered_data, elapsed):
    """Updates prometheus metrics."""
    update_average_request_time(data.shape[0], elapsed)
    update_time_histogram(filtered_data.shape[0], elapsed)
    increase_tweets_counter(filtered_data.shape[0])
    update_tweets_histogram(filtered_data.shape[0])
    update_tweets_average_length(filtered_data)
