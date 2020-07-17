from toolz import compose, partial


def statistics(file):
    with open(file, "r") as r:
        lines = r.readlines()
        return {
            "lines": len(lines),
            "words": sum((len(line.split(" ")) for line in lines)),
            "character" : sum((len(line) for line in lines))
        }


if __name__ == "__main__":
    print(statistics("story.txt"))
