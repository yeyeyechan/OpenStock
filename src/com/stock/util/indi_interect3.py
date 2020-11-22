from src.com.stock.common.import_lib import *




class EvtHandler:
    def ReceiveSysMsg(self, nResult):
        print("EvtHandler.EventLogin: nResult=%s" % nResult)
    def ReceiveSysMsg(self, nResult):
        print("EvtHandler.EventConnect: nResult=%s" % nResult)

class tr_object3(Thread):
    def __init__(self ):
        try:
            self.co = com.DispatchWithEvents("GIEXPERTCONTROL.GiExpertControlCtrl.1", EvtHandler)
        except Exception as e:
            raise RuntimeError('Cannot open PCBiz Active-X: %s' % str(e))

        self.login = self.co.StartIndi('xamevh123', 'florida1!23', 'florida1!23',
                                           'C:\SHINHAN-i\indi\giexpertstarter.exe')


if __name__ == "__main__":
    test = tr_object3()