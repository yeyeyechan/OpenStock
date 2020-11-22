'''input_dict["first_gubun"] = "5"
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
input_dict["2nd_gubun"] = "5"
# input_dict["2nd_up_target"] = 1.0'''



'''for i in TR_1206_collection.find({"일자": first_date.strftime("%Y%m%d")}):
    if input_dict["first_gubun"] == "":
        if total_trans_amount(i['가격'], i['누적거래량'], input_dict["first_trans_price"]) and check_for_amount(i['외국인순매수거래량'],
                                                                                                         input_dict[
                                                                                                             "first_foreign"]) and check_pro_amount(
                i['프로그램순매수'], input_dict["first_company"]):
            stock_code_list.append(copy(i['단축코드']))
    elif i['전일대비구분'] == input_dict["first_gubun"]:
        if total_trans_amount(i['가격'], i['누적거래량'], input_dict["first_trans_price"]) and check_per_amount(i['개인순매수거래량'],
                                                                                                         input_dict[
                                                                                                             "first_person"]) and check_for_min_amount(
                i['외국인순매수거래량'], input_dict["first_foreign"]) and check_pro_min_amount(i['프로그램순매수'],
                                                                                      input_dict["first_company"]):
            stock_code_list.append(copy(i['단축코드']))
for i in stock_code_list:
    data = TR_1206_collection.find_one({"일자": second_date.strftime("%Y%m%d"), "단축코드": i})
    if data is None:
        com_vari.TR_1206_logger.debug("TR_1206_db 데이터 없음 확인 필요   일자 " + second_date.strftime("%Y%m%d") + "   단축코드 " + i)
        continue
    elif data['전일대비구분'] == input_dict["2nd_gubun"] and check_for_amount(data['외국인순매수거래량'],
                                                                        input_dict["2nd_foreign"]) and check_pro_amount(
            data['프로그램순매수'], input_dict["2nd_program"]) and check_per_min_amount(data['개인순매수거래량'], input_dict[
        "2nd_person"]) and total_trans_amount(data['가격'], data['누적거래량'], input_dict["2nd_trans_price"]):
        final_stock_code_list.append(copy(data['단축코드']))'''


#########################################################################################################################################################################
#logic 2
#########################################################################################################################################################################

'''
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


'''

'''
 for i in TR_1206_collection.find({"일자": first_date.strftime("%Y%m%d")}):
        if input_dict["first_gubun"] == "":
            if total_trans_amount(i['가격'], i['누적거래량'], input_dict["first_trans_price"] ):
                stock_code_list.append(copy(i['단축코드']))
        elif i['전일대비구분'] == input_dict["first_gubun"]:
            if total_trans_amount(i['가격'], i['누적거래량'], input_dict["first_trans_price"] ):
                stock_code_list.append(copy(i['단축코드']))
    for i in stock_code_list:
        data = TR_1206_collection.find_one({"일자": second_date.strftime("%Y%m%d"), "단축코드":i })
        if data is None:
            com_vari.TR_1206_logger.debug("TR_1206_db 데이터 없음 확인 필요   일자 " + second_date.strftime("%Y%m%d") + "   단축코드 " + i)
            continue
        elif input_dict["first_gubun"] == "":
            if check_for_amount(data['외국인순매수거래량'], input_dict["2nd_foreign"] ) and check_pro_amount(data['프로그램순매수'], input_dict["2nd_program"])  and total_trans_amount(data['가격'],data['누적거래량'], input_dict["2nd_trans_price"]) :
                final_stock_code_list.append(copy(data['단축코드']))
        else:
            if data['전일대비구분'] == input_dict["2nd_gubun"] and check_for_amount(data['외국인순매수거래량'], input_dict["2nd_foreign"] ) and check_pro_amount(data['프로그램순매수'], input_dict["2nd_program"]) and check_up_price(data['가격'] , data['전일대비'],input_dict["2nd_up_target"] ) and total_trans_amount(data['가격'],data['누적거래량'], input_dict["2nd_trans_price"]) :
                final_stock_code_list.append(copy(data['단축코드']))


'''


#########################################################################################################################################################################


'''
 input_dict["first_gubun"] = "5"
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
    input_dict["2nd_gubun"] = "5"'''







'''    for i in TR_1206_collection.find({"일자": first_date.strftime("%Y%m%d")}):
        if input_dict["first_gubun"] == "":
            if total_trans_amount(i['가격'], i['누적거래량'], input_dict["first_trans_price"] ) and check_for_amount(i['외국인순매수거래량'], input_dict["first_foreign"] ) and check_pro_amount(i['프로그램순매수'], input_dict["first_company"]):
                stock_code_list.append(copy(i['단축코드']))
        elif i['전일대비구분'] == input_dict["first_gubun"]:
            if total_trans_amount(i['가격'], i['누적거래량'], input_dict["first_trans_price"] )  and check_per_amount(i['개인순매수거래량'], input_dict["first_person"] )  and check_for_min_amount(i['외국인순매수거래량'], input_dict["first_foreign"] ) and check_pro_min_amount(i['프로그램순매수'], input_dict["first_company"]):
                stock_code_list.append(copy(i['단축코드']))
    for i in stock_code_list:
        data = TR_1206_collection.find_one({"일자": second_date.strftime("%Y%m%d"), "단축코드":i })
        if data is None:
            com_vari.TR_1206_logger.debug("TR_1206_db 데이터 없음 확인 필요   일자 " + second_date.strftime("%Y%m%d") + "   단축코드 " + i)
            continue
        elif data['전일대비구분'] == input_dict["2nd_gubun"] and check_for_amount(data['외국인순매수거래량'], input_dict["2nd_foreign"] ) and check_pro_amount(data['프로그램순매수'], input_dict["2nd_program"]) and check_per_min_amount(data['개인순매수거래량'], input_dict["2nd_person"] ) and total_trans_amount(data['가격'],data['누적거래량'], input_dict["2nd_trans_price"]) :
            final_stock_code_list.append(copy(data['단축코드']))'''