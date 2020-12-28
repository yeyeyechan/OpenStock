

# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\OpenStock")
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari

'''
TR_1206 설명

종목별 일별 수급, 가격 , 등 정보 가져 올수있다.
'''

if __name__ == "__main__":
    #drop_collection("stock_data", "TR_1206")
    app = QApplication(sys.argv)

    from_collection = make_collection("stock_data", "stock_mst")
    collection_len = from_collection.estimated_document_count()
    index =0
    IndiControl = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
    if  len(sys.argv) > 1 and  sys.argv[1] == "search":
        start_date = sys.argv[2]
        end_date = sys.argv[3]
    if len(sys.argv) > 1 and  sys.argv[1] == "real_time":
        stock_data = make_collection("stock_data" , "3daySupply").find_one({'일자' :com_vari.Today_date })["stock_code"]
        drop_collection("stock_data", "real_TR_1206")
        TR_1206 = indi_object("real_TR_1206", IndiControl)
        start_date = com_vari.Today_date
        end_date = com_vari.Today_date
        gubun = "1"
        data_kind = "0"
        check_list = integrity_db_count(start_date, end_date, collection_len)
        com_vari.TR_1206_each_counts = check_list[0]
        com_vari.TR_1206_all_counts = check_list[1]
        input_list = ["", start_date, end_date, gubun, data_kind]

        input_dict_list = []
        for i in stock_data:
            stock_code = i
            input_list[0] = stock_code
            input_dict_list.append(copy(input_list))
    else:
        TR_1206 = indi_object("TR_1206", IndiControl)
        gubun = "1"
        data_kind = "0"
        check_list = integrity_db_count(start_date, end_date , collection_len)
        com_vari.TR_1206_each_counts = check_list[0]
        com_vari.TR_1206_all_counts = check_list[1]
        input_list = ["", start_date, end_date, gubun, data_kind]

        input_dict_list = []
        for i in from_collection.find():
            stock_code = i["단축코드"]

            input_list[0] = stock_code
            input_dict_list.append(copy(input_list))

    com_vari.TR_1206_logger.debug("TR_1206 호출 시작")
    TR_1206.set_input_data(input_dict_list)
    TR_1206.call_tr()
    com_vari.TR_1206_logger.debug("TR_1206 호출 완료")

    app.exec_()

    total_TR_1206_count = make_collection("stock_data", "TR_1206").estimated_document_count()

    print("예상되는 실제 db 적재 document 갯수   "+ str(check_list[1]))
    print("실제 db 적제된 document 갯수     "+str(total_TR_1206_count) )

    print("원래")
