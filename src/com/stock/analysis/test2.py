import sys

sys.path.append("C:\\dev\\OpenStock")

from src.com.stock.common.import_lib import *
def make_diff(TR_1206_2_data,TR_1206_2_data2 ):
    return (int(TR_1206_2_data["가격"]) - int(TR_1206_2_data2["가격"])) / int(TR_1206_2_data2["가격"]) * 100.0
def  make_won(int_number):
    check = False
    result = int_number / (10.0)**8
    result =  round(result,2)
    if result >= 100:
        check = True
    return check , str(result) +" 억"
def find_upjong():
    result = {}
    TR_1863 = make_collection("stock_data" , "new_TR_1863")
    upjong_code_mst = make_collection("stock_data" , "upjong_code_mst")
    for i in TR_1863.find({"입력일자" : "20210115"}).sort([("전일대비율" , -1)]):
        for j in upjong_code_mst.find({"단축코드" : i["단축코드"]}):
            print(j["업종명"] , end="")
            if not (j["업종명"] in result.keys()) :
                result[j["업종명"]] = 1
            else:
                result[j["업종명"]] += 1
        print()
    print(result)
def analysis_fail():
    fail_result  = make_collection("stock_data" , "fail_result").find_one({"일자": "20210115"})["stock_code"]

    TR_1206 = make_collection("stock_data" , "TR_1206")
    TR_1206_2 = make_collection("stock_data" , "TR_1206_2")

    TR_SCHART = make_collection("stock_data" ,"real_TR_SCHART")


    fail_result_len = len(fail_result)
    positive = 0
    semi_positive = 0
    result = {}
    result_stock_code = {"일자" : "20210115" , "stock_code" : []}
    for i in fail_result:
        TR_1206_data = TR_1206.find_one({"단축코드"  : i, "일자" : "20210115"})

        TR_1206_2_data = TR_1206_2.find_one({"단축코드"  : i, "일자" : "20210114"})
        TR_1206_2_data2 = TR_1206_2.find_one({"단축코드"  : i, "일자" : "20201224"})
        diff = make_diff(TR_1206_2_data,TR_1206_2_data2)
        vol_check, tot_vol = make_won(int(TR_1206_2_data["누적거래량"]) * int(TR_1206_2_data["가격"]))
        upjong_code_mst = make_collection("stock_data", "upjong_code_mst")
        today_data = TR_SCHART.find_one({"일자": "20210115", "시간": "0905" , "단축코드" : i})
        before_data = TR_SCHART.find_one({"일자": "20210114", "시간": "1530" , "단축코드" : i})
        if int(TR_1206_data["외국인순매수거래량"]) >0 and int(TR_1206_data["프로그램순매수"]) >0 and diff > 0 and int( TR_1206_data["기관순매수거래량"])>=0 and int(today_data["종가"]) >  int(today_data["시가"]) and int(today_data["종가"]) >  int(before_data["종가"]):
        #if int(TR_1206_data["외국인순매수거래량"]) >0 and int(TR_1206_data["프로그램순매수"]) >0 and diff > 0 and int( TR_1206_data["기관순매수거래량"])>=0 :
            positive +=1
            for j in upjong_code_mst.find({"단축코드": i}):
                print(j["업종명"], end="")
                if not (j["업종명"] in result.keys()):
                    result[j["업종명"]] = 1
                else:
                    result[j["업종명"]] += 1
            if vol_check :
                semi_positive += 1
                print(
                    " 전일 거래대금 100 억 초과  종목명  :  " + i)
            print(" 종목명  :  " + i + "  상승률   " + str(TR_1206_data["전일대비율"]) + "  개인순매수 거래량   " + TR_1206_data[
            "개인순매수거래량"] + "  외국인순매수거래량   " + TR_1206_data["외국인순매수거래량"] + "  기관순매수거래량   " + TR_1206_data["기관순매수거래량"] + "  프로그램순매수  " + TR_1206_data["프로그램순매수"]+" 당일  거래대금  " + make_won(int(TR_1206_data["누적거래량"]) *int(TR_1206_data["가격"]))[1])
            print(
                " 종목명  :  " + i + " 관찰 시작 부터 전일까지 가격 변화 비율  " + str(diff) + " 전일까지  개인순매수누적거래량   " + TR_1206_2_data["개인순매수누적거래량"] + "  외국인순매수누적거래량   " +
                TR_1206_2_data["외국인순매수누적거래량"] + "  기관순매수누적거래량   " + TR_1206_2_data["기관순매수누적거래량"]+" 전일  거래대금  " + tot_vol)
            result_stock_code["stock_code"].append(i)
            #print(" 종목명  :  " +i["한글종목명"] + "  상승률   " + str(i["전일대비율"]) + "  개인순매수 거래량   " + TR_1206_data["개인순매수거래량"]+ "  외국인순매수거래량   " + TR_1206_data["외국인순매수거래량"]+ "  기관순매수거래량   " + TR_1206_data["기관순매수거래량"])
            #print(" 종목명  :  " +i["한글종목명"] + " 전일까지  개인순매수누적거래량   " + TR_1206_2_data["개인순매수누적거래량"]+ "  외국인순매수누적거래량   " + TR_1206_2_data["외국인순매수누적거래량"]+ "  기관순매수누적거래량   " + TR_1206_2_data["기관순매수누적거래량"])
    print(" fail 종목수  "  + str(fail_result_len))
    print(" 그중에서 "  + str(positive))
    print(" 그중에서 전일 거래대금 100억 이상  갯수  "  + str(semi_positive))
    print(result)



def compare_fail():

    stock_code = make_collection("stock_data" , "3daySupply").find_one({"일자" : "20210115"})["stock_code"]

    true_result = make_collection("stock_data" , "result")

    drop_collection("stock_data" , "fail_result")
    fail_result  = make_collection("stock_data" , "fail_result")
    fail_result_data = {"일자" : "20210115" , "stock_code" : []}

    for i in stock_code:
        if not i in true_result.find_one({"일자" : "20210115"})["stock_code"]:
            fail_result_data["stock_code"].append(i)

    fail_result.insert_one(fail_result_data)

    TR_1206 = make_collection("stock_data" , "TR_1206")
    TR_1206_2 = make_collection("stock_data" , "TR_1206_2")

    fail_result_len = fail_result.count()
    semi_positive = 0
    result = {}
    result_stock_code = {"일자" : "20210115" , "stock_code" : []}
    for i in fail_result.find_one({"일자" : "20210115"})["stock_code"]:
        TR_1206_data = TR_1206.find_one({"단축코드"  : i, "일자" : "20210115"})

        TR_1206_2_data = TR_1206_2.find_one({"단축코드"  : i, "일자" : "20210114"})
        TR_1206_2_data2 = TR_1206_2.find_one({"단축코드"  : i, "일자" : "20201224"})
        diff = make_diff(TR_1206_2_data,TR_1206_2_data2)
        vol_check, tot_vol = make_won(int(TR_1206_2_data["누적거래량"]) * int(TR_1206_2_data["가격"]))
        upjong_code_mst = make_collection("stock_data", "upjong_code_mst")
        for j in upjong_code_mst.find({"단축코드": i}):
            print(j["업종명"], end="")
            if not (j["업종명"] in result.keys()):
                result[j["업종명"]] = 1
            else:
                result[j["업종명"]] += 1
        if vol_check :
            semi_positive += 1
            print(
                " 전일 거래대금 100 억 초과  종목명  :  " + i)
        print(" 종목명  :  " + i + "  상승률   " + str(TR_1206_data["전일대비율"]) + "  개인순매수 거래량   " + TR_1206_data[
        "개인순매수거래량"] + "  외국인순매수거래량   " + TR_1206_data["외국인순매수거래량"] + "  기관순매수거래량   " + TR_1206_data["기관순매수거래량"] +" 당일  거래대금  " + make_won(int(TR_1206_data["누적거래량"]) *int(TR_1206_data["가격"]))[1])
        print(
            " 종목명  :  " + i + " 관찰 시작 부터 전일까지 가격 변화 비율  " + str(diff) + " 전일까지  개인순매수누적거래량   " + TR_1206_2_data["개인순매수누적거래량"] + "  외국인순매수누적거래량   " +
            TR_1206_2_data["외국인순매수누적거래량"] + "  기관순매수누적거래량   " + TR_1206_2_data["기관순매수누적거래량"]+" 전일  거래대금  " + tot_vol)
        result_stock_code["stock_code"].append(i)
        #print(" 종목명  :  " +i["한글종목명"] + "  상승률   " + str(i["전일대비율"]) + "  개인순매수 거래량   " + TR_1206_data["개인순매수거래량"]+ "  외국인순매수거래량   " + TR_1206_data["외국인순매수거래량"]+ "  기관순매수거래량   " + TR_1206_data["기관순매수거래량"])
        #print(" 종목명  :  " +i["한글종목명"] + " 전일까지  개인순매수누적거래량   " + TR_1206_2_data["개인순매수누적거래량"]+ "  외국인순매수누적거래량   " + TR_1206_2_data["외국인순매수누적거래량"]+ "  기관순매수누적거래량   " + TR_1206_2_data["기관순매수누적거래량"])
    print(" fail 종목수  "  + str(fail_result_len))
    print(" 그중에서 전일 거래대금 100억 이상  갯수  "  + str(semi_positive))
    print(result)


def compare ():
    TR_1206 = make_collection("stock_data" , "TR_1206")
    TR_1206_2 = make_collection("stock_data" , "TR_1206_2")
    TR_1863 = make_collection("stock_data" , "new_TR_1863")

    TR_1863_len = TR_1863.count()
    positive = 0
    semi_positive = 0
    result = {}
    result_stock_code = {"일자" : "20210115" , "stock_code" : []}

    for i in TR_1863.find({"입력일자" : "20210115"}).sort([("전일대비율" , -1)]):
        TR_1206_data = TR_1206.find_one({"단축코드"  : i["단축코드"], "일자" : "20210115"})

        TR_1206_2_data = TR_1206_2.find_one({"단축코드"  : i["단축코드"], "일자" : "20210114"})
        TR_1206_2_data2 = TR_1206_2.find_one({"단축코드"  : i["단축코드"], "일자" : "20201224"})
        diff = make_diff(TR_1206_2_data,TR_1206_2_data2)
        vol_check, tot_vol = make_won(int(TR_1206_2_data["누적거래량"]) * int(TR_1206_2_data["가격"]))
        upjong_code_mst = make_collection("stock_data", "upjong_code_mst")
        if int(TR_1206_2_data["외국인순매수누적거래량"]) > 0 and int(TR_1206_2_data["외국인순매수누적거래량"]) > int(TR_1206_2_data2["외국인순매수누적거래량"]) and  int(TR_1206_data["외국인순매수거래량"]) >0 and int(TR_1206_data["개인순매수거래량"]) <0 and int(TR_1206_2_data["개인순매수누적거래량"]) <0 :
            check = True
            for j in TR_1206_2.find({"단축코드": i["단축코드"]}):
                if int(j["외국인순매수누적거래량"]) < 0 :
                    check = False
                    break
            if check:
                for j in upjong_code_mst.find({"단축코드": i["단축코드"]}):
                    print(j["업종명"], end="")
                    if not (j["업종명"] in result.keys()):
                        result[j["업종명"]] = 1
                    else:
                        result[j["업종명"]] += 1
                positive +=1
                if vol_check :
                    semi_positive += 1
                    print(
                        " 전일 거래대금 100 억 초과  종목명  :  " + i["한글종목명"])
                print(" 종목명  :  " + i["한글종목명"] + "  상승률   " + str(i["전일대비율"]) + "  개인순매수 거래량   " + TR_1206_data[
                "개인순매수거래량"] + "  외국인순매수거래량   " + TR_1206_data["외국인순매수거래량"] + "  프로그램순매수  " + TR_1206_data["프로그램순매수"]+ "  기관순매수거래량   " + TR_1206_data["기관순매수거래량"] +" 당일  거래대금  " + make_won(int(TR_1206_data["누적거래량"]) *int(TR_1206_data["가격"]))[1])
                print(
                    " 종목명  :  " + i["한글종목명"] + " 관찰 시작 부터 전일까지 가격 변화 비율  " + str(diff) + " 전일까지  개인순매수누적거래량   " + TR_1206_2_data["개인순매수누적거래량"] + "  외국인순매수누적거래량   " +
                    TR_1206_2_data["외국인순매수누적거래량"] + "  기관순매수누적거래량   " + TR_1206_2_data["기관순매수누적거래량"]+" 전일  거래대금  " + tot_vol)
                result_stock_code["stock_code"].append(i["단축코드"])

        #print(" 종목명  :  " +i["한글종목명"] + "  상승률   " + str(i["전일대비율"]) + "  개인순매수 거래량   " + TR_1206_data["개인순매수거래량"]+ "  외국인순매수거래량   " + TR_1206_data["외국인순매수거래량"]+ "  기관순매수거래량   " + TR_1206_data["기관순매수거래량"])
        #print(" 종목명  :  " +i["한글종목명"] + " 전일까지  개인순매수누적거래량   " + TR_1206_2_data["개인순매수누적거래량"]+ "  외국인순매수누적거래량   " + TR_1206_2_data["외국인순매수누적거래량"]+ "  기관순매수누적거래량   " + TR_1206_2_data["기관순매수누적거래량"])
    print(" 5프로 이상 상승 종목 수  "  + str(TR_1863_len))
    print(" 5프로 이상 상승 종목중 조건 만족하는 수  "  + str(positive))
    print(" 그중에서 전일 거래대금 100억 이상  갯수  "  + str(semi_positive))
    print(result)
    drop_collection("stock_data", "result")
    result_db = make_collection("stock_data", "result")
    result_db.insert_one(result_stock_code)

if __name__ ==  "__main__":
    #find_new_stocks()
    #check_3day_data()
    #cleansing_data()
    #compare()
    analysis_fail()