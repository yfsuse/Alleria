#! /usr/bin/env python
# --*-- coding : utf-8 --*--

__author__ = 'jeff.yu'

import sys
sys.path.append(sys.path[0].replace('/script', ''))


from common.producer import *
from sort import SortTest
from page import PageTest
from common.parser import QueryProducer
import ConfigParser
from time import ctime, strftime, localtime


def run_sort(islp = False, check_level = "low", runcount = 5):

    case_list = get_sort_cases(islp)
    suffix = strftime("%Y-%m-%d-%H_%M_%S", localtime())

    if islp:
        success_log = '../log/sortlp.success.log.{0}'.format(suffix)
    else:
        success_log = '../log/sort.success.log.{0}'.format(suffix)

    suc_handler = open(success_log, 'w')
    count = 0
    cases = case_list[slice(None, runcount)]
    for case in cases:
        positive_case_result = SortTest(case, check_level, islp)
        negative_case = QueryProducer(case).get_reverse_order()
        negative_case_result = SortTest(negative_case, islp)
        if negative_case_result == positive_case_result:
            suc_handler.writelines(case + '\n')
        else:
            pass
        count += 1
        if islp:
            print ctime() + " run lp sort case at : ", count
        else:
            print ctime() + " run sort case at : ", count
    suc_handler.close()


def run_page(islp = False, check_level = "low", runcount = 5):

    case_list = get_page_cases(islp)
    suffix = strftime("%Y-%m-%d-%H_%M_%S", localtime())

    if islp:
        success_log = '../log/pagelp.success.log.{0}'.format(suffix)
    else:
        success_log = '../log/page.success.log.{0}'.format(suffix)

    suc_handler = open(success_log, 'w')
    count = 0
    cases = case_list[slice(None, runcount)]
    for case in cases:
        negative_case_result = PageTest(case, check_level, islp)
        positive_case = QueryProducer(case).get_no_page_query()
        positive_case_result = PageTest(positive_case, islp)
        if negative_case_result == positive_case_result:
            suc_handler.writelines(case + '\n')
        else:
            pass
        count += 1
        if islp:
            print ctime() + " run lp page case at : ", count
        else:
            print ctime() + " run page case at : ", count
    suc_handler.close()


def runner():
    config_parser = ConfigParser.ConfigParser()
    config_parser.read('../config/running.ini')
    level = config_parser.get('check_rule', 'check_level')
    sort_count = int(config_parser.get('sort', 'runcasecount'))
    sort_lp_count = int(config_parser.get('sortlp', 'runcasecount'))
    page_count = int(config_parser.get('page', 'runcasecount'))
    page_lp_count = int(config_parser.get('pagelp', 'runcasecount'))

    run_sort(islp=True, check_level=level, runcount=sort_lp_count)
    run_sort(islp=False, check_level=level, runcount=sort_count)
    run_page(islp=False, check_level=level, runcount=page_count)
    run_page(islp=True, check_level=level, runcount=page_lp_count)


if __name__ == '__main__':
    runner()