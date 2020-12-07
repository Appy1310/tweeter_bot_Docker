#import pymongo
import pandas as pd
from sqlalchemy import create_engine
#from sqlalchemy.sql import text
#from sqlalchemy_utils import create_database
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import requests
#import pyjokes
from dotenv import load_dotenv
import os
load_dotenv()



print('Slackbot is running!')






#connect to postgres and collect the data

db = create_engine('postgres://postgres:titanic@my_postgresdb:5432/twitterdb')

tweet_data = pd.read_sql('SELECT * from tweets;', db)
#print(tweet_data)
# Sort Tweet data accorting to retweet counts:
tweet_data.sort_values(by=['retweet_count'], inplace = True, ascending=False)

#drop duplicates
tweet_data= tweet_data.drop_duplicates(subset=['twitter_text'])

#reset index
tweet_data.reset_index(inplace =True, drop=True)

#print(tweet_data[['twitter_text']].head(5))

## defining the webhook
webhook_url = os.getenv('webhook_url')



## post in slack-bot
#data = {'text': tweet_data.iloc[7]['twitter_text']}


#Define the data


data = {"blocks": [
		{"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": f"*Most retweeted by {tweet_data.iloc[0]['user_name']}@{tweet_data.iloc[0]['user_id']}*\n with Query of Donald Trump or Joe Biden"
				},
				{
					"type": "mrkdwn",
					"text": f"*Location:*\n {tweet_data.iloc[0]['location']}"
				},
				{
					"type": "mrkdwn",
					"text": f"*Tweeted at:*\n {tweet_data.iloc[0]['time']}"
				},
				{
					"type": "mrkdwn",
					"text": f"*Compound Vader Sentiment:*\n {tweet_data.iloc[0]['Sentiment']}"
				},
				{
					"type": "mrkdwn",
					"text": f"*Tweet_text:*\n {tweet_data.iloc[0]['twitter_text']}"
				}
			],
          "accessory": {
				"type": "image",
				"image_url": f"{tweet_data.iloc[0]['user_profile_image_url']}",
				"alt_text": "alt text for image"
			}
			},
]
}

#post in slackbot


#requests.post(url=webhook_url, json = data)
