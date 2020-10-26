#! /usr/bin/env python3

from timeit import timeit

# https://docs.python.org/3/library/timeit.html
# https://docs.python.org/3/library/timeit.html#timeit.timeit

items = {"a": 1, "b": 2}
default = -1


def use_catch(key):
    """Use try/catch to get a key with default"""
    try:
        return items[key]
    except KeyError:
        return default


def use_get(key):
    """Use dict.get to get a key with default"""
    return items.get(key, default)


if __name__ == "__main__":
    # Key is in the dictionary
    print(
        "catch - Key in dict",
        timeit('use_catch("a")', "from __main__ import use_catch"),
    )
    print("get - Key in dict", timeit('use_get("a")', "from __main__ import use_get"))

    # Key is missing from the dictionary
    print(
        "catch - Key not in dict",
        timeit('use_catch("x")', "from __main__ import use_catch"),
    )
    print(
        "get - Key not in dict", timeit('use_get("x")', "from __main__ import use_get")
    )
