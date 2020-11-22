# -*- coding: utf-8 -*-
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari



input_dict = {} # tr 호출 인풋 값 dictionary , make_dict 에 배열을 넣어 만들어준다.

pk_dict = {} # document 간 pk나 중요정보로 추가되어야하는 값

if __name__ == "__main__":
    #drop_collection("stock_data", "TR_1500")
    app = QApplication(sys.argv)

    collection = make_collection("stock_data", "TR_1500")

    IndiControl = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")

    activate_Tr = tr_class("TR_1500 ", collection, IndiControl)

    activate_Tr.set_single_call(input_dict, pk_dict)

    app.exec_()

    TR_1500_count = make_collection("stock_data", "TR_1500").estimated_document_count()

    print("TR_1500 테마그룹 조회 총 조회 갯수   "+ str(TR_1500_count))