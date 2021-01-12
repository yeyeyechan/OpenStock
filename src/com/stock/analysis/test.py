import sys

sys.path.append("C:\\dev\\OpenStock")

from src.com.stock.common.import_lib import *




if __name__ ==  "__main__":
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


