from itertools import count

from src.com.stock.common.import_lib import *

def total_trans_amount (price , volume, target):
    # 가격, 누적거래량
    if int(target) <= int(price)*int(volume):
        return True
    else:
        return False
def check_for_amount(volume ,target):
    # 외국인 순매수 거래량
    if int(target) <= int(volume):
        return True
    else:
        return False
def check_com_amount(volume , target):
    #기관순매수거래량
    if int(target) <= int(volume):
        return True
    else:
        return False
def check_pro_amount(volume, target):
    #프로그램순매수
    if int(target )<= int(volume):
        return True
    else:
        return False
def check_per_amount(volume , target):
    #개인순매수거래량
    if int(target) <= int(volume):
        return True
    else:
        return False
def check_for_min_amount(volume ,target):
    # 외국인 순매수 거래량
    if int(target) <= int(volume):
        return False
    else:
        return True
def check_com_min_amount(volume , target):
    #기관순매수거래량
    if int(target) <= int(volume):
        return False
    else:
        return True
def check_pro_min_amount(volume, target):
    #프로그램순매수
    if int(target )<= int(volume):
        return False
    else:
        return True
def check_per_min_amount(volume , target):
    #개인순매수거래량
    if int(target) <= int(volume):
        return False
    else:
        return True
def check_up_price(price,  diff, target):
    before = int(price) -int(diff)
    if  int(diff)/before *100 >=target:
        return True
    else:
        return False
def first_condition(target_date, input_dict, target_db):
    ''''
        first_gubun 5 (하락) 2(상승) 3(보합)
        first_trans_price 거래대금
        first_foreign: 외국인 거래대금 기준
        first_program: 프로그램 거래대금 기준
        first_company: 기관 거래대금 기준

        2nd_foreign: 외국인 거래대금 기준
        2nd_program: 프로그램 거래대금 기준
        2nd_company: 기관 거래대금 기준
        2nd_trans_price : 거래대금
        2nd_gubun : 전일대비구분
        2nd_up_target : 전일대비 상승률
    '''
    first_date = get_kr_working_day_by_diff(target_date , -2)
    second_date = get_kr_working_day_by_diff(target_date, -1)

    TR_1206_collection = target_db

    stock_code_list = []
    final_stock_code_list = []

    for i in TR_1206_collection.find({"일자": first_date.strftime("%Y%m%d")}):
        if input_dict["first_gubun"] == "":
            if total_trans_amount(i['가격'], i['누적거래량'], input_dict["first_trans_price"] ):
                stock_code_list.append(copy(i['단축코드']))
        elif i['전일대비구분'] == input_dict["first_gubun"]:
            if total_trans_amount(i['가격'], i['누적거래량'], input_dict["first_trans_price"] ):
                stock_code_list.append(copy(i['단축코드']))
    for i in stock_code_list:
        data = TR_1206_collection.find_one({"일자": second_date.strftime("%Y%m%d"), "단축코드":i })
        if data is None:
            com_vari.TR_1206_logger.debug("TR_1206_db 데이터 없음 확인 필요   일자 " + second_date.strftime("%Y%m%d") + "   단축코드 " + i)
            continue
        elif input_dict["first_gubun"] == "":
            if check_for_amount(data['외국인순매수거래량'], input_dict["2nd_foreign"] ) and check_pro_amount(data['프로그램순매수'], input_dict["2nd_program"])  and total_trans_amount(data['가격'],data['누적거래량'], input_dict["2nd_trans_price"]) :
                final_stock_code_list.append(copy(data['단축코드']))
        else:
            if data['전일대비구분'] == input_dict["2nd_gubun"] and check_for_amount(data['외국인순매수거래량'], input_dict["2nd_foreign"] ) and check_pro_amount(data['프로그램순매수'], input_dict["2nd_program"]) and check_up_price(data['가격'] , data['전일대비'],input_dict["2nd_up_target"] ) and total_trans_amount(data['가격'],data['누적거래량'], input_dict["2nd_trans_price"]) :
                final_stock_code_list.append(copy(data['단축코드']))
    print(target_date.strftime("%Y%m%d") + " 날짜에 예측되는 상승 종목 코드 리스트  ")
    print(final_stock_code_list)
    print()
    return final_stock_code_list
def check_actual_total_data(date_list, target_percent, target_db):
    TR_1206_db = target_db
    result_dict ={}
    for i in date_list:
        result_list = []
        for j in TR_1206_db.find({"일자": i.strftime("%Y%m%d")}):
            if j["전일대비구분"] =="2" and  check_up_price(j["가격"], j["전일대비"], target_percent):
                result_list.append(copy(j))
        result_dict[i.strftime("%Y%m%d")] = copy(result_list)
        result_dict[i.strftime("%Y%m%d")+"_total_count"] = TR_1206_db.find({"일자": i.strftime("%Y%m%d")}).count()
        result_dict[i.strftime("%Y%m%d")+"_success"] = len(result_list)
    return result_dict

def find_market_upjong_by_stock_code_dict ( stock_code_dict, date_list):
    upjong_code_mst_collection = make_collection("stock_data", "upjong_code_mst")
    result_dict = {}
    for i in date_list:
        result_list = []
        for j in stock_code_dict[i.strftime("%Y%m%d")] :
            for k in upjong_code_mst_collection.find({"단축코드":j}):
                result_list.append(copy(k))
        result_dict[i.strftime("%Y%m%d")] = copy(result_list)
    return result_dict
def check_market_upjong(date_list):
    TR_1205_collection = make_collection("stock_data", "TR_1205")

    result_dict = {}

    for i in date_list:
        result_list = []
        for j in TR_1205_collection.find({'일자': i.strftime("%Y%m%d")}).sort([('외국인순매수', -1)]).limit(10):
            result_list.append(copy(j))
        result_dict[i.strftime("%Y%m%d")] = copy(result_list)
    return result_dict

def check_with_data(input_data , target_percnet, target_db):
    TR_1206_db = target_db

    result_dict = {

    }

    for key  in input_data.keys() :
        result_list = []
        for i in input_data[key]:
            collection_value = TR_1206_db.find_one({"일자":key , "단축코드": i})
            if collection_value is None:
                com_vari.TR_1206_logger.debug("TR_1206_db 데이터 없음 확인 필요   일자 " +key + "   단축코드 "+ i )
                continue
            elif collection_value["전일대비구분"] =="2" and check_up_price(collection_value["가격"], collection_value["전일대비"], 5.0):
                result_list.append(copy(collection_value))
        result_dict[key] = copy(result_list)
        result_dict[key+"_total_count"] = len(input_data[key])
        result_dict[key+"_success"] = len(result_list)
        print("일자    " + key)
        print("일자   _total_count  갯수  " + str(len(input_data[key]) ))
        print("일자   _success 갯수" +  str(len(result_list) ))
    return result_dict



def make_price_con_function(target_percent, start_date , end_date):
    TR_1206_db = make_collection("stock_data", "TR_1206")

    date_list = get_kr_working_day(start_date . end_date)

    result_list = []
    result_dict = {}
    for i in date_list:
        result_list = []
        for j in TR_1206_db.find({"일자": str(i)}):
            if j["전일대비구분"] == "2" and int(j["전일대비"])/int(j["가격"]-j["전일대비"])*100 >= 5.0:
                result_list.append(copy(j))
        result_dict[str(i)] = copy(result_list)

    return result_dict
def strategy_2 ():
    #1. 상승률 5프로 이상의 종목을 선정한다.
    TR_1206_collection  = make_collection("stock_data" ,"TR_1206")
    selected_TR_1206 = []
    for i in TR_1206_collection.find({"일자" : "20201120"}):
        if i["전일대비구분"] =="2"  and check_up_price(i["가격"], i["전일대비"], 5.0) :
            selected_TR_1206.append(i)

    # 2. 상승종목 업종을 뽑아낸다.
    upjong_code_mst_collection = make_collection("stock_data" , "upjong_code_mst")
    selected_upjong_mst = {}
    for i in selected_TR_1206 :
            for j in upjong_code_mst_collection.find({"단축코드" :  i["단축코드"]}):
                if j["업종코드"] in selected_upjong_mst :
                    selected_upjong_mst[j["업종코드"]]["종목코드"].append(i["단축코드"])
                    selected_upjong_mst[j["업종코드"]]["상승수"]   += 1
                    selected_upjong_mst[j["업종코드"]]["상승비율"] = (selected_upjong_mst[j["업종코드"]]["상승수"] / selected_upjong_mst[j["업종코드"]]["전종목수"]) * 100.0
                else:
                    selected_upjong_mst[j["업종코드"]] = {}
                    selected_upjong_mst[j["업종코드"]]["종목코드"] = []
                    selected_upjong_mst[j["업종코드"]]["종목코드"].append(i["단축코드"])
                    selected_upjong_mst[j["업종코드"]]["업종명"] = j["업종명"]
                    selected_upjong_mst[j["업종코드"]]["업종코드"] = j["업종코드"]
                    selected_upjong_mst[j["업종코드"]]["상승수"] = 1
                    selected_upjong_mst[j["업종코드"]]["전종목수"] = upjong_code_mst_collection.find({"업종코드": j["업종코드"] }).count()
                    selected_upjong_mst[j["업종코드"]]["상승비율"] = (selected_upjong_mst[j["업종코드"]]["상승수"] / selected_upjong_mst[j["업종코드"]]["전종목수"]) * 100.0

    #3. 상승종목중 업종중 제일 상승률이 높은 것 부터 출력한다.
    selected_upjong_mst = dict(sorted(selected_upjong_mst.items() , key= (lambda x :  x[1]["상승비율"]), reverse=True ))
    rank = 1
    for key , value in selected_upjong_mst.items():
        if rank ==1 :
            for i in value["종목코드"]:
                print(i)
        value["등수"] = rank
        rank +=1
        print("    업종명   " + value["업종명"]  + "      상승비율   "  + str(value["상승비율"]) + " 업종 전종목수   "+  str(value["전종목수"]) +  " 업종 상승수   "+  str(value["상승수"]))
    #4. 상승종목 상승률 상위 업종 수급 추이를 전체 수급추이와 비교
    TR_1205_collection = make_collection("stock_data", "TR_1205")

    target_date = "20201120"

    target_date_1 = get_kr_working_day_by_diff(date(int(target_date[:4]),int(target_date[4:6]),int(target_date[6:])), -1)
    target_date_2 = get_kr_working_day_by_diff(date(int(target_date[:4]),int(target_date[4:6]),int(target_date[6:])), -2)
    target_date_3 = get_kr_working_day_by_diff(date(int(target_date[:4]),int(target_date[4:6]),int(target_date[6:])), -3)
    target_date_4 = get_kr_working_day_by_diff(date(int(target_date[:4]),int(target_date[4:6]),int(target_date[6:])), -4)
    target_date_5 = get_kr_working_day_by_diff(date(int(target_date[:4]),int(target_date[4:6]),int(target_date[6:])), -5)
    target_date_6 = get_kr_working_day_by_diff(date(int(target_date[:4]),int(target_date[4:6]),int(target_date[6:])), -6)
    target_date_7 = get_kr_working_day_by_diff(date(int(target_date[:4]),int(target_date[4:6]),int(target_date[6:])), -7)
    target_date_8 = get_kr_working_day_by_diff(date(int(target_date[:4]),int(target_date[4:6]),int(target_date[6:])), -8)


    '''for i in TR_1205_collection.find({"일자": target_date_2.strftime("%Y%m%d")}).sort([('기관순매수', -1)]).limit(5):
        print(i)
        for key , value in selected_upjong_mst.items():
            if value["업종명"] == i["한글업종명"]:
                print("상승 업종   " + value["업종명"]  + "      상승비율   "  + str(value["상승비율"])+ "      등수   "  + str(value["등수"]))'''

    for i in TR_1205_collection.find({"일자": target_date_2.strftime("%Y%m%d") , "한글업종명": "기타 제조"}):
        print(i)

    #for key , value in selected_upjong_mst.items():


    #selected_upjong_mst = sorted(selected_upjong_mst.items(), key = (lambda x : x[6]), reverse = True)





if __name__ == "__main__":
    collection = make_collection("stock_data", "TR_1206")

    stock_code_list = []
    final_stock_code_list = []
    for i in collection.find({"일자": "20201111"}):
        if i['전일대비구분'] == '5':
            if total_trans_amount(i['가격'], i['누적거래량'], '10000000000' ):
                stock_code_list.append(copy(i['단축코드']))
    for i in stock_code_list:
        data = collection.find_one({"일자": "20201112", "단축코드":i })
        if data is None:
            print()
            continue
        #print(data)
        if data['전일대비구분'] == '2' and check_for_amount(data['외국인순매수거래량'], '0') and check_pro_amount(data['프로그램순매수'], '0') and check_up_price(data['가격'] , data['전일대비']) and total_trans_amount(data['가격'],data['누적거래량'], '13000000000') :
            final_stock_code_list.append(copy(data['단축코드']))
    print(final_stock_code_list)


    TR_1205_date = get_kr_working_day("20201111", "20201112")

    collection2 = make_collection("stock_data", "TR_1205")

    for i in TR_1205_date :
        for j in collection2.find({'일자': i.strftime("%Y%m%d")}).sort([('외국인순매수', -1)]).limit(7):
            print(j)
        print()
