#!/usr/bin/env python3
import random
import re
import argparse


def read_confusables_file(path):
    with open(path, "r") as brute_confusables_text:
        lines = brute_confusables_text.readlines()
        lines = list(
            filter(
                lambda l: "latin small letter".upper() in l
                and "combining".upper() not in l,
                lines,
            )
        )
        return_dict = {}
        for line in lines:
            matched_text = re.search(r"\(.*\)", line)
            if not matched_text:
                continue
            letters = list(
                filter(
                    lambda s: s.isalnum(), matched_text.group()[2:-2].replace("→", "")
                )
            )
            if len(letters) == 2:
                if letters[1] not in return_dict:
                    return_dict[letters[1]] = []
                return_dict[letters[1]].append(letters[0])
    return return_dict


def confusable_word(confusable_dictionary, word):
    result = ""
    for letter in word:
        if letter in confusable_dictionary:
            result += random.choice(confusable_dictionary[letter.lower()])
        else:
            result += letter
    return result


def parse_arguments():
    parser = argparse.ArgumentParser(description="Create a confusable version of text.")
    parser.add_argument(
        "--words",
        metavar="-W",
        dest="words",
        type=str,
        nargs="+",
        help="the words to change",
    )
    parser.add_argument(
        "path",
        help="The path words the confusables text from unicode",
        type=str,
        nargs="?",
        default="",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    try:
        word_dict = read_confusables_file(args.path)
    except OSError:
        print("Incorrect file path")
    else:
        changed_words = []
        for word in args.words:
            changed_words.append(confusable_word(word_dict, word))
        words_on_string = "\n".join(changed_words)
        print(words_on_string)
