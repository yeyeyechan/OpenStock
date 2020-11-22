# -*- coding: utf-8 -*-
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari

input_dict = {}  # tr 호출 인풋 값 dictionary , make_dict 에 배열을 넣어 만들어준다.

# 아웃풋 컬럼명 배열

pk_dict = {}  # document 간 pk나 중요정보로 추가되어야하는 값

input_dict_list = []
pk_dict_list = []
if __name__ == "__main__":
    #drop_collection("stock_data", "TR_1500_1")
    app = QApplication(sys.argv)

    collection = make_collection("stock_data", "TR_1500_1")
    from_collection = make_collection("stock_data" , "TR_1500")

    IndiControl = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")

    activate_Tr = tr_class("TR_1500_1 ", collection, IndiControl)

    for i in from_collection.find():
        input_dict_list.append(copy(make_dict([i["L분류코드"]+i["S분류코드"]])))
        pk_dict["L분류코드"] = i["L분류코드"]
        pk_dict["S분류코드"] = i["S분류코드"]
        pk_dict_list.append(copy(pk_dict))
    input_len = len(input_dict_list)
    activate_Tr.set_multi_call(input_dict_list, pk_dict_list, input_len)

    app.exec_()

    TR_1500_1_count = make_collection("stock_data", "TR_1500_1").estimated_document_count()

    print("TR_1500_1 테마그룹 조회 총 조회 갯수   " + str(TR_1500_1_count))