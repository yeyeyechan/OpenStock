
# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\OpenStock")
from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari



def check_time(real_time , check_time):
    real_time = int(real_time)

    check_time = int(check_time)
    check_time = check_time * 10000

    if real_time <= check_time:
        return True
    else:
        return False