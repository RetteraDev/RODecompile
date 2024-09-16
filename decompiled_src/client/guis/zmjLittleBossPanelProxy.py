#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zmjLittleBossPanelProxy.o
import BigWorld
import const
import events
import formula
import utils
import uiUtils
import uiConst
import clientUtils
from callbackHelper import Functor
import zmjCommon
from asObject import ASObject
from asObject import TipManager
from asObject import ASUtils
from asObject import MenuManager
from gamestrings import gameStrings
import gameglobal
from uiProxy import UIProxy
from data import zmj_star_data as ZSD
from data import fame_data as FD
from data import zmj_fuben_config_data as ZFCD
from cdata import game_msg_def_data as GMDD
SHOW_ICON_PATH_PREFIX = 'zmjactivity/bossicon/%d.dds'
PREVIEW_SLOT_NUM = 6
MAX_SLOT_NUM = 6

class ZmjLittleBossPanelProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ZmjLittleBossPanelProxy, self).__init__(uiAdapter)
        self.widget = None
        self.updateTimerHandle = None
        self.reset()
        self.addEvent(events.EVENT_FAME_UPDATE, self.handleFameUpdate)

    def reset(self):
        self.cancelUpdate()
        self.selectedStar = 0
        self.selectedStarItem = None

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.updateInfo()

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def updateInfo(self):
        self.cancelUpdate()
        if self.hasBaseData():
            p = BigWorld.player()
            item = self.widget.mainMc.trackMc
            lastTrackTime = p.zmjData.get(const.ZMJ_FB_INFO_LAST_RANDOM_TIME, 0)
            self.refreshMonsterEscapeTime(item, lastTrackTime)
            if item and self.isTimeOutBoss():
                self.refreshInfo(False)
        self.updateTimerHandle = BigWorld.callback(1, self.updateInfo)

    def refreshMonsterEscapeTime(self, itemMc, lastTrackTime):
        finalTime = lastTrackTime + ZFCD.data.get('lowFbRandomValidTime', 0)
        remainTime = finalTime - utils.getNow()
        itemMc.escapeTimeTxt.text = gameStrings.ZMJ_MONSTER_ESCAPE_TXT % (utils.formatTimeStr(remainTime, 'h:m:s', sNum=2, mNum=2, hNum=2),)

    def cancelUpdate(self):
        if self.updateTimerHandle:
            BigWorld.cancelCallback(self.updateTimerHandle)
            self.updateTimerHandle = None

    def initUI(self):
        p = BigWorld.player()
        self.widget.zhanmoFameIcon.bonusType = 'zhanmo'
        self.widget.mainMc.zhanmoIcon.bonusType = 'zhanmo'
        self.widget.mainMc.zhanmoTxt.text = ZFCD.data.get('lowFbRandomCost', 0)
        self.widget.mainMc.monsterList.column = 1
        self.widget.mainMc.monsterList.itemHeight = 67
        self.widget.mainMc.monsterList.itemRenderer = 'ZmjLittleBos_StarItem'
        self.widget.mainMc.monsterList.labelFunction = self.starItemFunc
        self.widget.mainMc.monsterList.dataArray = []
        self.widget.mainMc.trackBtn.addEventListener(events.BUTTON_CLICK, self.handleTrackBtnClick, False, 0, True)
        self.widget.mainMc.exchangeAbilityBtn.addEventListener(events.BUTTON_CLICK, self.handleExchangeAbilityBtnClick, False, 0, True)
        self.widget.mainMc.exchangeRewardBtn.addEventListener(events.BUTTON_CLICK, self.handleExchangeRewardBtnClick, False, 0, True)
        self.widget.mainMc.mySpriteAssist.mySpriteAssistBtn.addEventListener(events.BUTTON_CLICK, self.handleMySpriteAssistBtnClick, False, 0, True)
        self.widget.chargeBtn.addEventListener(events.BUTTON_CLICK, self.handleChargeBtnClick, False, 0, True)
        self.widget.mainMc.mySpriteAssist.assitAwardFlag.visible = False
        self.widget.mainMc.mySpriteAssist.visible = gameglobal.rds.configData.get('enableZMJAssist', False)
        maxFiniFbStar = p.zmjData.get(const.ZMJ_FB_INFO_MAX_FINI_FB_STAR, 0)
        lowFubenMaxStar = ZFCD.data.get('lowFubenMaxStar', 50)
        starItemData = self.getStarItemData()
        self.widget.mainMc.monsterList.dataArray = starItemData
        self.widget.mainMc.monsterList.validateNow()
        curFbStar = p.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_STAR, 0)
        indexPosY = max(lowFubenMaxStar - curFbStar - 1, 0)
        pos = self.widget.mainMc.monsterList.getIndexPosY(indexPosY)
        self.widget.mainMc.monsterList.scrollTo(pos)
        if not self.selectedStar and starItemData:
            selectStar = 1
            for star in starItemData:
                if star <= maxFiniFbStar + 1:
                    selectStar = star
                    break

            self.setSelectedItemByStar(selectStar)
        playerFbNo = formula.getFubenNo(p.spaceNo)
        self.widget.mainMc.trackBtn.enabled = not formula.inZMJLowFuben(playerFbNo)
        p.base.getZMJAssistAwardInfo()
        zhanmoFameData = FD.data.get(const.ZMJ_ZHANMO_FAME_ID, {})
        zhanmoAutoIncLimit = zhanmoFameData.get('autoIncLimit', 200)
        autoIncIntervalMinute = zhanmoFameData.get('autoIncIntervalMinute', 1)
        incVal = zhanmoFameData.get('incVal', 1)
        zhanmoFameTips = ''
        if autoIncIntervalMinute == 1:
            zhanmoFameTips = gameStrings.ZMJ_FAME_INC_TXT % (incVal,)
        else:
            zhanmoFameTips = gameStrings.ZMJ_FAME_INC_TXT_1 % (autoIncIntervalMinute, incVal)
        self.widget.zhanmoFameProgress.maxValue = zhanmoAutoIncLimit
        TipManager.addTip(self.widget.zhanmoFameProgress, zhanmoFameTips)
        self.refreshRewardPreviewPhase()
        self.refreshInfo()

    def refreshInfo(self, resetSelectedStar = True):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        zhanmoFameData = FD.data.get(const.ZMJ_ZHANMO_FAME_ID, {})
        zhanmoAutoIncLimit = zhanmoFameData.get('autoIncLimit', 200)
        curZhanmo = p.fame.get(const.ZMJ_ZHANMO_FAME_ID, 0)
        curTaofa = p.fame.get(const.ZMJ_TAOFA_FAME_ID, 0)
        curGongxian = p.fame.get(const.ZMJ_GONGXIAN_FAME_ID, 0)
        self.widget.zhanmoFameProgress.currentValue = curZhanmo
        self.widget.mainMc.gongxianTxt.text = curGongxian
        self.widget.mainMc.taofaTxt.text = curTaofa
        curFbNo = p.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_NO, 0)
        curFbStar = p.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_STAR, 0)
        maxFiniFbStar = p.zmjData.get(const.ZMJ_FB_INFO_MAX_FINI_FB_STAR, 0)
        bossShowIcon = ZFCD.data.get('bossShowIcon', {})
        iconId = bossShowIcon.get(curFbNo, 0)
        self.widget.mainMc.headMc.icon.fitSize = True
        if iconId and not self.isTimeOutBoss():
            self.widget.mainMc.headMc.icon.loadImage(SHOW_ICON_PATH_PREFIX % (iconId,))
        else:
            self.widget.mainMc.headMc.icon.loadImage('')
        self.refreshTrackMc()
        playerFbNo = formula.getFubenNo(p.spaceNo)
        self.widget.mainMc.trackBtn.enabled = not formula.inZMJLowFuben(playerFbNo)

    def refreshInfoStarList(self):
        if not self.hasBaseData():
            return
        starItemData = self.getStarItemData()
        self.widget.mainMc.monsterList.dataArray = starItemData
        self.widget.mainMc.monsterList.validateNow()
        p = BigWorld.player()
        lowFubenMaxStar = ZFCD.data.get('lowFubenMaxStar', 50)
        curFbStar = p.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_STAR, 0)
        indexPosY = max(lowFubenMaxStar - curFbStar - 1, 0)
        pos = self.widget.mainMc.monsterList.getIndexPosY(indexPosY)
        self.widget.mainMc.monsterList.scrollTo(pos)

    def starItemFunc(self, *arg):
        star = int(arg[3][0].GetNumber())
        itemMc = ASObject(arg[3][1])
        if itemMc and star:
            p = BigWorld.player()
            curFbStar = p.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_STAR, 0)
            maxFiniFbStar = p.zmjData.get(const.ZMJ_FB_INFO_MAX_FINI_FB_STAR, 0)
            itemMc.itemBtn.focusable = False
            itemMc.itemBtn.selected = False
            itemMc.star = star
            canTrackStar = maxFiniFbStar + 1
            showStar = canTrackStar + 1
            if star >= showStar:
                itemMc.itemBtn.enabled = False
                ASUtils.setMcEffect(itemMc.rewardState, 'gray')
            else:
                itemMc.itemBtn.enabled = True
                ASUtils.setMcEffect(itemMc.rewardState, '')
            bonusId = ZSD.data.get(star, {}).get('bonusId', 0)
            if bonusId:
                itemMc.rewardState.visible = True
                awardStars = p.zmjData.get(const.ZMJ_FB_INFO_TOOK_AWARD_STAR_IDS, [])
                if star in awardStars:
                    itemMc.rewardState.gotoAndStop('alreadyGet')
                else:
                    maxFiniFbStar = p.zmjData.get(const.ZMJ_FB_INFO_MAX_FINI_FB_STAR, 0)
                    if star > maxFiniFbStar:
                        itemMc.rewardState.gotoAndStop('noneGet')
                    else:
                        itemMc.rewardState.gotoAndStop('canGet')
            else:
                itemMc.rewardState.visible = False
            headData = p.zmjPhotoData.get(star, ())
            if headData:
                gbId, roleName, nos, sex, school = headData
                itemMc.headIcon.visible = True
                if gbId == p.gbId:
                    itemMc.headIcon.playerIcon.gotoAndStop('wo')
                else:
                    itemMc.headIcon.playerIcon.gotoAndStop('bieren')
                itemMc.headIcon.playerIcon.icon.setContentUnSee()
                itemMc.headIcon.playerIcon.icon.imgType = uiConst.IMG_TYPE_NOS_FILE
                itemMc.headIcon.playerIcon.icon.fitSize = True
                itemMc.headIcon.playerIcon.icon.serverId = utils.getHostId()
                itemMc.headIcon.playerIcon.icon.url = self.getPhoto(nos, sex, school)
                TipManager.addTip(itemMc.headIcon, roleName)
            else:
                itemMc.headIcon.visible = False
            itemMc.itemBtn.starMc.starTxt.text = star
            itemMc.itemBtn.label = gameStrings.ZMJ_STAR_BTN_TXT % (star,)
            itemMc.itemBtn.addEventListener(events.BUTTON_CLICK, self.handleSelectedBtnClick, False, 0, True)
            itemMc.rewardState.addEventListener(events.BUTTON_CLICK, self.handleRewardBtnClick, False, 0, True)
            if star == self.selectedStar:
                itemMc.itemBtn.selected = True

    def getPhoto(self, nos, sex, school):
        if nos:
            return nos
        return 'headIcon/%s.dds' % str(school * 10 + sex)

    def setSelectedItemByStar(self, star):
        oldStar = self.selectedStar
        newStar = star
        listMc = self.widget.mainMc.monsterList
        items = []
        if listMc:
            items = listMc.items
        oldItem = None
        newItem = None
        for item in items:
            if newStar == item.star:
                newItem = item
            if oldStar == item.star:
                oldItem = item

        if newStar:
            if oldItem and self.selectedStar and oldItem.star == self.selectedStar:
                oldItem.itemBtn.selected = False
            self.selectedStar = newStar
            if newItem:
                self.selectedStarItem = newItem
            if self.selectedStarItem:
                self.selectedStarItem.itemBtn.selected = True
        else:
            self.selectedStar = 0
            self.selectedStarItem = None

    def showRewardInfoTips(self, target, star):
        if not self.hasBaseData():
            return
        bonusId = ZSD.data.get(star, {}).get('bonusId', 0)
        if not bonusId:
            return
        itemBonus = clientUtils.genItemBonus(bonusId)
        if not itemBonus:
            return
        rewardTipsPanel = self.widget.getInstByClsName('ZmjLittleBos_rewardTips')
        itemList = []
        for item in itemBonus:
            itemList.append([item[0], item[1]])

        for i in range(MAX_SLOT_NUM):
            item = rewardTipsPanel.getChildByName('slot%d' % i)
            if i < len(itemList):
                item.visible = True
                tInfo = itemList[i]
                item.slot.setItemSlotData(uiUtils.getGfxItemById(tInfo[0], tInfo[1]))
            else:
                item.visible = False

        itemSlotFirst = rewardTipsPanel.getChildByName('slot0')
        rewardTipsPanel.tipBg.width = 30 + len(itemList) * (itemSlotFirst.width + 2)
        rewardTipsPanel.textField.x = (rewardTipsPanel.tipBg.width - rewardTipsPanel.textField.width) * 1.0 / 2 + 8
        menuParent = self.widget
        x, y = ASUtils.local2Global(target, target.x, target.y)
        x, y = ASUtils.global2Local(self.widget, x, y)
        MenuManager.getInstance().showMenu(target, rewardTipsPanel, {'x': x + target.width + 5,
         'y': y - 35}, True, menuParent)

    def refreshRewardPreviewPhase(self):
        if not self.hasBaseData():
            return
        else:
            rewardPreviewPhase = ZFCD.data.get('rewardPreviewPhase', ())
            for i in xrange(PREVIEW_SLOT_NUM):
                slotMc = getattr(self.widget.mainMc, 'slot' + str(i), None)
                if slotMc:
                    slot = slotMc.slot
                    slot.dragable = False
                    if i < len(rewardPreviewPhase):
                        needGongxian, itemId = rewardPreviewPhase[i]
                        itemInfo = uiUtils.getGfxItemById(itemId)
                        slot.setItemSlotData(itemInfo)
                        slotMc.tipCanvas.visible = False
                        slotMc.visible = True
                    else:
                        slotMc.visible = False

            return

    def getStarItemData(self):
        p = BigWorld.player()
        lowFubenMaxStar = ZFCD.data.get('lowFubenMaxStar', 50)
        maxFiniFbStar = p.zmjData.get(const.ZMJ_FB_INFO_MAX_FINI_FB_STAR, 0)
        trackData = range(1, lowFubenMaxStar + 1)
        trackData.reverse()
        return trackData

    def getLittleBossInfo(self):
        p = BigWorld.player()
        curFbNo = p.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_NO, 0)
        curFbStar = p.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_STAR, 0)
        if curFbNo and curFbStar and not self.isTimeOutBoss():
            return [1]
        return []

    def isTimeOutBoss(self):
        p = BigWorld.player()
        lastTrackTime = p.zmjData.get(const.ZMJ_FB_INFO_LAST_RANDOM_TIME, 0)
        finalTime = lastTrackTime + ZFCD.data.get('lowFbRandomValidTime', 0)
        remainTime = finalTime - utils.getNow()
        if remainTime > 0:
            return False
        return True

    def handleFameUpdate(self, e):
        if e.data in (const.ZMJ_ZHANMO_FAME_ID, const.ZMJ_TAOFA_FAME_ID, const.ZMJ_GONGXIAN_FAME_ID):
            self.refreshInfo(False)

    def hasBaseData(self):
        if not self.widget:
            return False
        return True

    def transVal(self, val):
        if isinstance(val, str):
            return val
        val = round(int(val * 10) / 10.0, 1)
        if int(val) == val:
            return int(val)
        return str(val)

    def refreshTrackMc(self):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        curFbNo = p.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_NO, 0)
        curFbStar = p.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_STAR, 0)
        if curFbNo and curFbStar and not self.isTimeOutBoss():
            self.widget.mainMc.trackMc.visible = True
            self.widget.mainMc.noneTxt.visible = False
            isBoost = p.zmjData.get(const.ZMJ_FB_INFO_IS_BOOST, 0)
            isLucky = p.zmjData.get(const.ZMJ_FB_INFO_IS_LUCKY, 0)
            bossDeaded = p.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_SUCC, 0)
            itemMc = self.widget.mainMc.trackMc
            enterCnt = p.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_ENTER_CNT, 0)
            if enterCnt:
                if isBoost:
                    itemMc.powerfulTrackBtn.enabled = True
                    itemMc.entryBtn.enabled = False
                else:
                    itemMc.powerfulTrackBtn.enabled = False
                    itemMc.entryBtn.enabled = True
            else:
                itemMc.powerfulTrackBtn.enabled = True
                itemMc.entryBtn.enabled = True
            self.refreshItemInfo(itemMc, curFbNo, curFbStar, bossDeaded, enterCnt)
            luckyRewardRatio = ZFCD.data.get('luckyRewardRatio', 0)
            itemMc.doubleGongxianTxt.x = itemMc.gongxianTxt.x + itemMc.gongxianTxt.textWidth + 3
            itemMc.doubleTaofaTxt.x = itemMc.taofaTxt.x + itemMc.taofaTxt.textWidth + 3
            itemMc.doubleGongxianTxt.text = gameStrings.ZMJ_LUCKY_REWARD_RATIO_TXT % (self.transVal(luckyRewardRatio),)
            itemMc.doubleTaofaTxt.text = gameStrings.ZMJ_LUCKY_REWARD_RATIO_TXT % (self.transVal(luckyRewardRatio),)
            itemMc.doubleGongxianTxt.visible = isLucky
            itemMc.doubleTaofaTxt.visible = isLucky
            lastTrackTime = p.zmjData.get(const.ZMJ_FB_INFO_LAST_RANDOM_TIME, 0)
            self.refreshMonsterEscapeTime(itemMc, lastTrackTime)
        else:
            self.widget.mainMc.trackMc.visible = False
            self.widget.mainMc.noneTxt.visible = True

    def refreshItemInfo(self, itemMc, fbNo, star, bossDeaded, enterCnt):
        bossInfo = self.uiAdapter.zmjActivityBg.getBossInfo(fbNo)
        itemMc.bossName.text = bossInfo.get('name', '')
        itemMc.starMc.starTxt.text = star
        rewardPoint = self.getGXTF(fbNo, star)
        itemMc.gongxianTxt.text = rewardPoint
        itemMc.taofaTxt.text = rewardPoint
        itemMc.zhanmoFameIcon.bonusType = 'zhanmo'
        bossType = 0
        bossDifficultyPhase = ZFCD.data.get('bossDifficultyPhase', 0)
        for i, (lowStar, highStar) in enumerate(bossDifficultyPhase):
            if star >= lowStar and star <= highStar:
                bossType = i
                break

        itemMc.bossIcon.gotoAndStop('type' + str(bossType))
        fearType = ZFCD.data.get('bossFearType', {}).get(fbNo, 0)
        fearInfo = ZFCD.data.get('bossFearInfo', {}).get(fearType, ())
        if fearInfo:
            iconType, tips = fearInfo
            itemMc.fearIcon.gotoAndPlay('icon' + str(iconType))
            TipManager.addTip(itemMc.fearIcon, tips)
        lowFbFreeAfterCnt = ZFCD.data.get('lowFbFreeAfterCnt', {})
        if bossDeaded:
            itemMc.zhanmoTitleTxt.visible = False
            itemMc.zhanmoTxt.visible = False
            itemMc.zhanmoFameIcon.visible = False
            itemMc.renterTxt.visible = False
            itemMc.entryBtn.visible = False
            itemMc.powerfulTrackBtn.visible = False
            itemMc.deadMc.visible = True
        elif enterCnt >= lowFbFreeAfterCnt:
            itemMc.zhanmoTitleTxt.visible = False
            itemMc.zhanmoTxt.visible = False
            itemMc.zhanmoFameIcon.visible = False
            itemMc.renterTxt.visible = True
            itemMc.deadMc.visible = False
            itemMc.entryBtn.visible = True
            itemMc.powerfulTrackBtn.visible = True
        else:
            itemMc.zhanmoTitleTxt.visible = True
            itemMc.zhanmoTxt.visible = True
            itemMc.zhanmoFameIcon.visible = True
            itemMc.renterTxt.visible = False
            itemMc.zhanmoTxt.text = ZFCD.data.get('lowFubenCost', 0)
            itemMc.deadMc.visible = False
            itemMc.entryBtn.visible = True
            itemMc.powerfulTrackBtn.visible = True
        itemMc.entryBtn.addEventListener(events.BUTTON_CLICK, self.handleEntryBtn, False, 0, True)
        itemMc.powerfulTrackBtn.addEventListener(events.BUTTON_CLICK, self.handlePowerfulEntryBtn, False, 0, True)

    def getGXTF(self, fbNo, star):
        p = BigWorld.player()
        fbRecord = p.zmjData.get(const.ZMJ_FB_INFO_SUCC_FB_RECORD, {}).get(star, {})
        maxStar = p.zmjData.get(const.ZMJ_FB_INFO_MAX_FINI_FB_STAR, 0)
        isBoost = p.zmjData.get(const.ZMJ_FB_INFO_IS_BOOST, 0)
        succCnt = sum(fbRecord.values())
        deaded = p.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_SUCC, 0)
        if not deaded:
            succCnt += 1
        return zmjCommon.calcZMJAward(star, maxStar, succCnt, isBoost=isBoost)

    def handleEntryBtn(self, *arg):
        if not self.hasBaseData():
            return
        self._entryZMJLowFuben(False)

    def _entryZMJLowFuben(self, isBoost):
        p = BigWorld.player()
        lowFbFreeAfterCnt = ZFCD.data.get('lowFbFreeAfterCnt', 1)
        enterCnt = p.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_ENTER_CNT, 0)
        if enterCnt < lowFbFreeAfterCnt:
            lowFubenCost = zmjCommon.calcZMJLowCost(False)
            curZhanmo = p.fame.get(const.ZMJ_ZHANMO_FAME_ID, 0)
            if curZhanmo < lowFubenCost:
                p.showGameMsg(GMDD.data.ZMJ_LACK_ZHANMO_FAME_MSG, ())
                return
        if not zmjCommon.checkInZMJFbPermitTime():
            p.showGameMsg(GMDD.data.ZMJ_OPENING_TIME_LIMIT, ())
            return
        p.cell.applyZMJLowFuben(isBoost)

    def handlePowerfulEntryBtn(self, *arg):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        enterCnt = p.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_ENTER_CNT, 0)
        if enterCnt:
            self._entryZMJLowFuben(True)
        else:
            boostRewardRatio = ZFCD.data.get('boostRewardRatio', 0)
            lowFubenCost = zmjCommon.calcZMJLowCost(True)
            curZhanmo = p.fame.get(const.ZMJ_ZHANMO_FAME_ID, 0)
            if curZhanmo < lowFubenCost:
                p.showGameMsg(GMDD.data.ZMJ_LACK_ZHANMO_FAME_MSG, ())
                return
            powerfulTrackConfirmMsg = gameStrings.ZMJ_BOOST_TRACK_CONFIRM_TXT % (lowFubenCost, self.transVal(boostRewardRatio))
            msg = powerfulTrackConfirmMsg
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self._entryZMJLowFuben, True))

    def handleTrackBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        trackStar = self.selectedStar
        curFbNo = p.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_NO, 0)
        curFbStar = p.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_STAR, 0)
        bossDeaded = p.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_SUCC, 0)

        def _trackFunc():
            lowFbRandomCost = ZFCD.data.get('lowFbRandomCost', 0)
            curZhanmo = p.fame.get(const.ZMJ_ZHANMO_FAME_ID, 0)
            if curZhanmo < lowFbRandomCost:
                p.showGameMsg(GMDD.data.ZMJ_LACK_ZHANMO_FAME_MSG, ())
                return
            if not zmjCommon.checkInZMJFbPermitTime():
                p.showGameMsg(GMDD.data.ZMJ_OPENING_TIME_LIMIT, ())
                return
            p.cell.randomZMJFubenByStar(int(trackStar))

        if curFbNo and curFbStar and not bossDeaded and not self.isTimeOutBoss():
            self.uiAdapter.messageBox.showYesNoMsgBox(gameStrings.ZMJ_DMG_RETRACK_CONFIRM_TXT, _trackFunc)
            return
        _trackFunc()

    def handleExchangeAbilityBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        self.uiAdapter.compositeShop.closeShop()
        shopId = ZFCD.data.get('zmjAbilityShopId', 0)
        p = BigWorld.player()
        p.base.openPrivateShop(0, shopId)

    def handleExchangeRewardBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        self.uiAdapter.compositeShop.closeShop()
        shopId = ZFCD.data.get('zmjRewardShopId', 0)
        p = BigWorld.player()
        p.base.openPrivateShop(0, shopId)

    def handleMySpriteAssistBtnClick(self, *arg):
        gameglobal.rds.ui.zmjSpriteReward.show()

    def handleChargeBtnClick(self, *arg):
        zhanmoFameMallId = ZFCD.data.get('zhanmoFameMallId', 0)
        self.uiAdapter.tianyuMall.mallBuyConfirm(zhanmoFameMallId, 1, 'zhanmo.0')

    def handleSelectedBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        if t:
            self.setSelectedItemByStar(t.parent.star)

    def handleRewardBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        if t:
            p = BigWorld.player()
            star = t.parent.parent.star
            awardStars = p.zmjData.get(const.ZMJ_FB_INFO_TOOK_AWARD_STAR_IDS, [])
            if star not in awardStars:
                maxFiniFbStar = p.zmjData.get(const.ZMJ_FB_INFO_MAX_FINI_FB_STAR, 0)
                if star > maxFiniFbStar:
                    self.showRewardInfoTips(t, t.parent.parent.star)
                else:
                    p.cell.applyZMJStarAward(star)

    def setAssitAwardFlag(self, notTake):
        if self.widget:
            self.widget.mainMc.mySpriteAssist.assitAwardFlag.visible = bool(notTake)
