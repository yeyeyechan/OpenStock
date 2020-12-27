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
    subprocess.call([sys.executable, basic_path+"\\data\\TR_SCHART.py"])