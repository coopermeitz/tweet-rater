import twitter
from random import random
from os import environ
from time import sleep


# Credentials.
api_key = environ["TWITTER_API_KEY"]
api_secret = environ["TWITTER_API_SECRET"]
access_token = environ["TWITTER_ACCESS_KEY"]
access_secret = environ["TWITTER_ACCESS_SECRET"]

def rate_tweet(tweet):
    if random() < 0.5:
        return "average tweet"
    else:
        return "based tweet"

last_tweet = None
while True:
    try:
        api = twitter.Api(api_key, api_secret, access_token, access_secret, True)
        results = api.GetSearch(
        raw_query="q=(from%3Acoopermeitz)%20-filter%3Areplies", 
        count = 5)
        print([t.text for t in results])
        tweets_to_rate = []

        
        if last_tweet == None:
            last_tweet = results[0].text
            #set the most recent tweet to the last tweet then start polling again
            sleep(10)
            continue

        #find all the newest tweets in an overly complicated way
        for tweet in results:
            if tweet.text == last_tweet:
                last_tweet = tweet.text
                break
            if "RT @" not in tweet.text:
                tweets_to_rate.append(tweet)
        
        print(last_tweet, tweets_to_rate)

        #tweet the rating to all unrated tweets
        api = twitter.Api(api_key, api_secret, access_token, access_secret, False)
        for tweet in tweets_to_rate:
            rating = rate_tweet(tweet)
            api.PostUpdate(rating, in_reply_to_status_id=tweet.id)
        if len(tweets_to_rate) > 0:
            last_tweet = tweets_to_rate[0].text
        sleep(90)
    except Exception as e:
        print("restarting due to " + str(e))
        last_tweet = None
        sleep(15 * 60)    







