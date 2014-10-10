#! /usr/bin/env python
# --*-- coding:utf-8 --*--

__author__ = 'jeff.yu'

import sys
sys.path.append(sys.path[0].replace('/script', ''))

from base import Test
from common.parser import QueryProducer
from common.http import get_data
import logging
import logging.config

class TopnTest(Test):

    def __init__(self, query):
        super(TopnTest, self).__init__(query)
        self.qop = QueryProducer(query)
        logging.config.fileConfig("../config/logging.ini")
        self.log_identifier = "topn"
        self.logger = logging.getLogger("alleria")
        self.slice = self.qop.get_topn_threshold()

    def getNoTopnData(self):

        noTopnQuery = self.qop.get_no_topn_query()
        return get_data(noTopnQuery)

    def _compare(self):
        no_topn_data = self.getNoTopnData()[:self.slice]
        topn_data = self.http_data
        if topn_data == no_topn_data:
            return True
        else:
            self.logger.error("""[{0}] topn test failed:
{1}
{2}
{3}""".format(self.log_identifier, self.query, topn_data, no_topn_data))

if __name__ == '__main__':
        tt = TopnTest('{"settings":{"time":{"start":1404172800,"end":1409529600,"timezone":0},"data_source":"contrack_druid_datasource_ds", "report_id":"121212","pagination":{"size":1000000,"page":0}},"group":["year","week","offer_id"],"topn":{"metricvalue":"clicks","threshold":10},"data":["clicks","outs","ctr","cr","income","cost","convs","roi","net"],"filters":{"$and":{}},"sort":[]}')
        tt._compare()