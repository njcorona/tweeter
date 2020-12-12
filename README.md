# Project description

My final project for CIS 192 (Python) is Tweeter, a clone of Twitter.  Tweeter uses a Flask backend with basic html, Bootstrap, and Jinja for the frontend.

# Installation

There is a requirements.txt file that details all of the required modules and module versions I used in this project.  Tweeter is hosted on Heroku, so you can visit Tweeter, register as a user, and post your own tweets at:  https://tweeter-njcorona.herokuapp.com/.  If too many people access the URL at the same time, new users cannot access the URL, so please remember to close your tab once you're done.

To run the app locally, install all of the requirements and run: ``python3 app.py``.

# Code structure

## General Overview

My project's functionality is split across .html files and .py files.

- app.py: this contains all of the logic for the server
- tweets.py: this represents a dictionary mapping tweet IDs to tweets
- tweet.py: this represents a dictionary mapping fields to values for an individual tweet
- register_template.html: displays a form to register a new user
- login_template.html: displays a form to log in as an existing user
- personal_feed_template.html: displays the current user's personal feed, prioritizing tweets from user's the current user follows and by recency
- global_feed_template.html: displays the global feed, all tweets sorted by recency of interation (retweet or creation)
- post_template.html: displays a form to post a tweet

### .py files

app.py initializes the app.  It handles requests from the frontend and renders html to display on the frontend.  app.py reads from and writes to two json files: tweets.json and users.json.  This allows the server to exhibit tweet and user permanence across sessions when being run locally.  At the same time, the server keeps track of a current session.  This session stores the current tweets and the currently-logged-in user, if any.

tweets.py represents a map of tweets, as it maps tweet IDs to tweets.  Its most important functionalities are:  (1) providing a sorted list of tweets to display on the global and personal feeds and (2) providing a string representation of itself for debugging.  

tweet.py represents an individual tweet.  Its most important functionalities are: (1) providing a dict representation of itself to use when writing to tweets.json and (2) providing a string representation of itself for debugging.

### .html files

I used the third-party module Flask-Bootstrap to allow for better style and modular html in my frontend.  base.html is a base html template that inherits from bootstrap's base html.  I customized it to include a title and always display flashed messages directly below the title.  Each other html file extends this base.html file, extending the inherited html blocks when necessary by calling super().

In the .html files, I frequently provide buttons or forms to facilitate the collection of information and navigation across the website.

## Final Project Requirements