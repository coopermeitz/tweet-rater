import twitter
from random import random
from os import environ

# Credentials.
api_key = environ["TWITTER_API_KEY"]
api_secret = environ["TWITTER_API_SECRET"]
access_token = environ["TWITTER_ACCESS_KEY"]
access_secret = environ["TWITTER_ACCESS_SECRET"]

def rate_tweet(tweet):
    if random.random() < 0.5:
        return "average tweet"
    else:
        return "based tweet"


api = twitter.Api(api_key, api_secret, access_token, access_secret, True)
results = api.GetSearch(
    raw_query="q=(from%3Acoopermeitz)%20-filter%3Areplies")
api = twitter.Api(api_key, api_secret, access_token, access_secret, False)
for tweet in results:
    if "RT @" not in tweet.text:
        print(tweet.text)
        
        api.PostUpdate("hey its me a bot", in_reply_to_status_id=tweet.id)




