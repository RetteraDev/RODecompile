#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/newServiceFirstKillProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import time
import utils
import clientUtils
import const
import commNewServerActivity
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis import uiUtils
from asObject import MenuManager
from data import mail_template_data as MTD
from data import new_server_activity_data as NSAD
FBNO_MUDENG = 1008
FBNO_JIXIEBOSHI = 1504
FIRST_KILL_REWARD = {FBNO_MUDENG: 2574,
 FBNO_JIXIEBOSHI: 2575}
TEAM_MEMBER_MAX_NUM = 10

class NewServiceFirstKillProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NewServiceFirstKillProxy, self).__init__(uiAdapter)
        self.widget = None
        self.firstKillData = {}
        self.addEvent(events.EVENT_NEW_SERVICE_FIRST_KILL, self.onFirstKillDataChanged, isGlobal=True)

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def unRegisterPanel(self):
        self.widget = None

    def clearCache(self):
        self.firstKillData = {}

    def initUI(self):
        p = BigWorld.player()
        p.base.queryNSFirstKillData()

    def refreshInfo(self):
        if not self.widget:
            return
        fbNos = NSAD.data.get('firstKillFubens', ())
        if len(fbNos) == 2:
            fbNo1 = fbNos[0]
            fbNo2 = fbNos[1]
        else:
            fbNo1 = FBNO_MUDENG
            fbNo2 = FBNO_JIXIEBOSHI
        mailId1 = NSAD.data.get('firstKillRewards', {}).get(1, FIRST_KILL_REWARD[FBNO_MUDENG])
        fbDataMudeng = self.firstKillData.get('data', {}).get(fbNo1, ())
        self._setFubenData(fbDataMudeng, mailId1, self.widget.main.reward1, self.widget.main.team1)
        mailId2 = NSAD.data.get('firstKillRewards', {}).get(2, FIRST_KILL_REWARD[FBNO_JIXIEBOSHI])
        fbDataJixie = self.firstKillData.get('data', {}).get(fbNo2, ())
        self._setFubenData(fbDataJixie, mailId2, self.widget.main.reward2, self.widget.main.team2)

    def _setFubenData(self, fbData, mailId, rewardMc, teamMc):
        if fbData:
            leftTimeStr = self._getLeftTimeStr(fbData[0])
            captainGbid = fbData[1]
            members = fbData[2]
        else:
            leftTimeStr = self._getLeftTimeStr(0)
            captainGbid = 0
            members = ()
        bonusId = MTD.data.get(mailId, {}).get('bonusId', 0)
        bonusList = clientUtils.genItemBonus(bonusId)
        if len(bonusList) > 0:
            itemId, itemCount = bonusList[0]
            itemData = uiUtils.getGfxItemById(itemId, itemCount)
        else:
            itemData = None
        rewardMc.leftTime.text = leftTimeStr
        rewardMc.icon.setItemSlotData(itemData)
        rewardMc.icon.dragable = False
        teamMc.nobody.visible = len(members) == 0
        for i in range(TEAM_MEMBER_MAX_NUM):
            child = teamMc.getChildByName('player%d' % (i + 1))
            if i < len(members):
                gbId = members[i][0]
                roleName = members[i][1]
                isCaptain = gbId == captainGbid
                child.visible = True
                child.roleName.text = roleName
                child.captain.visible = isCaptain
                MenuManager.getInstance().registerMenuById(child, uiConst.MENU_ENTITY, {'roleName': roleName,
                 'gbId': gbId})
            else:
                child.visible = False

    def onFirstKillDataChanged(self, event):
        self.firstKillData = event.data
        self.refreshInfo()

    def _getLeftTimeStr(self, killTime):
        if killTime > 0:
            return gameStrings.NEW_SERVICE_FIRST_KILL_KILL_TIME % utils.formatDatetime(killTime)
        else:
            leftDay = NSAD.data.get('firstKillActivityOpenDay', 60) - utils.getServerOpenDays()
            if leftDay < 0:
                return ''
            return gameStrings.NEW_SERVICE_FIRST_KILL_LEFT_TIME % leftDay

    def canOpenTab(self):
        ret = True
        ret &= commNewServerActivity.isNewServerActivityOpen(const.NEW_SERVICE_FIRST_KILL)
        ret &= commNewServerActivity.checkNSFirstKillInDisplayTime(self.firstKillData.get('data', {}))
        return ret

    def makeFakeData(self):
        import random
        self.firstKillData = {'data': {FBNO_MUDENG: (random.random() * 10000, 0, [(55555L, 'aaa'), (66666, 'bbb')]),
                  FBNO_JIXIEBOSHI: (random.random() * 10000, 0, [(55555, 'ccc')])}}
        self.refreshInfo()
