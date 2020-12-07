#!/usr/bin/env python
# coding: utf-8

# In[22]:


import os
import tweepy
import logging
from dotenv import load_dotenv
import pymongo
# load environment variables from a .env file
load_dotenv()


# In[2]:


# OAuth 2 - APP only - read-only access to public information.
auth = tweepy.OAuthHandler(
    consumer_key=os.getenv('api_key'),
    consumer_secret=os.getenv('api_secret_key')
)
# OAuth 1 - User - access user information, post tweets and connect to twitter stream
# auth.set_access_token(os.getenv('access_token'), os.getenv('access_token_secret'))


# In[3]:


api = tweepy.API(auth)


# ### Getting full tweet text for a specific user

# In[18]:


cursor = tweepy.Cursor(
    api.search,
    q='"Donald Trump" or "Joe Biden"',
    #result_type = 'popular',
    tweet_mode='extended',
    count=2000
)


# In[19]:


twitter_text = []

for status in cursor.items(1000):
    twitter_temp = {}
    twitter_temp['user_name'] = status.author.name
    twitter_temp['user_id'] = status.author.screen_name
    twitter_temp['location'] = status.author.location
    twitter_temp['time'] = status.created_at
    twitter_temp['followers_count'] = status.author.followers_count
    twitter_temp['friends_count'] = status.author.friends_count
    twitter_temp['retweet_count'] = status.retweet_count
    try:
        twitter_temp['twitter_text'] = status.retweeted_status.full_text
    except AttributeError:  # Not a Retweet
        twitter_temp['twitter_text'] = status.full_text

    twitter_temp['user_profile_image_url'] = status.author.profile_image_url

    twitter_text.append(twitter_temp)


# In[20]:


# twitter_text


# In[8]:


# # Adding the data to a MongoDb database

# In[23]:


client = pymongo.MongoClient("mongodb://mongodb:27017/")
#db = client.twitter


# In[25]:


mydb = client.tweet_collector
#mycol = mydb["tweeter"]


# In[27]:


mydb.mycol.insert_many(twitter_text)
