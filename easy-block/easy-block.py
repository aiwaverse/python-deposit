#%%
from typing import Set, Tuple, Union
import tweepy
import os
from dotenv import load_dotenv
from tqdm import tqdm
import sys

#%%
def get_keys() -> Tuple[Union[str, None], Union[str, None]]:
    load_dotenv()
    key = os.getenv("TWITTER_API_KEY")
    secret = os.getenv("TWITTER_API_SECRET")
    return (key, secret)


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


def get_user_info() -> Tuple[Set[str], Set[str], Set[str]]:
    user_friends = set(api.friends_ids())
    user_followers = set(api.followers_ids())
    user_blocks = set(api.blocks_ids())
    return (user_friends, user_followers, user_blocks)


def get_blocking_information(user_masterblock: str) -> Union[None, Set[str]]:
    try:
        followers = set(api.followers_ids(user_masterblock))
    except tweepy.TweepError:
        print("User unreachable!")
        return None
    else:
        followers.add(user_masterblock)
        return followers


def generate_blocking_list(user_masterblock: str) -> Union[None, Set[str]]:
    friends, followers, blocks = get_user_info()
    blocklist = get_blocking_information(user_masterblock)
    if blocklist:
        return blocklist - friends - followers - blocks
    else:
        return None


def block_users(blocklist: Set[str]) -> None:
    for user in tqdm(blocklist):
        try:
            api.create_block(user)
        except tweepy.TweepError:
            continue


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
        blocklist = generate_blocking_list(to_block)
        if not blocklist:
            raise ValueError(
                "Blocklist couldn't be generated, check if the @ is correct"
            )
        block_users(blocklist)
        keep_going = do_again()

