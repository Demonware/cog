# -*- coding: utf-8 -*-

# Copyright (c) 2013, Activision Publishing, Inc.

# the cog project is free software under 3-clause BSD licence
# see the LICENCE file in the project root for copying terms

# miscellaneous utility functions, mostly borrowed

import os
import sys
import pwd
import string
import re
import random
import crypt

from passlib.hash import sha512_crypt

def randomized_string(size=16, chars=string.letters + string.digits + string.punctuation):
    # string.printable produces more than we can eat, unfortunately
    return ''.join(random.choice(chars) for x in range(size))

def make_pass(passwd=None):
    # generate password using crypt()'s SHA-512 method, randomized salt and
    # randomized number of rounds.
    if passwd is None:
        passwd = randomized_string(17)
    salt = randomized_string(16, ( './' + string.letters + string.digits))
    iterations = random.randint(40000, 80000)
    return '{CRYPT}' + sha512_crypt.encrypt(passwd, salt=salt, rounds=iterations)

def get_current_uid():
    return pwd.getpwuid(os.getuid()).pw_name

def flatten_list(messy_list):
    # <http://stackoverflow.com/a/952914>
    return [item for sublist in messy_list for item in sublist]

def merge(d1, d2):
    # stack overflow <http://stackoverflow.com/a/8310229/218563>
    for k1,v1 in d1.iteritems():
        if not k1 in d2:
            d2[k1] = v1
        elif isinstance(v1, list):
            d2[k1] = list(set(d2[k1] + v1))
        elif isinstance(v1, dict):
            merge(v1, d2[k1])
    return d2

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

