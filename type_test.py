import typing
import toolz


def some_func(arg: str) -> int:
    return int(arg)


data = [1, "a", "b", 2, 1.5, object(), 3]
only_ints = list(filter(toolz.flip(isinstance, int), data))
print(only_ints)
