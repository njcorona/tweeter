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
        print(int(max(self.tweets.keys())))
        tw = Tweet(tweet, sender, int(max(self.tweets.keys())) + 1)
        self.tweets[str(int(max(self.tweets.keys())) + 1)] = tw.to_dict()

    def get_tweets(self):
        return self.tweets

    def delete_tweet(self, tweet, sender):
        print(tweet)
        print(sender)
        print(self)
        if self.tweets[tweet]["sender"] == sender:
            del self.tweets[tweet]

    def __str__(self):
        """
        Produces a string representation of a collection of Tweets.

        Args:
            None
        Returns:
            A string representation of a collection of Tweets.
        """
        return str(self.tweets)


if __name__ == "__main__":
    tweets = Tweets({})
    tweets.create_tweet("hey", "tony")
    tweets.create_tweet("heyoo", "tony")
    print(tweets)