# -*- coding: utf-8 -*-

# Copyright (c) Gary Wilson Jr. <gary@thegarywilson.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
A re-implementation of the ldap module's cidict that inherits from dict instead
of UserDict so that we can, in turn, inherit from cidict.
"""


class cidict(dict):
    """
    Case-insensitive but case-respecting dictionary.
    """

    def __init__(self, default=None):
        self._keys = {}
        super(cidict, self).__init__({})
        self.update(default or {})

    def __getitem__(self, key):
        return super(cidict, self).__getitem__(key.lower())

    def __setitem__(self, key, value):
        lower_key = key.lower()
        self._keys[lower_key] = key
        super(cidict, self).__setitem__(lower_key, value)

    def __delitem__(self, key):
        lower_key = key.lower()
        del self._keys[lower_key]
        super(cidict, self).__delitem__(lower_key)

    def update(self, dict):
        for key in dict:
            self[key] = dict[key]

    def has_key(self, key):
        return super(cidict, self).has_key(key.lower())

    __contains__ = has_key

    def get(self, key, *args, **kwargs):
        return super(cidict, self).get(key.lower(), *args, **kwargs)

    def keys(self):
        return self._keys.values()

    def items(self):
        return [(k, self[k]) for k in self.keys()]
