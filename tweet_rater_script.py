import twitter

# Standard libraries.
from random import random
from os import environ
from time import sleep
from sys import platform
from datetime import datetime

# NLP and grammar libraries.
from textblob import TextBlob
import nltk
# from language_tool_python import LanguageTool
import text2emotion as te

# Checks if the OS is Linux to determine if syslog can be used.
LINUX = "linux" in platform.lower()
if LINUX:
    import syslog

# Credentials.
API_KEY = environ["TWITTER_API_KEY"]
API_SECRET = environ["TWITTER_API_SECRET"]
ACCESS_TOKEN = environ["TWITTER_ACCESS_KEY"]
ACCESS_SECRET = environ["TWITTER_ACCESS_SECRET"]

def emotion(tweet):
    stuff = te.get_emotion(tweet.text)
    max_emotion = None
    max_score = None
    for emotion, score in stuff.items():
        if max_emotion == None or score > max_score:
            max_emotion, max_score = emotion, score
    return "%s tweet" % (
        max_emotion if type(max_emotion) == str else "ambiguous"
    )

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


def sentiment_rating(tweet):
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
        return 0, 0
    return avg_polarity, avg_subjectivity


# def correct_your(tweet):
#     """Checks that the tweet uses the correct form you your/you're.

#     :param tweet: Tweet sent by me.
#     :type tweet: twitter.Status
#     :return: Boolean describing if this tweet uses the correct form of your/you're. Will return
#     True if neither word was used.
#     :rtype: bool
#     """
#     tool = LanguageTool(language="en-US")
#     errors = tool.check(tweet.text)
#     return not any(
#         "YOUR" in match.ruleId or "YOU'RE" in match.ruleId for match in errors
#     )


# Tweet rating function.
def rate_tweet(tweet):
    """Rates a given tweet based on the features of the tweet, including
    but not limited to, the text within the tweet.

    :param tweet: Tweet sent by me.
    :type tweet: twitter.Status
    :return: String that gives the rating of the tweet.
    :rtype: str
    """
    # if not correct_your(tweet):  # Just hammer me for using bad grammar.
    #     return "one-of-you're-worst tweet"
    if is_sigma(tweet):  # Most importantly, check if this tweet is a SIGMA tweet.
        return "grindset tweet"
    if is_aggressive(tweet):  # Calm the crowd down after my aggression.
        return "needs-bob-ross tweet"
    return emotion(tweet)
    polarity, subjectivity = sentiment_rating(tweet)
    if polarity == 0:
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
    elif polarity > 0.5 and subjectivity > 0.5:
        return "probably a simp tweet"
    elif polarity > 0.5 and subjectivity <= 0.5:
        return "kinda wholesome tweet"
    elif -0.25 < polarity < 0:
        return "passive aggressive tweet"
    elif polarity < -0.25:
        return "more-negative-than-an-electron tweet"
    else:
        return "not sure how to rate this tweet"


def debug_tweet(error):
    text = "restarting due to " + str(error)
    api = twitter.Api(
        API_KEY,
        API_SECRET,
        ACCESS_TOKEN,
        ACCESS_SECRET,
        application_only_auth=False,
    )
    reply = "1338657164437688323"
    api.PostUpdate(text, in_reply_to_status_id=reply)


def main():
    last_tweet = None
    while True:
        try:
            start = datetime.now()
            api = twitter.Api(
                API_KEY,
                API_SECRET,
                ACCESS_TOKEN,
                ACCESS_SECRET,
                application_only_auth=True,
            )
            results = api.GetSearch(
                raw_query="q=(from%3Acoopermeitz)%20-filter%3Areplies"
            )
            print("Found", [t.text for t in results])
            print([emotion(t) for t in results])
            if last_tweet == None:
                last_tweet = results[0].id
                # set the most recent tweet to the last tweet then start polling again
                sleep(10)
                continue

            # Get non-retweet tweets that are newer than the last one checked.
            tweets_to_rate = [
                tweet
                for tweet in results
                if "RT @" not in tweet.text and tweet.id > last_tweet
            ]
            print("Rating", [t.text for t in tweets_to_rate])

            if len(tweets_to_rate) > 0:
                last_tweet = tweets_to_rate[0].id

            print(last_tweet)

            # Tweet the rating to all unrated tweets.
            api = twitter.Api(
                API_KEY,
                API_SECRET,
                ACCESS_TOKEN,
                ACCESS_SECRET,
                application_only_auth=False,
            )
            for tweet in tweets_to_rate:
                rating = rate_tweet(tweet)
                print(rating)
                api.PostUpdate(rating, in_reply_to_status_id=tweet.id)
                if LINUX:
                    syslog.syslog("tweeted reply to " + str(tweet.text))
            end = datetime.now()
            seconds_taken = (end - start).total_seconds()
            if seconds_taken < 90:
                # Sleep so this cycle takes at least 90 seconds total.
                sleep(90 - seconds_taken)
            last_tweet = results[0].id
            print(datetime.now())
        except Exception as e:
            debug_tweet(e)
            if LINUX:
                syslog.syslog("restarting due to " + str(e))
            print("restarting due to " + str(e))
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
