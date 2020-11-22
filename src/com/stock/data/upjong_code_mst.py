

# -*- coding: utf-8 -*-
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari

'''
upjong_code_mst 설명


'''

input_dict = {} # tr 호출 인풋 값 dictionary , make_dict 에 배열을 넣어 만들어준다.
col_name_in = [
"단축코드",
"종목명"
]  # 아웃풋 컬럼명 배열
col_name = make_dict(col_name_in) # 아웃풋 컬럼명 배열을 index ,value 형태의 dictionary로 변형
pk_dict = {"업종코드": "", "업종명": "" , "시장명" : ""} # document 간 pk나 중요정보로 추가되어야하는 값

if __name__ == "__main__":
    drop_collection("stock_data", "upjong_code_mst")

    from_collection = make_collection("stock_data", "upjong_code_mst")

    pk_dict_list = []
    input_dict_list = []

    for i in from_collection.find({"시장명": "KOSPI"}):
        input_dict = make_dict([i["업종코드"]])
        pk_dict["업종코드"] = i["업종코드"]
        pk_dict["업종명"] = i["업종명"]
        pk_dict["시장명"] = i["시장명"]

        input_dict_list.append(copy(input_dict))
        pk_dict_list.append(copy(pk_dict))

    for i in from_collection.find({"시장명": "KOSDAQ"}):
        input_dict = make_dict([i["업종코드"]])
        pk_dict["업종코드"] = i["업종코드"]
        pk_dict["업종명"] = i["업종명"]
        pk_dict["시장명"] = i["시장명"]

        input_dict_list.append(copy(input_dict))
        pk_dict_list.append(copy(pk_dict))

    app = QApplication(sys.argv)

    collection = make_collection("stock_data", "upjong_code_mst")
    index =0
    activate_Tr = tr_object("upjong_code_mst", collection)


    collection_len = len(input_dict_list)
    com_vari.upjong_code_mst_logger.debug("upjong_code_mst 호출 시작")
    activate_Tr.set_multi_call(input_dict_list, col_name, pk_dict_list, collection_len)
    com_vari.upjong_code_mst_logger.debug("upjong_code_mst 호출 완료")

    app.exec_()

    total_upjong_code_mst_count = make_collection("stock_data", "upjong_code_mst").estimated_document_count()

    print("실제 db 적제된 document 갯수     "+str(total_upjong_code_mst_count) )

    print("원래")
