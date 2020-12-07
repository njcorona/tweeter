from tweet import *

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


    def create_tweet(self, tweet, sender):
        tw = Tweet(tweet, sender, len(self.tweets))
        self.tweets[str(len(self.tweets))] = tw.to_dict()


    def __str__(self):
        """
        Produces a string representation of the Tweet.

        Args:
            None
        Returns:
            A string representation of the Tweet.
        """
        return str(self.tweets)


if __name__ == "__main__":
    tweets = Tweets({})
    tweets.create_tweet("hey", "tony")
    tweets.create_tweet("heyoo", "tony")
    print(tweets)