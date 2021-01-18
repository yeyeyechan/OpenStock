import sys

sys.path.append("C:\\dev\\OpenStock")

from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari

def call_monitor():
    monitoring = make_collection("stock_data", "monitoring")

    SK = make_collection("stock_data", "SK")
    SP = make_collection("stock_data", "SP")
    TR_SCHART = make_collection("stock_data", "TR_SCHART")
    real_TR_SCHART = make_collection("stock_data", "real_TR_SCHART")

    monitoring_data = monitoring.find_one({"일자" : "20210118"})["stock_code"]

    for i in monitoring_data:
        SK_data = SK.find_one({"단축코드" : i , "일자" : com_vari.Today_date}, sort=[("체결시간", pymongo.DESCENDING)])
        SP_data = SP.find_one({"단축코드" : i , "일자" : com_vari.Today_date}, sort=[("시간", pymongo.DESCENDING)])
        TR_SCHART_data = TR_SCHART.find_one({"단축코드" : i , "일자" :"20210115", "시간" : "1530"})
        real_TR_SCHART_data = TR_SCHART.find_one({"단축코드" : i , "일자" :"20210118", "시간" : "0905"})

        if int(SK_data["외국계순매수수량"]) >= 0 and int(SK_data["국내총순매수수량"]) < 0 and int(SP_data["비차익매수위탁체결수량"] )-int(SP_data["비차익매도위탁체결수량"] ) >0:
            send_telegram(i + "  1단계 조건 달성  외 0 이상 프 0 초과 국내 0 미만 ")
            if int(real_TR_SCHART_data["종가"]) > int(real_TR_SCHART_data["시가"]) and int(real_TR_SCHART_data["종가"]) > int(TR_SCHART_data["종가"]):
                send_telegram(i + "  2단계 조건 달성 초기가격 조건  거래대금 100 억 이상 밑 기관 수급 체크 필요")


def scheduler_monitoring():
    sched_sc = BlockingScheduler()
    sched_sc.add_job(call_monitor, CronTrigger(hour='9-16', minute='*/6'))
    sched_sc.start()

if __name__ == "__main__":
    scheduler_monitoring()