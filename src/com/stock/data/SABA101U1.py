# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\OpenStock")
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari


if __name__ == "__main__":
    app = QApplication(sys.argv)
    input_dict = {
        "계좌번호" : "27024779616",
        "계좌상품" : "01",
        "계좌비밀번호" : "6930",
        "선물대용매도여부" : "0",
        "신용거래구분" : "00",
        "매수매도구분" : "2",
        "종목코드" : "A055550",
        "주문수량" : "1",
        "주문가격" : "42800",
        "정규시간외구분코드" : "1",
        "호가유형코드" : "2",
        "주문조건코드" : "0",
        "신용대출통합주문구분코드" : "0",
        "결과메시지 처리여부" : "Y",
    }
    IndiControl = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
    SABA101U1 = indi_object("SABA101U1", IndiControl)
    SABA101U1.set_input_data_dict(input_dict)
    SABA101U1.call_tr()
    app.exec_()
