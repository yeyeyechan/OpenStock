from src.com.stock.common.import_lib import *


if __name__ == "__main__":
    logic_name = "logic3"
    collection = make_collection("stock_data", logic_name)


    test_date = get_kr_working_day("20201118", "20201119")
    input_dict = {
        "first_gubun": "",
        "first_trans_price": "",
        "first_foreign": "",
        "first_program": "",
        "first_company": "",
        "2nd_foreign": "",
        "2nd_program": "",
        "2nd_company": "",
        "2nd_trans_price": "",
        "2nd_gubun": "",
        "2nd_up_target": ""
    }
    input_dict["first_gubun"] = ""
    input_dict["first_trans_price"] = "10000000000"

    input_dict["first_person"] = "0"
    input_dict["first_foreign"] = "0"
    input_dict["first_program"] = "0"
    input_dict["first_company"] = "0"

    input_dict["2nd_person"] = "0"
    input_dict["2nd_foreign"] = "10"
    input_dict["2nd_program"] = "10"
    input_dict["2nd_company"] = "0"
    input_dict["2nd_trans_price"] = "13000000000"
    input_dict["2nd_gubun"] = ""
    input_dict["2nd_up_target"] = 3.0
    TR_1206_collection = make_collection("stock_data", "TR_1206")


    expected_stock_code_list = {}
    for i in test_date:
        first_condition_data = first_condition(i , input_dict, TR_1206_collection)
        expected_stock_code_list[i.strftime("%Y%m%d")] = copy(first_condition_data)
        update_collection(collection, {"일자":i.strftime("%Y%m%d") , "stock_code" : copy(first_condition_data) })
    result_data_dict = checked_result_data = check_with_data(expected_stock_code_list , 5.0, TR_1206_collection)
    actual_data_dict = actual_data = check_actual_total_data(test_date, 5.0, TR_1206_collection)

    for key , value in result_data_dict.items():
        if type(value) == list:
            print("예측 종목 중 실제 5퍼 이상 상승 종목    "+ key + "   실제 값 " +'     '.join(value))
        else:
            print("예측 종목 중 실제 5퍼 이상 상승 종목    "+ key + "   실제 값 " +value)
    #print("전 종목 중 실제 5퍼 이상 상승 종목    "+ actual_data_dict)
    for i in test_date:
        print(i.strftime("%Y%m%d")+ "일자 상승 예상 종목  수  " + str(checked_result_data[i.strftime("%Y%m%d")+"_total_count"]))
        print(i.strftime("%Y%m%d") + "일자 상승 예측 성공 종목수   " +str( checked_result_data[i.strftime("%Y%m%d")+"_success"]))
        print(i.strftime("%Y%m%d") + "일자 실제 상승 종목수  " + str(actual_data[i.strftime("%Y%m%d")+"_success"]))
        if (int(actual_data[i.strftime("%Y%m%d")+"_total_count"])==0):
            print(i.strftime("%Y%m%d") + "일자 전 종목중 5프로이상 오른 종목 없음  " )
        else:
            print(i.strftime("%Y%m%d") + "일자 상승 종목 전종목 대비 비율    " + str(int(actual_data[i.strftime("%Y%m%d")+"_success"])/int(actual_data[i.strftime("%Y%m%d")+"_total_count"])*100.0))

        if (int(checked_result_data[i.strftime("%Y%m%d")+"_total_count"])==0):
            print(i.strftime("%Y%m%d") + "일자 예측된 종목 없음  " )
        else:
            print(i.strftime("%Y%m%d") + "일자 상승 종목 예측 성공률    " + str(int(checked_result_data[i.strftime("%Y%m%d") + "_success"]) / int(checked_result_data[i.strftime("%Y%m%d") + "_total_count"]) * 100.0))

