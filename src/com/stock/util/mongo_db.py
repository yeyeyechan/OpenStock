from pymongo import MongoClient

client_main = MongoClient('127.0.0.1', 27017)


def make_collection(db_name, collection_name):
    if (db_name is not None and collection_name is not None):
        db = client_main[db_name]
        collection = db[collection_name]
    else:
        return None
    return collection
def update_collection(collection_name, data):
    if ( collection_name is not None):
        try:
            collection_name.update(data, data, upsert=True)
        except:
            print("collection update error   ")
            return
def drop_collection(db_name, collection_name):
    db = client_main[db_name]
    collection = db[collection_name]
    collection.drop()
    return collection

def show_database():
    result_list = []
    for db in client_main.list_databases():
        result_list.append(db)
    return result_list
def delete_database(db_name):
    if db_name =="ALL":
        for i in show_database():
            if i['name'] == "stock_data":
                print("this!")
            elif i['name'] == "admin":
                print("admin!")
            else:
                client_main.drop_database(i['name'])
    if db_name =="REAL_ALL":
        for i in show_database():
            if i['name'] == "stock_data":
                print("this!")
            elif i['name'] == "admin":
                print("admin!")
            else:
                client_main.drop_database(i['name'])

if __name__ ==  "__main__":
    delete_database("ALL")
    #drop_collection("stock_data", "TR_1206")
    '''drop_collection("stock_data", "TR_1206")'''