from tweet import *
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


    def global_sorter(item):
        # We have id, sender, most recent timestamp, and contents.
        date_time_obj = datetime.strptime(item["recent_timestamp"], '%m-%d-%Y %H:%M:%S')
        return (date_time_obj, item["sender"])


    def personal_sorter(item):
        # We have id, sender, most recent timestamp, and ,
        date_time_obj = datetime.strptime(item["recent_timestamp"], '%m-%d-%Y %H:%M:%S')

        # Python sorts False to be before True, and we want priority tweets to go first, so we use the not operator
        return (not item["priority"], date_time_obj)


    def get_sorted_tweets(self, users, user):
        # Tweets have timestamps and users.  Retweets would essentially update the timestamp.
        # So let's add a timestamp and a boolean - the boolean won't be used here, but it'll add a "retweeted" tag on the html.
        # So there will be two total timestamps:  time of created and time of most recent bump, which is either the time of the most recent retweet
        # or the time of creation, whatever came most recently.
        # So for the personal feed, we want to sort by: time
        # For the general feed, we want to sort by: most retweets,
        if not user:
            return sorted(self.tweets, key=global_sorter)
        else:
            enhanced_tweets = {}
            for (key, value) in self.tweets:
                if value["sender"] in users[user]["following"]:
                    value["priority"] = True
                enhanced_tweets[key] = value
            return sorted(self.tweets, key=personal_sorter)

    def __str__(self):
        """
        Produces a string representation of a collection of Tweets.

        Args:
            None
        Returns:
            A string representation of a collection of Tweets.
        """
        return str(self.tweets)
        # Construct tweets using tweet class.
        # Print each one of them.