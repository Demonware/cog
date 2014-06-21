# -*- coding: utf-8 -*-

# Copyright (c) 2013, Activision Publishing, Inc.

# the cog project is free software under 3-clause BSD licence
# see the LICENCE file in the project root for copying terms

# miscellaneous utility functions, some of them borrowed

import os
import sys
import pwd
import random
import string

from functools import wraps
from passlib.hash import sha512_crypt


# encoding conversion functions
def to_utf8(obj):
    """
    Convert non-utf-8 bytestream or an unicode string to utf-8 bytestream.
    """
    local_encoding = sys.stdin.encoding
    if isinstance(obj, unicode):
        obj = obj.encode('utf-8')
    elif isinstance(obj, basestring) and local_encoding != 'utf-8':
        obj = obj.decode(local_encoding).encode('utf-8')
    return obj


def to_unicode(obj, encoding='utf-8'):
    """
    Convert bytestream to unicode.
    """
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj


def ensure_utf8(f):
    """
    Decorator - forces the wrapped function to return utf-8 bytestream.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        return to_utf8(f(*args, **kwargs))
    return decorated


# password & system helpers
@ensure_utf8
def randomized_string(size=16, chars=string.letters + string.digits + string.punctuation):
    # string.printable produces more than we can eat, unfortunately
    return ''.join(random.choice(chars) for x in range(size))


@ensure_utf8
def make_pass(passwd=None):
    """
    Generate password using SHA-512 method, randomized salt and randomized
    number of rounds.
    """
    if passwd is None:
        passwd = randomized_string(17)
    salt = randomized_string(16, ('./' + string.letters + string.digits))
    iterations = random.randint(40000, 80000)
    return '{CRYPT}' + sha512_crypt.encrypt(passwd, salt=salt, rounds=iterations)


@ensure_utf8
def get_current_uid():
    """
    Return the owner of the cog process.
    """
    return pwd.getpwuid(os.getuid()).pw_name


# data structure helpers
def flatten_list(messy_list):
    # <http://stackoverflow.com/a/952914>
    return [item for sublist in messy_list for item in sublist]


def merge(d1, d2):
    # stack overflow <http://stackoverflow.com/a/8310229/218563>
    for k1, v1 in d1.iteritems():
        if not k1 in d2:
            d2[k1] = v1
        elif isinstance(v1, list):
            d2[k1] = list(set(d2[k1] + v1))
        elif isinstance(v1, dict):
            merge(v1, d2[k1])
    return d2


def apply_to(dct, f):
    """
    Apply a function to dictionary-like object values, recursively.
    """
    for key in dct:
        if isinstance(dct[key], dict):
            dct[key] = apply_to(dct.get(key), f)
        else:
            dct[key] = f(dct[key])
    return dct


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
