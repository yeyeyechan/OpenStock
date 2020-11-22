from src.com.stock.common.import_lib import *


def integrity_db_count(startdate, enddate, totla_count):
    date_list = get_kr_working_day(startdate, enddate)

    len_date_list = len(date_list)

    expected_all_cocunt = len_date_list*totla_count
    expected_each_count = len_date_list

    return [expected_each_count , expected_all_cocunt]


def check_each_count(real_count, expected_count, logging_string):
    if real_count != expected_count:
        myLogger.debug(logging_string)
