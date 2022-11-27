import tweepy
import json
import re
import pandas as pd
import string
from tweepy import OAuthHandler
from textblob import TextBlob
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
# nltk.download('stopwords')
from .config import *

def keyword_search(keyword, no_tweet):
    query = keyword + " -is:retweet"

    api = tweepy.Client(bearer_token=settings.bearer_token, consumer_key=settings.consumer_key, consumer_secret=settings.consumer_secret, access_token=settings.access_token, access_token_secret=settings.access_token_secret, wait_on_rate_limit=True)
    tweets = api.search_recent_tweets(query=query, max_results=no_tweet)
    tweets_df = create_array(tweets)
    tweets_df['Tweet'] = tweets_df['Tweet'].apply(clean_tweet)
    tweets_df['Tweet'] = tweets_df['Tweet'].apply(remove_punctuation)
    tweets_df['Tweet'] = tweets_df['Tweet'].apply(remove_stopwords)
    tweets_df['Tweet'] = tweets_df['Tweet'].apply(remove_emoji)
    return tweets_df.to_dict('records')

    # data = []
    # for tweet in tweets.data:
    #     data.append({ 'tweet': tweet.text })
    # return data
    # tweet_list = []
    # tweet_user = []
    # for tweet in tweets.data:
    #     tweet_user.append(tweet.user.name)
    #     tweet_list.append(tweet.text)
    #     tweets_df = pd.DataFrame({'User': tweet_user, 'Tweet': tweet_list})
    # return tweets_df.__dict__
    
    # tweet_df = create_array(tweets)
    # tweet_df['Tweet'] = tweet_df['Tweet'].apply(clean_tweet)
    # tweet_df['Tweet'] = tweet_df['Tweet'].apply(remove_punctuation)
    # tweet_df['Tweet'] = tweet_df['Tweet'].apply(remove_stopwords)
    # tweet_df['Tweet'] = tweet_df['Tweet'].apply(remove_emoji)
    # return tweet_df.to_dict('records')


def create_array(tweets):
    tweet_text = []

    for tweet in tweets.data:
        tweet_text.append({'Tweet': tweet.text})
        tweets_df = pd.DataFrame(tweet_text)
    return tweets_df

def clean_tweet(tweet):
    tweet = re.sub(r'@[A-Za-z0–9]+', '', tweet) #Removing @mentions
    tweet = re.sub(r'#', '', tweet) # Removing '#' hash tag
    tweet = re.sub(r'RT[\s]+', '', tweet) # Removing RT
    tweet = re.sub(r'https?:\/\/\S+', '', tweet) # Removing hyperlink
    return tweet

def remove_punctuation(tweet):
    table=str.maketrans('','',string.punctuation)
    return tweet.translate(table)

def remove_stopwords(tweet):
    words = [w for w in tweet.split() if len(w)>3]
    return " ".join(words)

def remove_emoji(tweet):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', tweet)
