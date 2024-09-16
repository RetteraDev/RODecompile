#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fightForLoveRankListProxy.o
import BigWorld
import gameglobal
import uiConst
import gamelog
import events
import gametypes
import copy
from uiProxy import UIProxy
from asObject import ASObject
from guis.asObject import MenuManager
from data import fight_for_love_config_data as FFLCD
from gamestrings import gameStrings
PLAYER_NUM = 4
TIP_NUM = 3

class FightForLoveRankListProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FightForLoveRankListProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_FIGHT_FOR_LOVE_RANK_LIST, self.hide)

    def reset(self):
        self.info = []
        self.createrGbId = 0
        self.memberInfo = []
        self.myInfo = ()
        self.createrName = ''
        self.phase = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FIGHT_FOR_LOVE_RANK_LIST:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FIGHT_FOR_LOVE_RANK_LIST)
        if BigWorld.player():
            BigWorld.player().unlockTarget()

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FIGHT_FOR_LOVE_RANK_LIST)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        for i in xrange(PLAYER_NUM):
            item = self.widget.getChildByName('player%d' % i)
            item.visible = False

        FFLRankListTips = FFLCD.data.get('FFLRankListTips', {})
        if FFLRankListTips:
            for idx in xrange(TIP_NUM):
                item = self.widget.getChildByName('tip%d' % idx)
                item.text = FFLRankListTips.get(idx, '')

    def setScoreInfo(self, info):
        self.info = info
        playersGbIdList = [ x[0] for x in info ]
        if self.memberInfo:
            newMemberInfo = [ x for x in self.memberInfo if x[0] in playersGbIdList ]
            for memberInfo in newMemberInfo:
                for gbId, score in self.info:
                    if gbId == memberInfo[0]:
                        memberInfo[4] = score

                if memberInfo[0] == BigWorld.player().gbId:
                    self.myInfo = memberInfo

            self.memberInfo = newMemberInfo
        self.refreshInfo()

    def setMemberInfo(self, createrGbId, createrName, memberInfo):
        self.createrGbId = createrGbId
        self.createrName = createrName
        for info in memberInfo:
            for existInfo in self.memberInfo:
                if info[0] == existInfo[0]:
                    self.memberInfo.remove(existInfo)

            self.memberInfo.append(list(info))
            if info[0] == BigWorld.player().gbId:
                self.myInfo = info

        self.refreshInfo()

    def setPhase(self, phase):
        self.phase = phase

    def refreshInfo(self):
        if not self.widget:
            return
        if self.createrName and self.createrGbId:
            self.widget.createrIcon.visible = True
            self.widget.createrTip.visible = True
            self.widget.createrTip.txt.htmlText = gameStrings.FIGHT_FOR_LOVE_CREATER_NAME_TIP % self.createrName
            self.widget.createrTip.gbId = self.createrGbId
            menuParam = {'roleName': self.createrName,
             'gbId': self.createrGbId}
            MenuManager.getInstance().registerMenuById(self.widget.createrTip, uiConst.MENU_CHAT, menuParam)
            self.widget.createrTip.addEventListener(events.MOUSE_CLICK, self.handleItemClick, False, 0, True)
        else:
            self.widget.createrIcon.visible = False
            self.widget.createrTip.visible = False
        self.memberInfo = sorted(self.memberInfo, cmp=self.sortRank, reverse=True)
        if self.phase == gametypes.FIGHT_FOR_LOVE_PHASE_PREPARE:
            return
        if not self.memberInfo:
            return
        for i in xrange(PLAYER_NUM):
            item = self.widget.getChildByName('player%d' % i)
            item.visible = False

        for index in xrange(min(len(self.memberInfo), 3)):
            player = self.memberInfo[index]
            item = self.widget.getChildByName('player%d' % index)
            item.gbId = player[0]
            item.playerName.text = player[1]
            item.score.text = player[4]
            item.icon.gotoAndStop('no%d' % index)
            item.visible = True
            menuParam = {'roleName': player[1],
             'gbId': player[0]}
            MenuManager.getInstance().registerMenuById(item, uiConst.MENU_CHAT, menuParam)
            item.addEventListener(events.MOUSE_CLICK, self.handleItemClick, False, 0, True)

        if self.myInfo:
            myIndex = self.memberInfo.index(list(self.myInfo))
            myItem = self.widget.player3
            myItem.gbId = player[0]
            myItem.playerName.text = self.myInfo[1]
            myItem.score.text = self.myInfo[4]
            myItem.order.text = myIndex + 1
            myItem.visible = True
            menuParam = {'roleName': self.myInfo[1],
             'gbId': self.myInfo[0]}
            MenuManager.getInstance().registerMenuById(myItem, uiConst.MENU_CHAT, menuParam)
            myItem.addEventListener(events.MOUSE_CLICK, self.handleItemClick, False, 0, True)

    def sortRank(self, a, b):
        if a[4] > b[4]:
            return 1
        if a[4] == b[4]:
            if a[3] < b[3]:
                return 1
            if a[3] == b[3]:
                if a[0] < b[0]:
                    return 1
        return -1

    def initFFLScore(self):
        for e in BigWorld.entities.values():
            if not getattr(e, 'IsAvatar', False):
                continue
            if hasattr(e, 'gbId'):
                e.topLogo.setFFLScore(100)

    def removeFFLScore(self):
        for e in BigWorld.entities.values():
            if getattr(e, 'topLogo'):
                e.topLogo.removeFFLScore()

    def handleItemClick(self, *args):
        targetGbId = ASObject(args[3][0]).currentTarget.gbId
        p = BigWorld.player()
        for e in BigWorld.entities.values():
            if not getattr(e, 'IsAvatar', False):
                continue
            if hasattr(e, 'gbId') and e.gbId == long(targetGbId):
                p.lockTarget(e)
