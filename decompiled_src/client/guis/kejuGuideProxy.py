#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/kejuGuideProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import const
from guis import uiConst
from guis import uiUtils
from uiProxy import UIProxy
from data import keju_data as KD
from data import npc_puzzle_data as NPD

class KejuGuideProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(KejuGuideProxy, self).__init__(uiAdapter)
        self.modelMap = {'getGuideInfo': self.onGetGuideInfo,
         'closeGuide': self.onCloseGuide,
         'flyTo': self.onFlyTo,
         'autoFindTo': self.onAutoFindTo}
        self.guideWidgetId = uiConst.WIDGET_KEJU_GUIDE
        self.reset()

    def reset(self):
        self.kejuType = None
        self.kejuId = None
        self.mediator = None
        self.npcId = 0

    def _registerMediator(self, widgetId, mediator):
        if widgetId == self.guideWidgetId:
            self.mediator = mediator

    def show(self):
        self.hidePush()
        if not gameglobal.rds.configData.get('enableKeju', False):
            return
        kejuInfo = BigWorld.player().kejuInfo
        if not kejuInfo:
            return
        self.kejuId = BigWorld.player().kejuInfo.get('kejuId', 0)
        gameglobal.rds.ui.loadWidget(self.guideWidgetId)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(self.guideWidgetId)
        self.mediator = None
        self.addKejuPush()

    def checkKejuState(self):
        kejuInfo = BigWorld.player().kejuInfo
        if not kejuInfo:
            return
        self.addKejuPush()

    def refreshGuideInfo(self):
        if self.mediator:
            self.mediator.Invoke('refreshGuideInfo')

    def getNpcId(self):
        kejuInfo = BigWorld.player().kejuInfo
        if not kejuInfo:
            return
        cnt = -1
        for puzzleCnt in kejuInfo['puzzleIds'].keys():
            if kejuInfo.get('puzzleIds', {}).get(puzzleCnt, {}).get('result', -1) == const.PUZZLE_EMPTY:
                cnt = puzzleCnt
                break

        if cnt == -1:
            return
        puzzleRate = KD.data.get(self.kejuId).get('puzzleRate', [])
        npcIndex = 0
        for index, rate in enumerate(puzzleRate):
            if cnt < 0:
                npcIndex = index
                break
            cnt -= rate

        return KD.data.get(self.kejuId, {}).get('npcList', [])[npcIndex - 1]

    def addKejuPush(self):
        kejuInfo = BigWorld.player().kejuInfo
        if not kejuInfo:
            return
        if not gameglobal.rds.configData.get('enableKeju', False):
            return
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_KEJU_GUIDE)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_KEJU_GUIDE, {'click': self.kejuPushClick})

    def hidePush(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_KEJU_GUIDE)

    def kejuPushClick(self):
        self.show()

    def onGetGuideInfo(self, *arg):
        self.npcId = self.getNpcId()
        if not self.npcId:
            self.clearWidget()
            self.hidePush()
            return
        ret = {}
        kejuData = KD.data.get(self.kejuId, {})
        ret['title'] = kejuData.get('title', gameStrings.TEXT_KEJUGUIDEPROXY_112)
        ret['duration'] = kejuData.get('duration', gameStrings.TEXT_KEJUGUIDEPROXY_113)
        ret['tips'] = kejuData.get('tips', gameStrings.TEXT_KEJUGUIDEPROXY_114)
        ret['text'] = kejuData.get('text', gameStrings.TEXT_KEJUGUIDEPROXY_115)
        npcData = NPD.data.get(self.npcId, {})
        ret['stage'] = npcData.get('stage', '')
        ret['npcName'] = uiUtils.getNpcName(self.npcId)
        ret['canFly'] = npcData.get('canFly', 0)
        ret['trackId'] = npcData.get('trackId', 110750004)
        return uiUtils.dict2GfxDict(ret, True)

    def onCloseGuide(self, *arg):
        self.clearWidget()

    def onFlyTo(self, *arg):
        seekId = int(arg[3][0].GetNumber())
        uiUtils.gotoTrack(seekId)
        gameglobal.rds.uiLog.addFlyLog(seekId)

    def onAutoFindTo(self, *arg):
        seekId = arg[3][0].GetString()
        uiUtils.findPosById(seekId)
        gameglobal.rds.uiLog.addPathLog(seekId)
