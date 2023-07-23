import mysql.connector
import tweepy
from textblob import TextBlob

consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_token_secret = 'your_access_token_secret'

db_host = 'your_db_host'
db_user = 'your_db_user'
db_password = 'your_db_password'
db_name = 'your_db_name'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

cnx = mysql.connector.connect(user=db_user, password=db_password, host=db_host, database=db_name)
cursor = cnx.cursor()

def analyze_tweet(tweet_text):
    sentiment = TextBlob(tweet_text).sentiment.polarity
    add_sentiment = ("INSERT INTO tweet_sentiments "
                     "(tweet_text, sentiment_score) "
                     "VALUES (%s, %s)")
    data_sentiment = (tweet_text, sentiment)
    cursor.execute(add_sentiment, data_sentiment)
    cnx.commit()

def fetch_and_analyze_tweets(keyword, num_tweets):
    tweets = api.search(q=keyword, count=num_tweets)
    for tweet in tweets:
        tweet_text = tweet.text
        analyze_tweet(tweet_text)

keyword = 'your_keyword'
num_tweets = 100

fetch_and_analyze_tweets(keyword, num_tweets)

cursor.close()
cnx.close()
