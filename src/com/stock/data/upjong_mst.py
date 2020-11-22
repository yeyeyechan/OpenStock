# -*- coding: utf-8 -*-
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari



input_dict = {} # tr 호출 인풋 값 dictionary , make_dict 에 배열을 넣어 만들어준다.
col_name_in = [
    "업종코드",
    "업종명"
]  # 아웃풋 컬럼명 배열
col_name = make_dict(col_name_in) # 아웃풋 컬럼명 배열을 index ,value 형태의 dictionary로 변형
pk_dict = {"시장코드": "" , "시장명":""} # document 간 pk나 중요정보로 추가되어야하는 값
last_call = False

if __name__ == "__main__":
    drop_collection("stock_data", "upjong_mst")
    app = QApplication(sys.argv)

    collection = make_collection("stock_data", "upjong_mst")
    activate_Tr = tr_object("upjong_mst ", collection)


    upjong = ["1", "2", "3" , "4" , "5"] # Kospi , Kosdaq, Kopspi200,  kosdaq50, KRX
    upjong_dict = {
        "1" : "KOSPI",
        "2": "KOSDAQ",
        "3": "KOSPI200",
        "4": "KOSDAQ50",
        "5": "KRX"
    }
    pk_dict_list = []
    input_dict_list = []

    for i in upjong:
        print("upjong code    " + i )
        input_dict = make_dict([i])
        input_dict_list.append(copy(input_dict))
        pk_dict["시장코드"] = i
        pk_dict["시장명"] = upjong_dict[i]
        pk_dict_list.append(copy(pk_dict))


    collection_len = len(input_dict_list)
    print(collection_len)
    print("input dict list 길이     " + str((collection_len)))

    activate_Tr.set_multi_call(input_dict_list, col_name, pk_dict_list, collection_len)

    app.exec_()

    total_upjong_mst_count = make_collection("stock_data", "upjong_mst").estimated_document_count()

    print("업종코드 갯수  " + str(len(upjong)))

    print("실제 db 적제된 document 갯수     "+str(total_upjong_mst_count))

    print("원래")
