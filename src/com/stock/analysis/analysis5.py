# -*- conding: utf-8 -*-


from src.com.stock.common.import_lib import *

def check_rising_stock_facts(date_list):
    new_tr_1206 = make_collection("stock_data" , "new_TR_1206")
    TR_SCHART = make_collection("stock_data" , "TR_SCHART")

    for day in date_list:
        day  = day.strftime("%Y%m%d")
        print(day + "  상승 종목 특징 분석  ")
        before_day = get_kr_working_day_by_diff(day, -1).strftime("%Y%m%d")

        for new_tr_1206_data in new_tr_1206.find({"일자" : day}).sort([("전일대비율" , -1)]):
            if new_tr_1206_data["전일대비율"] <5.0 :
                print(day + "  상승 종목 특징 분석 종료  ")
                break
            before_day_tr_1206_data = new_tr_1206.find_one({"일자" : before_day, "단축코드" : new_tr_1206_data["단축코드"]})
            before_day_tr_schart_data = TR_SCHART.find_one({"일자" : before_day, "단축코드" : new_tr_1206_data["단축코드"] ,"시간" : "0905"})
            day_tr_schart_data = TR_SCHART.find_one({"일자" : day, "단축코드" : new_tr_1206_data["단축코드"] ,"시간" : "0905"})

            print("단축코드   "  + new_tr_1206_data["단축코드"]+ "     가격   "  + new_tr_1206_data["가격"]+ "     누적거래량   "  + new_tr_1206_data["누적거래량"]+ "     거래대금   "  + str(int( new_tr_1206_data["가격"])*int(new_tr_1206_data["누적거래량"]))+ "     전일대비율   "  + str(new_tr_1206_data["전일대비율"]))
            print("단축코드   "  + new_tr_1206_data["단축코드"]+ "     외국인매수비율   "  + str(int(new_tr_1206_data["외국인순매수거래량"])/int(new_tr_1206_data["누적거래량"])) + "     개인매수비율   "  + str(int(new_tr_1206_data["개인순매수거래량"])/int(new_tr_1206_data["누적거래량"]))+ "     기관매수비율   "  + str(int(new_tr_1206_data["기관순매수거래량"])/int(new_tr_1206_data["누적거래량"])) )
            print("단축코드   "  + new_tr_1206_data["단축코드"]+ "     누적거래량비교   "  + str(int(new_tr_1206_data["누적거래량"])/int(before_day_tr_1206_data["누적거래량"]))  )
            print("단축코드   "  + new_tr_1206_data["단축코드"]+ "     5분거래량비교   "  + str(int(day_tr_schart_data["단위거래량"])/int(before_day_tr_schart_data["단위거래량"]))  )

if __name__ ==  "__main__":
    date_list = get_kr_working_day("20201215" , "20201215")
    check_rising_stock_facts(date_list)