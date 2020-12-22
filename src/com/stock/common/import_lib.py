import sys
sys.path.append("C:\\dev\\OpenStock\\src\\com\\stock\\analysis")
sys.path.append("C:\\dev\\OpenStock\\src\\com\\stock\\common")
sys.path.append("C:\\dev\\OpenStock\\src\\com\\stock\\data")
sys.path.append("C:\\dev\\OpenStock\\src\\com\\stock\\login")
sys.path.append("C:\\dev\\OpenStock\\src\\com\\stock\\tr_data")
sys.path.append("C:\\dev\\OpenStock\\src\\com\\stock\\util")
sys.path.append("C:\\dev\\OpenStock\\src\\com\\stock\\util\\logger")
sys.path.append("C:\\dev\\OpenStock\\src\\com\\stock\\util\\util_data")
import os
import numpy as np
import pandas as pd
import logging
import logging.config
import xmltodict
import time
import win32com.client as com
from threading import Thread
import telegram
import pythoncom
from copy import copy
import requests
import urllib.parse as urlparse
from pytimekr.pytimekr import is_red_day
from datetime import date, timedelta
from datetime import datetime
from datetime import date as dt_dt
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import *
import pymongo
import matplotlib.pyplot as plt
from src.com.stock.util.mongo_db import *
from src.com.stock.common.openAPI import *
from src.com.stock.util.date import *
from src.com.stock.util.logger.myLogging import *
from src.com.stock.common.telegram_bot import *
from src.com.stock.data.common_data import *
from src.com.stock.analysis.analysis_filter import *
from src.com.stock.data.in_out_builder import *
from src.com.stock.util.indi_interect import *
from src.com.stock.util.data_check import *
from src.com.stock.analysis.analysis import *
from src.com.stock.util.toExcel import *
from src.com.stock.analysis.analysis2 import *
from src.com.stock.analysis.analysis3 import *
from src.com.stock.analysis.analysis4 import *
from src.com.stock.analysis.analysis5 import *
from src.com.stock.analysis.graph import *
from src.com.stock.analysis.real_TR_SCHART import *
from src.com.stock.analysis.real_checking import *
from src.com.stock.data.fix_data import *
TR_1206_len_counts = 0

myLogger = logging.getLogger("myLogger")
OpenStock = logging.getLogger("OpenStock")
TR_1206_logger = logging.getLogger("TR_1206")
simulation_1_logger = logging.getLogger("simulation_1")
upjong_code_mst_logger = logging.getLogger("upjong_code_mst")
Today_date = datetime.now()
Today_date = Today_date.strftime("%Y%m%d")
real_time_pk_dict = {
    "일자" : Today_date
}
mylogger_dict = {
    "OpenStock" : OpenStock,
    "myLogger" : myLogger,
    "TR_1206" : TR_1206_logger,
    "simulation_1" : simulation_1_logger,
    "upjong_code_mst" : upjong_code_mst_logger,
}


indiReal_dict = {}

path_to_tr_file = "C:\dev\OpenStock\src\com\stock\\tr_data\Indi_TR.xlsx"
DEFAILT_TR_DB_NAME ={
    "TR_1206" : "TR_1206",
    "stock_mst" : "stock_mst",
    "TR_1205" : "TR_1205",
    "TR_SCHART" : "TR_SCHART",
    "SK" : "SK",
    "SC" : "SC",
    "SP" : "SP",
    "SABA101U1" : "SABA101U1",
}

'''KOSPI_UPJONG_CODE={
"0001"	:"종합주가지수(KOSPI)",
"0002"	:"대형주",
"0003"	:"중형주",
"0004"	:"소형주",
"0005"	:"음식료품",
"0006"	:"섬유,의복",
"0007"	:"종이,목재",
"0008"	:"화학",
"0009"	: "의약품",
"0010"	:"비금속광물",
"0011"	:"철강및금속",
"0012"	:"기계",
"0013"	:"전기,전자",
"0014"	:"의료정밀",
"0015"	:"운수장비",
"0016"	:"유통업",
"0017"	:"전기가스업",
"0018"	:"건설업",
"0019"	:"운수창고",
"0020"	:"통신업",
"0021"	:"금융업",
"0022"	:"은행",
"0024"	:"증권",
"0025"	:"보험",
"0026"	:"서비스업",
"0027"	:"제조업"
}

KOSDAQ_UPJONG_CODE = {
"1001" :	"종합지수               " ,
"1002" :	"KOSDAQ 100             " ,
"1003" :	"KOSDAQ MID 300         " ,
"1004" :	"KOSDAQ SMALL           " ,
"1012" :	"기타서비스             " ,
"1015" :	"KOSDAQIT종합           " ,
"1024" :	"제조                   " ,
"1026" :	"건설                   " ,
"1027" :	"유통                   " ,
"1029" :	"운송                   " ,
"1031" :	"금융                   " ,
"1037" :	"오락문화               " ,
"1041" :	"통신방송서비스         " ,
"1042" :	"IT S/W & SVC           " ,
"1043" :	"IT H/W                 " ,
"1056" :	"음식료,담배            " ,
"1058" :	"섬유,의류              " ,
"1062" :	"종이,목재              " ,
"1063" :	"출판,매체복제          " ,
"1065" :	"화학                   " ,
"1066" :	"제약                   " ,
"1067" :	"비금속                 " ,
"1068" :	"금속                   " ,
"1070" :	"기계,장비              " ,
"1072" :	"일반전기전자           " ,
"1074" :	"의료,정밀기기          " ,
"1075" :	"운송장비,부품          " ,
"1077" :	"기타 제조              " ,
"1151" :	"통신서비스             " ,
"1152" :	"방송서비스             " ,
"1153" :	"인터넷                 " ,
"1154" :	"디지털컨텐츠           " ,
"1155" :	"소프트웨어             " ,
"1156" :	"컴퓨터서비스           " ,
"1157" :	"통신장비               " ,
"1158" :	"정보기기               " ,
"1159" :	"반도체                 " ,
"1160" :	"IT부품                 " ,
"1181" :	"코스닥 우량기업        " ,
"1182" :	"코스닥 벤처기업        " ,
"1183" :	"코스닥 중견기업        " ,
"1184" :	"코스닥 신성장기업      " ,
"1202" :	"KOSDAQ 프리미어지수    "
}

KOSPI_UPJONG_EX_CODE = {
"2101" :	"KOSPI200 종합              " ,
"2121" :	"KOSPI200 레버리지 지수     " ,
"2123" :	"F-KOSPI200 지수            " ,
"2124" :	"F-KOSPI200 인버스 지수     " ,
"2151" :	"K200 건설기계              " ,
"2152" :	"K200 조선운송              " ,
"2153" :	"K200 철강소재              " ,
"2154" :	"K200 에너지화학            " ,
"2155" :	"K200 정보통신              " ,
"2156" :	"K200 금융                  " ,
"2157" :	"K200 필수소비재            " ,
"2158" :	"K200 자유소비재            " ,
"2201" :	"KOSPI 100                  " ,
"2202" :	"KOSPI 50                   " ,
"2300" :	"정보통신지수               " ,
"2400" :	"KODI                       " ,
"2401" :	"K200 동일가중지수          " ,
"2402" :	"K100 동일가중지수          " ,
"2403" :	"K50 동일가중지수           " ,
"2500" :	"KOGI                       " ,
"2501" :	"사회책임투자지수           " ,
"2502" :	"환경책임투자지수           " ,
"2503" :	"녹색환경투자지수           " ,

}'''