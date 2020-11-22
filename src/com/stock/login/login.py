# -*- coding: utf-8 -*-
import sys
print(sys.path)
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import qApp
from src.com.common.my_logger import mylogger
class login(QMainWindow):
    def __init__(self):
        super().__init__()
        # 일반 TR OCX
        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.login = ""
        # 신한i Indi 자동로그인
        while True:
            self.login = self.IndiTR.StartIndi('xamevh123', 'florida1!23', 'florida1!23', 'C:\SHINHAN-i\indi\giexpertstarter.exe')
            if self.login == True :
                mylogger.info("login success")
                break
        if self.login == True:
            mylogger.info("login success")
            return
        mylogger.info("login failed")
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_variable = login()
    mylogger.info("login program exit")