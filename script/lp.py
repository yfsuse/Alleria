#! /usr/bin/env python
# --*-- coding:utf-8 --*--

__author__ = 'jeff.yu'

import sys
sys.path.append(sys.path[0].replace('/script', ''))

from base import Test


class Lp(Test):

    def __init__(self, query):
        super(Lp, self).__init__(query)