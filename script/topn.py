#! /usr/bin/env python
# --*-- coding:utf-8 --*--

__author__ = 'jeff.yu'

import sys
sys.path.append(sys.path[0].replace('/script', ''))

from base import Test
from common.parser import QueryProducer
from common.http import get_data
from common.tools import getMetricvalueData
import logging
import logging.config

class TopnTest(Test):

    def __init__(self, query):
        super(TopnTest, self).__init__(query)
        self.qop = QueryProducer(query)
        self.metricvalue = self.qop.get_topn_metricvalue()
        self.slice = self.qop.get_topn_threshold()
        self.noTopnQuery = self.qop.get_no_topn_query()


    def getNoTopnData(self):
        return get_data(self.noTopnQuery)

    def getExpected(self):
        no_topn_data = self.getNoTopnData()
        if not no_topn_data:
            return False
        dataIndex = no_topn_data[0].index(self.metricvalue)
        slice_no_topn_data = no_topn_data[1:][:self.slice]
        return getMetricvalueData(slice_no_topn_data, dataIndex)

    def getActual(self):
        dataIndex = self.http_data[0].index(self.metricvalue)
        return getMetricvalueData(self.http_data[1:], dataIndex)

    def _compare(self):
        actual = self.getActual()
        expected = self.getExpected()

        if actual == expected:
            return True
        else:
            return False

if __name__ == '__main__':
        tt = TopnTest('{"settings":{"time":{"start":1404201600,"end":1409558400,"timezone":0},"data_source":"contrack_druid_datasource_ds","report_id":"121212","pagination":{"size":1000000,"page":0}},"group":["ref_site"],"data":["clicks","outs","ctr","cr","income","cost","convs","roi","net"],"topn":{"metricvalue":"convs","threshold":50},"filters":{"$and":{}},"sort":[]}')
        print tt._compare()