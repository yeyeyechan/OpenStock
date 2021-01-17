from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari



def tr_output_dict(tr_name):
    result_output_dict = {}
    result_output_dict["single_output"] = {}
    result_output_dict["multi_output"]  = {}
    print(com_vari.TR_output_dict[tr_name.strip()]["single_output"])
    if com_vari.TR_output_dict[tr_name.strip()]["single_output"] != [] :
        for index, value in enumerate(com_vari.TR_output_dict[tr_name.strip()]["single_output"]):
            result_output_dict["single_output"][index] = value.strip()
    if com_vari.TR_output_dict[tr_name.strip()]["multi_output"] != []:
        print(com_vari.TR_output_dict[tr_name.strip()]["multi_output"])
        for index, value in enumerate(com_vari.TR_output_dict[tr_name.strip()]["multi_output"]):
            result_output_dict["multi_output"][index] = value.strip()

    return result_output_dict

def make_output_dict(single_output, multi_output):
    single_output = make_dict(single_output)  # 아웃풋 컬럼명 배열을 index ,value 형태의 dictionary로 변형
    multi_output = make_dict(multi_output)  # 아웃풋 컬럼명 배열을 index ,value 형태의 dictionary로 변형

    output_dict = {}
    output_dict["single_output"] = single_output
    output_dict["multi_output"] = multi_output

    return output_dict

def make_dict(array):
    dict = {}
    for i in range(len(array)):
        dict[i] = array[i]
    return dict

def make_dict(array):
    dict = {}
    for i in range(len(array)):
        dict[i] = array[i]
    return dict

class tr_result():
    def __init__(self, list, listLen):
        self.list = list
        self.listLen = listLen

        self.result = {"list": self.list, "lsitLen": self.listLen}

class real_indi_object(QMainWindow):
    def __init__(self, tr_name):
        super().__init__()
        self.tr_name = tr_name
        # Indi API event
        if tr_name not in com_vari.indiReal_dict.keys():
            com_vari.indiReal_dict[tr_name] = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        # Indi API event
        com_vari.indiReal_dict[self.tr_name].ReceiveRTData.connect(self.ReceiveRTData)
        com_vari.indiReal_dict[self.tr_name].ReceiveSysMsg.connect(self.ReceiveSysMsg)

        self.collection = make_collection("stock_data" , com_vari.DEFAILT_TR_DB_NAME[tr_name])

        self.input_dict_list = []
        self.pk_dict_list = []
        self.collection_len = 0
        self.in_out_builder = InOutBuilder(self.tr_name , com_vari.path_to_tr_file)

    def set_input_data(self,input_list):
        self.input_list = input_list
        self.in_out_builder.set_input_list(self.input_list)
        self.input_data_list = self.in_out_builder.get_input_data_list()
        self.single_output_dict = self.in_out_builder.get_single_output_dict()
        self.static_pk_dict = self.in_out_builder.get_static_pk_dict()
    def call_tr(self, input_data_list="first_call"):
        if input_data_list =="first_call":
            pass
        else:
            self.input_data_list = input_data_list

        for stock_code in self.input_data_list:
            ret = com_vari.indiReal_dict[self.tr_name].dynamicCall("RequestRTReg(QString, QString)", self.tr_name, stock_code)
            if  ret:
                print("실시간 TR   " + self.tr_name + "  에 대한   종목코드  " + stock_code + " 등록  성공")
            else:
                print("실시간 TR   " + self.tr_name + "  에 대한   종목코드  " + stock_code + " 등록  실패")

    def set_tr_data(self, tr_name, indi_object, single_output_dict, static_pk_dict):
        single_output_data = {}
        if single_output_dict:
            print(len(single_output_dict))
            for key, value in single_output_dict.items():
                if (indi_object.dynamicCall("GetSingleData(int)", key) == None):
                    print("  key   " + key + "   value    " + value)
                single_output_data[value.strip()] = indi_object.dynamicCall("GetSingleData(int)", key).strip()
        if static_pk_dict:
            for key, value in static_pk_dict.items():
                single_output_data[key.strip()] = value
        if not bool(single_output_data):
            print("실시간 TR  " + tr_name + "   데이터 reaceive 까진 왔으나 single_out_data 에  지정 안됨")
            pass
        return single_output_data

    def db_update(self , tr_name, single_output_data ):
        if tr_name == "SK":
            data_input = self.collection.find_one(
                {'단축코드': single_output_data['단축코드'], '체결시간': single_output_data['체결시간'],
                 "일자": single_output_data["일자"]})
        if tr_name == "SP":
            data_input = self.collection.find_one(
                {'단축코드': single_output_data['단축코드'], '시간': single_output_data['시간'],
                 "일자": single_output_data["일자"]})
        if tr_name == "SC":
            data_input = self.collection.find_one(
                {'단축코드': single_output_data['단축코드'], '체결시간': single_output_data['체결시간'],
                 "일자": single_output_data["일자"]})
            analysis(tr_name,single_output_data )
        if data_input != None:
            single_output_data['_id'] = data_input['_id']
            self.collection.replace_one(data_input, single_output_data, upsert=True)
        else:
            self.collection.insert_one(single_output_data)
        analysis(tr_name, single_output_data)
        print(
            "실시간 TR  " + tr_name + "  단축코드   " + single_output_data['단축코드'] + "  실시간 아웃풋   " + str(single_output_data))

    def ReceiveRTData(self, realType):
        print("실시간  TR data 수신 !!!!    " + realType)
        single_output_data = {}
        single_output_data = self.set_tr_data(realType , com_vari.indiReal_dict[self.tr_name] , self.single_output_dict , self.static_pk_dict)

        if single_output_data is None:
            pass
        else:
            self.db_update(realType, single_output_data)

    # 시스템 메시지를 받은 경우 출력합니다.
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
        print("System Error Message Received = ", com_vari.indiReal_dict[self.tr_name].GetErrorMessage())



class indi_object(QMainWindow):
    def __init__(self, tr_name , control):
        super().__init__()
        # Indi API event
        self.IndiTR = control
        # Indi API event
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)

        self.rqidD = {}  # TR 관리를 위해 사전 변수를 하나 생성합니다.
        self.collection = make_collection("stock_data" , com_vari.DEFAILT_TR_DB_NAME[tr_name])
        self.tr_name = com_vari.DEFAILT_TR_NAME[tr_name]
        print(self.tr_name)
        self.input_dict_list = []
        self.pk_dict_list = []
        self.collection_len = 0
        self.in_out_builder = InOutBuilder(self.tr_name , com_vari.path_to_tr_file)

        self.tr_data_list = []

    def set_input_data_dict(self, input_data_dict):
        self.input_data_dict = input_data_dict
        self.in_out_builder.set_input_data_dict(self.input_data_dict)
        self.single_output_dict = self.in_out_builder.get_single_output_dict()
        self.multi_output_dict = self.in_out_builder.get_multi_output_dict()
        self.static_pk_dict = self.in_out_builder.get_static_pk_dict()


    def set_input_data(self,input_data_list):
        self.input_data_list = input_data_list
        self.in_out_builder.set_input_list(self.input_data_list)
        self.single_output_dict = self.in_out_builder.get_single_output_dict()
        self.multi_output_dict = self.in_out_builder.get_multi_output_dict()
        self.static_pk_dict = self.in_out_builder.get_static_pk_dict()

    def call_tr(self, input_data_dict="first_call"):
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", self.tr_name)
        if input_data_dict =="first_call":
            self.input_data_dict = self.in_out_builder.get_input_dict()
            print(self.input_data_dict)
        if not bool(self.input_data_dict) and input_data_dict =="first_call":
            pass
        elif bool(self.input_data_dict):
            for key, value in self.input_data_dict.items():
                print("key   " + str(key)  + "  value  " + value)
                ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", int(key), str(value))
        else:
            print("input data 가 없습니다 !!")
            QCoreApplication.instance().exit()
        rqid = self.IndiTR.dynamicCall("RequestData()")
        self.rqidD[rqid] = self.tr_name


    def ReceiveData(self, rqid):
        TRName = self.rqidD[rqid]
        print("TR data 수신 !!!!    " + TRName)

        self.pk_data_dict = self.in_out_builder.get_pk_dict()

        self.tr_data_list_input = []
        print( self.IndiTR.dynamicCall("GetErrorState()"))
        print( self.IndiTR.dynamicCall("GetErrorCode()"))
        print( self.IndiTR.dynamicCall("GetErrorMessage()"))
        print( self.IndiTR.dynamicCall("GetCommState()"))
        if TRName == self.tr_name:
            nCnt = self.IndiTR.dynamicCall("GetMultiRowCount()")
            singleCnt = self.IndiTR.dynamicCall("GetSingleRowCount()")

            single_output_data = {}
            if  self.single_output_dict:
                for key , value in self.single_output_dict.items():
                    single_output_data[value.strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", key).strip()
            if  self.pk_data_dict:
                for key , value in self.pk_data_dict.items():
                    single_output_data[key.strip()] = value.strip()
            if self.tr_name == "SK" or self.tr_name =="SP"  or self.tr_name =="real_TR_1206":
                if self.static_pk_dict:
                    for key, value in self.static_pk_dict.items():
                        single_output_data[key.strip()] = value
            for i in range(0, nCnt):
                if  self.multi_output_dict :
                    multi_output_data = {}
                    for key , value in self.multi_output_dict.items():
                        multi_output_data[value.strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, key).strip()

                    final_data = {}
                    final_data.update(single_output_data)
                    final_data.update(multi_output_data)
                    self.tr_data_list_input.append(copy(final_data))

            #print("Tr " + self.tr_name + " 의  인풋  " +str(self.input_data_dict) + "  에 대한 아웃풋   ")
            #print(str(self.tr_data_list_input))
            print("수신 받은 데이터   " +str(self.tr_data_list_input))
            self.tr_data_list.extend(copy(self.tr_data_list_input))
            if len(self.tr_data_list) >= 4000:
                self.collection.insert_many(self.tr_data_list)
                self.tr_data_list = []
            #print("  tr_data_list   에 추가 되었습니다.....")
            self.input_data_dict = self.in_out_builder.get_input_dict()
            if  bool (self.input_data_dict) :
                self.call_tr(self.input_data_dict)
            else:
                print(" 마지막 루프 tr 호출 종료")
                print(" tr_data_list 가 DB에 저장 됩니다  ")
                print(self.tr_data_list)
                if self.tr_data_list == [] :
                    print("Tr data list 가 없습니다")
                else:
                    self.collection.insert_many(self.tr_data_list)
                print(" tr_data_list 저장 완료  ")
                QCoreApplication.instance().exit()

    def GetDataAll(self):
        result = tr_result(self.list, self.listLen)
        return result
    # 시스템 메시지를 받은 경우 출력합니다.
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
        print("System Error Message Received = ",self.IndiTR.GetErrorMessage())