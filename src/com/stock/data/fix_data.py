from src.com.stock.common.import_lib import *

def make_new_float_field (new_collection, before_collection, target_field , filter ):
    if collection.find_one(filter) is None:
        print("필터   " + str(filter) +" 존재 하지 않음 " )
        return
    for i in collection.find(filter):
        i[target_field] = float(i[target_field])
        del i["_id"]
        new_collection.update(i, i, upsert=True)
        print(i)



if __name__ == "__main__":
    collection = make_collection("stock_data" , "TR_1206")
    to_collection = make_collection("stock_data" , "new_TR_1206")
    date_list = get_kr_working_day("20201202" , "20201202")
    for i in date_list:
        print("날짜 :  " +i.strftime("%Y%m%d") + " 변환시도")
        make_new_float_field(to_collection,collection, "전일대비율" , {"일자": i.strftime("%Y%m%d")})
