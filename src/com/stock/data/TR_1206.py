

# -*- coding: utf-8 -*-
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari

'''
TR_1206 설명

종목별 일별 수급, 가격 , 등 정보 가져 올수있다.
'''

input_dict = {} # tr 호출 인풋 값 dictionary , make_dict 에 배열을 넣어 만들어준다.
col_name_in = ["일자                      " ,
"가격                      " ,
"시가                      " ,
"고가                      " ,
"저가                      " ,
"전일대비구분              " ,
"전일대비                  " ,
"누적거래량                " ,
"개인매수거래량            " ,
"개인매도거래량            " ,
"개인순매수거래량          " ,
"개인매수누적              " ,
"개인매도누적              " ,
"개인순매수누적거래량      " ,
"외국인매수거래량          " ,
"외국인매도거래량          " ,
"외국인순매수거래량        " ,
"외국인매수누적            " ,
"외국인매도누적            " ,
"외국인순매수누적거래량    " ,
"기관매수거래량            " ,
"기관매도거래량            " ,
"기관순매수거래량          " ,
"기관매수누적              " ,
"기관매도누적              " ,
"기관순매수누적거래량      " ,
"금융투자매수거래량        " ,
"금융투자매도거래량        " ,
"금융투자순매수거래량      " ,
"금융투자매수누적          " ,
"금융투자매도누적          " ,
"금융투자순매수누적거래량  " ,
"투신매수거래량            " ,
"투신매도거래량            " ,
"투신순매수거래량          " ,
"투신매수누적              " ,
"투신매도누적              " ,
"투신순매수누적거래량      " ,
"은행매수거래량            " ,
"은행매도거래량            " ,
"은행순매수거래량          " ,
"은행매수누적              " ,
"은행매도누적              " ,
"은행순매수누적거래량      " ,
"기타금융매수거래량        " ,
"기타금융매도거래량        " ,
"기타금융순매수거래량      " ,
"기타금융매수누적          " ,
"기타금융매도누적          " ,
"기타금융순매수누적거래량  " ,
"보험매수거래량            " ,
"보험매도거래량            " ,
"보험순매수거래량          " ,
"보험매수누적              " ,
"보험매도누적              " ,
"보험순매수누적거래량      " ,
"기금매수거래량            " ,
"기금매도거래량            " ,
"기금순매수거래량          " ,
"기금매수누적              " ,
"기금매도누적              " ,
"기금순매수누적거래량      " ,
"기타매수거래량            " ,
"기타매도거래량            " ,
"기타순매수거래량          " ,
"기타매수누적              " ,
"기타매도누적              " ,
"기타순매수누적거래량      " ,
"외국인기타매수거래량      " ,
"외국인기타매도거래량      " ,
"외국인기타순매수거래량    " ,
"외국인기타매수누적        " ,
"외국인기타매도누적        " ,
"외국인기타순매수누적거래량" ,
"국가지자체매수거래량      " ,
"국가지자체매도거래량      " ,
"국가지자체순매수거래량    " ,
"국가지자체매수누적        " ,
"국가지자체매도누적        " ,
"국가지자체순매수누적거래량" ,
"프로그램매수              " ,
"프로그램매도              " ,
"프로그램순매수            " ,
"프로그램누적매수          " ,
"프로그램누적매도          " ,
"프로그램누적순매수        " ,
"사모펀드매수              " ,
"사모펀드매도              " ,
"사모펀드순매수            " ,
"사모펀드누적매수          " ,
"사모펀드누적매도          " ,
"사모펀드누적순매수        " ,
"전일대비율                " ,
"외국인지분율              "
]  # 아웃풋 컬럼명 배열
col_name = make_dict(col_name_in) # 아웃풋 컬럼명 배열을 index ,value 형태의 dictionary로 변형
pk_dict = {"단축코드": "" , "데이터구분":""} # document 간 pk나 중요정보로 추가되어야하는 값
last_call = False

if __name__ == "__main__":
    #drop_collection("stock_data", "TR_1206")
    app = QApplication(sys.argv)

    from_collection = make_collection("stock_data", "stock_mst")
    collection_len = from_collection.estimated_document_count()
    index =0
    collection = make_collection("stock_data", "TR_1206")
    activate_Tr = tr_object("TR_1206", collection)


    start_date = "20190101"
    end_date = "20191201"
    gubun = "1"
    data_kind = "0"

    check_list = integrity_db_count(start_date, end_date , collection_len)
    com_vari.TR_1206_len_counts = check_list[0]
    pk_dict["데이터구분"] = data_kind
    input_dict = make_dict(["", start_date, end_date, gubun, data_kind])

    pk_dict_list = []
    input_dict_list = []
    for i in from_collection.find():
        stock_code = i["단축코드"]

        pk_dict["단축코드"] = stock_code
        input_dict[0] = stock_code

        pk_dict_list.append(copy(pk_dict))
        input_dict_list.append(copy(input_dict))
    com_vari.TR_1206_logger.debug("TR_1206 호출 시작")
    activate_Tr.set_multi_call(input_dict_list, col_name, pk_dict_list, collection_len)
    com_vari.TR_1206_logger.debug("TR_1206 호출 완료")

    app.exec_()

    total_TR_1206_count = make_collection("stock_data", "TR_1206").estimated_document_count()

    print("예상되는 실제 db 적재 document 갯수   "+ str(check_list[1]))
    print("실제 db 적제된 document 갯수     "+str(total_TR_1206_count) )

    print("원래")
