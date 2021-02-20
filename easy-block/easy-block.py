#%%
import tweepy
import os

#%%
consumer_key = "E5B3Ou0yYXE9AVUgQTSHxPjM8"
consumer_secret = "7WiOeUt6EgJDzOKxChXMecMQ26rjfi9durdmEsei34LLBNMnjO"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback="oob")

auth_url = auth.get_authorization_url()
print("Authorization URL: " + auth_url)

verifier = input("PIN: ").strip()
auth.get_access_token(verifier)

auth.set_access_token(auth.access_token, auth.access_token_secret)

api = tweepy.API(auth)
#%%
followers = set(api.followers_ids("mandarafact"))
current_blocking = set(api.blocks_ids())
blockable = followers - current_blocking
for each_blockable_user in blockable:
    api.create_block(each_blockable_user)

# %%
