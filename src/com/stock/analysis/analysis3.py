from src.com.stock.common.import_lib import *

def check_rising_stock(data, db, target_percent):

    other_stock_list = []
    result_stock_list = []
    result_dict = {}
    result_dict["전체종목수"] = db.find({"일자" : data["일자"]}).count()
    result_dict["후보종목수"] = len(data["stock_code"])
    result_dict["전체종목중상승종목"] = []
    result_dict["후보종목중상승종목"] = []
    result_dict["후보종목외상승종목"] = []

    for i in db.find({"일자" : data["일자"]}):
        if i["전일대비율"] >= target_percent:
            result_dict["전체종목중상승종목"].append(i["단축코드"])
            if i["단축코드"] in data["stock_code"] :
                result_dict["후보종목중상승종목"].append(i["단축코드"])
            else:
                result_dict["후보종목외상승종목"].append(i["단축코드"])

    return result_dict

if __name__ ==  "__main__":

    collection = make_collection("stock_data" , "new_TR_1206")
    date = "20201201"
    day_range = -3
    date_count = abs(day_range)
    result_db_name = "3daySupply"
    date_list = get_kr_str_working_day_list_by_diff(date,day_range)

    from_collection = make_collection("stock_data" , "stock_mst")
    to_collection = make_collection("stock_data" , result_db_name)
    result_list =[]
    print(date_list)
    for i in from_collection.find():
        index = True
        per_vol = 0
        for_vol = 0
        com_vol = 0
        pro_vol = 0

        last_per_vol = 0
        last_for_vol = 0
        last_com_vol = 0
        last_pro_vol = 0

        if len(date_list) == date_count:
            for j in collection.find({"단축코드" : i["단축코드"], "일자" :{"$in" : date_list}}):
                if index :
                    last_per_vol = int(j["개인순매수거래량"])
                    last_for_vol = int(j["외국인순매수거래량"])
                    last_com_vol = int(j["기관순매수거래량"])
                    last_pro_vol = int(j["프로그램순매수"])

                    index = False
                per_vol += int(j["개인순매수거래량"])
                for_vol += int(j["외국인순매수거래량"])
                com_vol += int(j["기관순매수거래량"])
                pro_vol += int(j["프로그램순매수"])
        else:
            continue

        if per_vol <0 and for_vol >0 and com_vol >0 and pro_vol >0 and  last_per_vol <0 and last_for_vol >0 and last_com_vol >0 and last_pro_vol >0:
            print(i["단축코드"])
            result_list.append(i["단축코드"])

    #save_collection = make_collection("stock_data" , "logic4")

    data = {"일자" :date , "stock_code": ""}
    data["stock_code"]= result_list

    update_collection_sec(to_collection,data, {"일자": date})
    '''result = check_rising_stock(data,collection,5.0)

    print(date)
    print(result["전체종목수"])
    print(result["전체종목중상승종목"])
    print(result["후보종목수"])
    print(result["후보종목중상승종목"])
    print(result["전체종목수"]-result["후보종목수"])
    print(result["후보종목외상승종목"])'''
    #update_collection(save_collection, data)


