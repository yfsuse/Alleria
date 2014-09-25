__author__ = 'jeff.yu'

#! /usr/bin/env python
# --*-- coding:utf-8 --*--

from common.http import get_data
from common.parser import QueryProducer
import logging


logger = logging.getLogger("endlesscode")
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', '%d %b %Y %H:%M:%S')
file_handler = logging.FileHandler("../output/compare.debug.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)



class SortTest(object):

    def __init__(self, query):
        self.query = query
        self.http_data = get_data(self.query)
        self.http_len_data = len(self.http_data)


    def get_len_data(self):
        return len(self.http_data)

    def get_orderdata_list(self):
        orderBy = QueryProducer(self.query).get_order_key()
        order_index = self.http_data[0].index(orderBy)
        orderdata = []
        for dataset in self.http_data[1:]:
            orderdata.append(dataset[order_index])
        return orderdata

    def __cmp__(self, other):

        if self.http_len_data == other.http_len_data:
            if len(set(str(self.http_data)) - set(str(other.http_data))) == 0: # if not str() then unhashable type: 'list' raised
                reverse_data = other.get_orderdata_list()
                reverse_data.reverse()
                order_data_list = self.get_orderdata_list()
                if order_data_list == reverse_data:
                    return 0
                else:
                    logger.debug("""Data Order Not Equal: {0}
                                                    {1}\n\n""".format(order_data_list, reverse_data))
                    return -1
            else:
                logger.debug('data set not equal')
                return -1
        else:
            logger.debug('data len not equal\n')
            return -1

if __name__ == '__main__':
    query = '{"settings":{"time":{"start":1404172800,"end":1409529600,"timezone":0},"data_source":"contrack_druid_datasource_ds","report_id":"121212","pagination":{"size":1000000,"page":0}},"group":["year","week","offer_id"],"data":["clicks","outs","ctr","cr","income","cost","convs","roi","net"],"filters":{"$and":{"offer_id":{"$eq":-1}}},"sort":[{"orderBy":"clicks","order":-1}]}'
    reverse_query = QueryProducer(query).get_reverse_order()
    query_obj = SortTest(query)
    reverse_query_obj = SortTest(reverse_query)
    if query_obj == reverse_query_obj:
        print "equal"