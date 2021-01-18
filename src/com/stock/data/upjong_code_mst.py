

# -*- coding: utf-8 -*-
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari

'''
upjong_code_mst 설명


'''
def make_upjong_code_mst():

    upjong_mst = make_collection("stock_data","upjong_mst")
    upjong_code_mst = make_collection("stock_data","upjong_code_mst")
    result = []
    for i in upjong_code_mst.find():
        upjong_mst_data = upjong_mst.find_one({"업종코드" : i["업종코드"]})
        i["업종명"] = upjong_mst_data["업종명"]
        i["시장코드"] = upjong_mst_data["시장코드"]
        i["시장명"] = upjong_mst_data["시장명"]
        del i['_id']
        result.append(copy(i))
    drop_collection("stock_data", "upjong_code_mst")
    upjong_code_mst.insert_many(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    drop_collection("stock_data", "upjong_code_mst")

    upjong_code_mst = make_collection("stock_data", "upjong_code_mst")
    upjong_mst = make_collection("stock_data", "upjong_mst")

    IndiControl = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")

    upjong_code_mst = indi_object("upjong_code_mst", IndiControl)

    input_dict_list = []
    for i in upjong_mst.find():
        input_data = []
        input_data.append((i["업종코드"]))
        input_dict_list.append(copy(input_data))

    upjong_code_mst.set_input_data(input_dict_list)
    upjong_code_mst.call_tr()
    app.exec_()
    make_upjong_code_mst()