# -*- conding: utf-8 -*-

from src.com.stock.common.import_lib import *

from src.com.stock.common import import_lib  as com_vari


if __name__ ==  "__main__":
    today = com_vari.Today_date
    before_today = get_kr_working_day_by_diff(com_vari.Today_date, -1).strftime("%Y%m%d")

    from_collection = make_collection("stock_data" , "additional_data")
    from_collection2 = make_collection("stock_data", "TR_SCHART")

    from_collection3 = make_collection("stock_data", "TR_1206")

    stock_code =  from_collection.find_one({"일자" : today})["stock_code"]

    for i in stock_code:
        before_TR_SCHART_DATA = from_collection2.find_one({"일자" : before_today, "시간" : "0905"})["단위거래량"]
        today_TR_SCHART_DATA = from_collection2.find_one({"일자" : today, "시간" : "0905"})["단위거래량"]
        before_TR_1206_DATA = int(from_collection3.find_one({"일자" : before_today, "단축코드" : i})["누적거래량"])/79
        if int(today_TR_SCHART_DATA)/int(before_TR_SCHART_DATA) >=1.9:
            if int(today_TR_SCHART_DATA)/before_TR_1206_DATA>=2.0:
                print("예측거래량 전일대비 2배 이상   "+i)
            else:
                print("초반 5분 거래량  전일대비 1.9 배 이상   "+i)

