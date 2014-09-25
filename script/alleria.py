__author__ = 'jeff.yu'


#! /usr/bin/env python
# --*-- coding : utf-8 --*--


from common.producer import get_cases
from sort import SortTest
from common.parser import QueryProducer


def run():

    err_handler = open('../output/trading_desk.error.log', 'w')
    suc_handler = open('../output/trading_desk.success.log', 'w')
    count = 0
    case_list = get_cases()
    for case in case_list[:10]:
        positive_case_result = SortTest(case)
        negative_case = QueryProducer(case).get_reverse_order()
        negative_case_result = SortTest(negative_case)
        if negative_case_result == positive_case_result:
            suc_handler.writelines(case + '\n')
        else:
            err_handler.writelines(case + '\n')
        count += 1
        print count

    err_handler.close()
    suc_handler.close()

if __name__ == '__main__':
    run()


