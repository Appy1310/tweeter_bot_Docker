import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

# OAuth2: app context only
# OAuth 2 - APP only - read-only access to public information.
auth = tweepy.OAuthHandler(
    consumer_key=os.getenv('api_key'),
    consumer_secret=os.getenv('api_secret_key')
)

try:

    # get the request token (verification code) from twitter
    redirect_url = auth.get_authorization_url()
    print(f'Please visit: {redirect_url}')
    verifier = input('Please input verifier: ')

    # get the access token key and secret
    access_token = auth.get_access_token(verifier)

    # update the authentification
    auth.set_access_token(*access_token)

    # test it
    api = tweepy.API(auth)
    for status in api.home_timeline():
        print(status.text)

    # write to disk
    with open('./access_token', 'w') as f:
        for token, label in zip(
            access_token, [
                'access_token', 'access_token_secret']):
            f.write(f'{label}={token}\n')

except tweepy.TweepError:
    print('Error! User authentification failed.')
