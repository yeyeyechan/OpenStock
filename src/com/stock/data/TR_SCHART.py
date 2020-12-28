

# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\OpenStock")
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari

'''
TR_SCHART 설명

종목별 일별 수급, 가격 , 등 정보 가져 올수있다.
'''
def TR_SCHART(**kwargs):
    try:
        app = QApplication(sys.argv)
        param_dict = locals()['kwargs']
        if param_dict['type'] == "search":
            start_date = param_dict['start_date']
            end_date = param_dict['end_date']

        IndiControl = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")

        if param_dict['type'] == "real_time":
            drop_collection("stock_data", "real_TR_SCHART")
            TR_SCHART = indi_object("real_TR_SCHART", IndiControl)
            date_list = get_kr_working_day(com_vari.Today_date,com_vari.Today_date)
            #stock_mst = make_collection("stock_data" , "stock_mst")
            stock_data = make_collection("stock_data" , "3daySupply").find_one({'일자' :com_vari.Today_date })["stock_code"]
            input_dict_list = []
            for i in stock_data:
                stock_code = i
                graph_kind = "1"
                time_gap = "5"
                start_date =date_list[0].strftime("%Y%m%d")
                end_date =date_list[-1].strftime("%Y%m%d")
                search_count = com_vari.tr_schart_real_count
                input_dict_list.append(copy([stock_code , graph_kind, time_gap , start_date, end_date, search_count]))
        else:
            TR_SCHART = indi_object("TR_SCHART", IndiControl)
            date_list = get_kr_working_day(start_date, end_date)
            stock_mst = make_collection("stock_data" , "stock_mst")
            input_dict_list = []
            for i in stock_mst.find():
                stock_code = i["단축코드"]
                graph_kind = "1"
                time_gap = "5"
                start_date =date_list[0].strftime("%Y%m%d")
                end_date =date_list[-1].strftime("%Y%m%d")
                search_count = "237"
                input_dict_list.append(copy([stock_code , graph_kind, time_gap , start_date, end_date, search_count]))
        TR_SCHART.set_input_data(input_dict_list)
        TR_SCHART.call_tr()
        app.exec_()
    except:
        return False
    return True
def call_TR_SCHART():
    print("sibal")
    TR_SCHART(type = 'search',start_date='20200112', end_date='20200115')
def real_TR_SCHART():
    print("sibal")
    TR_SCHART(type = 'real_time',start_date= com_vari.Today_date , end_date=com_vari.Today_date)
def scheduler_TR_SCHART():
    sched_sc = BlockingScheduler()
    sched_sc.add_job(real_TR_SCHART, CronTrigger(hour='9-16', minute='*/3'))
    sched_sc.start()
if __name__ == "__main__":
    scheduler_TR_SCHART()
    '''#drop_collection("stock_data", "TR_SCHART")
    app = QApplication(sys.argv)

    IndiControl = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
    drop_collection("stock_data", "real_TR_SCHART")
    TR_SCHART = indi_object("real_TR_SCHART", IndiControl)

    if len(sys.argv) > 1 and sys.argv[1] == "real_time":
        drop_collection("stock_data", "real_TR_SCHART")
        TR_SCHART = indi_object("real_TR_SCHART", IndiControl)
        date_list = get_kr_working_day(com_vari.Today_date,com_vari.Today_date)
        #stock_mst = make_collection("stock_data" , "stock_mst")
        stock_data = make_collection("stock_data" , "3daySupply").find_one({'일자' :com_vari.Today_date })["stock_code"]
        input_dict_list = []
        for i in stock_data:
            stock_code = i
            graph_kind = "1"
            time_gap = "5"
            start_date =date_list[0].strftime("%Y%m%d")
            end_date =date_list[-1].strftime("%Y%m%d")
            search_count = com_vari.tr_schart_real_count
            input_dict_list.append(copy([stock_code , graph_kind, time_gap , start_date, end_date, search_count]))
    else:
        TR_SCHART = indi_object("TR_SCHART", IndiControl)
        date_list = get_kr_working_day("20201224","20201224")
        stock_mst = make_collection("stock_data" , "stock_mst")
        input_dict_list = []
        for i in stock_mst.find():
            stock_code = i["단축코드"]
            graph_kind = "1"
            time_gap = "5"
            start_date =date_list[0].strftime("%Y%m%d")
            end_date =date_list[-1].strftime("%Y%m%d")
            search_count = "237"
            input_dict_list.append(copy([stock_code , graph_kind, time_gap , start_date, end_date, search_count]))
    TR_SCHART.set_input_data(input_dict_list)
    TR_SCHART.call_tr()
    app.exec_()'''

