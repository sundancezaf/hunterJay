from html import entities
from urllib.parse import quote_plus
import json
import requests
from modulesForOauth.requests_oauthlib import OAuth1  # Multilevel relative import
import sys
from secrets import *

sys.path.insert(0, "./modulesForOauth")

# The code in this file won't work until you set up your Twitter "app"
# at https://dev.twitter.com/apps


class Hunter:
    """Class that contains methods to connect to the Twitter API and search for
    tweets based on keywords.
    """

    def __init__(self):
        self.client = self.authTwitter()
        self.response = None

    def authTwitter(self):
        """Authorization for the Twitter API. This must be called first for the
        rest of the methods to work.
        """
        client = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return client

    def searchTwitter(self, searchString, count=20):
        query = (
            "https://api.twitter.com/1.1/search/tweets.json?q="
            + quote_plus(searchString)
            + "&count="
            + str(count)
            + "&tweet_mode=extended"
        )

        self.response = requests.get(query, auth=self.client)
        resultDict = json.loads(self.response.text)
        # The most important information in resultDict is the value associated with
        # key 'statuses'
        tweets = resultDict["statuses"]
        for tweetIndex in range(len(tweets)):
            tweet = tweets[tweetIndex]
            entities = tweet["entities"]
            urlsEntity = entities["urls"]
            user_info = tweet["user"]
            screen_name = user_info["screen_name"]
            name = user_info["name"]

            print(f"The screen name: {screen_name}")
            print("The tweet: %", tweet["full_text"])
            if len(urlsEntity) != 0:
                urlsDict = urlsEntity[0]
                final_url = urlsDict["url"]
                print("\n")
                print("The URLS:")
                print(final_url)
                print("\n")
            print("---------------------------")

        # return tweets

    def printable(self, s):
        """This function helps transform tweets that can't be printed in the Python shell.

        Args:
            s (str): Unprintable string

        Returns:
            str: printable string
        """
        result = ""
        for c in s:
            result = result + (c if c <= "\uffff" else "?")
        return result


# ------ Testing ------------

if __name__ == "__main__":
    first = Hunter()
    first.searchTwitter("#pizza")
