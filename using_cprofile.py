#! /usr/bin/env python3

from random import random
from crypt import crypt
import sqlite3
import cProfile

salt = "$6$ZmBkxkRFj03LQOvr"  # Bad security, store safely
db = sqlite3.connect("passwords.db")
db.row_factory = sqlite3.Row  # Access columns by names


def user_passwd(user):
    """Get user password from db"""
    cur = db.cursor()
    cur.execute("SELECT passwd FROM users WHERE user = ?", (user,))
    row = cur.fetchone()
    if row is None:  # No such user
        raise KeyError(user)
    return row["passwd"]


def encrypt_passwd(passwd):
    """Encrypt user password"""
    return crypt(passwd, salt)


def login(user, password):
    """Return True is user/password pair matches"""
    try:
        db_passwd = user_passwd(user)
    except KeyError:
        return False

    passwd = encrypt_passwd(password)
    return passwd == db_passwd


def gen_cases(n):
    """Generate tests cases"""
    for _ in range(n):
        if random() > 0.1:  # 90% of logins are OK
            yield ("daffy", "rabbit season")
        else:
            if random() < 0.2:
                yield ("tweety", "puddy tat")  # no such user
            else:
                yield ("daffy", "duck season")


def bench_login(cases):
    """Benchmark login with test cases"""
    for user, passwd in cases:
        login(user, passwd)


if __name__ == "__main__":
    n = 100
    cases = list(gen_cases(n))
    # print(cases)
    # Change if statement to true to run the code
    if 0:
        # running cprofile in the terminal
        # python -m cProfile using_cprofile.py
        bench_login(cases)

    if 0:
        # running cProfile on test cases
        # https://docs.python.org/3/library/profile.html

        cProfile.run("bench_login(cases)")

    if 1:
        """
        Checking the contents of the file generated

        python -m pstats prof.out
            prof.out% stats top 10
            prof.out% sort cumtime
            prof.out% stats top 10
            
        https://docs.python.org/3/library/profile.html#module-pstats
        """
        cProfile.run("bench_login(cases)", filename="prof.out")
