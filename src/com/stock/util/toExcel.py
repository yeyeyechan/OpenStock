from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari

excel_dir = os.path.dirname(os.path.abspath(__file__))


if __name__ ==  "__main__":
    file_name = "test1.xls"

    file_dir = excel_dir+"/util_data/"+file_name

    print(file_dir)
    from_collection = make_collection("stock_data", "logic3")

    from_collection_data =  from_collection.find_one({"일자": Today_date})

    stock_code_data = from_collection_data["stock_code"]
    stock_name_data = []
    to_collection = make_collection("stock_data" , "stock_mst")

    for i in stock_code_data:
        stock_mst = to_collection.find_one({"단축코드" : i})
        stock_name_data.append(copy(stock_mst["종목명"]))

    df = pd.DataFrame({"종목코드" : stock_code_data , "종목명" : stock_name_data})

    writer = pd.ExcelWriter(file_dir, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='test' , index= False)
    writer.close()