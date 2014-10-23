#! /usr/bin/env python
# --*-- coding : utf-8 --*--

__author__ = 'jeff.yu'

import sys
sys.path.append(sys.path[0].replace('/script', ''))


from common.producer import *
from sort import SortTest
from page import PageTest
from lp import LpTest
from topn import TopnTest
from timeselect import TimeSelectTest
from common.parser import QueryProducer
import ConfigParser
from time import ctime, strftime, localtime
import logging


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


def run_page(islp=False, check_level="low", runcount = 5):

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


def run_topn(runcount = 5):
    case_list = get_topn_case()
    suffix = strftime("%Y-%m-%d-%H_%M_%S", localtime())
    success_log = '../log/topn.success.log.{0}'.format(suffix)
    suc_handler = open(success_log, 'w')
    count = 0
    cases = case_list[slice(None, runcount)]
    sumCount = len(cases)
    logging.config.fileConfig("../config/logging.ini")
    logger = logging.getLogger("root")
    print 'Get case count: {0}\n'.format(sumCount)
    for case in cases:
        lt = TopnTest(case)
        if lt._compare():
            suc_handler.writelines(case + '\n')
        else:
            actual = lt.getActual()
            expected = lt.getExpected()
            logger.error(" >> [topn Error] {0}\nActual: {1}\nExpected: {2}\n ".format(case, actual, expected))
        count += 1
        print ctime() + "Run topn case at : {0}/{1}".format(count, sumCount)
    suc_handler.close()


def run_lp(runcount = 5):
    case_list = get_lp_case()
    suffix = strftime("%Y-%m-%d-%H_%M_%S", localtime())
    success_log = '../log/lp.success.log.{0}'.format(suffix)
    suc_handler = open(success_log, 'w')
    count = 0
    cases = case_list[slice(None, runcount)]
    sumCount = len(cases)
    for case in cases:
        lt = LpTest(case)
        if lt.isSuccess:
            suc_handler.writelines(case + '\n')
        count += 1
        print ctime() + " run lp case at : {0}/{1}".format(count, sumCount)
    suc_handler.close()


def run_timeselect(runcount = 5):
    caseList = get_timeselect_case()
    suffix = strftime("%Y-%m-%d-%H_%M_%S", localtime())
    success_log = '../log/timeFilter.success.log.{0}'.format(suffix)
    suc_handler = open(success_log, 'w')
    count = 1
    cases = caseList[slice(None, runcount)]
    sumCount = len(cases)
    logging.config.fileConfig("../config/logging.ini")
    logger = logging.getLogger("root")
    for case in cases:
        tst = TimeSelectTest(case)
        isEquals = tst._compare()
        if isEquals:
            suc_handler.writelines(case + '\n')
        else:
            actual = tst.getActual()
            expected = tst.getExpected()
            logger.error(" >> [timeFilter Error] {0}\nactual:{1}\nexpected:{2} ".format(case, actual, expected))
        print ctime() + " Run timeselect case at : {0}/{1}".format(count, sumCount)
        count += 1
    suc_handler.close()


def runner():
    config_parser = ConfigParser.ConfigParser()
    config_parser.read('../config/running.ini')
    level = config_parser.get('check_rule', 'check_level')
    try:
        sort_count = int(config_parser.get('sort', 'runcasecount'))
        sort_lp_count = int(config_parser.get('sortlp', 'runcasecount'))
        page_count = int(config_parser.get('page', 'runcasecount'))
        page_lp_count = int(config_parser.get('pagelp', 'runcasecount'))
        lp_count = int(config_parser.get('lp', 'runcasecount'))
        topn_count = int(config_parser.get('topn', 'runcasecount'))
        timeSelect_count = int(config_parser.get('timefilter', 'runcasecount'))
    except ValueError as e:
        sort_count, sort_lp_count, page_count, page_lp_count, lp_count, topn_count, timeselectcount = None, None, None, None, None, None, None


    # run_sort(islp=True, check_level=level, runcount=sort_lp_count)
    # run_sort(islp=False, check_level=level, runcount=sort_count)
    # run_page(islp=False, check_level=level, runcount=page_count)
    # run_page(islp=True, check_level=level, runcount=page_lp_count)
    # run_lp(lp_count)
    run_topn(topn_count)
    run_timeselect(timeSelect_count)

if __name__ == '__main__':
    runner()