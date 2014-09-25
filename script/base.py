__author__ = 'jeff.yu'

#! /usr/bin/env python
# --*-- coding = utf-8 --*--

from common.http import get_data


class Test(object):

    def __init__(self, query):
        self.query = query
        self.http_data = get_data(self.query)
        try:
            self.http_len_data = len(self.http_data)
        except Exception as e:
            self.http_len_data = 0

    def get_len_data(self):
        return len(self.http_data)

    def __eq__(self, other):
        pass

    def __str__(self):
        pass
