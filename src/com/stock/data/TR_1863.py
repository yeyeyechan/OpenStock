

# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\OpenStock")
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari

'''
TR_1863 설명

종목별 일별 수급, 가격 , 등 정보 가져 올수있다.
'''
def TR_1863(**kwargs):
    try:
        drop_collection("stock_data", "TR_1863")
        app = QApplication(sys.argv)
        param_dict = locals()['kwargs']
        if param_dict['type'] == "search":
            start_date = param_dict['start_date']
            end_date = param_dict['end_date']

        IndiControl = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")

        if param_dict['type'] == "search":
            drop_collection("stock_data", "TR_1863")
            TR_1863 = indi_object("TR_1863", IndiControl)
            date_list = get_kr_working_day(start_date,end_date)
            input_dict_list = []
            for i in date_list:
                market_gubun = "2"
                data_kind = "0"
                up_dpwm = "5"
                up_top = "30"
                vol = "1"
                if i.strftime("%Y%m%d") == com_vari.Today_date:
                    check = "0"
                else:
                    check = "1"
                date = i.strftime("%Y%m%d")
                price = "1"
                condition = "1"
                input_dict_list.append(copy([market_gubun , data_kind, up_dpwm , up_top ,vol, check,date,price,condition]))
        TR_1863.set_input_data(input_dict_list)
        TR_1863.call_tr()
        app.exec_()
    except:
        return False
    return True
if __name__ == "__main__":

    TR_1863( type = "search",start_date ="20210115",end_date = "20210115",)