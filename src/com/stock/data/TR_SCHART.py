

# -*- coding: utf-8 -*-
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari

'''
TR_SCHART 설명

종목별 일별 수급, 가격 , 등 정보 가져 올수있다.
'''

input_dict = {} # tr 호출 인풋 값 dictionary , make_dict 에 배열을 넣어 만들어준다.

pk_dict = {"단축코드": "" , "데이터구분":"", "시간간격" : ""} # document 간 pk나 중요정보로 추가되어야하는 값
last_call = False

if __name__ == "__main__":
    drop_collection("stock_data", "TR_SCHART")
    app = QApplication(sys.argv)
    date = "20201202"
    #from_collection = make_collection("stock_data", "additional_data").find_one({"일자": date})["stock_code"]
    index =0
    IndiControl = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
    from_collection = make_collection("stock_data" , "stock_mst")
    collection = make_collection("stock_data", "TR_SCHART")
    activate_Tr = tr_class("TR_SCHART", collection , IndiControl)

    input_dict_list = []
    pk_dict_list = []

    graph_kind = "1"
    time_gap = "5"
    start_date = "20201201"
    end_date = "20201202"
    search_count = "158"

    pk_dict["데이터구분"] = "1"
    pk_dict["시간간격"] = "5"
    for i in from_collection.find():
        if i['단축코드'] =="003670":
            print(i)
        input_dict = make_dict([i["단축코드"], graph_kind, time_gap, start_date, end_date,search_count])
        input_dict_list.append(copy(input_dict))
        pk_dict["단축코드"] = i["단축코드"]
        pk_dict_list.append(copy(pk_dict))

    collection_len = len(input_dict_list)
    activate_Tr.set_multi_call(input_dict_list,pk_dict_list,collection_len)
    app.exec_()

