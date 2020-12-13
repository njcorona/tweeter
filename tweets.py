"""
tweets.py

Class that represents a map of tweet IDs to tweets.
"""

import json

from datetime import datetime
from tweet import *


class Tweets:
    def __init__(self, tweets):
        """
        Constructs an instance of the Tweets class.

        Attributes:
            - self.tweets (dict): the tweets in this instance

        Args:
            tweets (dict): the tweets to store in this instance
        """
        self.tweets = tweets

    def get_sorted_tweets(self, users, user):
        """
        Produces a sorted list of tweets, for the purposes of
        displaying in a Tweeter feed.  The sorted list will
        either be sorted first by whether the current user
        is following the tweets' senders or retweeters and
        second by time of posting or most recent retweet,
        or be sorted solely by time of posting or most recent
        retweet.

        Args:
            users (dict): all users registered on the server
            user (str): the user that is currently logged in
        Returns:
            a sorted list of tweets, sorted as explained above
        """
        def sorter(item):
            """
            A local function used as an argument to sorted()
            to determine how to sort tweets stored in a list.

            Args:
                item (dict): the tweet currently being sorted
            Returns:
                a tuple of the elements to consider, in order,
                when sorting this item in a list
            """
            if item["retweet_time"]:
                return (item["priority"],
                        datetime.strptime(item["retweet_time"],
                                          '%m/%d/%Y %H:%M:%S'))
            else:
                return (item["priority"],
                        datetime.strptime(item["timestamp"],
                                          '%m/%d/%Y %H:%M:%S'))

        enhanced_tweets = []

        for key in self.tweets:
            new_value = self.tweets[key]

            new_value["priority"] = user and
            (new_value["sender"] in users[user]["following"] or
             new_value["retweeter"] in users[user]["following"])

            enhanced_tweets.append(new_value)

        return sorted(enhanced_tweets, key=sorter, reverse=True)

    def __str__(self):
        """
        Produces a string representation of Tweets, drawing
        on the Tweet class for support in representing
        individual tweets as strings.

        Args:
            None
        Returns:
            A string representation of Tweets.
        """
        strt = ""
        for key in self.tweets:
            strt = strt + str(Tweet(self.tweets[key]["tweet"],
                                    self.tweets[key]["sender"],
                                    self.tweets[key]["id"],
                                    self.tweets[key]["timestamp"]))

        return "[\n" + strt + "\n]"


if __name__ == "__main__":
    tweets = Tweets(json.load(open("tweets.json")))
    print(tweets)
