from src.com.stock.common.import_lib import *
def print_anal4(date, from_collection):
    check_data = from_collection.find_one({'일자' : date})["stock_code"]
    print(len(check_data))
    print(str(check_data))
def additional_condition(data, collection):
    result = {}
    result['일자'] = data["일자"]
    result['stock_code'] = []
    from_collection = make_collection("stock_data", "TR_1206")
    for i in data["stock_code"]:
        today_data = collection.find_one({"일자": data["일자"], "단축코드" : i, "시간" : "0905"})["종가"]
        print(i)
        before_data = from_collection.find_one({"일자": "20201130", "단축코드" : i})["가격"]
        if check_first_price(today_data , before_data , 0.7 ,2.0):
            result['stock_code'].append(i)
            print("additional_condition" + i)
    return result

def check_stock_data_anal4(date, from_collection , check_collection, target_percent):

    rising_stock = []
    down_stock = []

    from_data = from_collection.find_one({"일자" : date})['stock_code']

    for i in from_data:
        check_data = check_collection.find_one({"일자" : date, "단축코드" : i})
        if check_data["전일대비율"] >= target_percent:
            rising_stock.append(i)
        else:
            down_stock.append(i)

    print("상승 종목   " + str(rising_stock))
    print("하락 종목   " + str(down_stock))

    check_data = check_collection.find({"일자" : date, "단축코드" : {"$in" : rising_stock}}).sort([("전일대비율" ,-1)])
    for i in check_data:
        if int(i["외국인순매수누적거래량"]) >0 :
            print("단축코드   " + i["단축코드"] + "  누적거래량   "  + i["누적거래량"] +   "  외국인 매수 비율  " + str(int(i["외국인순매수거래량"])/int(i["누적거래량"])) + " 개인 매수 배율   " +str(int(i["개인순매수거래량"])/int(i["누적거래량"]))  +"    기관 매수 비율  " + str(int(i["기관순매수거래량"])/int(i["누적거래량"])) +" 전일대비율  " + str(i["전일대비율"]) )
        else:
            print("단축코드   " + i["단축코드"] + "  누적거래량   "  + i["누적거래량"] +   "  외국인 매수 비율  " + str(int(i["외국인순매수거래량"])/int(i["누적거래량"])) + " 개인 매수 배율   " +str(int(i["개인순매수거래량"])/int(i["누적거래량"]))  +"    기관 매수 비율  " + str(int(i["기관순매수거래량"])/int(i["누적거래량"])) +" 전일대비율  " + str(i["전일대비율"]) )

if __name__ ==  "__main__":
    date = "20201202"
    collection = make_collection("stock_data" , "3daySupply")

    print_anal4(date,collection )
    '''db_name ="3daySupply"
    collection = make_collection("stock_data" , "new_TR_1206")
    from_collection = make_collection("stock_data" , db_name)
    target_percent = 5.0
    from_collection = make_collection("stock_data" , db_name)
    stock_code = from_collection.find_one({"일자" : date})

    collection2 = make_collection("stock_data" , "TR_SCHART")
    additional_result = additional_condition(stock_code,collection2)
    result = check_rising_stock(additional_result,collection,target_percent)

    print(date)
    print("전체종목수   " + str(result["전체종목수"]))
    print("전체종목중상승종목   " + str(len(result["전체종목중상승종목"])))
    print("후보종목수   " + str(result["후보종목수"]))
    print("후보종목중상승종목   " + str(len(result["후보종목중상승종목"])))
    print("전체종목수 - 후보종목수   " + str( result["전체종목수"]-result["후보종목수"]))
    print("후보종목외상승종목   " + str(len(result["후보종목외상승종목"])))

    check_stock_data_anal4(date, from_collection ,collection ,target_percent)'''
    '''collection = make_collection("stock_data" , "5daySupply")

    stock_code = collection.find_one({"일자" : "20201125"})["stock_code"]

    real_rise = []
    real_down = []
    for i in stock_code:'''



