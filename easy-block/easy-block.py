#%%
import tweepy
import os
from dotenv import load_dotenv

#%%
load_dotenv()
CONSUMER_KEY = os.getenv('TWITTER_API_KEY')
CONSUMER_SECRET = os.getenv('TWITTER_API_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, callback="oob")

auth_url = auth.get_authorization_url()
print("Authorization URL: " + auth_url)

verifier = input("PIN: ").strip()
auth.get_access_token(verifier)

auth.set_access_token(auth.access_token, auth.access_token_secret)

api = tweepy.API(auth)

master_block = input("Type in the @ of the account you want to block!\n")
#%%
followers = set(api.followers_ids(master_block))
current_blocking = set(api.blocks_ids())
blockable = followers - current_blocking
for each_blockable_user in blockable:
    api.create_block(each_blockable_user)
api.create_block(master_block)
# %%
