#! /usr/bin/env python
# --*-- coding:utf-8 --*--

__author__ = 'jeff.yu'

from base import Test
from common.parser import QueryProducer
from common.tools import toJsonList
from common.http import get_data
from common.dao import Pydbc
from common.producer import get_timeselect_case
from string import letters
from string import digits

class TimeSelectTest(Test):

    """
    use mongodb
    """
    def __init__(self, query):
        super(TimeSelectTest, self).__init__(query)
        self.qop = QueryProducer(query)
        self.dao = Pydbc()
        self.getExpect()

    def getExpect(self):
        noFilterQuery = self.qop.getNoFilterQuery()
        noFilterData = get_data(noFilterQuery)
        jsonListData = toJsonList(noFilterData)
        mongodbFilter = self.qop.get_filters()
        self.dao.insertCollection(jsonListData)
        self.expectData = self.dao.queryCollection(mongodbFilter)

    def _compare(self):

        realData = toJsonList(self.http_data)
        print realData
        print self.expectData

        if set(realData) == set(self.expectData):
            return True
        else:
            return False


if __name__ == '__main__':
    caseList = get_timeselect_case()
    for case in caseList:
        print case
        tst = TimeSelectTest(case)
        print tst._compare()
        break