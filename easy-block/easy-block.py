#%%
import tweepy
import os
from dotenv import load_dotenv
from tqdm import tqdm
#%%
load_dotenv()
CONSUMER_KEY = os.getenv('TWITTER_API_KEY')
CONSUMER_SECRET = os.getenv('TWITTER_API_SECRET')

if(CONSUMER_KEY and CONSUMER_SECRET):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, callback="oob")

    auth_url = auth.get_authorization_url()
    print("Authorization URL: " + auth_url)

    verifier = input("PIN: ").strip()
    auth.get_access_token(verifier)

    auth.set_access_token(auth.access_token, auth.access_token_secret)

    api = tweepy.API(auth)
    own_user_id = api.me().id
    user_friends = set(api.friends_ids(own_user_id))
    user_followers = set(api.followers_ids(own_user_id))
    answer = "y"
    while answer == "y":
        master_block = input("Type in the @ of the account you want to block!\n")
        #%%
        try:
            followers = set(api.followers_ids(master_block))
        except tweepy.TweepError:
            print("User unreachable!")
            continue
        current_blocking = set(api.blocks_ids())
        blockable = followers - current_blocking - user_friends - user_followers
        print(f"Now blocking {master_block}")
        for each_blockable_user in tqdm(blockable):
            try:
                api.create_block(each_blockable_user)
            except tweepy.TweepError:
                continue
        api.create_block(master_block)
        answer_ok = False
        while not answer_ok:
            answer = input("Do you wish to block another user and their followers? (y/n)\n").strip().lower()
            answer_ok = answer in "yn"
            if not answer_ok:
                print("Please input a correct answer.")

    # %%
else:
    print("Keys not present.")
