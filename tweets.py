from tweet import *
import json
from datetime import datetime

class Tweets:
    def __init__(self, tweets):
        """
        Construct an instance of the Tweet class.

        Attributes:
            - self.tweet: the text of the tweet
            - self.sender: the sender of the tweet

        Args:
            tweet (str): the text of the tweet
            sender (str): the sender of the tweet
        """
        self.tweets = tweets


    def get_sorted_tweets(self, users, user):
        # Tweets have timestamps and users.  Retweets would essentially update the timestamp.
        # So let's add a timestamp and a boolean - the boolean won't be used here, but it'll add a "retweeted" tag on the html.
        # So there will be two total timestamps:  time of created and time of most recent bump, which is either the time of the most recent retweet
        # or the time of creation, whatever came most recently.
        # So for the personal feed, we want to sort by: time
        # For the general feed, we want to sort by: most retweets,
        def sorter(item):
            # We have id, sender, most recent timestamp, and ,
            if item["retweet_time"]:
                return (item["priority"], datetime.strptime(item["retweet_time"], '%m/%d/%Y %H:%M:%S'))
            else:
                return (item["priority"], datetime.strptime(item["timestamp"], '%m/%d/%Y %H:%M:%S'))          

        enhanced_tweets = []
        for key in self.tweets:
            new_value = self.tweets[key]
            new_value["priority"] = user and (new_value["sender"] in users[user]["following"] or new_value["retweeter"] in users[user]["following"])
            enhanced_tweets.append(new_value)
        return sorted(enhanced_tweets, key=sorter, reverse=True)
    

    def __str__(self):
        """
        Produces a string representation of a collection of Tweets.

        Args:
            None
        Returns:
            A string representation of a collection of Tweets.
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