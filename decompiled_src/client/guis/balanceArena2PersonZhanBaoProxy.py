#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/balanceArena2PersonZhanBaoProxy.o
import time
import BigWorld
import gameglobal
import uiConst
import utils
from guis import uiUtils
from uiProxy import UIProxy
from gamestrings import gameStrings
from cdata import game_msg_def_data as GMDD
from data import duel_config_data as DCD
from doubleArenaTeamVal import DoubleArenaSpecialFight

class BalanceArena2PersonZhanBaoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BalanceArena2PersonZhanBaoProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.cache = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_BALANCE_ARENA_2PERSON_ZHANBAO, self.hide)

    def reset(self):
        pass

    def onGetServerData(self, data):
        self.cache = []
        for itemData in data:
            self.cache.append(DoubleArenaSpecialFight().fromDTO(itemData))

        self.refreshInfo()

    def generateTestInfo(self):
        currTime = utils.getNow()
        testData = type('Zhanbao', (object,), {'msgId': 51618,
         'winTeam': 'ddd',
         'loseTeam': 'ddd2',
         'val': 5,
         'timeStamp': currTime,
         'camp': 3})
        self.onGetServerData([testData, testData])

    def generateInfo(self):
        infoList = self.cache
        retLines = ''
        zhenyingInfos = DCD.data.get('doubleArenaZhenYingInfo', {})
        if infoList:
            for info in infoList:
                timeInfo = info.timeStamp
                timeTuple = utils.getTimeTuple(timeInfo)
                timeStr = time.strftime("<font color = \'#D7D7D7\'>%Y.%m.%d %H:%M</font>", timeTuple)
                msgId = info.msgId
                msg = uiUtils.getTextFromGMD(msgId)
                if msg:
                    num = msg.count('%')
                    detailInfo = ''
                    if msgId == GMDD.data.MSG_51619:
                        detailInfo = msg % (info.winTeam, str(info.val))
                    elif msgId == GMDD.data.MSG_51620:
                        detailInfo = msg % (info.winTeam, info.loseTeam, str(info.val))
                    elif msgId == GMDD.data.MSG_51621:
                        detailInfo = msg % (info.winTeam, zhenyingInfos.get(info.camp, {}).get('name', ''), str(info.val))
                    else:
                        detailInfo = msg % (info.winTeam, info.loseTeam, str(info.val))
                    infoLine = '%s %s\n' % (timeStr, detailInfo)
                    retLines = '%s%s' % (retLines, infoLine)

        if not retLines:
            retLines = DCD.data.get('doubleArenaZhanBaoDefault', gameStrings.DOUBLE_ARENA_NO_ZHANBAO)
        return retLines

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BALANCE_ARENA_2PERSON_ZHANBAO:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BALANCE_ARENA_2PERSON_ZHANBAO)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BALANCE_ARENA_2PERSON_ZHANBAO)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        p = BigWorld.player()
        p.base.dArenaQuerySpFight()

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.infoArea.canvas.textField.htmlText = self.generateInfo()
