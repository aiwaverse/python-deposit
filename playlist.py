playlist = {
    "title": "agatha's playlist",
    "auhor": "aiwaverse",
    "songs": [
        {"title": "Cool World", "artist": ["Red Velvet"], "duration": 3.0},
        {
            "title": "Cool World Gee's remix",
            "artist": ["Red Velvet", "Gee"],
            "duration": 3.5,
        },
        {
            "title": "The Miha",
            "artist": ["chisato moritaka".title()],
            "duration": 5.35,
        },
    ],
}

i = 1
for song in playlist["songs"]:
    print(f"Song nº {i}")
    i += 1
    print(f"Title: {song['title']}")
    print("Artists: ", end="")
    print(", ".join(song["artist"]), end="")
    print(f"\nDuration: {song['duration']}\n")
