

# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\OpenStock")
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari


if __name__ == "__main__":
    drop_collection("stock_data", "TR_1205")
    app = QApplication(sys.argv)
    IndiControl = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")

    upjong = ["0", "1"]
    start_date = get_kr_working_day("20201101", "20201130")
    input_dict_list= []
    for i in upjong:
        for j in start_date:
            input_list = [i, j.strftime("%Y%m%d"),j.strftime("%Y%m%d"), "K"]
            input_dict_list.append(copy(input_list))

    stock_mst = indi_object("TR_1205", IndiControl)
    stock_mst.set_input_data(input_dict_list)
    stock_mst.call_tr()

    app.exec_()

    total_TR_1205_count = make_collection("stock_data", "TR_1205").estimated_document_count()

    print("실제 db 적제된 document 갯수     "+str(total_TR_1205_count))

    print("원래")
