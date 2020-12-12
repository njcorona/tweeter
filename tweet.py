from datetime import datetime

class Tweet:
    def __init__(self, tweet, sender, unique, timestamp):
        """
        Construct an instance of the Tweet class.

        Attributes:
            - self.tweet: the text of the tweet
            - self.sender: the sender of the tweet

        Args:
            tweet (str): the text of the tweet
            sender (str): the sender of the tweet
        """
        self.id = unique
        self.tweet = tweet
        self.sender = sender
        self.timestamp = timestamp
        self.retweet_time = ""
        self.retweeter = ""

    def to_dict(self):
        return { "id" : self.id,
                 "tweet" : self.tweet,
                 "sender" : self.sender,
                 "timestamp" : self.timestamp,
                 "retweet_time" : self.retweet_time,
                 "retweeter" : self.retweeter
               }

    def __str__(self):
        """
        Produces a string representation of the Tweet.

        Args:
            None
        Returns:
            A string representation of the Tweet.
        """
        return "\nTWEET {}\n\n  {}\n\n  @{}\n  {}\n".format(
            self.id,
            self.tweet,
            self.sender,
            self.timestamp)


if __name__ == "__main__":
    tweet = Tweet("Hello, world!",  "NickyC", 1, "Today.")
    print(tweet)