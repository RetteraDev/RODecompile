#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/clanChallengeObListProxy.o
import BigWorld
import const
from guis.asObject import ASObject
from guis.asObject import TipManager
import uiConst
import events
import utils
from gamestrings import gameStrings
from uiProxy import UIProxy
from data import clan_war_fort_data as CWFD
from data import clan_war_challenge_config_data as CWCCD
from data import region_server_config_data as RSCD
MEMBER_MAX_CNT = 5

class ClanChallengeObListProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ClanChallengeObListProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CLAN_CHALLENGE_OB_LIST, self.hide)

    def reset(self):
        self.infoList = []

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CLAN_CHALLENGE_OB_LIST:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CLAN_CHALLENGE_OB_LIST)

    def show(self):
        BigWorld.player().cell.queryClanWarChallengeOberveInfo()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CLAN_CHALLENGE_OB_LIST)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.eventList.itemRenderer = 'ClanChallengeObList_ItemRender'
        self.widget.eventList.labelFunction = self.labelFunction
        self.widget.eventList.itemHeight = 86

    def getInfoList(self):
        infoList = []
        p = BigWorld.player()
        for fortData in getattr(p, 'clanChallengeObData', []):
            fortId, defNuid, defName, defMember, defLayout, atkNuid, atkName, atkMember, atkLayout, hostId, winSide = fortData
            fortName = CWFD.data.get(fortId, {}).get('showName', '')
            if hostId != p.getOriginHostId():
                fortName += '-' + utils.getServerName(hostId)
            info = {}
            info['fortId'] = fortId
            info['fortName'] = fortName
            info['defGuildName'] = defName
            info['showResult'] = bool(winSide)
            info['defWin'] = winSide == defNuid
            defJobList = []
            for memberGbId in defLayout:
                if not memberGbId:
                    continue
                name, icon, school, sex, borderId = defMember.get(memberGbId, [0] * 4)
                defJobList.append((school, name))

            info['defJobList'] = defJobList
            info['atkGuildName'] = atkName
            atkJobList = []
            for memberGbId in atkLayout:
                if not memberGbId:
                    continue
                name, icon, school, sex, borderId = atkMember.get(memberGbId, [0] * 4)
                atkJobList.append((school, name))

            info['atkJobList'] = atkJobList
            info['hostId'] = hostId
            infoList.append(info)

        return infoList

    def refreshInfo(self):
        if not self.widget:
            return
        self.infoList = self.getInfoList()
        self.widget.eventList.dataArray = range(len(self.infoList))

    def labelFunction(self, *args):
        dataIdx = int(args[3][0].GetNumber())
        info = self.infoList[dataIdx] if dataIdx < len(self.infoList) else {}
        if not info:
            return
        itemMc = ASObject(args[3][1])
        itemMc.dataIdx = dataIdx
        itemMc.txtClanName.text = info['fortName']
        itemMc.defGuildName.text = info['defGuildName']
        itemMc.atkGuildName.text = info['atkGuildName']
        itemMc.fortId = info['fortId']
        defJobList = info['defJobList']
        atkJobList = info['atkJobList']
        for i in xrange(MEMBER_MAX_CNT):
            defJobMc = itemMc.getChildByName('defJob%d' % i)
            if i < len(defJobList):
                defJobMc.visible = True
                school, name = defJobList[i]
                defJobMc.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(school, 'yuxu'))
                TipManager.addTip(defJobMc, name)
            else:
                defJobMc.visible = False
            atkJobMc = itemMc.getChildByName('atkJob%d' % i)
            if i < len(atkJobList):
                atkJobMc.visible = True
                school, name = atkJobList[i]
                atkJobMc.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(school, 'yuxu'))
                TipManager.addTip(atkJobMc, name)
            else:
                atkJobMc.visible = False

        if info['showResult']:
            defWin = info['defWin']
            itemMc.defResult.visible = True
            itemMc.atkResult.visible = True
            itemMc.defResult.gotoAndStop('win' if defWin else 'lost')
            itemMc.atkResult.gotoAndStop('lost' if defWin else 'win')
        else:
            itemMc.defResult.visible = False
            itemMc.atkResult.visible = False
        itemMc.obBtn.addEventListener(events.BUTTON_CLICK, self.handleObBtnClick, False, 0, True)
        itemMc.hostId = info['hostId']
        itemMc.shareBtn.addEventListener(events.BUTTON_CLICK, self.handleShareBtnClick, False, 0, True)

    def handleObBtnClick(self, *args):
        e = ASObject(args[3][0])
        fortId = int(e.currentTarget.parent.fortId)
        if not fortId:
            return
        hostId = int(e.currentTarget.parent.hostId)
        BigWorld.player().cell.startObserveClanWarChallenge(fortId, hostId)

    def handleShareBtnClick(self, *args):
        e = ASObject(args[3][0])
        dataIdx = int(e.currentTarget.parent.dataIdx)
        if dataIdx >= len(self.infoList):
            return
        info = self.infoList[dataIdx]
        hostId = int(e.currentTarget.parent.hostId)
        msg = CWCCD.data.get('clanChallengeOb', gameStrings.CLAN_CHALLENGE_OB) % (info['atkGuildName'],
         info['defGuildName'],
         info['fortName'],
         info['fortId'],
         hostId)
        self.uiAdapter.chat.setChatText(msg)
