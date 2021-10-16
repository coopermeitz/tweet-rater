import twitter

# Standard libraries.
from random import random
from os import environ
from time import sleep
from sys import platform

# NLP libraries.
from textblob import TextBlob
import nltk

# Checks if the OS is Linux to determine if syslog can be used.
LINUX = "linux" in platform.lower()
if LINUX:
    import syslog

# Credentials.
API_KEY = environ["TWITTER_API_KEY"]
API_SECRET = environ["TWITTER_API_SECRET"]
ACCESS_TOKEN = environ["TWITTER_ACCESS_KEY"]
ACCESS_SECRET = environ["TWITTER_ACCESS_SECRET"]

# Helper functions used for the rating algorithm.
def is_sigma(tweet):
    """Tests that the tweet was written by a sigma male.

    :param tweet: Tweet sent by me.
    :type tweet: twitter.Status
    :return: Boolean where True means the tweet is a sigma tweet, and False
    means the tweet is alpha and/or beta.
    :rtype: bool
    """
    return "sigma" in tweet.text.lower()


def is_aggressive(tweet):
    """Checks to see if this tweet is an aggressive one.

    :param tweet: Tweet sent by me.
    :type tweet: twitter.Status
    :return: Boolean that describes whether or not the given tweet
    is aggressive.
    :rtype: bool
    """
    return tweet.text.isupper()


def is_extremely_negative(tweet):
    """Checks to see if the bot should be kinda tilted because I
    tweeted something negative. Uses textblob for sentiment analysis.
    Positive vibes only!

    :param tweet: Tweet sent by me.
    :type tweet: twitter.Status
    :return: Boolean describing if this tweet is too negative for the timeline.
    :rtype: bool
    """
    blob = TextBlob(tweet.text)
    avg_polarity, avg_subjectivity, n = 0, 0, 0
    for sentence in blob.sentences:
        avg_polarity += sentence.sentiment.polarity
        avg_subjectivity += sentence.sentiment.subjectivity
        n += 1
    if n > 0:
        avg_polarity /= n
        avg_subjectivity /= n
    else:
        return False
    return avg_polarity < -0.25


# Tweet rating function.
def rate_tweet(tweet):
    """Rates a given tweet based on the features of the tweet, including
    but not limited to, the text within the tweet.

    :param tweet: Tweet sent by me.
    :type tweet: twitter.Status
    :return: String that gives the rating of the tweet.
    :rtype: str
    """
    if is_sigma(tweet):  # Most importantly, check if this tweet is a SIGMA tweet.
        return "grindset tweet"
    if is_aggressive(tweet):
        return "needs-bob-ross tweet"
    if is_extremely_negative(tweet):
        return "more-negative-than-an-electron tweet"

    # Just return something at random, since I've run out of ideas to look for.
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
            results = api.GetSearch(
                raw_query="q=(from%3Acoopermeitz)%20-filter%3Areplies"
            )
            print([t.text for t in results])
            tweets_to_rate = []

            if last_tweet == None:
                last_tweet = results[0].id
                # set the most recent tweet to the last tweet then start polling again
                sleep(10)
                continue

            # find all the newest tweets in an overly complicated way
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

            # tweet the rating to all unrated tweets
            api = twitter.Api(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, False)
            for tweet in tweets_to_rate:
                rating = rate_tweet(tweet)
                print(rating)
                api.PostUpdate(rating, in_reply_to_status_id=tweet.id)
                if LINUX:
                    syslog.syslog("tweeted reply to " + str(tweet.text))
            if len(tweets_to_rate) > 0:
                last_tweet = tweets_to_rate[0].id
            sleep(90)
        except Exception as e:
            if LINUX:
                syslog.syslog("restarting due to " + str(e))
            if "rate" in str(e).lower():
                sleep(15 * 60)
            else:
                sleep(60)


if __name__ == "__main__":
    if LINUX:
        syslog.syslog("Starting script")
    nltk_pkgs = ["brown", "punkt"]
    for label in nltk_pkgs:
        nltk.download(label)
    main()
