from src.com.stock.common.import_lib import *

collection = make_collection("stock_data", "TR_1206")

field_name_list = [
"누적거래량                ",
"개인순매수거래량          ",
"외국인순매수거래량        ",
"기관순매수거래량          ",
"금융투자순매수거래량      ",
"투신순매수거래량          ",
"은행순매수거래량          ",
"기타금융순매수거래량      ",
"보험순매수거래량          ",
"기금순매수거래량          ",
"기금순매수거래량          ",
"기타순매수거래량          ",
"외국인기타순매수거래량    ",
"국가지자체순매수거래량    ",
"프로그램순매수            "
]
def find_rising_other_stock_codes(target_rising_rate, date ):
    result_list = []
    for i in collection.find({"일자" :date , "전일대비율" : {"$lt" : target_rising_rate} }):
        result_list.append(i)
        print(i)
    return result_list
def find_rising_stock_codes(target_rising_rate, date ):
    result_list = []
    for i in collection.find({"일자" :date , "전일대비율" : {"$gt" : target_rising_rate} }):
        result_list.append(i)
        #print(i)
    return result_list
def make_int_value_dict(field_name_list, collection_dict):
    result_dict= {}
    for i in field_name_list:
        result_dict[i.strip()] = float(collection_dict[i.strip()])
    return result_dict

def find_supply_data(stock_code, date, day_range):
    result_dict = {}

    date_list = get_kr_str_working_day_list_by_diff(date,day_range)
    #print(date_list)
    if type(stock_code) is list:
        for i in stock_code:
            total_vol  = 0
            per_vol = 0
            for_vol = 0
            com_vol = 0
            for j in collection.find({"일자" : {"$in" : date_list}, "단축코드" : i["단축코드"]}):
                if j["단축코드"] in result_dict:
                    result_dict[j["단축코드"]][j["일자"]] = make_int_value_dict(field_name_list , j)
                else:
                    result_dict[j["단축코드"]] = {}
                    result_dict[j["단축코드"]][j["일자"]] = make_int_value_dict(field_name_list , j)
                total_vol += float(j["누적거래량"])
                per_vol += float(j["개인순매수거래량"])
                for_vol += float(j["외국인순매수거래량"])
                com_vol += float(j["기관순매수거래량"])
            if total_vol !=0:
                result_dict[i["단축코드"]]["누적거래량합"]          = total_vol
                result_dict[i["단축코드"]]["개인순매수거래량합"]    = per_vol
                result_dict[i["단축코드"]]["외국인순매수거래량합"]  =for_vol
                result_dict[i["단축코드"]]["기관순매수거래량합"]    =com_vol

                result_dict[i["단축코드"]]["개인순매수거래량비율"]    = per_vol/total_vol
                result_dict[i["단축코드"]]["외국인순매수거래량비율"]  =for_vol/total_vol
                result_dict[i["단축코드"]]["기관순매수거래량비율"]    =com_vol/total_vol
            else:
                result_dict[i["단축코드"]]["누적거래량합"] = 0
                result_dict[i["단축코드"]]["개인순매수거래량합"] = 0
                result_dict[i["단축코드"]]["외국인순매수거래량합"] = 0
                result_dict[i["단축코드"]]["기관순매수거래량합"] = 0

                result_dict[i["단축코드"]]["개인순매수거래량비율"] = 0
                result_dict[i["단축코드"]]["외국인순매수거래량비율"] = 0
                result_dict[i["단축코드"]]["기관순매수거래량비율"] = 0
            #print("     개인순매수거래량비율    "+ str(result_dict[i["단축코드"]]["개인순매수거래량비율"]) + "     외국인순매수거래량비율    "+ str(result_dict[i["단축코드"]]["외국인순매수거래량비율"])   + "     기관순매수거래량비율    "+ str(result_dict[i["단축코드"]]["기관순매수거래량비율"] )  )
            #print(result_dict[i["단축코드"]])
    return result_dict

if __name__ ==  "__main__":
    #1. 분석 대상 날짜의 목표 상승 가 달성한 주식을 뽑는다.
    stock_code_list = find_rising_stock_codes(5.0 , "20201123")
    stock_code_other_list = find_rising_other_stock_codes(2.0 , "20201123")
    #2.해당 종목들의 5일근(특정일)간 수급을 분석한다.

    #2-1 특정일치 수급 데이터를 모은다.
    sugup_dict = find_supply_data(stock_code_list, "20201123", -5)
    #print(stock_code_other_list)
    sugup_other_dict = find_supply_data(stock_code_other_list, "20201123", -5)

    #2-2 분석로직을 만든다.

    for key , value in sugup_dict.items():
        print(value)





