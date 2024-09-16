#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bfDotaFinalDetailProxy.o
import BigWorld
import gameglobal
import const
import events
import gametypes
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from guis import tipUtils
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis.asObject import ASUtils
from data import duel_config_data as DCD
from data import state_data as SD
from cdata import game_msg_def_data as GMDD
TAB_IDX_JIE_SUAN = 1
TAB_IDX_ZHAN_KUANG = 2
TAB_IDX_TONG_JI = 3
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
BUFF_MAX_CNT = 5
ACHIEVEMENT_ICON_MAX_CNT = 7

class BfDotaFinalDetailProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BfDotaFinalDetailProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_BF_DOTA_FINAL_DETAIL, self.handleCloseBtn)

    def reset(self):
        self.tabIdx = TAB_IDX_JIE_SUAN

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BF_DOTA_FINAL_DETAIL:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BF_DOTA_FINAL_DETAIL)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BF_DOTA_FINAL_DETAIL)
        p = BigWorld.player()
        p.cell.queryAllBattleFieldDotaTotalCash()
        p.cell.queryOtherBagInfoInDotaBattleField(getattr(p, 'oldEquipVersion', 0))

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

    def initUI(self):
        p = BigWorld.player()
        self.widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleCloseBtn, False, 0, True)
        self.widget.tabJieSuan.tabIdx = TAB_IDX_JIE_SUAN
        self.widget.tabJieSuan.addEventListener(events.BUTTON_CLICK, self.handleTabChange, False, 0, True)
        self.widget.tabZhanKuang.tabIdx = TAB_IDX_ZHAN_KUANG
        self.widget.tabZhanKuang.addEventListener(events.BUTTON_CLICK, self.handleTabChange, False, 0, True)
        self.widget.tabTongJi.tabIdx = TAB_IDX_TONG_JI
        self.widget.tabTongJi.addEventListener(events.BUTTON_CLICK, self.handleTabChange, False, 0, True)
        self.updateHeadNum(SIDE_LEFT, p.getBfOwnStas(const.BF_DOTA_OWN_STATS_MYSIDE_KILL_TYPE))
        self.updateHeadNum(SIDE_RIGHT, p.getBfOwnStas(const.BF_DOTA_OWN_STATS_OTHERSIDE_KILL_TYPE))
        if getattr(p, 'bfResult', const.WIN) == const.WIN:
            self.widget.result.gotoAndPlay('win')
        else:
            self.widget.result.gotoAndPlay('lose')

    def refreshInfo(self):
        if not self.widget:
            return
        self.jieSuanInfo = self.getJieSuanInfo()
        self.zhanKuangInfo = self.getZhanKuangInfo()
        self.tongjiInfo = self.getTongJiInfo()
        if self.tabIdx == TAB_IDX_JIE_SUAN:
            self.refreshJieSuan()
        elif self.tabIdx == TAB_IDX_ZHAN_KUANG:
            self.refreshZhanKuang()
        else:
            self.refreshTongJi()

    def handleTabChange(self, *args):
        e = ASObject(args[3][0])
        tabIdx = int(e.currentTarget.tabIdx)
        if tabIdx != self.tabIdx:
            self.tabIdx = tabIdx
            self.refreshInfo()

    def getZhanKuangInfo(self):
        return gameglobal.rds.ui.bfDotaDetail.getFrameInfo()

    def getMemberPerform(self, gbId):
        p = BigWorld.player()
        for info in p.bfMemPerforms:
            if info.get('gbId', 0) == gbId:
                return info

        return {}

    def getJieSuanInfo(self):
        p = BigWorld.player()
        info = {}
        buffIconList = []
        info['buffList'] = buffIconList
        dataList = []
        rewardZhanXun = p.bfResultInfo.get('rewardZhanXun', 0)
        rewardJunZi = p.bfResultInfo.get('rewardJunZi', 0)
        dailyZhanxun = p.bfResultInfo.get('dailyZhanxun', 0)
        dailyJunzi = p.bfResultInfo.get('dailyJunzi', 0)
        if dailyZhanxun + dailyJunzi:
            cfg = DCD.data.get('bfDotaRewardBuffs', {}).get('daily', ('', '%d,%d'))
            iconPath = 'bfDotaJieSuanBuffs/%s.dds' % cfg[0]
            tips = cfg[1] % (dailyZhanxun, dailyJunzi)
            buffIconList.append((iconPath, tips))
        dailyWinZhanxun = p.bfResultInfo.get('dailyWinZhanxun', 0)
        dailyWinJunzi = p.bfResultInfo.get('dailyWinJunzi', 0)
        if dailyWinZhanxun + dailyWinJunzi:
            cfg = DCD.data.get('bfDotaRewardBuffs', {}).get('dailyWin', ('', '%d,%d'))
            iconPath = 'bfDotaJieSuanBuffs/%s.dds' % cfg[0]
            tips = cfg[1] % (dailyWinZhanxun, dailyWinJunzi)
            buffIconList.append((iconPath, tips))
        teamOpenTimeZhanxun = p.bfResultInfo.get('teamOpenTimeZhanxun', 0)
        teamOpenTimeJunzi = p.bfResultInfo.get('teamOpenTimeJunzi', 0)
        if teamOpenTimeZhanxun + teamOpenTimeJunzi:
            cfg = DCD.data.get('bfDotaRewardBuffs', {}).get('teamOpenTime', ('', '%d,%d'))
            iconPath = 'bfDotaJieSuanBuffs/%s.dds' % cfg[0]
            tips = cfg[1] % (teamOpenTimeZhanxun, teamOpenTimeJunzi)
            buffIconList.append((iconPath, tips))
        dotaKingWinMultiCardVal = p.bfResultInfo.get('dotaKingWinMultiCardVal', 0)
        if dotaKingWinMultiCardVal:
            cfg = DCD.data.get('bfDotaRewardBuffs', {}).get('dotaKingWinMultiCardVal' + str(int(dotaKingWinMultiCardVal)), ('', ''))
            iconPath = 'bfDotaJieSuanBuffs/%s.dds' % cfg[0]
            tips = cfg[1]
            buffIconList.append((iconPath, tips))
        dotaKingDateMultiCardVal = p.bfResultInfo.get('dotaKingDateMultiCardVal', 0)
        if dotaKingDateMultiCardVal:
            ranges = [dotaKingDateMultiCardVal] if dotaKingDateMultiCardVal != 3 else [1, 2]
            for carVal in ranges:
                cfg = DCD.data.get('bfDotaRewardBuffs', {}).get('dotaKingDateMultiCardVal' + str(int(carVal)), ('', ''))
                iconPath = 'bfDotaJieSuanBuffs/%s.dds' % cfg[0]
                tips = cfg[1]
                buffIconList.append((iconPath, tips))

        dataList.append(p.bfResultInfo.get(const.BF_COMMON_JI_BAI, (0, 0, 0, 0, 0)))
        dataList.append(p.bfResultInfo.get(const.BF_DOTA_DAMAGE_TO_AVATR, (0, 0, 0, 0, 0)))
        dataList.append(p.bfResultInfo.get(const.BF_DOTA_DAMAGE_WITH_TOWER, (0, 0, 0, 0, 0)))
        dataList.append(p.bfResultInfo.get(const.BF_DOTA_BE_DAMAGE_FROM_AVATR, (0, 0, 0, 0, 0)))
        dataList.append(p.bfResultInfo.get(const.BF_COMMON_CURE, (0, 0, 0, 0, 0)))
        info['dataList'] = dataList
        info['rewardZhanXun'] = rewardZhanXun
        info['rewardJunZi'] = rewardJunZi
        info['addFame'] = p.bfResultInfo.get('rewardDotaKing', 0)
        return info

    def refreshJieSuan(self):
        self.widget.gotoAndStop('jieSuan')
        self.widget.tabJieSuan.selected = True
        self.widget.tabZhanKuang.selected = False
        self.widget.tabTongJi.selected = False
        self.widget.jieSuan.btnLeave.addEventListener(events.BUTTON_CLICK, self.handleCloseBtn, False, 0, True)
        buffList = self.jieSuanInfo['buffList']
        for index in xrange(BUFF_MAX_CNT):
            buffMc = self.widget.jieSuan.getChildByName('buff%d' % index)
            if index < len(buffList):
                buffMc.fitSize = True
                buffIcon, tips = buffList[index]
                buffMc.loadImage(buffIcon)
                TipManager.addTip(buffMc, tips)
                buffMc.visible = True
            else:
                buffMc.visible = False

        self.widget.jieSuan.txtFame.text = self.jieSuanInfo['addFame']
        self.widget.jieSuan.txtZhanXun.text = self.jieSuanInfo['rewardZhanXun']
        self.widget.jieSuan.txtJunZi.text = self.jieSuanInfo['rewardJunZi']
        for index, data in enumerate(self.jieSuanInfo['dataList']):
            txtValue = self.widget.jieSuan.getChildByName('value%d' % index)
            txtDonation = self.widget.jieSuan.getChildByName('donation%d' % index)
            txtRewardZhanXun = self.widget.jieSuan.getChildByName('rewardZhanXun%d' % index)
            txtRewardJunZi = self.widget.jieSuan.getChildByName('rewardJunZi%d' % index)
            txtValue.text = str(data[const.BF_RESULT_INFO_VALUE_IDX])
            txtDonation.text = str(data[const.BF_RESULT_INFO_DONATE_IDX])
            txtRewardZhanXun.text = str(data[const.BF_RESULT_INFO_ZHANXUN_IDX])
            txtRewardJunZi.text = str(data[const.BF_RESULT_INFO_JUNZI_IDX])

    def updateZhanKuangSideInfo(self, side, sideInfo):
        sideMc = self.widget.zhanKuang.getChildByName(side)
        playerList = sideInfo['playerList']
        voteResult = self.voteResult
        for index in xrange(TEAM_MATE_MAX_CNT):
            playerMc = sideMc.getChildByName('player%d' % index).player
            if index >= len(playerList):
                playerMc.visible = False
                continue
            else:
                playerMc.visible = True
            playerInfo = playerList[index]
            self.setPlayerBasicInfo(playerMc, playerInfo)
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
                TipManager.addItemTipById(itemMc.itemIcon, itemList[itemIndex]['id'])

            playerMc.txtKill.text = '%d/' % playerInfo['kill']
            playerMc.txtDead.text = '%d/' % playerInfo['death']
            playerMc.txtAssist.text = '%d/' % playerInfo['assist']
            playerMc.txtLastHit.text = '%d' % playerInfo['cash']
            playerGbId = long(playerMc.gbId)
            if playerGbId in voteResult.keys():
                playerMc.vote.visible = True
                tip = ''
                if voteResult[playerGbId] == gametypes.DOTA_BF_PUNISH_TYPE_NONE:
                    playerMc.vote.visible = False
                elif voteResult[playerGbId] == gametypes.DOTA_BF_PUNISH_TYPE_ALL_QL:
                    tip = gameStrings.DOTA_BF_PUNISH_TYPE_ALL_QL_TIP
                elif voteResult[playerGbId] == gametypes.DOTA_BF_PUNISH_TYPE_GXQL:
                    tip = gameStrings.DOTA_BF_PUNISH_TYPE_GXQL_TIP
                elif voteResult[playerGbId] == gametypes.DOTA_BF_PUNISH_TYPE_GXJB:
                    tip = gameStrings.DOTA_BF_PUNISH_TYPE_GXJB_TIP
                if tip:
                    TipManager.addTip(playerMc.vote, tip)
            else:
                playerMc.vote.visible = False

    def handleAddFriend(self, *args):
        e = ASObject(args[3][0])
        p = BigWorld.player()
        gbId = int(e.currentTarget.parent.gbId)
        memItem = p.getMemInfoByGbId(gbId)
        roleName = memItem.get('roleName', '')
        p.base.addContact(roleName, gametypes.FRIEND_GROUP_FRIEND, const.FRIEND_SRC_BATTLE_FIELD)

    def refreshSelfInfo(self):
        selfInfo, selfSideInfo, enemySideInfo = self.zhanKuangInfo
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

    def updateTongJiSideInfo(self, side, sideInfo, sidePercentList):
        sideMc = self.widget.tongJi.getChildByName(side)
        playerList = sideInfo['playerList']
        for index in xrange(TEAM_MATE_MAX_CNT):
            playerMc = sideMc.getChildByName('player%d' % index).player
            if index >= len(playerList):
                playerMc.visible = False
                continue
            else:
                playerMc.visible = True
            playerInfo = playerList[index]
            self.setPlayerBasicInfo(playerMc, playerInfo)
            dmgPercent, dmgAvatarPercent, beDmgPercent = sidePercentList[index]
            playerMc.dps.currentValue = dmgPercent * 100
            playerMc.dps.validateNow()
            playerMc.dps.textField.text = '%.1f%%' % (dmgPercent * 100)
            playerMc.dpsAvatar.currentValue = dmgAvatarPercent * 100
            playerMc.dpsAvatar.validateNow()
            playerMc.dpsAvatar.textField.text = '%.1f%%' % (dmgAvatarPercent * 100)
            playerMc.beDamaged.currentValue = beDmgPercent * 100
            playerMc.beDamaged.validateNow()
            playerMc.beDamaged.textField.text = '%.1f%%' % (beDmgPercent * 100)

    def setPlayerBasicInfo(self, playerMc, playerInfo):
        playerMc.gbId = playerInfo['gbId']
        playerMc.btnAddFriend.visible = playerInfo['canAddFriend']
        playerMc.btnAddFriend.addEventListener(events.MOUSE_CLICK, self.handleAddFriend, False, 0, True)
        playerMc.level.text = str(playerInfo['lv'])
        if self == SIDE_LEFT:
            playerMc.txtName.gotoAndStop('lan')
        else:
            playerMc.txtName.gotoAndStop('hong')
        playerMc.txtName.txtName.text = playerInfo['name']
        playerMc.headIcon.fitSize = True
        iconPath = uiUtils.getZaijuLittleHeadIconPathById(playerInfo['zaijuId'])
        playerMc.headIcon.loadImage(iconPath)
        playerMc.selfBg.visible = playerInfo['isSelf']
        ASUtils.setHitTestDisable(playerMc.mvp, True)
        playerMc.mvp.visible = playerInfo['isMVP']
        achievementList = playerInfo['achievemenList']
        for index in xrange(ACHIEVEMENT_ICON_MAX_CNT):
            iconMc = playerMc.getChildByName('achievementIcon%d' % index)
            if index < len(achievementList):
                iconMc.visible = True
                iconMc.fitSize = True
                ddsName, tips = achievementList[index]
                ddsName = 'bfDotaAchievement/%s.dds' % ddsName
                iconMc.loadImage(ddsName)
                TipManager.addTip(iconMc, tips)
            else:
                iconMc.visible = False

    def refreshZhanKuang(self):
        self.widget.gotoAndStop('zhanKuang')
        self.widget.tabJieSuan.selected = False
        self.widget.tabZhanKuang.selected = True
        self.widget.tabTongJi.selected = False
        selfInfo, mySideInfo, enemySideInfo = self.zhanKuangInfo
        self.updateZhanKuangSideInfo(SIDE_LEFT, mySideInfo)
        self.updateZhanKuangSideInfo(SIDE_RIGHT, enemySideInfo)
        self.refreshSelfInfo()

    def getTongJiInfo(self):
        p = BigWorld.player()
        mySideTotalDmgToAvatar = 0
        mySideTotalBeDmg = 0
        mySideTotalToTower = 0
        enemySideTotalDmgToAvatar = 0
        enemySideTotalBeDmg = 0
        enemySideTotalDmgToTower = 0
        selfInfo, mySideInfo, enemySideInfo = self.zhanKuangInfo
        for teamMateInfo in p.bfMemPerforms:
            gbId = teamMateInfo['gbId']
            memberPerform = self.getMemberPerform(gbId)
            dmgTower = memberPerform.get(const.BF_DOTA_DAMAGE_WITH_TOWER, 0)
            dmgToAvatr = memberPerform.get(const.BF_DOTA_DAMAGE_TO_AVATR, 0)
            beDmg = memberPerform.get(const.BF_DOTA_BE_DAMAGE_FROM_AVATR, 0)
            if memberPerform.get(const.BF_COMMON_SIDE_NUID, 0) == p.bfSideNUID:
                mySideTotalBeDmg += beDmg
                mySideTotalDmgToAvatar += dmgToAvatr
                mySideTotalToTower += dmgTower
            else:
                enemySideTotalDmgToAvatar += dmgToAvatr
                enemySideTotalBeDmg += beDmg
                enemySideTotalDmgToTower += dmgTower

        mySideTongJiList = []
        enemySideTongJiList = []
        for teamMateInfo in mySideInfo['playerList']:
            gbId = teamMateInfo['gbId']
            memberPerform = self.getMemberPerform(gbId)
            dmgTower = memberPerform.get(const.BF_DOTA_DAMAGE_WITH_TOWER, 0)
            dmgToAvatr = memberPerform.get(const.BF_DOTA_DAMAGE_TO_AVATR, 0)
            beDmg = memberPerform.get(const.BF_DOTA_BE_DAMAGE_FROM_AVATR, 0)
            dmgPercent = (dmgTower + dmgToAvatr) * 1.0 / (mySideTotalDmgToAvatar + mySideTotalToTower) if mySideTotalDmgToAvatar + mySideTotalToTower else 0
            dmgToAvatarPecent = dmgToAvatr * 1.0 / mySideTotalDmgToAvatar if mySideTotalDmgToAvatar else 0
            beDmgPercent = beDmg * 1.0 / mySideTotalBeDmg if mySideTotalBeDmg else 0
            mySideTongJiList.append((dmgPercent, dmgToAvatarPecent, beDmgPercent))

        for teamMateInfo in enemySideInfo['playerList']:
            gbId = teamMateInfo['gbId']
            memberPerform = self.getMemberPerform(gbId)
            dmgTower = memberPerform.get(const.BF_DOTA_DAMAGE_WITH_TOWER, 0)
            dmgToAvatr = memberPerform.get(const.BF_DOTA_DAMAGE_TO_AVATR, 0)
            beDmg = memberPerform.get(const.BF_DOTA_BE_DAMAGE_FROM_AVATR, 0)
            dmgPercent = (dmgTower + dmgToAvatr) * 1.0 / (enemySideTotalDmgToTower + enemySideTotalDmgToAvatar) if enemySideTotalDmgToTower + enemySideTotalDmgToAvatar else 0
            dmgToAvatarPercent = dmgToAvatr * 1.0 / enemySideTotalDmgToAvatar if enemySideTotalDmgToAvatar else 0
            beDmgPercent = beDmg * 1.0 / enemySideTotalBeDmg if enemySideTotalBeDmg else 0
            enemySideTongJiList.append((dmgPercent, dmgToAvatarPercent, beDmgPercent))

        return (mySideTongJiList, enemySideTongJiList)

    def refreshTongJi(self):
        self.widget.gotoAndStop('tongJi')
        self.widget.tabJieSuan.selected = False
        self.widget.tabZhanKuang.selected = False
        self.widget.tabTongJi.selected = True
        selfInfo, mySideInfo, enemySideInfo = self.zhanKuangInfo
        mySidePercentList, enemySidePercentList = self.tongjiInfo
        self.updateTongJiSideInfo(SIDE_LEFT, mySideInfo, mySidePercentList)
        self.updateTongJiSideInfo(SIDE_RIGHT, enemySideInfo, enemySidePercentList)
        self.refreshSelfInfo()

    def handleCloseBtn(self, *args):
        p = BigWorld.player()
        msg = uiUtils.getTextFromGMD(GMDD.data.CONFIRM_QUIT_BF_DOTA, '')
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, p.cell.quitBattleField)
