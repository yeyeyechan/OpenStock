

# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\OpenStock")
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari


def analysis (tr_name , data):
    if tr_name == "SC" :
        if check_time(data["체결시간"], "0905"):
            TR_1206 = make_collection("stock_data" , "TR_1206")
            SK = make_collection("stock_data" , "SK")
            SP = make_collection("stock_data" , "SP")

            SK_data = SK.find_one({"단축코드" : data["단축코드"]}).sort([("체결시간" ,-1)])
            SP_data = SP.find_one({"단축코드" : data["단축코드"]}).sort([("체결시간" ,-1)])

            before_day = get_kr_working_day_by_diff(data["일자"] , -1).strftime("%Y%m%d")
            before_TR_1206_data = TR_1206.find_one({"단축코드" : data["단축코드"] , "일자" : before_day})
            if data["전일대비구분"] == "2" and int(data["저가"]) > int(before_TR_1206_data["가격"]) and int(data["전일대비율"]) >= 0.7 and  int(data["전일대비율"]) <= 2.0  :
                if SK_data["외국계순매수수량"] > 0 :
                    if int(SP_data["비차익매수위탁체결수량"]) - int(SP_data["비차익매도위탁체결수량"]) > 0 :
                        send_telegram(data["단축코드"])


    else:
        pass
