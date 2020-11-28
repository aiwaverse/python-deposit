from pyfiglet import Figlet
from termcolor import cprint

def print_ascii_art(text,color_pick="magenta"):
    available_colors = (
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
    )
    if color_pick.lower() not in available_colors:
        raise ValueError("This color is unavailable")
    f = Figlet()
    cprint(f.renderText(text), color=color_pick)

