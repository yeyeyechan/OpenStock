# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\OpenStock")
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari
today = date.today().strftime("%Y%m%d")

###### data 변수  ######

day = today
#day = "20201223"
stock_code_collection = make_collection("stock_data" , "3daySupply")
stock_code = stock_code_collection.find_one({"일자": day})['stock_code']

sk_data = make_collection("stock_data", "SK")
sp_data = make_collection("stock_data", "SP")
real_TR_SCHART = make_collection("stock_data", "real_TR_SCHART")

###### data 변수  ######
app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Div([
            dcc.Dropdown(
            id="stock_code",
            options=[{'label': i , 'value' : i} for i in stock_code],
            value = stock_code[0],
            style={'width' :'50%'}
        )
    ],style={'width' : '100%' , 'display' :'inline-block'}),
    html.Div([
        dcc.Graph(id='graph1')
    ],style={'width' : '100%' , 'display' :'inline-block'})
]
)

@app.callback(
    Output(component_id='graph1', component_property='figure'),
    [Input(component_id='stock_code', component_property='value')]
)
def update_output(stock_code_input):
    sk_df = []
    data=[]

    if (sk_data.count_documents({}) == 0):
        pass
    else:
        try:
            for i in sk_data.find({"단축코드": stock_code_input, "일자": day}):
                sk_df.append(i)
            sk_df = pd.DataFrame(sk_df)
            sk_df_x = sk_df["체결시간"].astype('int32')
            sk_df_for = sk_df["외국계순매수수량"].astype('int32')
            data.append( {'x' : sk_df_x , 'y': sk_df_for, 'type' :'line' , 'name' : '외국계순매수수량'})
            sk_df_kor = sk_df["국내총순매수수량"].astype('int32')
            data.append( {'x' : sk_df_x , 'y': sk_df_kor, 'type' :'line' , 'name' : '국내총순매수수량'})
        except:
            print("sk_df 다루던중 오류")

    if (real_TR_SCHART.count_documents({}) == 0):
        pass
    else:
        try:
            tr_schart_df = []
            for i in real_TR_SCHART.find({"단축코드": stock_code_input, "일자": day}):
                tr_schart_df.append(i)
            tr_schart_df = pd.DataFrame(tr_schart_df)

            tr_schart_df_x = tr_schart_df["시간"].astype('int32').multiply(other=100)
            tr_schart_df_price = tr_schart_df["종가"].astype('int32')
            data.append({'x' : tr_schart_df_x , 'y': tr_schart_df_price, 'type' :'line' , 'name' : '5분 단위 현재가'})
        except:
            print("tr_schart_df 다루던중 오류")
        if (sp_data.count_documents({}) == 0):
            pass
        else:
            try:
                sp_df = []
                for i in sp_data.find({"단축코드": stock_code_input, "일자": day}):
                    sp_df.append(i)
                sp_df = pd.DataFrame(sp_df)

                sp_df_x = sp_df["시간"].astype('int32')
                sp_df_buy = sp_df["비차익매수위탁체결수량"].astype('int32')
                sp_df_sell = sp_df["비차익매도위탁체결수량"].astype('int32')
                sp_df_pure = sp_df_buy - sp_df_sell
                data.append({'x': sp_df_x, 'y': sp_df_pure, 'type': 'line', 'name': '프로그램순매수수량'})
            except:
                print("sp_df 다루던중 오류")
    if not data:
        data.append({'x' : [] , 'y': [], 'type' :'line' , 'name' : '데이터 없음'})
    figure = {
        'data':data,
        'layout':{
            'title':'Dash Data Visualization'
        }
    }
    return figure
if __name__ == "__main__":
    app.run_server(debug=True, port=8080, host='0.0.0.0')
