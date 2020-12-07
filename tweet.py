from datetime import datetime

class Tweet:
    def __init__(self, tweet, sender, unique):
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
        self.timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    def to_dict(self):
        return { "id" : self.id,
                 "tweet" : self.tweet,
                 "sender" : self.sender,
                 "timestamp" : self.timestamp }


    def __str__(self):
        """
        Produces a string representation of the Tweet.

        Args:
            None
        Returns:
            A string representation of the Tweet.
        """
        return "Unique ID: {}\nTweet: \"{}\"\nSender ID: {}\nTime Posted: {}\n".format(
            self.id,
            self.tweet,
            self.sender,
            self.timestamp)


if __name__ == "__main__":
    tweet = Tweet("Hello, world!",  "Nicky C", 1)
    print(tweet)
    print(tweet.to_dict())