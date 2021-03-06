#! /usr/bin/env python3

# https://pypi.org/project/line-profiler/
# https://github.com/pyutils/line_profiler

from random import random
from crypt import crypt
import sqlite3
import cProfile
from hashlib import sha256
from line_profiler import profile


salt = "$6$ZmBkxkRFj03LQOvr"  # Bad security, store safely
salt256 = salt.encode("utf-8")  # Convert to bytes
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


def encrypt_passwd2(passwd):
    """Encrypt password with sha256"""
    return sha256(passwd.encode("utf-8") + salt256).hexdigest()


@profile
def login_crypt(user, password):
    """Return True is user/password pair matches"""
    try:
        db_passwd = user_passwd(user)
    except KeyError:
        return False
    passwd = encrypt_passwd(password)
    return passwd == db_passwd


@profile
def login_sha256(user, password):
    """Return True is user/password pair matches"""
    try:
        db_passwd = user_passwd(user)
    except KeyError:
        return False

    passwd = encrypt_passwd2(password)
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


def bench_login_crypt(cases):
    """Benchmark login with test cases"""
    for user, passwd in cases:
        login_crypt(user, passwd)


def bench_login_sha256(cases):
    """Benchmark login with test cases"""
    for user, passwd in cases:
        login_sha256(user, passwd)


if __name__ == "__main__":
    n = 100
    cases = list(gen_cases(n))
    # print(cases)
    # Change "if statement" to true to run the code
    if 1:
        # running cprofile in the terminal
        # python -m cProfile using_cprofile.py
        # Also used with line_profiler
        """
        To view the file generated by line_profiler use the following 
        command at the cmd prompt:

        kernprof -l using_line_profiler.py
        python -m line_profiler using_line_profiler.py.lprof
        """
        bench_login_crypt(cases)
        bench_login_sha256(cases)
