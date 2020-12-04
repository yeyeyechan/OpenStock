from src.com.stock.common.import_lib import *

ServiceKey = 'IH3eLzricz4H%2BL6d6%2F6Jsfgv2FLrk2Gcb%2BtTO6kosso8AlkHeqZZbSyjsKAuBU9HrH2%2FGfAkFC2mXxZgv3RE8g%3D%3D'

today = date.today().strftime("%Y%m%d")
# 공공 데이터 포탈 api 호출 공통함수
def call_api(ServiceKey, url, params, operation):
    params = urlparse.urlencode(params)
    request_query = url + '/' + operation + '?' + params + '&' + 'serviceKey' + '=' + ServiceKey
    response = requests.get(url=request_query).content
    xmlObject = xmltodict.parse(response)

    return xmlObject


# 공공데이터 포탈 공휴일 호출 함수
def get_holiday(solYear, solMonth):
    date_db = make_collection("stock_data" , "kr_holidays")
    if date_db.find_one({"일자" : today}) is not None:
        for i in date_db.find() :
            if "kr_holidays" in i:
                return i["kr_holidays"]
    URL = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService'
    # OPERATION = 'getHoliDeInfo' # 국경일 + 공휴일 정보 조회 오퍼레이션
    OPERATION = "getHoliDeInfo"
    all_month = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    list_kor_holiday = []
    xmlObject = ""
    allData = ""
    lenAllData = ""
    try:
        if solMonth == "ALL":
            solMonth = all_month
        for i in solYear:
            for j in solMonth:
                params = {
                    "solYear": "",
                    "solMonth": ""}
                params["solYear"] = i
                params["solMonth"] = j
                xmlObject = call_api(ServiceKey, URL, params, OPERATION)
                if xmlObject["response"]["body"]["items"] is None:
                    continue
                allData = xmlObject["response"]["body"]["items"]["item"]
                if type(allData) is list:
                    lenAllData = len(allData)
                    for k in range(lenAllData):
                        print(allData[k]["locdate"])
                        list_kor_holiday.append(allData[k]["locdate"])
                else:
                    list_kor_holiday.append(allData["locdate"])
                    print(allData["locdate"])
        drop_collection("stock_data" , "kr_holidays")
        update_collection(date_db,{"kr_holidays" : list_kor_holiday, "일자" : today})
    except:
         if date_db.find().count() >0:
           for i in date_db.find():
               return i["kr_holidays"]
         else:
            print('기존 kr holidays 정보가 없습니다.')
    return list_kor_holiday

if __name__ == "__main__":
    get_holiday(["2020"], ["01", "02", "03", "04", "05", "06"])