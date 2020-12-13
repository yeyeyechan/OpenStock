

# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\OpenStock")
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari




if __name__ == "__main__":
    app = QApplication(sys.argv)
    logic_name= "3daySupply"
    from_collection = make_collection("stock_data", logic_name)
    from_collection = from_collection.find_one({"일자": "20201125"})["stock_code"]
    SC = real_indi_object("SC")
    SC.set_input_data(from_collection)
    SC.call_tr()

    '''logic_name = "logic3"


    from_collection = make_collection("stock_data", logic_name)

    collection = make_collection("stock_data", "Real_Time_SK")
    activate_Tr = real_tr_object("SK", collection)

    input_list = []
    for i in from_collection.find({"일자": com_vari.Today_date}):
        input_list.append(copy(i["stock_code"]))
    pk_dict["일자"] = com_vari.Today_date

    collection_len = len(input_list)
    activate_Tr.set_multi_call(input_list, col_name, pk_dict, collection_len)'''

    app.exec_()


