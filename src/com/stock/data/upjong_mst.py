# -*- coding: utf-8 -*-
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari

def make_upjong_mst():
    upjong_dict = {
        "1" : "KOSPI",
        "2": "KOSDAQ",
        "3": "KOSPI200",
        "4": "KOSDAQ50",
        "5": "KRX"
    }
    upjong_mst = make_collection("stock_data","upjong_mst")
    result = []
    for i in upjong_mst.find():
        i["시장명"] = upjong_dict[i["시장코드"]]
        del i['_id']
        result.append(copy(i))
    drop_collection("stock_data", "upjong_mst")
    upjong_mst = make_collection("stock_data","upjong_mst")
    upjong_mst.insert_many(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    #종목코드 삭제된 종목을 날리기 위해 전부 날려버림
    drop_collection("stock_data", "upjong_mst")
    IndiControl = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")

    upjong_mst = indi_object("upjong_mst", IndiControl)

    upjong = ["1", "2", "3" , "4" , "5"] # Kospi , Kosdaq, Kopspi200,  kosdaq50, KRX

    input_dict_list = []
    for i in upjong:
        input_data = []
        input_data.append((i))
        input_dict_list.append(copy(input_data))

    upjong_mst.set_input_data(input_dict_list)
    upjong_mst.call_tr()
    app.exec_()
    make_upjong_mst()

