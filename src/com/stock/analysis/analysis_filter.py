

# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\OpenStock")
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari


def check_layer(data, layer):
    daily_check = make_collection("stock_data", "daily_check")
    daily_check_data = daily_check.find_one({"일자" :  data["일자"] , "단축코드" : data["단축코드"] , "단계" : layer})

    if daily_check_data is not None and ("단계" in daily_check_data.keys()) :
        daily_check.insert(data)
        return True
    return False
def analysis_by_scheduler():
    if tr_name == "SC" :
        if check_time(data["체결시간"], "1530"):
            TR_1206 = make_collection("stock_data" , "TR_1206")
            SK = make_collection("stock_data" , "SK")
            SP = make_collection("stock_data" , "SP")


            SK_data = SK.find_one({"단축코드" : data["단축코드"], "일자" : data["일자"]}, sort=[("체결시간", pymongo.DESCENDING)])
            SP_data = SP.find_one({"단축코드" : data["단축코드"], "일자" : data["일자"]}, sort=[("체결시간", pymongo.DESCENDING)])

            before_day = get_kr_working_day_by_diff(data["일자"] , -1).strftime("%Y%m%d")
            before_TR_1206_data = TR_1206.find_one({"단축코드" : data["단축코드"] , "일자" : before_day})
            if data["전일대비구분"] == "2" and int(data["저가"]) > int(before_TR_1206_data["가격"]) and float(data["전일대비율"]) >= 0.7 and  float(data["전일대비율"]) <= 2.0  :
                print("  1단계 조건 달성  ")
                if check_layer(data, "1"):
                    send_telegram(data["단축코드"]+ "  1단계 조건 달성  ")
                if SK_data is not None and  "외국계순매수수량" in SK_data.keys() and  int(SK_data["외국계순매수수량"] )> 0 :
                    print("  2단계 조건 달성  ")
                    if check_layer(data, "2"):
                        send_telegram(data["단축코드"] + "  2단계 조건 달성  ")
                    if SP_data is not None and  "비차익매수위탁체결수량" in SP_data.keys()  and int(SP_data["비차익매수위탁체결수량"]) - int(SP_data["비차익매도위탁체결수량"]) > 0 :
                        print("  3단계 조건 달성  ")
                        if check_layer(data, "3"):
                            send_telegram(data["단축코드"] + "  3단계 조건 달성  ")
    else:
        pass
def analysis (tr_name , data):
    if tr_name == "SC" :
        if check_time(data["체결시간"], "1530"):
            TR_1206 = make_collection("stock_data" , "TR_1206")
            SK = make_collection("stock_data" , "SK")
            SP = make_collection("stock_data" , "SP")


            SK_data = SK.find_one({"단축코드" : data["단축코드"], "일자" : data["일자"]}, sort=[("체결시간", pymongo.DESCENDING)])
            SP_data = SP.find_one({"단축코드" : data["단축코드"], "일자" : data["일자"]}, sort=[("체결시간", pymongo.DESCENDING)])

            before_day = get_kr_working_day_by_diff(data["일자"] , -1).strftime("%Y%m%d")
            before_TR_1206_data = TR_1206.find_one({"단축코드" : data["단축코드"] , "일자" : before_day})
            if data["전일대비구분"] == "2" and int(data["저가"]) > int(before_TR_1206_data["가격"]) and float(data["전일대비율"]) >= 0.7 and  float(data["전일대비율"]) <= 2.0  :
                print("  1단계 조건 달성  ")
                if check_layer(data, "1"):
                    send_telegram(data["단축코드"]+ "  1단계 조건 달성  ")
                if SK_data is not None and  "외국계순매수수량" in SK_data.keys() and  int(SK_data["외국계순매수수량"] )> 0 :
                    print("  2단계 조건 달성  ")
                    if check_layer(data, "2"):
                        send_telegram(data["단축코드"] + "  2단계 조건 달성  ")
                    if SP_data is not None and  "비차익매수위탁체결수량" in SP_data.keys()  and int(SP_data["비차익매수위탁체결수량"]) - int(SP_data["비차익매도위탁체결수량"]) > 0 :
                        print("  3단계 조건 달성  ")
                        if check_layer(data, "3"):
                            send_telegram(data["단축코드"] + "  3단계 조건 달성  ")
    else:
        pass
