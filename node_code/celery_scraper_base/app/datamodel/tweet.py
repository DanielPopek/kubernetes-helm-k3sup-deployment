"""Tweet data model."""


class Tweet:
    """Tweet DTO."""

    def __init__(self, id, conversation_id, author, date,
                 text, embedding, likes, retweets,
                 replies, hashtags):
        """Fields saved in db."""
        self.tweet_id = id
        self.conversation_id = conversation_id
        self.author = author
        self.date = date
        self.text = text
        self.embedding = embedding
        self.likes = likes
        self.retweets = retweets
        self.replies = replies
        self.hashatags = hashtags
