import sys

sys.path.append("C:\\dev\\OpenStock")

from src.com.stock.common.import_lib import *
def find_stock():
    data = make_collection("stock_data", "3daySupply")
    stock_data= data.find_one({"일자" : "20210114"})["stock_code"]
    TR_1206 = make_collection("stock_data", "new_TR_1206")

    for i in stock_data:
        TR_1206_data = TR_1206.find_one({"일자" : "20210114" , "단축코드" : i})

        if TR_1206_data["전일대비율"] > 5.0:
            print(i)

def cleansing_data():
    data = make_collection("stock_data", "3daySupply")
    stock_data= data.find_one({"일자" : "20210114"})["stock_code"]
    SK = make_collection("stock_data", "SK")
    SP = make_collection("stock_data", "SP")

    for i in stock_data:
        for j in SK.find({"일자" : "20210114", "단축코드" : i}):
            if j["체결시간"] =="" :
                SK.delete_one({"_id" :j["_id"]})
        for j in SP.find({"일자" : "20210114", "단축코드" : i}):
            if j["시간"] =="" :
                SP.delete_one({"_id" :j["_id"]})
def check_3day_data():
    data = make_collection("stock_data", "3daySupply")
    stock_data= data.find_one({"일자" : "20210114"})["stock_code"]

    data.delete_many({"일자" : "20210114"})

    SK = make_collection("stock_data", "SK")
    SP = make_collection("stock_data", "SP")

    new_data = []
    for i in stock_data:
        if SK.find_one({"일자" : "20210114", "단축코드" : i}) is not None and SP.find_one({"일자" : "20210114", "단축코드" : i}) is not None :
            new_data.append(i)

    result ={"일자" : "20210114" , "stock_code":[]}
    result["stock_code"] = new_data

    update_collection(data,result)

def find_new_stocks():
    stock_mst = make_collection("stock_data", "stock_mst")
    TR_1206_2 = make_collection("stock_data", "TR_1206_2")
    result_upjong = {}
    upjong_code_mst = make_collection("stock_data", "upjong_code_mst")

    #drop_collection("stock_data", "TR_1206_2")
    test_start_date = "20201224"
    test_end_date = "20210115"
    #check = subprocess.call([sys.executable, basic_path + "\\data\\TR_1206.py", "new_search", test_start_date, test_end_date])
    result = []
    for i in stock_mst.find():
        first_data = TR_1206_2.find_one({'단축코드' : i["단축코드"], "일자" : test_start_date})
        if first_data is None:
            continue
        last_data =TR_1206_2.find_one({'단축코드' : i["단축코드"], "일자" : test_end_date})
        if last_data is None:
            continue
        if int(last_data["외국인순매수누적거래량"]) >  int(first_data["외국인순매수누적거래량"]) and int(last_data["개인순매수누적거래량"]) <0 and int(last_data["프로그램누적순매수"]) >0:
            print("단축코드   "  + i["단축코드"] + "   외국인 순매수 누적개래량 비교 성공 ")
            #if  (int(last_data["가격"]) -  int(first_data["가격"]))/ int(first_data["가격"]) *100.0 <15.0 and int(last_data["가격"]) *int(last_data["누적거래량"])>=10000000000 :
            #    print("가격 상승 15 퍼 이내")
            check =True
            for j in TR_1206_2.find({"단축코드": i["단축코드"]}):
                #if int(j["외국인순매수누적거래량"]) < 0 or int(j["기관순매수누적거래량"]) < 0:
                if int(j["외국인순매수누적거래량"]) < 0 :
                    print("단축코드   " + i["단축코드"] + "   외국인 순매수 or 기관 순매수 누적개래량 음 발견 ")
                    check = False
                    break
            if check:
                for j in upjong_code_mst.find({"단축코드": i["단축코드"]}):
                    print(j["업종명"], end="")
                    if not (j["업종명"] in result_upjong.keys()):
                        result_upjong[j["업종명"]] = 1
                    else:
                        result_upjong[j["업종명"]] += 1
                print("최종 합격 발생")
                result.append(i["단축코드"])
    result_db_name = "3daySupply"
    to_collection = make_collection("stock_data", result_db_name)
    to_collection.delete_one({"일자": "20210118"})
    data = {"일자": "20210118", "stock_code": ""}
    data["stock_code"] = result

    update_collection_sec(to_collection, data, {"일자":"20210118"})
    print(result)
    print(result_upjong)
    print(len(result))

def find_top_upjong():
    result_db_name = "3daySupply"
    to_collection = make_collection("stock_data", result_db_name).find_one({"일자" : "20210118"})["stock_code"]
    upjong_code_mst = make_collection("stock_data", "upjong_code_mst")

    data = {"일자" : "20210118", "stock_data": []}
    for i in to_collection:
        for j in upjong_code_mst.find({"단축코드" : i}):
            if j["업종명"] == "제조업" or  j["업종명"] == "제조":
                data["stock_data"].append(j["단축코드"])
    monitoring = make_collection("stock_data", "monitoring")
    drop_collection("stock_data", "monitoring")
    monitoring.insert_one(data)


def print_top_rising_stock():
    test_date = "20210112"
    new_TR_1206 = make_collection("stock_data", "new_TR_1206").find({"일자": test_date})

    for i in new_TR_1206:
        if i["전일대비율"] >10.0 :

           print(i)

def make_new_3daySupply():
    test_date = "20210111"
    new_TR_1206 = make_collection("stock_data", "new_TR_1206").find({"일자": test_date})
    result_db_name = "3daySupply"
    to_collection = make_collection("stock_data", result_db_name)
    result ={
        "일자" : "20210112",
        "stock_code": []
    }
    for i in new_TR_1206:
        if i["전일대비율"] >=0 and int(i["외국인순매수거래량"]) >0 and int(i["개인순매수거래량"]) <0 and int(i["프로그램순매수"]) >0 and int(i["기관순매수거래량"]) >0 and int(i["누적거래량"]) * int(i["가격"]) >= 10000000000 and int(i["외국인순매수거래량"])** int(i["가격"]) >= 400000000 :
            result["stock_code"].append(i["단축코드"])
            print(i["단축코드"])
    update_collection_sec(to_collection , result , {"일자" :test_date})
if __name__ ==  "__main__":
    #find_new_stocks()
    #check_3day_data()
    #cleansing_data()
    #find_new_stocks()
    find_top_upjong()
