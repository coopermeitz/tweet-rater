# tweet-rater
A bot that rates my tweets. Pretty dumb

It runs on an Amazon EC2 instance in the cloud.

If you want to make it rate smartly, create an issue or a pull request.

If you want to make me happy, follow me on Twitter, [@coopermeitz](https://twitter.com/coopermeitz).
## How it works
#### API Access and Polling
I got access to the Twitter API's from the [Twitter for Developers](https://developer.twitter.com/en) website. This site gives credentials for the app to run, and for the app to tweet on my behalf.
Then, the script uses those credentials to poll for my tweets every 90 seconds. If it finds a new one, it runs the
`rate_tweet()` algorithm on the new tweet(s) and determines a rating. Finally, it uses the credentials (along with my account credentials) to post the rating as a reply.

#### Rating Algorithm
The rating algorithm follows a hierarchy of function calls until valid rating is found.
1. Your/You're Test: If I used the wrong form of your/you're, the bot slanders me. Sigmas don't make spelling errors. 
2. Sigma Test: We gotta know if my tweet was a Sigma Male Grindset tweet. _**"She asked me my favorite position. I said CEO"**_
3. Aggression Test: If I used all-caps, this test makes sure the bot calms down the timeline. 
4. Sentiment Test: Lastly, I use a sentiment analysis library to get a polarity value [-1,1] and subjectivity value [0,1]. See the coordinate plane below to see how these values are used. 
[Insert photo]
#### Amazon Web Services
I run this script continuously on one EC2 instance. Once the API credentials are added as environmental variables, I pull the content or *requirements.txt* and *tweet_rater_script.py* into files on the virtual machine. Finally, I install the dependencies listed in *requirements.txt* using **pip** and start the script on Python 3.

Environmental variables can be added from the Linux command terminal like so:

`export TWITTER_API_KEY="1232213124012393412421412-1231231324-hehexd"`

Files can be downloaded from Github directly like so:

`wget -O requirements.txt https://raw.githubusercontent.com/coopermeitz/tweet-rater/master/requirements.txt`

Finally, run `python3 -m pip install requirements.txt` and `python3 tweet_rater_script.py` in a tmux window and sleep peacefully knowing that no matter how hard I try,
my tweets will be rated for all of eternity.


