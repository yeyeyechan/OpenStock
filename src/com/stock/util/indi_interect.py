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

class real_tr_object(QMainWindow):
    def __init__(self, tr_name, db_collection):
        super().__init__()
        # Indi API event
        self.tr_name = tr_name

        if tr_name not in com_vari.indiReal_dict.keys():
            com_vari.indiReal_dict[tr_name] = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        # Indi API event
        com_vari.indiReal_dict[self.tr_name ].ReceiveRTData.connect(self.ReceiveRTData)
        com_vari.indiReal_dict[self.tr_name ].ReceiveSysMsg.connect(self.ReceiveSysMsg)

        self.rqidD = {}  # TR 관리를 위해 사전 변수를 하나 생성합니다.
        self.collection = db_collection
        self.col_name = {}
        self.input_index = 0

        self.list = []
        self.listLen = 0

        self.input_list = []
        self.pk_dict = []
        self.collection_len = 0

    def set_multi_call(self, input_list, output_dict, pk_dict, collection_len):

        self.input_list = input_list
        self.pk_dict = pk_dict
        self.collection_len = collection_len
        self.col_name = output_dict
        print(self.input_list)
        for input in input_list :
            ret1 = com_vari.indiReal_dict[self.tr_name ].dynamicCall("UnRequestRTReg(QString, QString)", self.tr_name, input)
            if not ret1:
                print("실시간 TR   "+ self.tr_name +"  에 대한   종목코드  " + input + " 등록 해제 실패")
                ret1 = com_vari.indiReal_dict[self.tr_name ].dynamicCall("RequestRTReg(QString, QString)", self.tr_name, input)
                if not ret1:
                    print("실시간 TR   "+ self.tr_name +"  에 대한   종목코드  " + input + " 등록  실패")
                else:
                    print("실시간 TR   "+ self.tr_name +"  에 대한   종목코드  " + input+ " 등록  성공")

            else:
                print("실시간 TR   "+ self.tr_name +"  에 대한   종목코드  " + input+ " 등록 해제 성공")
                ret1 = com_vari.indiReal_dict[self.tr_name ].dynamicCall("RequestRTReg(QString, QString)", self.tr_name, input)
                if not ret1:
                    print("실시간 TR   "+ self.tr_name +"  에 대한   종목코드  " + input + " 등록  실패")
                else:
                    print("실시간 TR   "+ self.tr_name +"  에 대한   종목코드  " + input+ " 등록  성공")


    def ReceiveRTData(self, realType):
        if realType == "SK":
            DATA = {}
            # 데이터 받기
            DATA['단축코드'] = com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 1)
            DATA['시간'] = com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 2)
            DATA['국내총순매수수량'] = (int)(com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 41))
            DATA['외국계순매수수량'] = (int)(com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 47))
            DATA['전체순매수수량'] = (int)(com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 53))
            for key , value in self.pk_dict:
                DATA[key] = value

            if self.collection.find_one({'단축코드': DATA['단축코드'], '시간':DATA['시간'], "일자": DATA["일자"]}) != None:
                data_input = self.collection.find_one({'단축코드': DATA['단축코드'], '시간':DATA['시간'], "일자": DATA["일자"]}).copy()
                DATA['_id'] = data_input['_id']
                self.collection.replace_one(data_input, DATA, upsert=True)
            else:
                self.collection.insert_one(DATA)

        if realType == "SP":
            DATA = {}
            # 데이터 받기
            DATA['단축코드'] = com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 1)
            DATA['일자'] = com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 2)
            DATA['시간'] = com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 3)
            DATA['매도위탁체결수량'] = com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 12)
            DATA['매도자기체결수량'] = com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 13)
            DATA['매수위탁체결수량'] = com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 14)
            DATA['매수자기체결수량'] = com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 15)
            DATA['매도위탁체결금액'] = com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 16)
            DATA['매도자기체결금액'] = com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 17)
            DATA['매수위탁체결금액'] = com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 18)
            DATA['매수자기체결금액'] = com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 19)
            DATA['차익매도위탁체결수량'] = int(com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 27))
            DATA['차익매수위탁체결수량'] = int(com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 28))
            DATA['차익매수자기체결수량'] = int(com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 29))
            DATA['비차익매도위탁체결수량'] = int(com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 30))
            DATA['비차익매도자기체결수량'] = int(com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 31))
            DATA['비차익매수위탁체결수량'] = int(com_vari.indiReal_dict[self.tr_name ].dynamicCall("GetSingleData(int)", 32))
            DATA['비차익위탁프로그램순매수'] = DATA['비차익매수위탁체결수량'] - DATA['비차익매도위탁체결수량']
            DATA['차익위탁프로그램순매수'] = DATA['차익매수위탁체결수량'] - DATA['차익매도위탁체결수량']

            if self.collection.find_one({'단축코드': DATA['단축코드'], '시간':DATA['시간'], "일자": DATA["일자"]}) != None:
                data_input = self.collection.find_one({'단축코드': DATA['단축코드'], '시간':DATA['시간'], "일자": DATA["일자"]}).copy()
                DATA['_id'] = data_input['_id']
                self.collection.replace_one(data_input, DATA, upsert=True)
            else:
                self.collection.insert_one(DATA)

    # 시스템 메시지를 받은 경우 출력합니다.
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
        print("System Error Message Received = ", com_vari.indiReal_dict[self.tr_name ].GetErrorMessage())

class tr_object(QMainWindow):
    def __init__(self, tr_name, db_collection):
        super().__init__()

        # Indi API event
        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        # Indi API event
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)

        self.rqidD = {}  # TR 관리를 위해 사전 변수를 하나 생성합니다.
        self.collection = db_collection
        self.tr_name = tr_name
        self.col_name = {}
        self.input_index = 0

        self.list = []
        self.listLen = 0

        self.multi= False
        self.input_dict_list = []
        self.pk_dict_list = []
        self.collection_len = 0

    def set_single_call(self, input_dict, output_dict, pk_dict):
        self.multi= False
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", self.tr_name)
        for key, value in input_dict.items():
            ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", key, value)
        rqid = self.IndiTR.dynamicCall("RequestData()")
        self.rqidD[rqid] = self.tr_name
        self.col_name = output_dict
        self.pk_dict = pk_dict

    def set_multi_call(self, input_dict_list, output_dict, pk_dict_list, collection_len):
        self.multi= True
        self.list = []
        self.listLen = 0
        self.input_index = 0

        self.input_dict_list = input_dict_list
        self.pk_dict_list = pk_dict_list
        self.collection_len = collection_len

        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", self.tr_name)
        for key, value in input_dict_list[0].items():
            ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", key, value)
        rqid = self.IndiTR.dynamicCall("RequestData()")

        self.rqidD[rqid] = self.tr_name
        self.col_name = output_dict

    def inner_call(self):
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", self.tr_name)
        for key, value in self.input_dict_list[self.input_index].items():
            ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", key, value)
        rqid = self.IndiTR.dynamicCall("RequestData()")
        self.rqidD[rqid] = self.tr_name

    def ReceiveData(self, rqid):
        TRName = self.rqidD[rqid]
        #com_vari.TR_1206_logger.debug("TR_1206 데이터 수신")
        if TRName == self.tr_name:
            nCnt = self.IndiTR.dynamicCall("GetMultiRowCount()")
            singleCnt = self.IndiTR.dynamicCall("GetSingleRowCount()")
            self.list = []
            self.listLen = nCnt
            if(self.multi):
                for i in range(0, nCnt):
                    # 데이터 받기
                    DATA = {}
                    for key , value in self.pk_dict_list[self.input_index].items():
                        DATA[key] = value
                    for key, value in self.col_name.items():
                        if self.tr_name == "TR_1205":
                            if key != 0 and key != 1 and key != 2 :
                                DATA[value.strip()] = int(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, key))
                            else:
                                DATA[value.strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, key)
                        else:
                            DATA[value.strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, key)
                        # print(DATA)
                    update_collection(self.collection, DATA)
                    self.list.append(DATA)

                print(self.list)
                if(self.list == []):
                    for key, value in self.input_dict_list[self.input_index].items():
                        com_vari.upjong_code_mst_logger.debug("데이터없음  key  "  +  str(key)  + "  value   " + value)
                    for key , value in self.pk_dict_list[self.input_index].items():
                        com_vari.upjong_code_mst_logger.debug("데이터없음  key  "  +  key  + "  value   " + value)
                    com_vari.upjong_code_mst_logger.debug("데이터 없음 체크 완료")

                if(TRName == "TR_1206" and com_vari.TR_1206_len_counts != self.listLen):
                    logging_string = TRName +" 단축코드 : "+self.pk_dict_list[self.input_index]["단축코드"] + "가 " +str(nCnt)  + " 만큼 적재 되었습니다."
                    com_vari.TR_1206_logger.debug(logging_string)
                print()
                self.input_index += 1
                if self.input_index != self.collection_len:
                    self.inner_call()
                else:
                    QCoreApplication.instance().exit()
            else:
                for i in range(0, nCnt):
                    # 데이터 받기
                    DATA = {}
                    for key, value in self.pk_dict.items():
                        DATA[key] = value
                    for key, value in self.col_name.items():
                        DATA[value.strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, key)
                    print(DATA)
                    update_collection(self.collection, DATA)
                QCoreApplication.instance().exit()

    def GetDataAll(self):
        result = tr_result(self.list, self.listLen)
        return result
    # 시스템 메시지를 받은 경우 출력합니다.
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
        print("System Error Message Received = ",self.IndiTR.GetErrorMessage())


class tr_object(QMainWindow):
    def __init__(self, tr_name, db_collection, control):
        super().__init__()

        # Indi API event
        self.IndiTR = control
        # Indi API event
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)

        self.rqidD = {}  # TR 관리를 위해 사전 변수를 하나 생성합니다.
        self.collection = db_collection
        self.tr_name = tr_name
        self.col_name = {}
        self.input_index = 0

        self.list = []
        self.listLen = 0

        self.multi= False
        self.input_dict_list = []
        self.pk_dict_list = []
        self.collection_len = 0

    def set_single_call(self, input_dict, output_dict, pk_dict):
        self.multi= False
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", self.tr_name)
        for key, value in input_dict.items():
            ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", key, value)
        rqid = self.IndiTR.dynamicCall("RequestData()")
        self.rqidD[rqid] = self.tr_name
        self.col_name = output_dict
        self.pk_dict = pk_dict

    def set_multi_call(self, input_dict_list, output_dict, pk_dict_list, collection_len):
        self.multi= True
        self.list = []
        self.listLen = 0
        self.input_index = 0

        self.input_dict_list = input_dict_list
        self.pk_dict_list = pk_dict_list
        self.collection_len = collection_len

        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", self.tr_name)
        for key, value in input_dict_list[0].items():
            ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", key, value)
        rqid = self.IndiTR.dynamicCall("RequestData()")

        self.rqidD[rqid] = self.tr_name
        self.col_name = output_dict

    def inner_call(self):
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", self.tr_name)
        for key, value in self.input_dict_list[self.input_index].items():
            ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", key, value)
        rqid = self.IndiTR.dynamicCall("RequestData()")
        self.rqidD[rqid] = self.tr_name

    def ReceiveData(self, rqid):
        TRName = self.rqidD[rqid]
        #com_vari.TR_1206_logger.debug("TR_1206 데이터 수신")
        if TRName == self.tr_name:
            nCnt = self.IndiTR.dynamicCall("GetMultiRowCount()")
            singleCnt = self.IndiTR.dynamicCall("GetSingleRowCount()")
            self.list = []
            self.listLen = nCnt
            if(self.multi):
                for i in range(0, nCnt):
                    # 데이터 받기
                    DATA = {}
                    for key , value in self.pk_dict_list[self.input_index].items():
                        DATA[key] = value
                    for key, value in self.col_name.items():
                        if self.tr_name == "TR_1205":
                            if key != 0 and key != 1 and key != 2 :
                                DATA[value.strip()] = int(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, key))
                            else:
                                DATA[value.strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, key).strip()
                        else:
                            DATA[value.strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, key).strip()
                        # print(DATA)
                    update_collection(self.collection, DATA)
                    self.list.append(DATA)

                print(self.list)
                if(self.list == []):
                    for key, value in self.input_dict_list[self.input_index].items():
                        com_vari.upjong_code_mst_logger.debug("데이터없음  key  "  +  str(key)  + "  value   " + value)
                    for key , value in self.pk_dict_list[self.input_index].items():
                        com_vari.upjong_code_mst_logger.debug("데이터없음  key  "  +  key  + "  value   " + value)
                    com_vari.upjong_code_mst_logger.debug("데이터 없음 체크 완료")

                if(TRName == "TR_1206" and com_vari.TR_1206_len_counts != self.listLen):
                    logging_string = TRName +" 단축코드 : "+self.pk_dict_list[self.input_index]["단축코드"] + "가 " +str(nCnt)  + " 만큼 적재 되었습니다."
                    com_vari.TR_1206_logger.debug(logging_string)
                print()
                self.input_index += 1
                if self.input_index != self.collection_len:
                    self.inner_call()
                else:
                    QCoreApplication.instance().exit()
            else:
                for i in range(0, nCnt):
                    # 데이터 받기
                    DATA = {}
                    for key, value in self.pk_dict.items():
                        DATA[key] = value
                    for key, value in self.col_name.items():
                        DATA[value.strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, key)
                    print(DATA)
                    update_collection(self.collection, DATA)
                QCoreApplication.instance().exit()

    def GetDataAll(self):
        result = tr_result(self.list, self.listLen)
        return result
    # 시스템 메시지를 받은 경우 출력합니다.
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
        print("System Error Message Received = ",self.IndiTR.GetErrorMessage())


class tr_class(QMainWindow):
    def __init__(self, tr_name, db_collection, indi_control):
        super().__init__()

        # Indi API event
        self.IndiTR =indi_control

        self.output_col = tr_output_dict(tr_name)
        # Indi API event
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)

        self.rqidD = {}  # TR 관리를 위해 사전 변수를 하나 생성합니다.
        self.collection = db_collection
        self.tr_name = tr_name
        self.input_index = 0

        self.list = []
        self.listLen = 0

        self.multi= False
        self.input_dict_list = []
        self.pk_dict_list = []
        self.collection_len = 0

    def set_single_call(self, input_dict , pk_dict):
        self.multi= False
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", self.tr_name)
        for key, value in input_dict.items():
            ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", key, value)
        rqid = self.IndiTR.dynamicCall("RequestData()")
        self.rqidD[rqid] = self.tr_name
        self.pk_dict = pk_dict

    def set_multi_call(self, input_dict_list, pk_dict_list, collection_len):
        self.multi= True
        self.list = []
        self.listLen = 0
        self.input_index = 0

        self.input_dict_list = input_dict_list
        self.pk_dict_list = pk_dict_list
        self.collection_len = collection_len

        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", self.tr_name)
        for key, value in input_dict_list[0].items():
            ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", key, value)
        rqid = self.IndiTR.dynamicCall("RequestData()")

        self.rqidD[rqid] = self.tr_name

    def inner_call(self):
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", self.tr_name)
        for key, value in self.input_dict_list[self.input_index].items():
            ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", key, value)
        rqid = self.IndiTR.dynamicCall("RequestData()")
        self.rqidD[rqid] = self.tr_name

    def ReceiveData(self, rqid):
        TRName = self.rqidD[rqid]

        if TRName == self.tr_name:
            nCnt = self.IndiTR.dynamicCall("GetMultiRowCount()")
            singleCnt = self.IndiTR.dynamicCall("GetSingleRowCount()")
            self.list = []
            self.listLen = nCnt

            if(self.multi):
                for i in range(0, nCnt):
                    # 데이터 받기
                    DATA = {}
                    if len(self.pk_dict_list)  != 0:
                        for key , value in self.pk_dict_list[self.input_index].items():
                            DATA[key] = value
                    if singleCnt != 0 :
                        for key, value in self.output_col["single_output"].items():
                            print(key)
                            print(value)
                            DATA[value.strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", key)
                    if nCnt != 0 :
                        for key, value in self.output_col["multi_output"].items():
                            if self.tr_name == "TR_1205":
                                if key != 0 and key != 1 and key != 2 :
                                    DATA[value.strip()] = int(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, key))
                                else:
                                    DATA[value.strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, key)
                            else:
                                DATA[value.strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, key)
                        update_collection(self.collection, DATA)
                        self.list.append(DATA)
                print(self.list)
                if(self.list == []):
                    for key, value in self.input_dict_list[self.input_index].items():
                        com_vari.upjong_code_mst_logger.debug("데이터없음  key  "  +  str(key)  + "  value   " + value)
                    for key , value in self.pk_dict_list[self.input_index].items():
                        com_vari.upjong_code_mst_logger.debug("데이터없음  key  "  +  key  + "  value   " + value)
                    com_vari.upjong_code_mst_logger.debug("데이터 없음 체크 완료")

                if(TRName == "TR_1206" and com_vari.TR_1206_len_counts != self.listLen):
                    logging_string = TRName +" 단축코드 : "+self.pk_dict_list[self.input_index]["단축코드"] + "가 " +str(nCnt)  + " 만큼 적재 되었습니다."
                    com_vari.TR_1206_logger.debug(logging_string)
                print()
                self.input_index += 1
                if self.input_index != self.collection_len:
                    self.inner_call()
                else:
                    QCoreApplication.instance().exit()
            else:
                for i in range(0, nCnt):
                    # 데이터 받기
                    DATA = {}
                    if singleCnt != 0:
                        for key, value in self.output_col["single_output"].items():
                            DATA[value.strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", key)
                    if len(self.pk_dict) != 0:
                        for key, value in self.pk_dict.items():
                            DATA[key] = value
                    if nCnt != 0 :
                        for key, value  in self.output_col["multi_output"].items():
                            print(type(key))
                            DATA[value.strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, key)
                        print(DATA)
                        update_collection(self.collection, DATA)
                QCoreApplication.instance().exit()

    def GetDataAll(self):
        result = tr_result(self.list, self.listLen)
        return result
    # 시스템 메시지를 받은 경우 출력합니다.
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
        print("System Error Message Received = ",self.IndiTR.GetErrorMessage())
