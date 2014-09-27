#! \usr\bin\env python
# --*-- coding:utf-8 --*--

__author__ = 'jeff.yu'



import sys
sys.path.append(sys.path[0].replace('/script', ''))

from common.parser import QueryProducer
from base import Test
import logging
import logging.config
from common.dataconv import sub_seq


class SortTest(Test):

    def __init__(self, query, check_level = "low", islp = False):
        logging.config.fileConfig("../config/logging.ini")
        self.logger = logging.getLogger("alleria")
        self.check_level = check_level
        if islp:
            self.log_identifier = "SortLp"
        else:
            self.log_identifier = "Sort"
        super(SortTest, self).__init__(query)

    def get_orderdata_list(self):
        qp = QueryProducer(self.query)
        orderBy = qp.get_order_key()
        try:
            order_index = self.http_data[0].index(orderBy)
        except TypeError as e:
            return None
        except ValueError as e:
            order_index = len(qp.get_group()) + qp.get_data().index(orderBy) - 1
        print order_index
        orderdata = []
        for dataset in self.http_data[1:]:
            orderdata.append(dataset[order_index])
        return orderdata

    def __eq__(self, other):

        reverse_data = other.get_orderdata_list()
        if reverse_data == None:
            return False
        reverse_data.reverse()
        order_data_list = self.get_orderdata_list()
        if order_data_list == None:
            return False
        return sub_seq(reverse_data, order_data_list)


if __name__ == '__main__':
    query = '{"settings":{"time":{"start":1404172800,"end":1409529600,"timezone":0},"data_source":"contrack_druid_datasource_ds","report_id":"121212","pagination":{"size":1000000,"page":0}},"group":["year","week","offer_id"],"data":["clicks","outs","ctr","cr","income","cost","convs","roi","net"],"filters":{"$and":{"offer_id":{"$eq":-1}}},"sort":[{"orderBy":"clicks","order":-1}]}'
    reverse_query = QueryProducer(query).get_reverse_order()
    query_obj = SortTest(query)
    reverse_query_obj = SortTest(reverse_query)
    if query_obj == reverse_query_obj:
        print "equal"