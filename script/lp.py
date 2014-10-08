#! /usr/bin/env python
# --*-- coding:utf-8 --*--

__author__ = 'jeff.yu'

import sys
sys.path.append(sys.path[0].replace('/script', ''))

from common.parser import QueryProducer
from common.producer import get_lp_case
import logging
import logging.config
from common.http import get_data
from common.tools import listList_convert_listMap, listGeneric_convert_listStr
from base import Test


class LpTest(Test):

    def __init__(self, query):
        super(LpTest, self).__init__(query)
        self.qp = QueryProducer(self.query)
        self.groupKey = self.qp.get_group()
        logging.config.fileConfig("../config/logging.ini")
        self.log_identifier = "lp"
        self.logger = logging.getLogger("alleria")

    def get_no_lp_data(self):
        no_lp_query = self.qp.get_no_lp_query()
        return get_data(no_lp_query)

    @property
    def isSuccess(self):
        self.groupKey.remove("offer_id")
        lpKeys = self.groupKey
        no_lp_data_list = self.get_no_lp_data()
        lp_data_list = self.http_data
        lp_data_map = listList_convert_listMap(lp_data_list)
        no_lp_data_map = listList_convert_listMap(no_lp_data_list)

        selectLpValueList = []
        for lp_data in lp_data_map:
            selectLpValues = []
            for lpKey in lpKeys:
                selectLpValues.append(lp_data.get(lpKey))
            selectLpValues.append(lp_data.get('clicks'))
            selectLpValueList.append(selectLpValues)

        selectNoLpValueList = []
        for no_lp_data in no_lp_data_map:
            selectNoLpValues = []
            for lpKey in lpKeys:
                selectNoLpValues.append(no_lp_data.get(lpKey))
            selectNoLpValues.append(no_lp_data.get('clicks'))
            selectNoLpValueList.append(selectNoLpValues)

        selectNoLpValueList = [listGeneric_convert_listStr(data) for data in selectNoLpValueList]
        for selectLpValue in selectLpValueList:
            if listGeneric_convert_listStr(selectLpValue) in selectNoLpValueList:
                continue
            else:
                self.logger.error(""" lp clicks not equal to no lp clicks:
                                      {1}
                """.format(self.query))
                return False
        return True

if __name__ == '__main__':
    lp_case_list = get_lp_case()
    for case in lp_case_list[:50]:
        lt = LpTest(case)
        print lt._compare()
