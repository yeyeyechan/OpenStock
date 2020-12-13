
# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\OpenStock")
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari



def send_telegram(text):
    telgm_token = '1013576743:AAFkCdmafOY61N-I1FAEIEsOdFZwR47_ZQ8'
    bot = telegram.Bot(token=telgm_token)
    bot.sendMessage(chat_id='813531834', text=text)

