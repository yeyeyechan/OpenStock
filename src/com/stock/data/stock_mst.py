

# -*- coding: utf-8 -*-
from src.com.stock.common.import_lib import *

'''
stock_mst 설명

전 종목 코드 정보 조회
'''

# 아웃풋 컬럼명 배열
if __name__ == "__main__":
    app = QApplication(sys.argv)

    #종목코드 삭제된 종목을 날리기 위해 전부 날려버림
    drop_collection("stock_data", "stock_mst")
    IndiControl = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")

    stock_mst = indi_object("stock_mst", IndiControl)
    stock_mst.set_input_data([])
    stock_mst.call_tr()


    app.exec_()
