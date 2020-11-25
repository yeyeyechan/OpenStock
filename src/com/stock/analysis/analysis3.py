from src.com.stock.common.import_lib import *



if __name__ ==  "__main__":

    collection = make_collection("stock_data" , "TR_1206")
    date = "20201126"
    day_range = -5
    date_list = get_kr_str_working_day_list_by_diff(date,day_range)

    from_collection = make_collection("stock_data" , "stock_mst")
    result_list =[]
    print(date_list)
    for i in from_collection.find():
        per_vol = 0
        for_vol = 0
        com_vol = 0
        if len(date_list) == 5:
            for j in collection.find({"단축코드" : i["단축코드"], "일자" :{"$in" : date_list}}):
                per_vol += int(j["개인순매수거래량"])
                for_vol += int(j["외국인순매수거래량"])
                com_vol += int(j["기관순매수거래량"])
        else:
            continue

        if per_vol <0 and for_vol >0 and com_vol >0 :
            result_list.append(i["단축코드"])

    save_collection = make_collection("stock_data" , "logic4")

    data = {"일자" :"20201126" , "stock_code": ""}
    data["stock_code"]= result_list

    update_collection(save_collection, data)


