

# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\OpenStock")
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari

'''
TR_SCHART 설명

종목별 일별 수급, 가격 , 등 정보 가져 올수있다.
'''



if __name__ == "__main__":
    #drop_collection("stock_data", "TR_SCHART")
    app = QApplication(sys.argv)

    IndiControl = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")

    date_list = get_kr_working_day("20201216","20201217")
    TR_SCHART = indi_object("TR_SCHART", IndiControl)
    stock_mst = make_collection("stock_data" , "stock_mst")
    input_dict_list = []
    for i in stock_mst.find():
        stock_code = i["단축코드"]
        graph_kind = "1"
        time_gap = "5"
        start_date =date_list[0].strftime("%Y%m%d")
        end_date =date_list[-1].strftime("%Y%m%d")
        search_count = "158"
        input_dict_list.append(copy([stock_code , graph_kind, time_gap , start_date, end_date, search_count]))
    TR_SCHART.set_input_data(input_dict_list)
    TR_SCHART.call_tr()
    app.exec_()

