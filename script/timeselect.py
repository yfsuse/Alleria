#! /usr/bin/env python
# --*-- coding:utf-8 --*--

__author__ = 'jeff.yu'

from base import Test
from common.parser import QueryProducer
from common.tools import toJsonList, equals, getMongoFilter
from common.http import get_data
from common.dao import Pydbc
from common.producer import get_timeselect_case


class TimeSelectTest(Test):

    """
    use mongodb
    """
    def __init__(self, query):
        super(TimeSelectTest, self).__init__(query)
        self.actual = toJsonList(self.http_data)
        self.qop = QueryProducer(query)
        self.dao = Pydbc()
        self.setExpect()

    def setExpect(self):
        mongodbFilter = self.qop.get_filters()
        noFilterQuery = self.qop.getNoFilterQuery()
        noFilterData = get_data(noFilterQuery)
        jsonListData = toJsonList(noFilterData)
        if not jsonListData:
            self.expected = []
        else:
            self.dao.insertCollection(jsonListData)
            mongoFilter = getMongoFilter(mongodbFilter)
            self.expected = self.dao.queryCollection(mongoFilter)

    def getExpected(self):
        return self.expected

    def getActual(self):
        return self.actual

    def _compare(self):

        if equals(self.getActual(), self.getExpected()):
            return True
        else:
            return False


if __name__ == '__main__':
    case = '{"settings":{"time":{"start":1404172800,"end":1412121600,"timezone":0},"data_source":"ymds_druid_datasource","report_id":"121212","pagination":{"size":1000000,"page":0}},"group":["cpa","year","month"],"data":["click","conversion"],"filters":{"$and":{"month":{"$eq":"Sep"}}},"sort":[]}'
    case_b = '{"settings":{"time":{"start":1404172800,"end":1412121600,"timezone":0},"data_source":"ymds_druid_datasource","report_id":"121212","pagination":{"size":1000000,"page":0}},"group":["adv_sub3","hour","year"],"data":["click","conversion"],"filters":{"$and":{"year":{"$neq":"2013"}}},"sort":[]}'
    tst = TimeSelectTest(case_b)
    print tst._compare()