'''
ETL script
'''
import pymongo
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy_utils import create_database
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


#Extract
#connect to mongodb
client = pymongo.MongoClient("mongodb://mongodb:27017/")
#print(client)
#use find command to extract data
result = client.tweet_collector.mycol.find()
#print(result)
#transform
tweet_list =[]
for docs in result:
    row = (docs['user_name'], docs['user_id'], docs['twitter_text'], 
    docs['location'], docs['time'], docs['retweet_count'],docs['user_profile_image_url'])
    tweet_list.append(row)

#print(tweet_list)
#put in table form

df = pd.DataFrame(tweet_list, columns=['user_name', 'user_id', 'twitter_text', 'location', 
                   'time', 'retweet_count', 'user_profile_image_url'])
print(df.shape)

#load
#connect to postgres server
db = create_engine('postgres://postgres:titanic@my_postgresdb:5432/twitterdb')

#add sentiment analysis
sid_obj = SentimentIntensityAnalyzer()

df['Sentiment']=[sid_obj.polarity_scores(text)['compound'] for text in df.twitter_text]
#create_database(db.url)

print(df.shape)

#use sqlalchemy to create/insert table

try:
    df.to_sql('tweets', db, if_exists='replace', index=False)
    print('db updated')
except ConnectionError:
    print('connection not made')

print('end script')