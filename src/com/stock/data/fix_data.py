from src.com.stock.common.import_lib import *

def make_new_float_field (collection, target_field , filter ):
    for i in collection.find(filter):
        i[target_field] = float(i[target_field])
        collection.update({'_id' : i['_id']}, i)
        print(i)



if __name__ == "__main__":
    collection = make_collection("stock_data" , "TR_1206")

    make_new_float_field(collection, "전일대비율" , {"일자": "20201124"})