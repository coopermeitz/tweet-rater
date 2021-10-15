import twitter
from random import random
from os import environ
from time import sleep
import syslog

# Credentials.
API_KEY = environ["TWITTER_API_KEY"]
API_SECRET = environ["TWITTER_API_SECRET"]
ACCESS_TOKEN = environ["TWITTER_ACCESS_KEY"]
ACCESS_SECRET = environ["TWITTER_ACCESS_SECRET"]

def rate_tweet(tweet):
    if "sigma" in tweet.text.lower():
        return "grindset tweet"
    rating = random()
    if rating < 0.01:
        return "cringe tweet"
    elif rating < 0.5:
        return "average tweet"
    elif rating < 0.99:
        return "good tweet"
    else:
        return "based tweet"

def main():
    last_tweet = None
    while True:
        try:
            api = twitter.Api(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, True)
            results = None
            if last_tweet != None:
                results = api.GetSearch(
                raw_query="q=(from%3Acoopermeitz)%20-filter%3Areplies")
            else:
                results = api.GetSearch(
                raw_query="q=(from%3Acoopermeitz)%20-filter%3Areplies", 
                since_id = last_tweet)
            print([t.text for t in results])
            tweets_to_rate = []

            
            if last_tweet == None:
                last_tweet = results[0].id
                #set the most recent tweet to the last tweet then start polling again
                sleep(10)
                continue

            #find all the newest tweets in an overly complicated way
            unchanged = True
            for tweet in results:
                if tweet.id == last_tweet:
                    last_tweet = tweet.id
                    unchanged = False
                    break
                if "RT @" not in tweet.text:
                    tweets_to_rate.append(tweet)
            if len(tweets_to_rate) > 0 and unchanged:
                last_tweet = tweets_to_rate[0].id
            
            print(last_tweet, tweets_to_rate)

            #tweet the rating to all unrated tweets
            api = twitter.Api(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, False)
            for tweet in tweets_to_rate:
                rating = rate_tweet(tweet)
                api.PostUpdate(rating, in_reply_to_status_id=tweet.id)
                syslog.syslog("tweeted reply to " + str(tweet.text))
            if len(tweets_to_rate) > 0:
                last_tweet = tweets_to_rate[0].text
            sleep(90)
        except Exception as e:
            syslog.syslog("restarting due to " + str(e))
            if "rate" in str(e).lower():
                sleep(15 * 60)
            else:
                sleep(60)    


if __name__ == "__main__":
    syslog.syslog("Starting script")
    main()






