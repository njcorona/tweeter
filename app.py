# built-in modules
import json
import os
import datetime

# non-trivial third-party modules
from flask import Flask, flash, render_template, request, redirect, session
from flask_bootstrap import Bootstrap

from tweet import *
from tweets import *

# Flask constants
app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'ax9o4klasi-0oakdn'  # random secret key (needed for flashing)


def save_tweets():
    """
    Saves the current session's tweets to tweets.json.

    Args:
        None

    Returns:
        None
    """
    with open("tweets.json", "w") as outfile:
        json.dump(session["tweets"], outfile)


@app.route("/tweet", methods=['GET', 'POST'])
def post_tweet():
    """
    Posts a tweet to the server.  Requires the current user
    to be logged in, the tweet to be non-empty, and the tweet
    to have fewer than 281 characters.

    Args:
        tweet (str): the tweet to be added to the server, provided via html form

    Returns:
        render_template of post_template if 'GET' or if post fails to be created,
        otherwise render_template of personal_feed_template
    """
    if request.method == 'GET':
        if "user" in session:
            flash("You are currently logged in as " + session["user"] + ".")
            return render_template("post_template.html",
            	   loggedin=True,
            	   title="Post a Tweet")
        else:
            flash("You are not logged in.  Please log in to post a tweet.")
            return render_template("post_template.html",
            	   loggedin=False,
            	   title="Post a Tweet")

    if not session["user"]:
        flash("You must be logged in to post a tweet!")
        return render_template("post_template.html",
            	               loggedin=False,
            	               title="Post a Tweet")

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


@app.route("/delete", methods=['POST'])
def delete_tweet():
    """
    Deletes a tweet from the server.  Requires the current user
    to be logged in and deleting a tweet they posted.

    Args:
        tweet (str): id for the tweet to be deleted, provided via http request
        global (str): "True" if redirect to /global_feed,
                      otherwise redirect to /personal_feed,
                      provided via http request

    Returns:
        redirect to global_feed or personal_feed,
        as determined by args described above
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
    Renders the current user's feed.  Feed is composed of
    tweets sorted first by whether they were posted by
    someone the current user is following and second by
    chronological order of most recent retweet or time of
    posting.

    Args:
        None
    Returns:
        render_template of personal_feed_template if there is
        a current user logged in, otherwise redirects to the
        global_feed.
    """
    if "user" in session:
        return render_template("personal_feed_template.html",
            	               tweets=Tweets(session["tweets"]),
            	               user=session["user"],
            	               users=json.load(open("users.json")),
            	               title="Personal Feed")
    else:
        return redirect("/global_feed")

@app.route("/global_feed", methods=['GET'])
def global_feed():
    """
    Renders global Tweeter feed, in chronological order of
    most recent retweet or time of posting.  The global is
    global because it includes tweets posted by all users.

    Args:
        None
    Returns:
        render_template of global_feed_template
    """
    if "user" in session:
    	return render_template("global_feed_template.html",
                               tweets=Tweets(session["tweets"]),
                               user=session["user"],
                               users=json.load(open("users.json")),
                               title="Global Feed")
    else:
    	return render_template("global_feed_template.html",
                               tweets=Tweets(session["tweets"]),
                               user="",
                               title="Global Feed")


@app.route("/retweet", methods=['POST'])
def retweet():
    """
    Marks a tweet as retweeted by the current user.  This
    moves a tweet to the top of the global feed for all
    and the top of a user's personal feed if the tweet
    was posted by or retweeted by someone they follow.

    Code in the html template with Jinja guarantees
    retweets can only occur when a user is logged in.

    Args:
        tweet (str): id for the tweet to be retweeted, provided via http request
    Returns:
        redirect to /personal_feed
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
    Logs a user in.  The current user is stored in the
    server session.  Tweets posted or retweets from
    now on will be under the current user's name. The
    user will have access to a personal feed, which
    displays their tweets, their followers' tweets,
    and their followers' retweets.

    Users must have registered in order to log in.

    Args:
        username (str): username for user to log in, provided via html form
        password (str): password for user to log in, provided via html form
    Returns:
        redirect to /login if username does not exist or password is incorrect,
        redirect to /personal_feed if log in is successful
    """
    if request.method == 'GET':
        if "user" in session:
            flash("You are currently logged in as " + session["user"] + ".  This will log you out.")
            return render_template("login_template.html", title="Log In")
        else:
            flash("You are not currently logged in.")
            return render_template("login_template.html", title="Log In")

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
    Registers a user to users.json.  Now that user
    can log in via /login.

    Args:
        username (str): username for user to register, provided via html form
        password (str): password for user to register, provided via html form
    Returns:
        redirect to /register if empty username or password or existing
        username, redirect to /login if log in is successful
    """
    if request.method == 'GET':
        return render_template("register_template.html",
        	                   title="Register")

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

    return redirect("/login")


@app.route("/logout", methods=['GET'])
def logout():
    """
    Logs a user out from the server session.

    Args:
        None
    Returns:
        redirect to /login
    """
    session.pop("user")

    return redirect("/login")


@app.route("/follow", methods=['POST'])
def follow():
    """
    Causes the current user to follow another user.
    This will cause the other user's posts and 
    reweets to appear on the current user's personal feed.

    Args:
        followee (str): username of the other user to follow, provided via http request
    Returns:
        redirect to /personal_feed if there is a current user logged in,
        otherwise redirect to /global_feed 
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
    Causes the current user to unfollow another user.
    This will cause the other user's posts and reweets
    to stop appearing on the current user's personal feed.

    Args:
        unfollowee (str): username of the other user to unfollow, provided via http request
    Returns:
        redirect to /personal_feed if there is a current user logged in,
        otherwise redirect to /global_feed
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
    Redirect the user from the root to the /global_feed.

    Args:
        None
    Returns:
        redirect to /global_feed
    """
    session["tweets"] = json.load(open("tweets.json"))
    return redirect("/global_feed")


if __name__ == "__main__":
    app.run(port=5000, debug=True)