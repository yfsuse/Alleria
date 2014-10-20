#! /usr/bin/env python
# --*-- coding:utf-8 --*--
__author__ = 'jeff.yu'

import json
from random import choice, randint


def recursion_del_key(del_dict, del_key):

    """
    :param del_dict: {"name": "yufeng", "info":{"age":25, "sex":"male"}}
    :param del_key: "sex"
    :return: {"name": "yufeng", "info":{"age":25}}
    """

    if not isinstance(del_dict, dict):
        print 'del key from del_dict error: del_dict is not instance of dict or json'
        exit(-1)

    dict_keys = del_dict.keys()
    for dict_key in dict_keys:
        value = del_dict.get(dict_key)
        if del_key == dict_key:
            del del_dict[del_key]
        else:
            if isinstance(value, dict):
                recursion_del_key(value, del_key)
            else:
                pass
    return del_dict

def listList_convert_listMap(listList):
    """
    :param listList: [["name", "age"], ["yufeng", 23]]
    :return: [{"name":"yufeng", "age":23}]
    """
    keys, values = listList[0], listList[1:]
    listMap = []
    for value in values:
        listMap.append(dict(zip(keys, value)))
    return listMap


def listGeneric_convert_listStr(listList):
    returnList = []
    for data in listList:
        try:
            strData = str(data)
        except ValueError as e:
            strData = data
        returnList.append(strData)
    return returnList

def vagueEquals(listA, listB):
    """
    :param listA: [1, u'', 212]
    :param listB: [u'1', u'', 212]
    :return: listA == listB ? True
    """
    return listGeneric_convert_listStr(listA) == listGeneric_convert_listStr(listB)


def mutichoice(seqlist):

    returnList = []
    seqListLen = len(seqlist)
    for i in range(randint(1, seqListLen)):
        select = choice(seqlist)
        if select not in returnList:
            returnList.append(select)
    return returnList

def makeDayList(beginYear, endYear, beginMonth, endMonth , beginDay):

    dayList = []
    for year in range(beginYear, endYear):
        for month in range(beginMonth, endMonth):
            for day in range(beginDay, 30):
                if day < 10:
                    strDay = '0{0}'.format(day)
                else:
                    strDay = str(day)

                if month < 10:
                    strMonth = '0{0}'.format(month)
                else:
                    strMonth = str(month)
                wholeDay = '{0}-{1}-{2}'.format(year, strMonth, strDay)
                dayList.append(wholeDay)
    return dayList


def toJsonList(dataSet):
    key = dataSet[0]
    values = dataSet[1:]
    returnData = []
    for value in values:
        data = dict(zip(key, value))
        returnData.append(data)
    return returnData


if __name__ == '__main__':
    pass
    # del_dict = {"settings":{"time":{"start":1411689600,"end":1411776000,"timezone":0},"process_type":"lp",
    #                         "report_id":"232sds3232","data_source":"contrack_druid_datasource_ds",
    #                         "pagination":{"size":1000000,"page":0}},
    #             "group":[],
    #             "data":["clicks","outs","ctr"],
    #             "filters":{"$and":{}},
    #             "sort":[]}
    # del_key = 'process_type'
    # print recursion_del_key(del_dict, del_key)
    # print listList_convert_listMap([[u'device_id', u'offer_id', u'clicks', u'outs', u'convs', u'income', u'cost', u'ctr', u'cr', u'roi', u'net'], [1, u'108', 286, 0, 0, 0.0, 445.344, 0.0, 0.0, -1.0, -445.344]])
    # print vagueEquals([1, u'', 212], [u'1', u'', 212])
    # print mutichoice(('year','month','day','week','hour'))
    # print makeDayList(2014,2015, 7, 10, 1)
