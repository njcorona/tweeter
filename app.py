# nice html / css - no
# Do I need one instance of Tweets that exists across the program?  OR do I just create one each time I need it fromthe json?
# Is my use of a class definition interesting enough
# Are my dunder methods interesting at all
# how to specify whether redirect is get or post

# built-in modules
import json
import os

# web dev modules
from flask import Flask, flash, render_template, request, url_for, redirect, session
from werkzeug.utils import secure_filename

from tweet import *
from tweets import *
from datetime import datetime

# Flask constants, do not change!
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.secret_key = 'ax9o4klasi-0oakdn'  # random secret key (needed for flashing)


def save_tweets():
    with open("tweets.json", "w") as outfile:
        json.dump(session["tweets"], outfile)


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
        if "user" in session:
            return render_template("post_template.html",
            	   message="You are currently logged in as " + session["user"] + ".",
            	   loggedin=True)
        else:
            return render_template("post_template.html",
            	   message="You are not logged in.  Please log in to post a tweet.",
            	   loggedin=False)

    if not session["user"]:
        flash("You must be logged in to post a tweet!")
        return render_template("post_template.html",
        	                   message="You are not logged in.  Please log in to post a tweet.",
            	               loggedin=False)

    tweet = request.form["tweet"]

    if not tweet:
        flash("Please provide a non-empty tweet.")
        return redirect("/tweet")

    if len(tweet) > 280:
        flash("Tweets must be 280 characters or less.")
        return redirect("/tweet")
    
    if len(session["tweets"].keys()) == 0:
        tw = Tweet(tweet, session["user"], 0, datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        tws = session["tweets"]
        tws["0"] = tw.to_dict()
        session["tweets"] = tws
    else:
        tw = Tweet(tweet, session["user"], int(max(session["tweets"].keys())) + 1, datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        tws = session["tweets"]
        tws[str(int(max(session["tweets"].keys())) + 1)] = tw.to_dict()
        session["tweets"] = tws
    save_tweets()

    return redirect("/personal_feed")


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
    tw_id = request.args.get("tweet")
    global_feed = request.args.get("global")

    tws = session["tweets"]
    tws.pop(tw_id)
    session["tweets"] = tws
    save_tweets()

    if global_feed == "True":
        return redirect("/global_feed")
    else:
        return redirect("/personal_feed")


@app.route("/personal_feed", methods=['GET'])
def personal_feed():
    """
    Renders the user's feed, in chronological order.

    Args:
        None
    Returns:
        True if successful, False otherwise
    """
    if "user" in session:
        return render_template("personal_feed_template.html",
            	               tweets=Tweets(session["tweets"]),
            	               user=session["user"],
            	               users=json.load(open("users.json")))
    else:
        return redirect("/global_feed")

@app.route("/global_feed", methods=['GET'])
def global_feed():
    """
    Renders the user's feed, in chronological order.

    Args:
        None
    Returns:
        True if successful, False otherwise
    """
    if "user" in session:
    	return render_template("global_feed_template.html",
                               tweets=Tweets(session["tweets"]),
                               user=session["user"],
                               users=json.load(open("users.json")))
    else:
    	return render_template("global_feed_template.html",
                               tweets=Tweets(session["tweets"]),
                               user="")


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
    tw_id = request.args.get("tweet")

    tws = session["tweets"]
    tws[tw_id]["retweet_time"] = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    tws[tw_id]["retweeter"] = session["user"]

    session["tweets"] = tws
    save_tweets()

    return redirect("/personal_feed")


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    """
    if request.method == 'GET':
        if "user" in session:
            return render_template("login_template.html",
        	                   message="You are currently logged in as " + session["user"] + ".  This will log you out.")
        else:
            return render_template("login_template.html",
        	                   message="You are not currently logged in.")

    un = request.form["username"]
    pw = request.form["password"]

    users = json.load(open("users.json"))

    if un not in users:
    	flash("Username does not exist.")
    	return redirect("/login")

    if pw != users[un]["pw"]:
        flash("Incorrect password.")
        return redirect("/login")

    session["user"] = un

    return redirect("/personal_feed")


@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    """
    if request.method == 'GET':
        return render_template("register_template.html")

    un = request.form["username"]
    pw = request.form["password"]

    users = json.load(open("users.json"))

    if not un:
        flash("Please provide a non-empty username.")
        return redirect("/register")

    if not pw:
        flash("Please provide a non-empty password.")
        return redirect("/register")

    if any(c.isspace() for c in un):
        flash("Please provide a username without whitespace.")
        return redirect("/register")

    if any(c.isspace() for c in pw):
        flash("Please provide a password without whitespace.")
        return redirect("/register")

    if un in users:
        flash("User already registered.")
        return redirect("/register")

    users[un] = { "pw" : pw,
                  "following": [un],
                  "followers": [un]
    }

    with open("users.json", "w") as outfile:  
        json.dump(users, outfile)

    return redirect(url_for("login"))


@app.route("/logout", methods=['GET'])
def logout():
    """
    """
    session.pop("user")

    return redirect("/login")


@app.route("/follow", methods=['POST'])
def follow():
    """
    """
    if "user" in session:
        followee = request.args.get("followee")
        users = json.load(open("users.json"))
        users[session["user"]]["following"].append(followee)
        users[followee]["followers"].append(session["user"])
        with open("users.json", "w") as outfile:  
            json.dump(users, outfile)
        return redirect("/personal_feed")
    else:
    	flash("You must be logged in to follow someone.")
    	return redirect("/global_feed")

@app.route("/unfollow", methods=['POST'])
def unfollow():
    """
    """
    if "user" in session:
        unfollowee = request.args.get("unfollowee")
        users = json.load(open("users.json"))
        users[session["user"]]["following"].remove(unfollowee)
        users[unfollowee]["followers"].remove(session["user"])
        with open("users.json", "w") as outfile:  
            json.dump(users, outfile)
        return redirect("/personal_feed")
    else:
    	flash("You must be logged in to unfollow someone.")
    	return redirect("/global_feed")


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
    session["tweets"] = json.load(open("tweets.json"))
    return redirect("/global_feed")


if __name__ == "__main__":
    app.run(port=5000, debug=True)