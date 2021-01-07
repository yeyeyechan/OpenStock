# -*- coding: utf-8 -*-
import sys

from plotly.tools import make_subplots

sys.path.append("C:\\dev\\OpenStock")
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari

today = date.today().strftime("%Y%m%d")

###### data 변수  ######

day = today
day = "20210107"
before_day = get_kr_working_day_by_diff(day, -1).strftime("%Y%m%d")
stock_code_collection = make_collection("stock_data" , "3daySupply")
stock_code = stock_code_collection.find_one({"일자": day})['stock_code']

sk_data = make_collection("stock_data", "SK")
sp_data = make_collection("stock_data", "SP")
real_TR_SCHART = make_collection("stock_data", "real_TR_SCHART")
tr_1206 = make_collection("stock_data", "TR_1206")
stock_mst = make_collection("stock_data", "stock_mst")
real_tr_1206 = make_collection("stock_data", "real_TR_1206")


###### data 변수  ######
radio_option = {
"전체후보군": "0",
"실시간 외국계 수급 플러스": "1",
"실시간 외국계 수급 마이너스": "2",
"실시간 외국계 수급 없음": "3",

}
app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Div([
            dcc.RadioItems(
                id='stock-radio',
                options=[{'label': k, 'value': radio_option[k]} for k in radio_option.keys()],
                value=radio_option["전체후보군"]
            ),
            dcc.Dropdown(
            id="stock_code",
            #options=[{'label': i , 'value' : i} for i in stock_code],
            style={'width' :'50%'}
        ),
        html.Span([
            html.Span("  총 갯수 : "),
            html.Span(id='total_count'),
            html.Span("  수익 난 종목 수  :  "),
            html.Span(id='up_stock'),
            html.Span("  5% 이상 수익 난 종목 수  :  "),
            html.Span(id='five_up_stock'),
            html.Span("  손해 난 종목 수  :  "),
            html.Span(id='down_stock'),
            html.Span("  보합 난 종목 수  :  "),
            html.Span(id='same_stock'),
            html.Span("  카테고리 내 갯수 대비 수익률  :  "),
            html.Span(id='ratio'),
            html.Span("  카테고리 내 갯수 대비 5% 이상  수익률  :  "),
            html.Span(id='five_ratio'),
        ]),
    ],style={'width' : '100%' , 'display' :'inline-block'}),
    html.Div([
        html.Span([
            html.Span("  종목명 : "),
            html.Span(id='stock_name'),
            html.Span("  종목코드  :  "),
            html.Span(id='stock-code'),
            html.Span(" 수익율  :  "),
            html.Span(id='stock_ratio'),
            html.Span(" 거래량  :  "),
            html.Span(id='stock_vol'),
            html.Span(" 가격  :  "),
            html.Span(id='stock_price'),
            html.Span(" 거래대금  :  "),
            html.Span(id='stock_trd_vol'),
        ]),
        dcc.Graph(id='graph1')
    ],style={'width' : '100%' , 'display' :'inline-block'})
]
)
def check_data_2(stock_code, day):
    real_TR_SCHART_data = int(real_TR_SCHART.find_one({"일자" : day , "단축코드" : stock_code},  sort=[("체결시간", pymongo.DESCENDING)])["종가"])
    tr_1206_data = int(tr_1206.find_one({"일자" : before_day , "단축코드" : stock_code})["가격"])
    real_tr_1206_data = real_tr_1206.find_one({"일자" : day , "단축코드" : stock_code})

    stock_name = stock_mst.find_one({"단축코드" : stock_code})["종목명"]
    stock_ratio = round((real_TR_SCHART_data - tr_1206_data) / tr_1206_data * 100.0, 2)
    stock_vol =  int(real_tr_1206_data["누적거래량"])

    stock_price =int(real_tr_1206_data["가격"])

    stock_trd_vol = stock_vol*stock_price

    return stock_name , stock_ratio ,stock_vol ,stock_price,stock_trd_vol
def check_data(stock_code, day, total_count , up_stock, five_up_stock,  down_stock,same_stock, ratio , five_ratio):
    total_count +=1
    real_TR_SCHART_data = int(real_TR_SCHART.find_one({"일자" : day , "단축코드" : stock_code},  sort=[("체결시간", pymongo.DESCENDING)])["종가"])
    tr_1206_data = int(tr_1206.find_one({"일자" : before_day , "단축코드" : stock_code})["가격"])

    if real_TR_SCHART_data > tr_1206_data:
        up_stock += 1
        if (real_TR_SCHART_data - tr_1206_data)/tr_1206_data*100.0 >=5.0:
            five_up_stock += 1
    elif real_TR_SCHART_data == tr_1206_data:
        same_stock += 1
    elif real_TR_SCHART_data < tr_1206_data:
        down_stock += 1
    ratio = up_stock/total_count*100.0
    five_ratio = five_up_stock/total_count*100.0
    return total_count , up_stock, five_up_stock , down_stock,same_stock, ratio, five_ratio
def check_data_up(stock_code, day, total_stock ,  five_up_stock):
    real_TR_SCHART_data = int(real_TR_SCHART.find_one({"일자" : day , "단축코드" : stock_code},  sort=[("체결시간", pymongo.DESCENDING)])["종가"])
    tr_1206_data = int(tr_1206.find_one({"일자" : before_day , "단축코드" : stock_code})["가격"])

    if real_TR_SCHART_data > tr_1206_data:
        if (real_TR_SCHART_data - tr_1206_data)/tr_1206_data*100.0 >=5.0:
            five_up_stock += 1
            total_stock.append(stock_code)
    return total_stock, five_up_stock
@app.callback(
    [
        Output(component_id='stock_code', component_property='options'),
        Output(component_id='stock_code', component_property='value'),
        Output(component_id='total_count', component_property='children'),
        Output(component_id='up_stock', component_property='children'),
        Output(component_id='five_up_stock', component_property='children'),
        Output(component_id='down_stock', component_property='children'),
        Output(component_id='same_stock', component_property='children'),
        Output(component_id='ratio', component_property='children'),
        Output(component_id='five_ratio', component_property='children'),
     ],
    [Input(component_id='stock-radio', component_property='value')])
def set_stock_code_options(selected_option):
    postive_for_stock_code =[]
    negative_for_stock_code =[]
    no_for_stock_code =[]

    total_count = 0
    up_stock = 0
    five_up_stock = 0
    down_stock = 0
    same_stock = 0
    ratio = 0.0
    five_ratio = 0.0
    '''if selected_option == "0":
           total_stock = []
           for i in stock_code:
               total_stock,  five_up_stock = check_data_up(i,day,total_stock,five_up_stock)

           return [{'label': i, 'value': i} for i in total_stock], total_stock[0], total_count, up_stock, five_up_stock, down_stock, same_stock, ratio, five_ratio
       #### 외국인 수급 양 ##############'''
    if selected_option =="0":
        for i in stock_code:
            total_count, up_stock, five_up_stock, down_stock, same_stock, ratio, five_ratio = check_data(i, day, total_count, up_stock, five_up_stock, down_stock, same_stock,ratio, five_ratio)
        ratio = round(ratio, 2)
        five_ratio = round(five_ratio, 2)
        return [{'label': i , 'value' : i} for i in stock_code], stock_code[0], total_count , up_stock, five_up_stock,  down_stock,same_stock, ratio , five_ratio
    elif selected_option =="1":
        for i in stock_code:
            for_data = int(sk_data.find_one({"단축코드" : i, "일자" : day }, sort=[("체결시간", pymongo.DESCENDING)])["외국계순매수수량"])
            if for_data >0:
                print("외국계 순매수 수량 양   단축코드  "  +  i + "   " + str(for_data))
                postive_for_stock_code.append(i)
                total_count, up_stock, five_up_stock, down_stock, same_stock, ratio, five_ratio = check_data(i, day, total_count , up_stock, five_up_stock,  down_stock,same_stock, ratio , five_ratio)
        ratio = round(ratio, 2)
        five_ratio = round(five_ratio, 2)
        return [{'label': i, 'value': i} for i in postive_for_stock_code], postive_for_stock_code[0], total_count , up_stock, five_up_stock,  down_stock,same_stock, ratio , five_ratio
    #### 외국인 수급 양 ##############

    #### 외국인 수급 음 ##############
    elif selected_option =="2":
        for i in stock_code:
            for_data = int(sk_data.find_one({"단축코드" : i, "일자" : day }, sort=[("체결시간", pymongo.DESCENDING)])["외국계순매수수량"])
            if for_data <0:
                print("외국계 순매수 수량 음   단축코드  "  +  i + "   " + str(for_data))
                negative_for_stock_code.append(i)
                total_count, up_stock, five_up_stock, down_stock, same_stock, ratio, five_ratio = check_data(i, day, total_count , up_stock, five_up_stock,  down_stock,same_stock, ratio , five_ratio)
        ratio = round(ratio, 2)
        five_ratio = round(five_ratio, 2)
        return [{'label': i, 'value': i} for i in negative_for_stock_code], negative_for_stock_code[0], total_count , up_stock, five_up_stock,  down_stock,same_stock, ratio , five_ratio
    #### 외국인 수급 음 ##############
    #### 외국인 수급 무 ##############
    elif selected_option =="3":
        for i in stock_code:
            for_data = int(sk_data.find_one({"단축코드" : i, "일자" : day }, sort=[("체결시간", pymongo.DESCENDING)])["외국계순매수수량"])
            if for_data == 0:
                print("외국계 순매수 수량 없음     단축코드  "  +  i + "   " + str(for_data))
                no_for_stock_code.append(i)
                total_count, up_stock, five_up_stock, down_stock, same_stock, ratio, five_ratio = check_data(i, day, total_count , up_stock, five_up_stock,  down_stock,same_stock, ratio , five_ratio)
        ratio = round(ratio, 2)
        five_ratio = round(five_ratio, 2)
        return [{'label': i, 'value': i} for i in no_for_stock_code], no_for_stock_code[0], total_count , up_stock, five_up_stock,  down_stock,same_stock, ratio , five_ratio
    #### 외국인 수급 무 ##############



@app.callback(
    [
        Output(component_id='graph1', component_property='figure'),
        Output(component_id='stock_name', component_property='children'),
        Output(component_id='stock-code', component_property='children'),
        Output(component_id='stock_ratio', component_property='children'),
        Output(component_id='stock_vol', component_property='children'),
        Output(component_id='stock_price', component_property='children'),
        Output(component_id='stock_trd_vol', component_property='children'),
     ],
    [Input(component_id='stock_code', component_property='value')]
)
def update_output(stock_code_input):
    sk_df = []
    data=[]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    stock_name  = stock_mst.find_one({"단축코드" : stock_code_input})["종목명"]
    stock_code = stock_code_input

    stock_ratio = 0
    stock_vol = 0
    stock_price = 0
    stock_trd_vol = 0
    stock_name, stock_ratio, stock_vol, stock_price, stock_trd_vol = check_data_2(stock_code_input, day)
    if (sk_data.count_documents({}) == 0):
        pass
    else:
        try:
            for i in sk_data.find({"단축코드": stock_code_input, "일자": day}, sort=[("체결시간", pymongo.ASCENDING)]):
                sk_df.append(i)
            sk_df = pd.DataFrame(sk_df)

            sk_df_x = sk_df["체결시간"].apply ( lambda x : string_to_datetime (day, x))
            '''print("sk_df_x   ")
            print(sk_df_x)
            print("sk_df_x   ")
            sk_df_for = sk_df["외국계순매수수량"].astype('int32')
            print("sk_df_for   ")
            print(sk_df_for)
            print("sk_df_for   ")
            #data.append( {'x' : sk_df_x , 'y': sk_df_for, 'type' :'line' , 'name' : '외국계순매수수량'})
            # Add traces
            fig.add_trace(
                go.Scatter(x=sk_df_x, y=sk_df_for, name="외국계순매수수량"),
                secondary_y=False,
            )'''
            sk_df_kor = sk_df["국내총순매수수량"].astype('int32')
            print("sk_df_kor   ")
            print(sk_df_kor)
            print("sk_df_kor   ")
            #data.append( {'x' : sk_df_x , 'y': sk_df_kor, 'type' :'line' , 'name' : '국내총순매수수량'})
            # Add traces
            fig.add_trace(
                go.Scatter(x=sk_df_x, y=sk_df_kor, name="국내총순매수수량"),
                secondary_y=False,
            )
            '''sk_df_all = sk_df["전체총매수수량"].astype('int32')
            print("sk_df_all   ")
            print(sk_df_all)
            print("sk_df_all   ")
            #data.append( {'x' : sk_df_x , 'y': sk_df_kor, 'type' :'line' , 'name' : '국내총순매수수량'})
            # Add traces
            fig.add_trace(
                go.Scatter(x=sk_df_x, y=sk_df_all, name="전체총매수수량"),
                secondary_y=False,
            )'''
        except:
            print("sk_df 다루던중 오류")

    if (real_TR_SCHART.count_documents({}) == 0):
        pass
    else:
        try:
            tr_schart_df = []
            for i in real_TR_SCHART.find({"단축코드": stock_code_input, "일자": day}, sort=[("체결시간", pymongo.ASCENDING)]):
                tr_schart_df.append(i)
            tr_schart_df = pd.DataFrame(tr_schart_df)

            tr_schart_df_x = tr_schart_df["시간"]
            tr_schart_df_x = tr_schart_df_x.apply(lambda x: string_to_datetime(day, x))

            tr_schart_df_price = tr_schart_df["종가"].astype('int32')
            # Add traces
            fig.add_trace(
                go.Scatter(x=tr_schart_df_x, y=tr_schart_df_price, name="5분 단위 현재가"),
                secondary_y=True,
            )

            tr_schart_df_vol = tr_schart_df["단위거래량"].astype('int32')
            # Add traces
            fig.add_trace(
                go.Scatter(x=tr_schart_df_x, y=tr_schart_df_vol, name="5분 단위거래량"),
                secondary_y=False,
            )

            #data.append({'x' : tr_schart_df_x , 'y': tr_schart_df_price, 'type' :'line' , 'name' : '5분 단위 현재가'})
        except:
            print("tr_schart_df 다루던중 오류")
        if (sp_data.count_documents({}) == 0):
            pass
        else:
            try:
                sp_df = []
                for i in sp_data.find({"단축코드": stock_code_input, "일자": day}, sort=[("시간", pymongo.ASCENDING)]):
                    sp_df.append(i)
                sp_df = pd.DataFrame(sp_df)


                sp_df_x = sp_df["시간"].apply(lambda x: string_to_datetime(day, x))

                sp_df_buy = sp_df["비차익매수위탁체결수량"].astype('int32')
                sp_df_sell = sp_df["비차익매도위탁체결수량"].astype('int32')
                sp_df_pure = sp_df_buy - sp_df_sell
                # Add traces
                fig.add_trace(
                    go.Scatter(x=sp_df_x, y=sp_df_pure, name="프로그램순매수수량"),
                    secondary_y=False,
                )
                #data.append({'x': sp_df_x, 'y': sp_df_pure, 'type': 'line', 'name': '프로그램순매수수량'})
            except:
                print("sp_df 다루던중 오류")
    if not data:
        data.append({'x' : [] , 'y': [], 'type' :'line' , 'name' : '데이터 없음'})

    # Set x-axis title
    fig.update_xaxes(title_text="분석 그래프 ")
    # Set y-axes titles
    fig.update_yaxes(
        tickformat=',',
        title_text="<b>primary</b> 거래량 수치 ",
        secondary_y=False)
    fig.update_yaxes(
        tickformat =',',
        title_text="<b>secondary</b> 가격 값 " ,
        secondary_y=True)
    return fig , stock_name, stock_code_input, stock_ratio, stock_vol, stock_price, stock_trd_vol
    '''figure = {
         'data':data,
         'layout':{
             'title':'Dash Data Visualization'
         }
     }'''
    #return figure
if __name__ == "__main__":
    app.run_server(debug=True, port=8080, host='0.0.0.0')
