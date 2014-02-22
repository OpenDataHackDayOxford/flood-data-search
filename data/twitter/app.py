import twitter
import settings
from pymongo import MongoClient, DESCENDING


def mongoify(tweet):
    """Take a dictionary representing a tweet and recursively remove
    any key/value pair in which the key contains a full stop."""
    clean_dict = {}
    for key, value in tweet.iteritems():
        if not '.' in key:
            if type(value) == dict:
                clean_dict[key] = mongoify(value)
            else:
                clean_dict[key] = value
    return clean_dict

CONSUMER_KEY = settings.consumer_key
CONSUMER_SECRET = settings.consumer_secret
ACCESS_TOKEN = settings.access_token
ACCESS_TOKEN_SECRET = settings.access_token_secret

mongo_client = MongoClient(settings.mongo_name, settings.mongo_port)

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_TOKEN_SECRET)

db = mongo_client[settings.db_name]
tweets_doc = db.tweets
try:
    # Try to fetch the most recent tweet we've seen
    last_tweet_id = db.tweets.find().sort(
        'id', DESCENDING
    ).limit(1).next()['id']
except StopIteration:
    # Our default starting tweet
    last_tweet_id = 418544514270502912

search = api.GetSearch(term='oxford flood',
                       since_id=last_tweet_id,
                       include_entities=True,
                       count=100)
# TODO: get hashtags and set number of tweets to fetch
for tweet in search:
    tweets_doc.insert(mongoify(tweet.AsDict()))
