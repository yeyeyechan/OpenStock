# -*- conding: utf-8 -*-


from src.com.stock.common.import_lib import *
def print_anal4(date, from_collection):
    check_data = from_collection.find_one({'일자' : date})["stock_code"]
    print(len(check_data))
    print(str(check_data))
def additional_condition(data):
    '''
        시나리오 :
        당일 예측 종목 (3daySupply) 에서 당일 실제 데이터 TR_SCHART의 0905 의 종가 데이터와
        TR_1206 의 전일 가격 데이터 와 비교 한다 ( 상승 0.7 ~ 2.0 ) 이내 종목만 선별
    '''
    #여기서 일자는 예측 당일 일자
    result = {}
    result['일자'] = data["일자"]
    result['stock_code'] = []

    before_day = get_kr_working_day_by_diff(data["일자"] , -1).strftime("%Y%m%d")
    TR_1206 = make_collection("stock_data", "TR_1206")
    TR_SCHART = make_collection("stock_data", "TR_SCHART")

    for i in data["stock_code"]:
        today_data =  TR_SCHART.find_one({"일자": data["일자"], "단축코드" : i, "시간" : "0905"})
        if today_data is not None:
            today_price = today_data["종가"]
            before_data = TR_1206.find_one({"일자": before_day, "단축코드" : i})
            before_last_price =before_data["가격"]
            if check_first_price(today_price , before_last_price , 0.7 ,2.0):
                result['stock_code'].append(i)
                print("additional_condition" + i)
        else:
            print(' 종목코드    '  + i + "   에 대한   예측 당일   "    + data["일자"] + "   TR_SCHART  데이터가 없습니다   ")
            return False
    to_collection = make_collection("stock_data" , "additional_data")
    update_collection_sec(to_collection,result, {"일자":  result['일자'] })

    return result

def check_stock_data_anal4(date, data_collection , target_percent):
    rising_stock = []
    down_stock = []
    if type(data_collection) == dict :
        stock_code = data_collection['stock_code']
    else:
        #검증 대상 collection
        stock_code = data_collection.find_one({"일자" : date})['stock_code']

    ''' 검증된 종목에 대해 추가 분석
        
        검증 종목중 상승 종목과 하락 종목의
        당일/전일 누적거래량 비교
        당일 외국인 매수 , 개인매수, 기관 매수 비율 , 전일대비율 비교
        당일 00905 거래량 과 전일 0905 거래량비교
        전일 /당일 토탈 거래량 비율
         전일 /당일 5분 거래량 비율
    '''
    new_TR_1206 = make_collection("stock_data", "new_TR_1206")
    for i in stock_code:
        check_data = new_TR_1206.find_one({"일자" : date, "단축코드" : i})
        if check_data["전일대비율"] >= target_percent:
            rising_stock.append(i)
        else:
            down_stock.append(i)

    print("목표 상회 종목   " + str(rising_stock))
    print("목표 하회 종목   " + str(down_stock))

    before_date = get_kr_working_day_by_diff(date, -1).strftime("%Y%m%d")

    rising_stock_data = new_TR_1206.find({"일자" : date, "단축코드" : {"$in" : rising_stock}}).sort([("전일대비율" ,-1)])
    TR_SCHART_data = make_collection("stock_data" , "TR_SCHART")

    for i in rising_stock_data:
        rising_before_data = new_TR_1206.find_one({"일자": before_date, "단축코드" : i["단축코드"]})
        print("단축코드   " + i["단축코드"] + "  누적거래량   " + i["누적거래량"] + " 전일 누적거래량   " + rising_before_data["누적거래량"] + "  외국인 매수 비율  " + str(int(i["외국인순매수거래량"]) / int(i["누적거래량"])) + " 개인 매수 배율   " + str(int(i["개인순매수거래량"]) / int(i["누적거래량"])) + "    기관 매수 비율  " + str(int(i["기관순매수거래량"]) / int(i["누적거래량"])) + " 전일대비율  " + str(i["전일대비율"]))
        print("당일 0905 거래량   " + TR_SCHART_data.find_one({"단축코드" : i["단축코드"] , "일자" : date, "시간" : "0905"})["단위거래량"] + "    전일 0905 거래량   " + TR_SCHART_data.find_one({"단축코드" : i["단축코드"] , "일자" : before_date, "시간" : "0905"})["단위거래량"] )
        print(" 토탈 거래량 비교   전일비  " + str (int(i["누적거래량"])/int(rising_before_data["누적거래량"])))
        print(" 5분 거래량 비교   전일비  " + str (int(TR_SCHART_data.find_one({"단축코드" : i["단축코드"] , "일자" : date, "시간" : "0905"})["단위거래량"])/int(TR_SCHART_data.find_one({"단축코드" : i["단축코드"] , "일자" : before_date, "시간" : "0905"})["단위거래량"])))
        '''if int(i["외국인순매수누적거래량"]) >0 :
            print("단축코드   " + i["단축코드"] + "  누적거래량   "  + i["누적거래량"] +   "  외국인 매수 비율  " + str(int(i["외국인순매수거래량"])/int(i["누적거래량"])) + " 개인 매수 배율   " +str(int(i["개인순매수거래량"])/int(i["누적거래량"]))  +"    기관 매수 비율  " + str(int(i["기관순매수거래량"])/int(i["누적거래량"])) +" 전일대비율  " + str(i["전일대비율"]) )
        else:
            print("단축코드   " + i["단축코드"] + "  누적거래량   "  + i["누적거래량"] +   "  외국인 매수 비율  " + str(int(i["외국인순매수거래량"])/int(i["누적거래량"])) + " 개인 매수 배율   " +str(int(i["개인순매수거래량"])/int(i["누적거래량"]))  +"    기관 매수 비율  " + str(int(i["기관순매수거래량"])/int(i["누적거래량"])) +" 전일대비율  " + str(i["전일대비율"]) )'''

    down_stock_data = new_TR_1206.find({"일자" : date, "단축코드" : {"$in" : down_stock}}).sort([("전일대비율" ,-1)])
    print("목표치 하회 종목들")
    for i in down_stock_data:
        down_before_data = new_TR_1206.find_one({"일자": before_date, "단축코드" : i["단축코드"]})
        print("단축코드   " + i["단축코드"] + "  누적거래량   " + i["누적거래량"] + " 전일 누적거래량   " + down_before_data["누적거래량"] + "  외국인 매수 비율  " + str(int(i["외국인순매수거래량"]) / int(i["누적거래량"])) + " 개인 매수 배율   " + str(int(i["개인순매수거래량"]) / int(i["누적거래량"])) + "    기관 매수 비율  " + str(int(i["기관순매수거래량"]) / int(i["누적거래량"])) + " 전일대비율  " + str(i["전일대비율"]))
        print("당일 0905 거래량   " + TR_SCHART_data.find_one({"단축코드" : i["단축코드"] , "일자" : date, "시간" : "0905"})["단위거래량"] + "    전일 0905 거래량   " + TR_SCHART_data.find_one({"단축코드" : i["단축코드"] , "일자" : before_date, "시간" : "0905"})["단위거래량"] )
        print(" 토탈 거래량 비교   전일비  " + str (int(i["누적거래량"])/int(down_before_data["누적거래량"])))
        print(" 5분 거래량 비교   전일비  " + str (int(TR_SCHART_data.find_one({"단축코드" : i["단축코드"] , "일자" : date, "시간" : "0905"})["단위거래량"])/int(TR_SCHART_data.find_one({"단축코드" : i["단축코드"] , "일자" : before_date, "시간" : "0905"})["단위거래량"])))

        '''if int(i["외국인순매수누적거래량"]) >0 :
            print("단축코드   " + i["단축코드"] + "  누적거래량   "  + i["누적거래량"] +   "  외국인 매수 비율  " + str(int(i["외국인순매수거래량"])/int(i["누적거래량"])) + " 개인 매수 배율   " +str(int(i["개인순매수거래량"])/int(i["누적거래량"]))  +"    기관 매수 비율  " + str(int(i["기관순매수거래량"])/int(i["누적거래량"])) +" 전일대비율  " + str(i["전일대비율"]) )
        else:
            print("단축코드   " + i["단축코드"] + "  누적거래량   "  + i["누적거래량"] +   "  외국인 매수 비율  " + str(int(i["외국인순매수거래량"])/int(i["누적거래량"])) + " 개인 매수 배율   " +str(int(i["개인순매수거래량"])/int(i["누적거래량"]))  +"    기관 매수 비율  " + str(int(i["기관순매수거래량"])/int(i["누적거래량"])) +" 전일대비율  " + str(i["전일대비율"]) )'''

if __name__ ==  "__main__":

    date_list = get_kr_working_day("20201215" , "20201215")

    for day in date_list:
        day = day.strftime("%Y%m%d")
        db_name ="3daySupply"
        from_collection = make_collection("stock_data" , db_name)
        stock_code = from_collection.find_one({"일자" : day})
        target_percent = 5.0
        additional_data = make_collection("stock_data" , "additional_data")
        print("3day Supply len   "  +str(from_collection.count()))
        # analysis3 의 로직을통해 구해진 3daysupply 에서 조건을 추가해 additional data를 만든다 TR_SCHART 예측 당일의 데이터를 비교하는 것이기 때문에 따로 빼서 구현
        additional_result = additional_condition(stock_code)

        result1 = check_rising_stock(from_collection.find_one({"일자"  : day}),target_percent)

        print("      3daySupply       ")
        print(day)
        print("전체종목수   " + str(result1["전체종목수"]))
        print("전체종목중상승종목   " + str(len(result1["전체종목중상승종목"])))
        print("후보종목수   " + str(result1["후보종목수"]))
        print("후보종목중상승종목   " + str(len(result1["후보종목중상승종목"])))
        print("전체종목수 - 후보종목수   " + str( result1["전체종목수"]-result1["후보종목수"]))
        print("후보종목외상승종목   " + str(len(result1["후보종목외상승종목"])))
        check_stock_data_anal4(day, from_collection, target_percent)


        print("      3daySupply       ")

        result = check_rising_stock(additional_result,target_percent)

        print("      additional_data       ")
        print(day)
        print("전체종목수   " + str(result["전체종목수"]))
        print("전체종목중상승종목   " + str(len(result["전체종목중상승종목"])))
        print("후보종목수   " + str(result["후보종목수"]))
        print("후보종목중상승종목   " + str(len(result["후보종목중상승종목"])))
        print("전체종목수 - 후보종목수   " + str( result["전체종목수"]-result["후보종목수"]))
        print("후보종목외상승종목   " + str(len(result["후보종목외상승종목"])))
        print("      additional_data       ")

        check_stock_data_anal4(day, additional_data, target_percent)

    '''print_anal4(date,collection )
    stock_code = collection.find_one({"일자" : date})
    collection2 = make_collection("stock_data" , "TR_SCHART")
    additional_result = additional_condition(stock_code,collection2)'''


    '''collection = make_collection("stock_data" , "5daySupply")

    stock_code = collection.find_one({"일자" : "20201125"})["stock_code"]

    real_rise = []
    real_down = []
    for i in stock_code:'''



