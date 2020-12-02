# -*- coding: utf-8 -*-
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari



input_dict = {} # tr 호출 인풋 값 dictionary , make_dict 에 배열을 넣어 만들어준다.
col_name_in = ["표준코드              " ,
"단축코드              " ,
"체결시간              " ,
"매도거래원번호1       " ,
"매수거래원번호1       " ,
"매도수량1             " ,
"매수수량1             " ,
"매도대금1             " ,
"매수대금1             " ,
"매도거래원번호2       " ,
"매수거래원번호2       " ,
"매도수량2             " ,
"매수수량2             " ,
"매도대금2             " ,
"매수대금2             " ,
"매도거래원번호3       " ,
"매수거래원번호3       " ,
"매도수량3             " ,
"매수수량3             " ,
"매도대금3             " ,
"매수대금3             " ,
"매도거래원번호4       " ,
"매수거래원번호4       " ,
"매도수량4             " ,
"매수수량4             " ,
"매도대금4             " ,
"매수대금4             " ,
"매도거래원번호5       " ,
"매수거래원번호5       " ,
"매도수량5             " ,
"매수수량5             " ,
"매도대금5             " ,
"매수대금5             " ,
"총매도수량            " ,
"총매수수량            " ,
"총매도대금            " ,
"총매수대금            " ,
"국내총매도수량        " ,
"국내총매수수량        " ,
"국내총매도대금        " ,
"국내총매수대금        " ,
"국내총순매수수량      " ,
"국내총순매수대금      " ,
"외국계총매도수량      " ,
"외국계총매수수량      " ,
"외국계총매도대금      " ,
"외국계총매수대금      " ,
"외국계순매수수량      " ,
"외국계순매수대금      " ,
"전체총매도수량        " ,
"전체총매수수량        " ,
"전체총매도대금        " ,
"전체총매수대금        " ,
"전체순매수수량        " ,
"전체순매수대금        " ,
"매도증가수량1         " ,
"매수증가수량1         " ,
"매도증가수량2         " ,
"매수증가수량2         " ,
"매도증가수량3         " ,
"매수증가수량3         " ,
"매도증가수량4         " ,
"매수증가수량4         " ,
"매도증가수량5         " ,
"매수증가수량5         " ,

]  # 아웃풋 컬럼명 배열
col_name = make_dict(col_name_in) # 아웃풋 컬럼명 배열을 index ,value 형태의 dictionary로 변형
pk_dict = {"일자": ""} # document 간 pk나 중요정보로 추가되어야하는 값

if __name__ == "__main__":

    app = QApplication(sys.argv)
    logic_name= "3daySupply"
    from_collection = make_collection("stock_data", logic_name)
    from_collection = from_collection.find_one({"일자": com_vari.Today_date})["stock_code"][:50]
    collection = make_collection("stock_data", "Real_Time_SK")
    activate_Tr = real_tr_object("SK", collection)
    pk_dict["일자"] = com_vari.Today_date
    input_list = from_collection
    collection_len = len(input_list)
    activate_Tr.set_multi_call(input_list, col_name, pk_dict, collection_len)

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


