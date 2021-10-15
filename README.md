# tweet-rater
A bot that rates my tweets. Pretty dumb

It runs on an Amazon EC2 instance in the cloud.

If you want to make it rate smartly, create an issue or a pull request.

## How it works
#### Script
I got access to the Twitter API's from the [Twitter for Developers](https://developer.twitter.com/en) website. This site gives credentials for the app to run, and for the app to tweet on my behalf.
Then, the script uses those credentials to poll for my tweets every 90 seconds. If it finds a new one, it runs the
`rate_tweet()` algorithm on the new tweet(s) and determines a rating. Finally, it uses the credentials (along with my account credentials) to post the rating as a reply.


#### Amazon Web Services
I run this script continuously on one EC2 instance. Once the API credentials are added as environmental variables, I pull the content or *requirements.txt* and *tweet_rater_script.py* into files on the virtual machine. Finally, I install the dependencies listed in *requirements.txt* using **pip** and start the script on Python 3.

Environmental variables can be added from the Linux command terminal like so:

`export TWITTER_API_KEY="1232213124012393412421412-1231231324-hehexd"`

Files can be downloaded from Github directly like so:

`wget -O requirements.txt https://raw.githubusercontent.com/coopermeitz/tweet-rater/master/requirements.txt`

Finally, run `python3 -m pip install requirements.txt` and `python3 tweet_rater_script.py` in a tmux window and sleep peacefully knowing that no matter how hard I try,
my tweets will be rated for all of eternity.


