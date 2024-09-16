#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bfDotaDetailProxy.o
import BigWorld
from gamestrings import gameStrings
import const
import gameglobal
from uiProxy import UIProxy
from guis import uiUtils
from guis import uiConst
from guis import events
from guis import ui
from guis.bfDotaKillProxy import MAX_ACCMULAT_CNT, MAX_COMBO_KILL_CNT
from guis.asObject import TipManager
from guis.asObject import ASUtils
from data import duel_config_data as DCD
from cdata import game_msg_def_data as GMDD
TEAM_MATE_MAX_CNT = 5
MAX_ITEM_CNT = 6
BF_DOTA_SELF_DATA_CNT = 6
RANK_JIN = 'jin'
RANK_YIN = 'yin'
RANK_TONG = 'tong'
SIDE_LEFT = 'left'
SIDE_RIGHT = 'right'
RANK_MAP = {1: RANK_JIN,
 2: RANK_YIN,
 3: RANK_TONG}

class BfDotaDetailProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BfDotaDetailProxy, self).__init__(uiAdapter)
        self.widget = None
        self.allPlayerCash = {}
        self.reset()

    def reset(self):
        self.visible = False

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BF_DOTA_DETAIL:
            self.widget = widget
            self.initUI()
            self.doRefreshInfo()
            self.widget.visible = self.visible

    def getFrameInfo(self):
        p = BigWorld.player()
        mySideInfo = {}
        mySideInfo['headNum'] = p.getBfOwnStas(const.BF_DOTA_OWN_STATS_MYSIDE_KILL_TYPE)
        enemySideInfo = {}
        enemySideInfo['headNum'] = p.getBfOwnStas(const.BF_DOTA_OWN_STATS_OTHERSIDE_KILL_TYPE)
        mySideInfo['playerList'] = []
        enemySideInfo['playerList'] = []
        for bfMemInfo in p.bfMemPerforms:
            gbId = bfMemInfo['gbId']
            memItem = p.getMemInfoByGbId(bfMemInfo['gbId'])
            if not memItem:
                continue
            sideInfo = mySideInfo if memItem['sideNUID'] == p.bfSideNUID else enemySideInfo
            playerInfo = {}
            isSelf = gbId == p.gbId
            playerInfo['isSelf'] = isSelf
            playerInfo['zaijuId'] = p.bfDotaZaijuRecord.get(gbId, 0)
            newName = memItem['roleName']
            playerInfo['name'] = newName
            playerInfo['lv'] = p.getPlayerDotaLv(gbId)
            playerInfo['kill'] = bfMemInfo.get(const.BF_COMMON_KILL_NUM, 0) if not isSelf else p.getBfOwnStas(const.BF_DOTA_OWN_STATS_KILL_TYPE)
            playerInfo['death'] = bfMemInfo.get(const.BF_COMMON_DEATH_NUM, 0) if not isSelf else p.getBfOwnStas(const.BF_DOTA_OWN_STATS_DIE_TYPE)
            playerInfo['assist'] = bfMemInfo.get(const.BF_COMMON_ASSIST_NUM, 0) if not isSelf else p.getBfOwnStas(const.BF_DOTA_OWN_STATS_ASSIST_TYPE)
            playerInfo['cash'] = getattr(p, 'bfDotaTotalCashDict', {}).get(gbId, 0)
            playerInfo['isMVP'] = gbId in getattr(p, 'bfResultInfo', {}).get('mvps', ())
            if memItem.get('fromHostName', '') or isSelf:
                playerInfo['canAddFriend'] = False
            else:
                playerInfo['canAddFriend'] = not p.friend.isFriend(gbId)
            playerInfo['gbId'] = gbId
            self.addAchievement(playerInfo, bfMemInfo)
            itemList = []
            for j in xrange(MAX_ITEM_CNT):
                if gbId == p.gbId:
                    item = p.battleFieldBag.get(j, None)
                else:
                    item = p.bfDotaOtherEquipInfo.get(gbId, {}).get(j, None)
                itemInfo = {}
                if item == None:
                    continue
                else:
                    itemInfo['id'] = item.id
                    itemInfo['cnt'] = item.cwrap
                itemList.append(itemInfo)

            playerInfo['itemList'] = itemList
            sideInfo['playerList'].append(playerInfo)

        selfInfo = []
        killValue, killRank = p.getBfDuelStatsInfo(p.gbId, const.BF_COMMON_KILL_NUM)
        selfInfo.append(('kill', killValue, RANK_MAP[killRank]))
        assistValue, assistRank = p.getBfDuelStatsInfo(p.gbId, const.BF_COMMON_ASSIST_NUM)
        selfInfo.append(('assist', assistValue, RANK_MAP[assistRank]))
        dmgTowerValue, dmgTowerRank = p.getBfDuelStatsInfo(p.gbId, const.BF_DOTA_DAMAGE_WITH_TOWER)
        selfInfo.append(('dmgTower', dmgTowerValue, RANK_MAP[dmgTowerRank]))
        dmgValue, dmgRank = p.getBfDuelStatsInfo(p.gbId, const.BF_DOTA_DAMAGE_TO_AVATR)
        selfInfo.append(('dmg', dmgValue, RANK_MAP[dmgRank]))
        beDmgValue, bfDmgRank = p.getBfDuelStatsInfo(p.gbId, const.BF_DOTA_BE_DAMAGE_FROM_AVATR)
        selfInfo.append(('beDmg', beDmgValue, RANK_MAP[bfDmgRank]))
        deathValue, deathRank = p.getBfDuelStatsInfo(p.gbId, const.BF_COMMON_DEATH_NUM)
        selfInfo.append(('', deathValue, RANK_MAP[deathRank]))
        mySideInfo['playerList'] = sorted(mySideInfo['playerList'], cmp=lambda x, y: cmp(x['name'], y['name']))
        enemySideInfo['playerList'] = sorted(enemySideInfo['playerList'], cmp=lambda x, y: cmp(x['name'], y['name']))
        return (selfInfo, mySideInfo, enemySideInfo)

    def addAchievement(self, playerInfo, memPerform):
        p = BigWorld.player()
        achievementList = []
        maxComboKill = memPerform.get(const.BF_DOTA_MAX_COMBO_KILL_IN_TIME, 0)
        maxAccumulateKill = memPerform.get(const.BF_DOTA_MAX_COMBO_KILL, 0)
        killCntList = DCD.data.get('bfDotaComboKill', {}).keys()
        killCntList.sort()
        for killCnt in killCntList:
            if killCnt <= maxComboKill:
                achievementList.append(DCD.data.get('bfDotaComboKill', {}).get(killCnt))

        if maxAccumulateKill >= MAX_ACCMULAT_CNT:
            showInfo = DCD.data.get('bfDotaMaxAccumulateKill', ())
            if showInfo:
                achievementList.append(showInfo)
        _, rankDmgAvatar = p.getBfDuelStatsInfo(playerInfo['gbId'], const.BF_DOTA_DAMAGE_TO_AVATR)
        if rankDmgAvatar == 1:
            showInfo = DCD.data.get('bfDotaMaxDmgAvatar', ())
            if showInfo:
                achievementList.append(showInfo)
        _, rankDmgTower = p.getBfDuelStatsInfo(playerInfo['gbId'], const.BF_DOTA_DAMAGE_WITH_TOWER)
        if rankDmgTower == 1:
            showInfo = DCD.data.get('bfDotaMaxDmgTower', ())
            if showInfo:
                achievementList.append(showInfo)
        _, rankBeDmg = p.getBfDuelStatsInfo(playerInfo['gbId'], const.BF_DOTA_BE_DAMAGE_FROM_AVATR)
        if rankBeDmg == 1:
            showInfo = DCD.data.get('bfDotaMaxBeDmg', ())
            if showInfo:
                achievementList.append(showInfo)
        playerInfo['achievemenList'] = achievementList

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BF_DOTA_DETAIL)

    def show(self):
        p = BigWorld.player()
        if getattr(p, 'backToBfEnd', False):
            p.showGameMsg(GMDD.data.BACK_TO_BF_END, ())
            return
        if getattr(p, 'isInBfDotaChooseHero', False):
            p.showGameMsg(GMDD.data.IN_CHOOSE_HERO, ())
            return
        if getattr(p, 'bfEnd', False):
            return
        self.setVisible(True)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BF_DOTA_DETAIL)
        else:
            self.doRefreshInfo()
        p.cell.queryAllBattleFieldDotaTotalCash()
        p.cell.queryOtherBagInfoInDotaBattleField(getattr(p, 'oldEquipVersion', 0))
        self.queryStaticsDetail()

    def queryStaticsDetail(self):
        p = BigWorld.player()
        gbIdList, bfFrequentVerList, bfStableVerList = p.resetBfMemFromTeamInfo()
        p.cell.queryBattleFieldDetails(gbIdList, bfFrequentVerList, bfStableVerList)

    def initUI(self):
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleCloseBtnClick, False, 0, True)

    def setVisible(self, value):
        self.visible = value
        if self.widget and self.widget.visible != value:
            gameglobal.isWidgetNeedShowCursor = self.uiAdapter.isWidgetNeedShowCursor()
            self.widget.visible = value
            if value:
                self.uiAdapter.showCursorForActionPhysics()
                self.uiAdapter.playOpenSoundById(uiConst.WIDGET_BF_DOTA_DETAIL)
            else:
                self.uiAdapter.hideCursorForActionPhysics()
                self.uiAdapter.playCloseSoundById(uiConst.WIDGET_BF_DOTA_DETAIL)

    @ui.callInCD(0.2)
    @ui.uiEvent(uiConst.WIDGET_BF_DOTA_DETAIL, (events.EVENT_BF_TEAMINFO_CHANGE, events.EVNET_BF_DUEL_STATE_CHAGNE))
    def refreshInfo(self, event = None):
        self.doRefreshInfo()

    def doRefreshInfo(self):
        if not self.widget or not self.widget.visible:
            return
        selfInfo, mySideInfo, enemySideInfo = self.getFrameInfo()
        self.updateSideInfo(SIDE_LEFT, mySideInfo)
        self.updateSideInfo(SIDE_RIGHT, enemySideInfo)
        startX = 38
        offsetX = 15
        for i in xrange(BF_DOTA_SELF_DATA_CNT):
            itemMc = self.widget.getChildByName('data%d' % i)
            itemMc.x = startX
            frameName, cnt, level = selfInfo[i]
            itemMc.icon.gotoAndStop(frameName)
            itemMc.icon.icon.gotoAndStop(level)
            itemMc.icon.visible = frameName != ''
            text = '%s %d' % (gameStrings.BF_DOTA_DETAIL_DATA_MAP[frameName], cnt)
            ASUtils.textFieldAutoSize(itemMc.txtNum, text)
            startX += 23
            startX += itemMc.txtNum.width + offsetX

    def updateSideInfo(self, side, sideInfo):
        self.updateHeadNum(side, sideInfo['headNum'])
        sideMc = self.widget.getChildByName(side)
        playerList = sideInfo['playerList']
        for index in xrange(TEAM_MATE_MAX_CNT):
            playerMc = sideMc.getChildByName('player%d' % index).player
            if index >= len(playerList):
                playerMc.visible = False
                continue
            else:
                playerMc.visible = True
            playerInfo = playerList[index]
            playerMc.level.text = str(playerInfo['lv'])
            if self == SIDE_LEFT:
                playerMc.txtName.gotoAndStop('lan')
            else:
                playerMc.txtName.gotoAndStop('hong')
            playerMc.txtName.txtName.text = playerInfo['name']
            playerMc.headIcon.fitSize = True
            iconPath = uiUtils.getZaijuLittleHeadIconPathById(playerInfo['zaijuId'])
            playerMc.headIcon.loadImage(iconPath)
            itemList = playerInfo['itemList']
            for itemIndex in xrange(MAX_ITEM_CNT):
                itemMc = playerMc.getChildByName('item%d' % itemIndex)
                if itemIndex >= len(itemList):
                    itemMc.txtCnt.text = ''
                    itemMc.itemIcon.visible = False
                    continue
                else:
                    itemMc.itemIcon.visible = True
                itemCnt = itemList[itemIndex]['cnt']
                itemMc.txtCnt.text = str(itemCnt if itemCnt > 1 else '')
                iconPath = uiUtils.getItemIconPath(itemList[itemIndex]['id'])
                itemMc.itemIcon.fitSize = True
                itemMc.itemIcon.loadImage(iconPath)
                uiUtils.addItemTipById(itemMc.itemIcon, itemList[itemIndex]['id'])

            playerMc.txtKill.text = '%d/' % playerInfo['kill']
            playerMc.txtDead.text = '%d/' % playerInfo['death']
            playerMc.txtAssist.text = '%d/' % playerInfo['assist']
            playerMc.txtLastHit.text = '%d' % playerInfo['cash']
            playerMc.selfBg.visible = playerInfo['isSelf']

    def updateHeadNum(self, side, num):
        if side == SIDE_LEFT:
            numStr = '%03d' % num
            visible = False
            for i, str in enumerate(numStr):
                mc = self.widget.getChildByName('%sNum%d' % (side, i))
                visible = visible or str != '0'
                mc.gotoAndStop('num%s' % str)
                mc.visible = visible or i == 2

        else:
            numStr = '%d' % num
            index = 0
            for str in numStr:
                mc = self.widget.getChildByName('%sNum%d' % (side, index))
                mc.gotoAndStop('num%s' % str)
                mc.visible = True
                index += 1

            for i in range(index, 3):
                mc = self.widget.getChildByName('%sNum%d' % (side, i))
                mc.visible = False

    def handleCloseBtnClick(self, *args):
        p = BigWorld.player()
        if getattr(p, 'isShowEnd', False) or getattr(p, 'backToBfEnd', False):
            msg = uiUtils.getTextFromGMD(GMDD.data.CONFIRM_QUIT_BF_DOTA, '')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, p.cell.quitBattleField)
        else:
            self.hide()
