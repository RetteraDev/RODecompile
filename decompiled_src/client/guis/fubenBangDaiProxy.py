#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fubenBangDaiProxy.o
from gamestrings import gameStrings
import BigWorld
import uiConst
import gameglobal
import clientcom
from Scaleform import GfxValue
from ui import gbk2unicode
from uiProxy import UIProxy
from guis import uiUtils
from data import sys_config_data as SCD

class FubenBangDaiProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FubenBangDaiProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeBangDaiWidget': self.onCloseBangDaiWidget,
         'getSameMacTip': self.onGetSameMacTip}
        self.bangdaiData = []
        self.mediator = None
        self.isShow = False
        self.lastPlayerLenth = 0
        self.inBangDaiState = False

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FUBEN_BANGDAI:
            self.mediator = mediator
            return uiUtils.dict2GfxDict(self.getBangDaiInfo(), True)

    def getBangDaiInfo(self):
        ret = {}
        bangDaiPlayerList = []
        if self.bangdaiData:
            self.setPlayerBangDaiState()
            for data in self.bangdaiData:
                roleName = data.get('roleName', 'name')
                inFbHelp = data.get('inFbHelp', 0)
                if inFbHelp:
                    bangDaiPlayerList.append({'roleName': roleName,
                     'isSameMac': self.isSameMacBangDai(roleName)})

        if len(bangDaiPlayerList) == 0:
            ret = {'list': [],
             'label': True,
             'labelDesc': gameStrings.TEXT_FUBENBANGDAIPROXY_46}
        elif len(self.bangdaiData) == len(bangDaiPlayerList):
            ret = {'list': [],
             'label': True,
             'labelDesc': gameStrings.TEXT_FUBENBANGDAIPROXY_48}
        else:
            ret = {'list': bangDaiPlayerList,
             'label': False,
             'labelDesc': ''}
        self.isShowWidget(bangDaiPlayerList)
        return ret

    def isSameMacBangDai(self, roleName):
        if not self.inBangDaiState:
            return False
        else:
            p = BigWorld.player()
            team = p._getSortedMembers()
            if not team:
                return False
            targetMac = None
            for key, value in team:
                if value.get('roleName', '') == roleName:
                    targetMac = value['macAddress']

            beBangDaiMacs = []
            beBangDaiNames = []
            for data in self.bangdaiData:
                inFbHelp = data.get('inFbHelp', 0)
                if not inFbHelp:
                    beBangDaiNames.append(data.get('roleName', 'name'))

            for key, value in team:
                if value.get('roleName', '') in beBangDaiNames:
                    beBangDaiMacs.append(value['macAddress'])

            for mac in beBangDaiMacs:
                if mac != targetMac:
                    return False

            return True

    def setBangdaiData(self, infoList):
        self.bangdaiData = infoList
        self.setPlayerBangDaiState()

    def setPlayerBangDaiState(self):
        self.inBangDaiState = False
        p = BigWorld.player()
        for data in self.bangdaiData:
            roleName = data.get('roleName', 'name')
            inFbHelp = data.get('inFbHelp', 0)
            if inFbHelp:
                if p.roleName == roleName:
                    self.inBangDaiState = True

    def isShowWidget(self, bangDaiPlayerList):
        if len(bangDaiPlayerList) >= 1 and self.lastPlayerLenth == 0:
            self.isShow = True
        else:
            self.isShow = False
        self.lastPlayerLenth = len(bangDaiPlayerList)

    def onCloseBangDaiWidget(self, *arg):
        self.clearWidget()

    def reset(self):
        self.bangdaiData = []
        self.mediator = None
        self.isShow = False
        self.lastPlayerLenth = 0

    def autoShow(self):
        if self.isShow:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_BANGDAI)

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_BANGDAI)

    def clearWidget(self):
        self.inBangDaiState = False
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FUBEN_BANGDAI)

    def refreshInfo(self):
        info = self.getBangDaiInfo()
        if self.mediator:
            self.mediator.Invoke('refreshView', uiUtils.dict2GfxDict(info, True))
        else:
            self.autoShow()

    def onGetSameMacTip(self, *args):
        return GfxValue(gbk2unicode(SCD.data.get('bangDaiSameMacTip', '')))
