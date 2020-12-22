
# -*- conding: utf-8 -*-


from src.com.stock.common.import_lib import *
def graph_function():
    #데이터
    sk_data = make_collection("stock_data", "SK")
    sp_data = make_collection("stock_data", "SP")
    stock_code = "226950"
    date = "20201211"
    sk_test_data = sk_data.find({"단축코드" : stock_code, "일자" : date})
    sp_data_data = sp_data.find({"단축코드" : stock_code, "일자" : date})

    result = []
    for i in sk_test_data:
        result.append(i)
    result_sk = pd.DataFrame(result)

    #6 자리 153000
    time_sk = result_sk["체결시간"].astype('int32')
    foreign = result_sk["외국계순매수수량"].astype('int32')
    kor = result_sk["국내총순매수수량"].astype('int32')

    result = []
    for i in sp_data_data:
        result.append(i)
    result_sp = pd.DataFrame(result)

    #6 자리 153000
    time_sp = result_sp["시간"].astype('int32')
    buy = result_sp["비차익매수위탁체결수량"].astype('int32')
    sell = result_sp["비차익매도위탁체결수량"].astype('int32')
    pure = buy - sell


    fig = plt.figure(figsize=(20,20))
    fig.set_facecolor('white')

    ax1 = fig.add_subplot()
    ax1.plot(time_sk , foreign, "o-")
    ax2 = fig.add_subplot()
    ax2.plot(time_sk , kor, "or-")
    ax3 = fig.add_subplot()
    ax3.plot(time_sp , pure, "ob-")

    plt.xticks(np.arange(90500, 153000, 1000) , rotation = 25)
  #  plt.tick_params(axis='x' , width=10)

    plt.show()


if __name__ ==  "__main__":
    graph_function()

