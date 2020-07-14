"""Embedding worker."""
from worker import app
from docker_logs import get_logger
from pymagnitude import Magnitude
import gensim
import numpy as np
from mongo_task import mongo_task

logging = get_logger("embedding_task")
logging.propagate = False


def preproces_text(text):
    """Text splitted to tokens."""
    return gensim.utils.simple_preprocess(text)


def get_sentences_representation(vectors, splitted_sentence):
    """Counts average embedding."""
    length = 0
    av_sum = np.zeros(shape=(100,))
    for i in range(len(splitted_sentence)):
        if splitted_sentence[i] in vectors:
            av_sum = av_sum + vectors.query(splitted_sentence[i])
            length += 1
    if length > 0:
        av_sum = av_sum / length
    return av_sum


def get_text_embedding(vectors, text):
    """Gets text embedding."""
    return get_sentences_representation(vectors, preproces_text(text)).tolist()


@app.task(bind=True, name='embedding_task', queue='embedding')
def embedding_task(self, tweets):
    """Embedding task."""
    logging.info(f"DATAFRAME PASSED FOR EMBEDDING SIZE {len(tweets)} ")
    vectors = Magnitude("glove_vectors/glove.6B.100d.magnitude")
    for tweet in tweets:
        tweet.embedding = get_text_embedding(vectors, tweet.text)
    mongo_task(tweets)
    return tweets
