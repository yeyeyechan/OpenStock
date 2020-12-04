

# -*- coding: utf-8 -*-
from src.com.stock.common.import_lib import *

'''
stock_mst 설명

전 종목 코드 정보 조회
'''

input_dict = {} # tr 호출 인풋 값 dictionary , make_dict 에 배열을 넣어 만들어준다.
col_name_in = ["표준코드               " ,
"단축코드               " ,
"장구분                 " ,
"종목명                 " ,
"KOSPI200 세부업종      " ,
"결산월일               " ,
"거래정지구분           " ,
"관리구분               " ,
"시장경보구분코드       " ,
"락구분                 " ,
"불성실공시지정여부     " ,
"증거금 구분            " ,
"신용증거금 구분        " ,
"ETF 구분자             " ,
"소속구분               "
]  # 아웃풋 컬럼명 배열
col_name = make_dict(col_name_in) # 아웃풋 컬럼명 배열을 index ,value 형태의 dictionary로 변형
pk_dict = {} # document 간 pk나 중요정보로 추가되어야하는 값
last_call = False
if __name__ == "__main__":
    app = QApplication(sys.argv)

    input_dict = make_dict([])

    col_name = make_dict(col_name_in)

    pk_dict = {}
    #종목코드 삭제된 종목을 날리기 위해 전부 날려버림
    drop_collection("stock_data", "stock_mst")
    IndiControl = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")

    collection = make_collection("stock_data", "stock_mst")
    activate_Tr = tr_object("stock_mst", collection, IndiControl)

    last_call = True

    activate_Tr.set_single_call(input_dict, col_name, pk_dict)
    app.exec_()
