from src.com.stock.common.import_lib import *

def make_new_float_field_new(new_collection, before_collection, target_field, filter):
    data_list = []
    for i in before_collection.find(filter):
        i[target_field] = float(i[target_field])
        del i["_id"]
        data_list.append(i)
        print(i)
    print("db_update")
    new_collection.insert_many(data_list)

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
    if  len(sys.argv) > 1 and  sys.argv[1] == "job":
        start_date = sys.argv[2]
        end_date = sys.argv[3]
    else:
        start_date = "20201230"
        end_date =  "20210106"
    collection = make_collection("stock_data" , "TR_1206")
    to_collection = make_collection("stock_data" , "new_TR_1206")
    date_list = get_kr_working_day(start_date , end_date)
    #drop_collection("stock_data", "new_TR_1206")
    for i in date_list:
        print("날짜 :  " +i.strftime("%Y%m%d") + " 변환시도")
        make_new_float_field_new(to_collection,collection, "전일대비율" , {"일자": i.strftime("%Y%m%d")})
