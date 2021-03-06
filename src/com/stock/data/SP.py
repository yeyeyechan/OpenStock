

# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\OpenStock")
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari

def SP(**kwargs):
    try:
        logic_name = "3daySupply"
        from_collection = make_collection("stock_data", logic_name)
        from_collection = from_collection.find_one({"일자": com_vari.Today_date})["stock_code"]
        app = QApplication(sys.argv)
        IndiControl = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")

        param_dict = locals()['kwargs']
        if param_dict['type'] == "search":
            SP = indi_object("SP", IndiControl)
            SP.set_input_data(from_collection)
        elif param_dict['type'] == "real_time":
            SP = real_indi_object("SP")
            SP.set_input_data(from_collection)
        SP.call_tr()
        app.exec_()
    except:
        return False
    return True

def call_SP():
    SP(type = 'search')
def scheduler_SP():
    sched_sc = BlockingScheduler()
    sched_sc.add_job(call_SP, CronTrigger(hour='9-23', minute='*/1'))
    sched_sc.start()

if __name__ == "__main__":
    scheduler_SP()
    '''logic_name = "logic3"


    from_collection = make_collection("stock_data", logic_name)

    collection = make_collection("stock_data", "Real_Time_SK")
    activate_Tr = real_tr_object("SK", collection)

    input_list = []
    for i in from_collection.find({"일자": com_vari.Today_date}):
        input_list = copy(i["stock_code"])
    pk_dict["일자"] = com_vari.Today_date

    collection_len = len(input_list)
    activate_Tr.set_multi_call(input_list, col_name, pk_dict, collection_len)'''



