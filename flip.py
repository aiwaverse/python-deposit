from functools import wraps, partial


def flip(fn):
    """Create a new function from the original with the arguments reversed, only for two argument functions"""

    @wraps(fn)
    def wrapper(x, y):
        return fn(y, x)

    return wrapper


if __name__ == "__main__":
    correct_isinstance = flip(isinstance)
    lis = [1, 2, 3, 4, 5, "6", 7, 8]
    is_int = partial(correct_isinstance, int)
    print(all(map(is_int, lis)))

