#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/LZYDResultProxy.o
import BigWorld
import events
import formula
import gameglobal
import uiConst
import const
import gamelog
import uiUtils
from asObject import ASUtils
from uiProxy import UIProxy
from guis.asObject import ASObject
from gamestrings import gameStrings
from data import school_data as SD
ITEM_FLAG_SELF = 1
ITEM_FLAG_FRIEND = 2
ITEM_FLAG_ENEMY = 3
BG_MIN_ITEMCNT = 6
BG_MIN_H = 262
BG_MAX_H = 366
OFFSET = 5

class LZYDResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(LZYDResultProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_LZYD_RESULT, self.hide)

    def reset(self):
        self.info = None
        self.sortedArray = None
        self.myCampNum = -1

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_LZYD_RESULT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_LZYD_RESULT)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ARENA_FINAL_RESULT_BG)

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ARENA_FINAL_RESULT_BG)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_LZYD_RESULT)
        self.sortedArray = self.sortByName(BigWorld.player().arenaStatistics, uiConst.ARENA_SORT_BY_CAMP)
        self._doubleCheckForFinalResult()

    def _doubleCheckForFinalResult(self):
        tmpArray = []
        p = BigWorld.player()
        index = 0
        for item in self.sortedArray:
            if item['sideNUID'] == p.sideNUID:
                tmpArray.append(item)
                index += 1

        for item in self.sortedArray:
            if item not in tmpArray:
                tmpArray.append(item)

        self.sortedArray = tmpArray

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.addEventListener(events.BUTTON_CLICK, self.handleBtnClick, False, 0, True)
        self.widget.sortBtn.addEventListener(events.BUTTON_CLICK, self.handleSortBtnClick, False, 0, True)
        self.widget.quitBtn.addEventListener(events.BUTTON_CLICK, self.handleQuitBtnClick, False, 0, True)
        if self.widget.shareBtn:
            self.widget.shareBtn.addEventListener(events.BUTTON_CLICK, self.handleShareBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        self.info = self.getArenaResult()
        if self.info:
            leftCnt = 0
            itemInfo = self.info.get('itemInfo', {})
            for data in self.info.get('itemInfo', []):
                if data['itemFlag'] == ITEM_FLAG_SELF or data['itemFlag'] == ITEM_FLAG_FRIEND:
                    leftCnt += 1

            self.setMembers(itemInfo[0:leftCnt], 'leftMember')
            self.setMembers(itemInfo[leftCnt:len(itemInfo)], 'rightMember')
            self.widget.shareBtn.data = self.info.get('enableQrCode', '')
            self.widget.shareBtn.enabled = not self.widget.shareBtn.data

    def handleQuitBtnClick(self, *args):
        BigWorld.player().leaveArena()
        self.hide()

    def handleShareBtnClick(self, *args):
        if self.widget:
            qrInfo = gameglobal.rds.ui.qrCodeAppScanShare.createShareInfoInstance(dailyShare=True)
            gameglobal.rds.ui.qrCodeAppScanShare.show(qrInfo)

    def handleBtnClick(self, *args):
        e = ASObject(args[3][0])
        if not self.widget:
            return
        if e.target.parent == self.widget.campNum or e.target.parent == self.widget.killedNum or e.target.parent == self.widget.assistAtkNum or e.target.parent == self.widget.beKilledNum or e.target.parent == self.widget.cureNum or e.target.parent == self.widget.damageNum:
            self.handleArenaResultClick(e.target.parent.name)

    def handleVoteBtnClick(self, *args):
        p = BigWorld.player()
        if p.isUsingTemp():
            p.base.zanUsingCharTemp(long(p.charTempId))

    def setCloseBtnVisible(self, flag):
        self.widget.closeBtn.visible = flag

    def setJobIcon(self, jobIcon, jobId, isFriend = False):
        jobFrame = uiConst.SCHOOL_FRAME_DESC.get(jobId, '')
        jobFrameLan = jobFrame + 'lan'
        if jobFrame:
            if isFriend:
                jobIcon.job.gotoAndPlay(jobFrameLan)
            else:
                jobIcon.job.gotoAndPlay(jobFrame)
        elif isFriend:
            jobIcon.job.gotoAndPlay('shengtanglan')
        else:
            jobIcon.job.gotoAndPlay('shengtang')

    def setRoleName(self, mc, roleName):
        mc.roleName.textField.text = roleName

    def setBtnVisible(self, mc, flag):
        mc.killed.visible = flag
        mc.assistAtk.visible = flag
        mc.beKilled.visible = flag
        mc.cure.visible = flag
        mc.damage.visible = flag

    def setMembers(self, memberData, memberName, length = 5, isDiff = False):
        for i in xrange(len(memberData)):
            info = memberData[i]
            item = self.widget.getChildByName(memberName + str(i + 1))
            self.setJobIcon(item.member, info['school'])
            self.setRoleName(item.member, info['roleName'])
            item.killed.textField.text = str(info['killedNum'])
            item.assistAtk.textField.text = str(info['assistAtkNum'])
            item.beKilled.textField.text = str(info['beKilledNum'])
            item.cure.textField.text = str(info['cureNum'])
            item.damage.textField.text = str(info['damageNum'])
            if memberName == 'sortMember':
                item.visible = True
            else:
                self.setBtnVisible(item, True)

        for i in xrange(len(memberData), length):
            item = self.widget.getChildByName(memberName + str(i + 1))
            if memberName == 'sortMember':
                item.visible = False
            else:
                self.setBtnVisible(item, False)
                if item.member:
                    item.member.gotoAndPlay('empty')

    def getArenaResult(self):
        p = BigWorld.player()
        ret = {}
        ret['roleName'] = p.realRoleName
        ret['itemInfo'] = self._getItemInfo()
        ret['arenaFame'] = p.fame.get(const.JUN_ZI_FAME_ID, 0)
        ret['enableQrCode'] = gameglobal.rds.configData.get('enableQRCode', False)
        leftTeamName = ''
        rightTeamName = ''
        for item in self.sortedArray:
            if self._genItemFlag(item) == ITEM_FLAG_ENEMY:
                rightTeamName = item.get('fromHostName', '')
            else:
                leftTeamName = item.get('fromHostName', '')

        ret['leftTeamName'] = leftTeamName
        ret['rightTeamName'] = rightTeamName
        ret['winTeamName'] = gameStrings.ARENA_FINAL_RESULT_TITLE
        ret['isWin'] = getattr(p, 'arenaResult', const.LOSE) == const.WIN or getattr(p, 'arenaResult', const.LOSE) == const.WIN_QUIT_EARLY
        return ret

    def handleSortBtnClick(self, *args):
        self.widget.gotoAndPlay('stop')
        self.setMembers(self.info.get('itemInfo', []), 'sortMember', 10, True)
        ASUtils.callbackAtFrame(self.widget, 228, self.addQuitCallBack)

    def addQuitCallBack(self, *args):
        if self.widget.quitBtn:
            self.widget.quitBtn.addEventListener(events.BUTTON_CLICK, self.handleQuitBtnClick, False, 0, True)

    def refreshSortPanel(self):
        data = self._getItemInfo()
        self.widget.gotoAndPlay('sort')
        self.setMembers(data, 'sortMember', 10, True)
        ASUtils.callbackAtFrame(self.widget, 228, self.addQuitCallBack)

    def handleArenaResultClick(self, btnName):
        self.sortedArray = self.sortByName(BigWorld.player().arenaStatistics, btnName)
        self.refreshSortPanel()

    def sortByName(self, ar, attrName, myReverse = True):
        return sorted(ar, cmp=lambda x, y: cmp(x[attrName], y[attrName]), reverse=myReverse)

    def _genItemFlag(self, item):
        p = BigWorld.player()
        if item['id'] == p.id:
            return ITEM_FLAG_SELF
        elif getattr(p, 'sideNUID', 0) == item['sideNUID']:
            return ITEM_FLAG_FRIEND
        else:
            return ITEM_FLAG_ENEMY

    def _getItemInfo(self):
        p = BigWorld.player()
        ret = []
        if not self.sortedArray:
            return
        for item in self.sortedArray:
            if not p._checkValidSchool(item['school']):
                continue
            obj = {}
            obj['itemFlag'] = self._genItemFlag(item)
            if formula.isCrossServerLzyd(formula.getFubenNo(p.spaceNo)):
                newName = uiUtils.genDuelCrossName(item['roleName'], item.get('fromHostName', ''))
            else:
                newName = item['roleName']
            obj['roleName'] = newName
            obj['school'] = item['school']
            obj['campNum'] = item['campNum']
            obj['killedNum'] = item['killedNum']
            obj['assistAtkNum'] = item['assistAtkNum']
            obj['beKilledNum'] = item['beKilledNum']
            obj['cureNum'] = item['cureNum']
            obj['damageNum'] = item['damageNum']
            obj['gbId'] = str(item.get('gbId', 0))
            realRoleName = '%s-%s' % (item.get('roleName', ''), item.get('fromHostName', ''))
            obj['realRoleName'] = realRoleName
            ret.append(obj)

        return ret
