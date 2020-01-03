import requests as req
from fun_texts import print_ascii_art
from operator import itemgetter
from random import choice


def get_jokes(themes):
    url = "https://icanhazdadjoke.com/search"
    response = req.get(
        url,
        headers={"Accept": "application/json"},
        params={"term": themes, "limit": 30},
    )
    return response.json()["results"]


if __name__ == "__main__":
    print_ascii_art("Dad Jokes 3000")
    joke_theme = input("What's the theme of the joke you wanna search?\n")
    response = get_jokes(joke_theme)
    number_of_jokes = len(response)
    if number_of_jokes > 1:
        print(f"I got {len(response)} jokes about {joke_theme}, here's one:")
    else:
        print(f"I got one joke about {joke_theme}, here it is:")
    jokes = list(map(itemgetter("joke"), response))
    joke_choice = choice(jokes)
    print(joke_choice)

