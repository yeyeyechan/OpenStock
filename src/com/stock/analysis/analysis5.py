# -*- conding: utf-8 -*-


from src.com.stock.common.import_lib import *

#외국인, 기간 양 개인 음 로직 1
#반대 로직 2
#혼조 로직 3
result = {
    "logic1": {"stock_code": [], "avg_for": 0, "avg_com": 0, "avg_per": 0, "avg_vol_ratio": 0, "avg_five_vol_ratio": 0,
               "avg_trade_price": 0},
    "logic2": {"stock_code": [], "avg_for": 0, "avg_com": 0, "avg_per": 0, "avg_vol_ratio": 0, "avg_five_vol_ratio": 0,
               "avg_trade_price": 0},
    "logic3": {"stock_code": [], "avg_for": 0, "avg_com": 0, "avg_per": 0, "avg_vol_ratio": 0, "avg_five_vol_ratio": 0,
               "avg_trade_price": 0}
}
def check_rising_stock_condition(current_data , before_data, today_5min, before_5min):
    foreign_ratio =  int(current_data["외국인순매수거래량"])/int(current_data["누적거래량"])
    com_ratio =  int(current_data["기관순매수거래량"])/int(current_data["누적거래량"])
    per_ratio =  int(current_data["개인순매수거래량"])/int(current_data["누적거래량"])
    vol_ratio = int(current_data["누적거래량"]) / int(before_data["누적거래량"])
    five_vol_ratio =int(today_5min["단위거래량"])/int(before_5min["단위거래량"])
    trade_price =int( current_data["가격"])*int(before_data["누적거래량"])


    if  foreign_ratio >0 and com_ratio >0 and per_ratio <0 :
        result["logic1"]['stock_code'].append(current_data["단축코드"])
        result["logic1"]['avg_for'] += foreign_ratio
        result["logic1"]['avg_com'] += com_ratio
        result["logic1"]['avg_per'] += per_ratio
        result["logic1"]['avg_vol_ratio'] += vol_ratio
        result["logic1"]['avg_five_vol_ratio'] += five_vol_ratio
        result["logic1"]['avg_trade_price'] += trade_price
    elif foreign_ratio <0 and com_ratio <0 and per_ratio >0 :
        result["logic2"]['stock_code'].append(current_data["단축코드"])
        result["logic2"]['avg_for'] += foreign_ratio
        result["logic2"]['avg_com'] += com_ratio
        result["logic2"]['avg_per'] += per_ratio
        result["logic2"]['avg_vol_ratio'] += vol_ratio
        result["logic2"]['avg_five_vol_ratio'] += five_vol_ratio
        result["logic2"]['avg_trade_price'] += trade_price
    else:
        result["logic3"]['stock_code'].append(current_data["단축코드"])
        result["logic3"]['avg_for'] += foreign_ratio
        result["logic3"]['avg_com'] += com_ratio
        result["logic3"]['avg_per'] += per_ratio
        result["logic3"]['avg_vol_ratio'] += vol_ratio
        result["logic3"]['avg_five_vol_ratio'] += five_vol_ratio
        result["logic3"]['avg_trade_price'] += trade_price




def check_rising_stock_facts(date_list):
    new_tr_1206 = make_collection("stock_data" , "new_TR_1206")
    TR_SCHART = make_collection("stock_data" , "TR_SCHART")

    for day in date_list:
        day  = day.strftime("%Y%m%d")
        print(day + "  상승 종목 특징 분석  ")
        before_day = get_kr_working_day_by_diff(day, -1).strftime("%Y%m%d")

        for new_tr_1206_data in new_tr_1206.find({"일자" : day}).sort([("전일대비율" , -1)]).batch_size(5):
            if new_tr_1206_data["전일대비율"] <5.0 :
                print(day + "  상승 종목 특징 분석 종료  ")
                break
            before_day_tr_1206_data = new_tr_1206.find_one({"일자" : before_day, "단축코드" : new_tr_1206_data["단축코드"]})
            before_day_tr_schart_data = TR_SCHART.find_one({"일자" : before_day, "단축코드" : new_tr_1206_data["단축코드"] ,"시간" : "0905"})
            day_tr_schart_data = TR_SCHART.find_one({"일자" : day, "단축코드" : new_tr_1206_data["단축코드"] ,"시간" : "0905"})
            check_rising_stock_condition(new_tr_1206_data,before_day_tr_1206_data, day_tr_schart_data,before_day_tr_schart_data)

            print("단축코드   "  + new_tr_1206_data["단축코드"]+ "     가격   "  + new_tr_1206_data["가격"]+ "     누적거래량   "  + new_tr_1206_data["누적거래량"]+ "     거래대금   "  + str(int( new_tr_1206_data["가격"])*int(new_tr_1206_data["누적거래량"]))+ "     전일대비율   "  + str(new_tr_1206_data["전일대비율"]))
            print("단축코드   "  + new_tr_1206_data["단축코드"]+ "     외국인매수비율   "  + str(int(new_tr_1206_data["외국인순매수거래량"])/int(new_tr_1206_data["누적거래량"])) + "     개인매수비율   "  + str(int(new_tr_1206_data["개인순매수거래량"])/int(new_tr_1206_data["누적거래량"]))+ "     기관매수비율   "  + str(int(new_tr_1206_data["기관순매수거래량"])/int(new_tr_1206_data["누적거래량"])) )
            print("단축코드   "  + new_tr_1206_data["단축코드"]+ "     누적거래량비교   "  + str(int(new_tr_1206_data["누적거래량"])/int(before_day_tr_1206_data["누적거래량"]))  )
            print("단축코드   "  + new_tr_1206_data["단축코드"]+ "     5분거래량비교   "  + str(int(day_tr_schart_data["단위거래량"])/int(before_day_tr_schart_data["단위거래량"]))  )
        print(result)
if __name__ ==  "__main__":
    date_list = get_kr_working_day("20201217" , "20201217")
    check_rising_stock_facts(date_list)