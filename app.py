# user authentication
# nice html / css
# Do I need one instance of Tweets that exists across the program?  OR do I just create one each time I need it fromthe json?

# built-in modules
import json
import os

# web dev modules
from flask import Flask, flash, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename

from tweet import *
from tweets import *

# Flask constants, do not change!
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.secret_key = 'ax9o4klasi-0oakdn'  # random secret key (needed for flashing)

@app.route("/tweet", methods=['GET', 'POST'])
def post_tweet():
    """
    Adds a tweet to the server.  Takes in tweet as
    argument, but also notes identity of sender
    and current system time.

    Args:
        tweet (str): the tweet to be added to the server
    Returns:
        True if successful, False otherwise
    """
    if request.method == 'GET':
        return render_template("post_template.html")

    sender = request.form["sender"]
    tweet = request.form["tweet"]

    if not tweet:
        flash("Please provide a non-empty tweet.")
        return redirect("/tweet")

    if not sender:
        flash("Please provide a non-empty sender.")
        return redirect("/tweet")

    if any(c.isspace() for c in sender):
        flash("Please provide a sender without whitespace.")
        return redirect("/tweet")

    if len(tweet) > 280:
        flash("Tweets must be 280 characters or less.")
        return redirect("/tweet")

    tweets = Tweets(json.load(open("tweets.json")))
    tweets.create_tweet(tweet, sender)

    with open("tweets.json", "w") as outfile:  
        json.dump(tweets.get_tweets(), outfile) 

    return redirect("/render_feed")

    # TODO: update this to make the identifier the number of current tweets + 1.
    # TODO: save tweet to json, once I learn how to do that.


@app.route("/reply", methods=['POST'])
def post_reply():
    """
    Adds a tweet in response to another tweet to the server.
    (This creates a "thread" instead of a single tweet.)

    Args:
        tweet (str): the tweet to be added to the server
        prev (str): identifier for the replied-to tweet
    Returns:
        True if successful, False otherwise
    """
    raise NotImplementedError

@app.route("/delete", methods=['POST'])
def delete_tweet():
    """
    Deletes a tweet from the server.

    Args:
        tweet (str): identifier for the tweet to be deleted
    Returns:
        True if successful, False otherwise
    """
    tweet = request.args.get("tweet")
    sender = request.args.get("sender")

    tweets = Tweets(json.load(open("tweets.json")))
    tweets.delete_tweet(tweet, sender)

    with open("tweets.json", "w") as outfile:  
        json.dump(tweets.get_tweets(), outfile)

    return redirect("/render_feed")


@app.route("/render_feed", methods=['GET'])
def render_feed():
    """
    Renders the user's feed, in chronological order.

    Args:
        None
    Returns:
        True if successful, False otherwise
    """
    tweets = Tweets(json.load(open("tweets.json")))

    return render_template("feed_template.html",
                           tweets=tweets)

@app.route("/retweet", methods=['POST'])
def retweet():
    """
    Marks a tweet as retweeted by the current user.  This
    moves a tweet to the top of the feed for all users.

    Args:
        tweet (str): identifier for the tweet to be retweeted
    Returns:
        True if successful, False otherwise
    """
    sender = request.form["sender"]
    tweet = request.args.get("tweet")

    return redirect(url_for("post_tweet"))



@app.route("/", methods=['GET'])
def home():
    """
    Redirect the user from the root URL to the /upload URL.

    Args:
        None

    Returns:
        The required return by Flask so the user is redirected to the /upload
        URL
    """
    return redirect("/render_feed")


if __name__ == "__main__":
    app.run(port=5000, debug=True)