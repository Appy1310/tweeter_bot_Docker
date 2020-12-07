## Built a Dockerized Data Pipeline that analyzes the sentiment of tweets.

## 1) The pipeline collects tweets and store them in a MongoDB database (Tweet_collector)
## 2) Next, the sentiment of tweets is analyzed and the result stored in a second PostgresSQL database (etl_job). 
## 3) Finally, the best or worst sentiment for a given time interval is put on Slack automatically.

