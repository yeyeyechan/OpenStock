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

target_date_stock_supply = {}


def find_rising_other_stock_codes(target_rising_rate, date ):
    result_list = []
    for i in collection.find({"일자" :date , "전일대비율" : {"$lt" : target_rising_rate} }):
        result_list.append(i)
        print(i)
    return result_list
def find_rising_stock_codes(target_rising_rate, date ):
    result_list = []

    for i in collection.find({"일자" :date , "전일대비율" : {"$gt" : target_rising_rate} }):
       # if (float(i["고가"]) + float(i["저가"]))/2 *float(i["누적거래량"]) > 13000000000:
        result_list.append(i)
        target_date_stock_supply[i["단축코드"]] = {}
        target_date_stock_supply[i["단축코드"]]["개인순매수거래량"] = float(i["개인순매수거래량"])
        target_date_stock_supply[i["단축코드"]]["외국인순매수거래량"] = float(i["외국인순매수거래량"])
        target_date_stock_supply[i["단축코드"]]["기관순매수거래량"] = float(i["기관순매수거래량"])
        target_date_stock_supply[i["단축코드"]]["누적거래량"] = float(i["누적거래량"])

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
            if type(i) == dict:
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
                if total_vol != 0:
                    result_dict[i["단축코드"]]["누적거래량합"] = total_vol
                    result_dict[i["단축코드"]]["개인순매수거래량합"] = per_vol
                    result_dict[i["단축코드"]]["외국인순매수거래량합"] = for_vol
                    result_dict[i["단축코드"]]["기관순매수거래량합"] = com_vol

                    result_dict[i["단축코드"]]["개인순매수거래량비율"] = per_vol / total_vol
                    result_dict[i["단축코드"]]["외국인순매수거래량비율"] = for_vol / total_vol
                    result_dict[i["단축코드"]]["기관순매수거래량비율"] = com_vol / total_vol
                else:
                    result_dict[i["단축코드"]]["누적거래량합"] = 0
                    result_dict[i["단축코드"]]["개인순매수거래량합"] = 0
                    result_dict[i["단축코드"]]["외국인순매수거래량합"] = 0
                    result_dict[i["단축코드"]]["기관순매수거래량합"] = 0

                    result_dict[i["단축코드"]]["개인순매수거래량비율"] = 0
                    result_dict[i["단축코드"]]["외국인순매수거래량비율"] = 0
                    result_dict[i["단축코드"]]["기관순매수거래량비율"] = 0
            elif type(i) == str:
                for j in collection.find({"일자" : {"$in" : date_list}, "단축코드" : i}):
                    if j["단축코드"] in result_dict:
                        result_dict[j["단축코드"]][j["일자"]] = make_int_value_dict(field_name_list , j)
                    else:
                        result_dict[j["단축코드"]] = {}
                        result_dict[j["단축코드"]][j["일자"]] = make_int_value_dict(field_name_list , j)
                    total_vol += float(j["누적거래량"])
                    per_vol += float(j["개인순매수거래량"])
                    for_vol += float(j["외국인순매수거래량"])
                    com_vol += float(j["기관순매수거래량"])
                if total_vol != 0:
                    result_dict[i]["누적거래량합"] = total_vol
                    result_dict[i]["개인순매수거래량합"] = per_vol
                    result_dict[i]["외국인순매수거래량합"] = for_vol
                    result_dict[i]["기관순매수거래량합"] = com_vol

                    result_dict[i]["개인순매수거래량비율"] = per_vol / total_vol
                    result_dict[i]["외국인순매수거래량비율"] = for_vol / total_vol
                    result_dict[i]["기관순매수거래량비율"] = com_vol / total_vol
                else:
                    result_dict[i]["누적거래량합"] = 0
                    result_dict[i]["개인순매수거래량합"] = 0
                    result_dict[i]["외국인순매수거래량합"] = 0
                    result_dict[i]["기관순매수거래량합"] = 0

                    result_dict[i]["개인순매수거래량비율"] = 0
                    result_dict[i]["외국인순매수거래량비율"] = 0
                    result_dict[i]["기관순매수거래량비율"] = 0
            #print("     개인순매수거래량비율    "+ str(result_dict[i["단축코드"]]["개인순매수거래량비율"]) + "     외국인순매수거래량비율    "+ str(result_dict[i["단축코드"]]["외국인순매수거래량비율"])   + "     기관순매수거래량비율    "+ str(result_dict[i["단축코드"]]["기관순매수거래량비율"] )  )
            #print(result_dict[i["단축코드"]])
    return result_dict

if __name__ ==  "__main__":
    #1. 분석 대상 날짜의 목표 상승 가 달성한 주식을 뽑는다.
    stock_code_list = find_rising_stock_codes(5.0 , "20201124")
    #stock_code_other_list = find_rising_other_stock_codes(2.0 , "20201123")
    #2.해당 종목들의 5일근(특정일)간 수급을 분석한다.

    #2-1 특정일치 수급 데이터를 모은다.
    #sugup_dict = find_supply_data(stock_code_list, "20201123", -5)
    #print(stock_code_other_list)
    #sugup_other_dict = find_supply_data(stock_code_other_list, "20201123", -5)

    #2-2 분석로직을 만든다.

    #1) 상승 당일 수급 현황 조사
    foreign_count = 0
    per_count = 0
    com_count = 0

    count1 = 0
    count2 = 0

    total_len = len(target_date_stock_supply)
    result1 = []
    result2 = []
    for key ,value in target_date_stock_supply.items():
        if value["외국인순매수거래량"] > 0  and value["기관순매수거래량"] > 0  and value["개인순매수거래량"]  <0:
            count1 +=1
            result1.append(key)
            #print("종목코드   " + key + "  의 수급현황 조사    누적거래량 " + str(value["누적거래량"]) + "     개인순매수거래량 " + str(value["개인순매수거래량"])+ "    외국인순매수거래량 " + str(value["외국인순매수거래량"])+ "     기관순매수거래량 " + str(value["기관순매수거래량"]))
        if value["외국인순매수거래량"] < 0  and value["기관순매수거래량"] < 0  and value["개인순매수거래량"]  >0:
            result2.append(key)
            count2 +=1
        if value["개인순매수거래량"] > 0 :
            per_count +=1
        if value["외국인순매수거래량"] > 0 :
            foreign_count +=1
        if value["기관순매수거래량"] > 0 :
            com_count +=1
    print("총종목수  " + str(total_len))
    print("개인 수급 플러스  " + str(per_count))
    print("외국인 수급 플러스   " + str(foreign_count))
    print("기관 수급 플러스   " + str(com_count))
    print("count1   " + str(count1))
    print("count2  " + str(count2))

    collection = make_collection("stock_data" , "TR_1206")

    print("result1")
    for j in collection.find({"일자" : "20201124" ,"단축코드" : {"$in" : result1}}).sort("전일대비율" , -1):
        #print("종목코드   " + j["단축코드"] + "  의 수급현황 조사    누적거래량 " + str(j["누적거래량"]) + "     개인순매수거래량 " + str(j["개인순매수거래량"]) + "    외국인순매수거래량 " + str(j["외국인순매수거래량"]) + "     기관순매수거래량 " + str(j["기관순매수거래량"]))
        print("종목코드   " + j["단축코드"] + "  의 수급현황 조사    누적거래량 " + (j["누적거래량"]) + "     개인순매수거래비율 " + str(float(j["개인순매수거래량"])/float(j["누적거래량"])) + "    외국인순매수거래비율 " + str(float(j["외국인순매수거래량"])/float(j["누적거래량"])) + "     기관순매수거래비율 " + str(float(j["기관순매수거래량"])/float(j["누적거래량"]))+"    전일대비율  " + str(j["전일대비율"]))

    print("result2")
    for j in collection.find({"일자" : "20201124" ,"단축코드" : {"$in" : result2}}).sort("전일대비율" , -1):
        #print("종목코드   " + j["단축코드"] + "  의 수급현황 조사    누적거래량 " + str(j["누적거래량"]) + "     개인순매수거래량 " + str(j["개인순매수거래량"]) + "    외국인순매수거래량 " + str(j["외국인순매수거래량"]) + "     기관순매수거래량 " + str(j["기관순매수거래량"]))
        print("종목코드   " + j["단축코드"] + "  의 수급현황 조사    누적거래량 " + (j["누적거래량"]) + "     개인순매수거래비율 " + str(float(j["개인순매수거래량"])/float(j["누적거래량"])) + "    외국인순매수거래비율 " + str(float(j["외국인순매수거래량"])/float(j["누적거래량"])) + "     기관순매수거래비율 " + str(float(j["기관순매수거래량"])/float(j["누적거래량"]))+"    전일대비율  " + str(j["전일대비율"]))


    print("result1 의 수급 분석")
    sugup_dict = find_supply_data(result1, "20201125", -5)
    #print("result2 의 수급 분석")
    #sugup_dict2 = find_supply_data(result2, "20201124", -5)
    '''for i in result1:
        for key in sugup_dict[i]:
            if type(sugup_dict[i][key]) == dict:
                print("일자 " + key, end="")
                print("  누적거래량   "+ str(sugup_dict[i][key]["누적거래량"]) + "  개인순매수거래량   "+ str(sugup_dict[i][key]["개인순매수거래량"]) +"  외국인순매수거래량   "+ str(sugup_dict[i][key]["외국인순매수거래량"])+"  기관순매수거래량   "+ str(sugup_dict[i][key]["기관순매수거래량"]))
            print()
        print()'''
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0

    count1_list = []
    count2_list = []
    count3_list = []
    count4_list = []
    for i in result1:
        foreign_sum = 0
        com_sum = 0
        per_sum = 0
        total_sum = 0
        total_sum += sugup_dict[i]["누적거래량합"]
        foreign_sum += sugup_dict[i]["외국인순매수거래량합"]
        com_sum += sugup_dict[i]["기관순매수거래량합"]
        per_sum += sugup_dict[i]["개인순매수거래량합"]
        if foreign_sum >0 and com_sum >0 and per_sum < 0 :
            count1+=1
            count1_list.append(i)
        if foreign_sum > 0  and com_sum <0 and per_sum < 0 :
            count2+=1
            count2_list.append(i)
        if foreign_sum <0 and com_sum <0 and per_sum >0 :
            count3+=1
            count3_list.append(i)
        if foreign_sum <0 and com_sum > 0 and per_sum >0 :
            count4+=1
            count4_list.append(i)
    print(" 외국인 양 기관 양 개인 음  " + str(count1))
    for i in count1_list:
        print("   "+ i +"    ", end = "")
    print()
    print(" 외국인 양 기관음 개인 음  " + str(count2))
    for i in count2_list:
        print("   "+ i +"    ", end = "")
    print()
    print(" 외국인 기관 음  개인 양  " + str(count3))
    for i in count3_list:
        print("   "+ i +"    ", end = "")
    print()
    print(" 외국인 기관 양  개인 양  " + str(count4))
    for i in count4_list:
        print("   "+ i +"    ", end = "")
    print()
    '''print("result2 의 수급 분석")
    for j in result2:
        for key3 in sugup_dict2[j]:
            if type(sugup_dict2[j][key3]) == dict:
                print("일자 " + key3, end = "")
                for key4 in sugup_dict2[j][key3]:
                    if type(sugup_dict2[j][key3][key4]) == float:
                        print(key4 + "    " + str(sugup_dict2[j][key3][key4]) + "   ", end="")
                    else:
                        print(key4 + "    " + sugup_dict2[j][key3][key4] + "   ", end="")
                print()
            if type(sugup_dict2[j][key3]) == float:
                print(key3 +"   " + str(sugup_dict2[j][key3]) , end = "")
        print()'''