#%%
from typing import Set, Tuple, Union, List
import tweepy
import os
from dotenv import load_dotenv
from tqdm import tqdm
import time

#%%
def get_keys() -> Tuple[Union[str, None], Union[str, None]]:
    load_dotenv()
    key = os.getenv("TWITTER_API_KEY")
    secret = os.getenv("TWITTER_API_SECRET")
    return (key, secret)


#%%
def authenticate_user(key: str, secret: str) -> tweepy.API:
    auth = tweepy.OAuthHandler(key, secret, callback="oob")
    auth_url = auth.get_authorization_url()
    print("Authorization URL: " + auth_url)
    verifier = input("PIN: ").strip()
    if not verifier:
        raise IOError("Incorret PIN format!")
    auth.get_access_token(verifier)
    auth.set_access_token(auth.access_token, auth.access_token_secret)
    return tweepy.API(auth)


#%%
def read_blocks_file() -> List[str]:
    blocks: List[str] = []
    if os.path.exists("user_blocks.txt"):
        with open("user_blocks.txt", "r") as f:
            blocks = f.read().splitlines()
    return blocks


#%%
def get_user_info(user: tweepy.API) -> Tuple[Set[str], Set[str], Set[str]]:
    user_friends = []
    for friend in tweepy.Cursor(user.friends_ids).pages():
        user_friends += friend
    user_followers = []
    for follower in tweepy.Cursor(user.followers_ids).pages():
        user_followers += follower
    user_blocks = read_blocks_file()
    if not user_blocks:
        for block in tweepy.Cursor(user.blocks_ids).pages():
            user_blocks += block
    return (set(user_friends), set(user_followers), set(user_blocks))


#%%
def get_blocking_information(
    api: tweepy.API, user_masterblock: str
) -> Union[None, Set[str]]:
    try:
        # followers = set(api.followers_ids(user_masterblock))
        followers = []
        for follower in tweepy.Cursor(api.followers_ids, id=user_masterblock).pages():
            followers += follower
        followers.append(api.get_user(user_masterblock).id)
    except tweepy.TweepError:
        print("User unreachable!")
        return None
    return set(followers)


#%%
def generate_blocking_list(
    api: tweepy.API, user_masterblock: str
) -> Union[None, Set[str]]:
    friends, followers, blocks = get_user_info(api)
    blocklist = get_blocking_information(api, user_masterblock)
    if blocklist:
        blocklist = blocklist - friends - followers - blocks
        save_user_blocks(blocks, blocklist)
        return blocklist
    else:
        return None


#%%
def block_users(api: tweepy.API, blocklist: Set[str]) -> None:
    for user in tqdm(blocklist):
        try:
            api.create_block(user)
        except tweepy.TweepError:
            continue


#%%
def do_again() -> bool:
    answer_ok = False
    answer = ""
    while not answer_ok:
        answer = (
            input("Do you wish to block another user and their followers? (y/n)\n")
            .strip()
            .lower()
        )
        answer_ok = answer in "yn"
        if not answer_ok:
            print("Please input a correct answer.")
    if answer == "y":
        return True
    else:
        return False

#%%
def save_user_blocks(user_blocks: Set[str], blocklist: Set[str]) -> None:
    if not os.path.exists("user_blocks.txt"):
        with open("user_blocks.txt", "w") as f:
            for block in user_blocks:
                f.write(f"{block}\n")
    with open("user_blocks.txt", "a") as f:
        for block in blocklist:
            f.write(f"{block}\n")


#%%

if __name__ == "__main__":
    CONSUMER_KEY, CONSUMER_SECRET = get_keys()
    if not CONSUMER_KEY or not CONSUMER_SECRET:
        raise ValueError("Keys not found on .env!")
    api = authenticate_user(CONSUMER_KEY, CONSUMER_SECRET)
    keep_going = True
    while keep_going:
        to_block = input("Type in the @ of the account you want to block!\n").strip()
        if not to_block:
            raise ValueError("Empty input, please try again.")
        print("Generating blocklist...")
        try:
            blocklist = generate_blocking_list(api, to_block)
        except tweepy.RateLimitError:
            print(
                "The API has reach the request limit, please wait 15 minutes before trying again."
            )
            print("The program will wait for you, press Ctrl+C to leave.")
            time.sleep(60 * 15)
            continue
        if not blocklist:
            raise ValueError(
                "Blocklist couldn't be generated, check if the @ is correct"
            )
        print("Blocking users...")
        block_users(api, blocklist)
        keep_going = do_again()

