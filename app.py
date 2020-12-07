# built-in modules
import json
import os

# web dev modules
from flask import Flask, flash, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename

# deep learning/image modules
from PIL import Image
import torch
from torchvision import models, transforms

# For simplicity, we'll just store the model as a global
mobilenet = models.mobilenet_v2(pretrained=True)
mobilenet.eval()

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

    print(tweet)
    print(sender)

    if not tweet:
        flash("Please provide a non-empty tweet.")
        return redirect("/tweet")

    if len(tweet) > 280:
        flash("Tweets must be 280 characters or less.")
        return redirect("/tweet")

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
    raise NotImplementedError

@app.route("/render_feed", methods=['GET'])
def render_feed():
    """
    Renders the user's feed, in chronological order.

    Args:
        None
    Returns:
        True if successful, False otherwise
    """
    raise NotImplementedError

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
    raise NotImplementedError

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
    return redirect("/tweet")


if __name__ == "__main__":
    app.run(port=5000, debug=True)