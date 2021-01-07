# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\OpenStock")
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari


def call_TR_SCHART():
    print("sibal")
    TR_SCHART(type = 'search',start_date='20200112', end_date='20200115')
    #TR_SCHART(type = 'real_time')

def TR_SCHART_JOB():

    sched_sc = BlockingScheduler()
    sched_sc.add_job(call_TR_SCHART, CronTrigger(hour='2-3', minute='*/1'))
    sched_sc.start()
if __name__ == "__main__":
    target_date = "20210107"
    check = True
    TR_1206 = make_collection("stock_data", "TR_1206")
    date = TR_1206.find_one({"단축코드" : "055550"}, sort=[("일자", pymongo.DESCENDING)])["일자"]
    if date == target_date:
        print("TR_1206 데이터 적재 완료  "+ date + "   까지")
        check = False
    if check :
        date = get_kr_working_day_by_diff(date, 1).strftime("%Y%m%d")
        check = subprocess.call([sys.executable, basic_path+"\\data\\TR_1206.py", "search" ,date, target_date])
        print("TR_1206 데이터 적재 완료  "+ date + " 에서   "+ target_date + "  까지")
    check = True

    new_TR_1206 = make_collection("stock_data", "new_TR_1206")
    date = new_TR_1206.find_one({"단축코드" : "055550"}, sort=[("일자", pymongo.DESCENDING)])["일자"]
    if date == target_date:
        print("new_TR_1206 데이터 적재 완료  "+ date + "   까지")
        check = False
    if check :
        date = get_kr_working_day_by_diff(date, 1).strftime("%Y%m%d")
        check = subprocess.call([sys.executable, basic_path+"\\data\\fix_data.py", "job" ,date, target_date])
        print("new_TR_1206 데이터 적재 완료  "+ date + " 에서   "+ target_date + "  까지")

    check = subprocess.call([sys.executable, basic_path + "\\analysis\\analysis3.py", "job", "20210107", "20210107"])


