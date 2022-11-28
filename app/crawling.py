import tweepy
import re
import string

from PIL import Image
from wordcloud import WordCloud
import numpy as np
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

from app.config import settings


def keyword_search(keyword, no_tweet):
    query = keyword + " -is:retweet"

    auth = tweepy.OAuthHandler(settings.consumer_key, settings.consumer_secret)
    auth.set_access_token(settings.access_token, settings.access_token_secret)
    api = tweepy.API(auth)

    tweets = api.search_tweets(q=query, count=no_tweet, locale='id', lang='id')
    tweet = create_array(tweets)

    tweet = clean_tweet(tweet)
    tweet = remove_punctuation(tweet)
    tweet = remove_stopwords(tweet)
    tweet = remove_emoji(tweet)

    create_wordcloud(tweet, colo_func=multi_color_func)

    return "tmp/wordcloud.png"

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


def get_trends_twitter():
    auth = tweepy.OAuthHandler(settings.consumer_key, settings.consumer_secret)
    auth.set_access_token(settings.access_token, settings.access_token_secret)
    api = tweepy.API(auth)

    woeid = 23424846

    trends = api.get_place_trends(id=woeid)

    return trends


def create_array(tweets):
    tweet_text = []

    for tweet in tweets:
        tweet_text.append(tweet.text)

    return tweet_text


def clean_tweet(tweets):
    clean = []
    for tweet in tweets:
        tweet = re.sub(r'@[A-Za-z0–9]+', '', tweet)  # Removing @mentions
        tweet = re.sub(r'#', '', tweet)  # Removing '#' hash tag
        tweet = re.sub(r'RT\s+', '', tweet)  # Removing RT
        tweet = re.sub(r'https?://\S+', '', tweet)  # Removing hyperlink

        clean.append(tweet)

    return clean


def remove_punctuation(tweets):
    result = []

    for tweet in tweets:
        table = str.maketrans('', '', string.punctuation)
        result.append(tweet.translate(table))

    return result


def remove_stopwords(tweets):
    result = []

    for tweet in tweets:
        stop_factory = StopWordRemoverFactory()
        more_stopword = ['definisi', 'gk', 'kasih', 'dumdum', 'upay', 'Haaa', 'Woyyyy', 'jg', 'lgi', 'hrs', 'yah', 'yg',
                         'dmn', 'gak', 'kok']
        stopword = stop_factory.get_stop_words() + more_stopword
        words = [w for w in tweet.split() if len(w) > 4 or w not in stopword]
        result.append(" ".join(words))

    return result


def remove_emoji(tweets):
    result = []

    for tweet in tweets:
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
        result.append(emoji_pattern.sub(r'', tweet))

    return result


def multi_color_func(word=None, font_size=None,
                     position=None, orientation=None,
                     font_path=None, random_state=None):
    colors = [[198, 231, 252],
              [150, 211, 249],
              [125, 201, 248],
              [101, 191, 246],
              [77, 181, 245],
              [29, 161, 242],
              [12, 133, 208],
              [11, 118, 184],
              [9, 103, 160],
              [6, 72, 112]]
    rand = random_state.randint(0, len(colors) - 1)
    return "rgb({}, {}, {})".format(colors[rand][0], colors[rand][1], colors[rand][2])


def create_wordcloud(text, colo_func):
    mask = np.array(Image.open('static/mask.png'))
    stop_factory = StopWordRemoverFactory()
    more_stopword = ['definisi', 'gk', 'kasih', 'dumdum', 'upay', 'Haaa', 'Woyyyy', 'jg', 'lgi', 'hrs', 'yah', 'yg',
                     'dmn', 'gak', 'kok']
    stopword = stop_factory.get_stop_words() + more_stopword
    wc = WordCloud(background_color="#E1E8ED",
                   repeat=True,
                   mask=mask,
                   stopwords=stopword,
                   width=mask.shape[1],
                   height=mask.shape[0],
                   color_func=colo_func
                   )

    wc.generate(str(text))
    wc.to_file("/tmp/wordcloud.png")
