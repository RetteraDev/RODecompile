#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zmjActivityBossPanelProxy.o
import BigWorld
import gameglobal
import clientUtils
import const
import utils
import gametypes
from guis import events
from helpers import tickManager
from uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
import zmjCommon
from gamestrings import gameStrings
from guis.asObject import TipManager, ASObject
from data import fame_data as FD
from data import zmj_fuben_config_data as ZFCD
from guis import zmjActivityBgProxy
from guis import uiUtils
from gamestrings import gameStrings
SHOW_ICON_PATH_PREFIX = 'zmjactivity/bossicon/%d.dds'
MAX_SLOT_NUM = 6
PREVIEW_SLOT_NUM = 6

class ZmjActivityBossPanelProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ZmjActivityBossPanelProxy, self).__init__(uiAdapter)
        self.widget = None
        self.currBossId = None
        self.tickId = 0
        self.callback = None

    def reset(self):
        self.currBossId = None

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def unRegisterPanel(self):
        self.widget = None
        self.currBossId = None
        if self.tickId:
            tickManager.stopTick(self.tickId)

    def initUI(self):
        self.widget.zhanmoFameIcon.bonusType = 'zhanmo'
        self.widget.chargeBtn.addEventListener(events.BUTTON_CLICK, self.handleChargeBtnClick, False, 0, True)
        self.widget.mainMc.monsterList.itemRenderer = 'ZmjActivityBos_BossItem'
        self.widget.mainMc.monsterList.itemHeight = 65
        self.widget.mainMc.monsterList.labelFunction = self.starBossLabelFunc
        self.widget.mainMc.monsterList.dataArray = []
        self.widget.mainMc.shopBtn.addEventListener(events.BUTTON_CLICK, self.onShopBtnClick)
        self.initFame()
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.tickId = tickManager.addTick(0.5, self.refreshTime)

    def onPublishBtnClick(self, *args):
        gameglobal.rds.ui.zmjPublishBoss.show(self.currBossId)

    def starBossLabelFunc(self, *args):
        p = BigWorld.player()
        nuid = args[3][0].GetString()
        itemMc = ASObject(args[3][1])
        itemMc.bossId = nuid
        itemMc.addEventListener(events.MOUSE_CLICK, self.onBossItemClick)
        bossInfo = p.zmjStarBoss.get(long(nuid), None)
        if not bossInfo:
            return
        else:
            itemMc.selectMc.visible = nuid == str(self.currBossId)
            itemMc.star.text = 'x%d' % bossInfo.star
            bonusId = ZFCD.data.get('starBossReward', {}).get(bossInfo.star, 0)
            itemMc.slot.visible = False
            itemMc.slot.dragable = False
            if bonusId:
                itemIds = clientUtils.genItemBonus(bonusId)
                if itemIds:
                    itemId, itemNum = itemIds[0]
                    itemMc.slot.visible = True
                    itemInfo = uiUtils.getGfxItemById(itemId, itemNum)
                    itemMc.slot.dragable = False
                    itemMc.slot.setItemSlotData(itemInfo)
            itemMc.bossState.visible = False
            if bossInfo.killer:
                itemMc.bossState.visible = True
                itemMc.bossState.gotoAndStop('killed')
            elif bossInfo.ownerGbId:
                itemMc.bossState.visible = True
                itemMc.bossState.gotoAndStop('challenging')
            itemMc.tExpire = bossInfo.tExpire
            itemMc.tValid = bossInfo.tValid
            self.refreshZmjBossLeftTimeInfo(itemMc)
            return

    def refreshZmjBossLeftTimeInfo(self, itemMc):
        tExpire = itemMc.tExpire
        tValid = itemMc.tValid
        leftExpire = tExpire - utils.getNow()
        leftValid = tValid - utils.getNow()
        if leftExpire > 0:
            if leftValid > 0:
                itemMc.leftTimeTitle.text = gameStrings.ZMJ_ACTIVITY_BOSS_LEFT_SKILL_TITLE
                itemMc.leftTime.text = gameStrings.ZMJ_ACTIVITY_BOSS_LEFT_TIME % (leftValid / 60, leftValid % 60)
            else:
                itemMc.leftTimeTitle.text = gameStrings.ZMJ_ACTIVITY_BOSS_LEFT_SKILL_TITLE
                itemMc.leftTime.text = gameStrings.DOUBLEARENA_STATE_OVER
        else:
            itemMc.leftTimeTitle.text = gameStrings.ZMJ_ACTIVITY_BOSS_LEFT_SKILL_TITLE
            itemMc.leftTime.text = gameStrings.DOUBLEARENA_STATE_OVER
        if str(itemMc.bossId) == str(self.currBossId):
            self.refreshBossState()

    def onBossItemClick(self, *args):
        e = ASObject(args[3][0])
        if str(self.currBossId) != long(e.currentTarget.bossId):
            self.currBossId = long(e.currentTarget.bossId)
            self.widget.mainMc.monsterList.dataArray = self.widget.mainMc.monsterList.dataArray
            self.widget.mainMc.monsterList.validateNow()
            self.refreshBossInfo()

    def refreshTime(self):
        if not self.widget:
            return
        monsterList = self.widget.mainMc.monsterList
        if len(self.getBossList()) != len(self.widget.mainMc.monsterList.dataArray):
            self.refreshBossList()
            self.refreshPushMsg()
        else:
            for i in xrange(monsterList.canvas.numChildren):
                bossItem = monsterList.canvas.getChildAt(i)
                self.refreshZmjBossLeftTimeInfo(bossItem)

    def onStartBtnClick(self, *args):
        e = ASObject(args[3][0])
        bossId = e.currentTarget.bossId
        p = BigWorld.player()
        p.cell.applyZMJStarBossFuben(long(bossId))

    def getBossList(self):
        p = BigWorld.player()
        bossList = [ bossId for bossId in p.zmjStarBoss if p.zmjStarBoss.get(bossId).tValid > utils.getNow() ]
        bossList.sort(cmp=self.bossSortFunc)
        return bossList

    def bossSortFunc(self, bossId1, bossId2):
        p = BigWorld.player()
        boss1 = p.zmjStarBoss.get(bossId1, None)
        boss2 = p.zmjStarBoss.get(bossId2, None)
        if boss1.killer and not boss2.killer:
            return 1
        elif not boss1.killer and boss2.killer:
            return -1
        else:
            if boss1.founder.gbId != boss2.founder.gbId:
                if boss1.founder.gbId == p.gbId:
                    return -1
                if boss2.founder.gbId == p.gbId:
                    return 1
            return -cmp(boss1.star, boss2.star) or cmp(boss1.tExpire, boss2.tExpire)

    def isMeetRequireMent(self):
        p = BigWorld.player()
        maxLayer = p.zmjData.get(const.ZMJ_FB_INFO_MAX_FINI_FB_STAR, 0)
        starBossAppearLayer = ZFCD.data.get('starBossAppearLayer', 0)
        return maxLayer >= starBossAppearLayer

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        curZhanmo = p.fame.get(const.ZMJ_ZHANMO_FAME_ID, 0)
        self.widget.zhanmoFameProgress.currentValue = curZhanmo
        self.refreshRewardPreviewPhase()
        self.refreshPoints()
        self.refreshBossList()

    def refreshPoints(self):
        p = BigWorld.player()
        huangYeFame = p.fame.get(const.ZMJ_ZHANMO_STAR_BOSS_FAME_ID, 0)
        totalStar = 0
        bossRecord = p.zmjData.get(const.ZMJ_FB_INFO_STAR_BOSS_RECORD, {})
        starTip = ''
        maxStar = 0
        for star in bossRecord:
            if not star:
                continue
            num = bossRecord.get(star, 0)
            totalStar += star * num
            if starTip:
                starTip += '\n'
            starTip += gameStrings.ZMJ_STAR_TIP % (star, num)
            maxStar = max(maxStar, star)

        self.widget.mainMc.scoreTxt.text = huangYeFame
        self.widget.mainMc.starTxt.text = maxStar
        if starTip:
            TipManager.addTip(self.widget.mainMc.starTxt, starTip)
        else:
            TipManager.removeTip(self.widget.mainMc.starTxt)

    def refreshBossList(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            bossList = self.getBossList()
            if not bossList:
                self.widget.requireTip.visible = True
                if self.isMeetRequireMent():
                    self.widget.requireTip.textField.htmlText = gameStrings.ZMJ_ACTIVITY_BOSS_NO_BOSS
                else:
                    self.widget.requireTip.textField.htmlText = gameStrings.ZMJ_ACTIVITY_BOSS_REQUIRE_LV
                self.currBossId = None
            else:
                self.widget.requireTip.visible = False
                if not self.currBossId or not p.zmjStarBoss.get(self.currBossId, None):
                    self.currBossId = bossList[0]
            self.refreshBossInfo()
            self.widget.mainMc.monsterList.dataArray = bossList
            self.widget.mainMc.monsterList.validateNow()
            return

    def refreshRewardPreviewPhase(self):
        if not self.widget:
            return
        else:
            rewardPreviewPhase = ZFCD.data.get('starBossrewardPreviewPhase', ())
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

    def refreshBossInfo(self):
        p = BigWorld.player()
        bossInfo = p.zmjStarBoss.get(self.currBossId, None)
        if not bossInfo:
            self.widget.mainMc.headMc.icon.loadImage('')
            self.widget.mainMc.trackMc.visible = False
            return
        else:
            fbNo = bossInfo.fbNo
            star = bossInfo.star
            bossShowIcon = ZFCD.data.get('bossShowIcon', {})
            iconId = bossShowIcon.get(fbNo, 0)
            if iconId:
                self.widget.mainMc.headMc.icon.loadImage(SHOW_ICON_PATH_PREFIX % (iconId,))
            else:
                self.widget.mainMc.headMc.icon.loadImage('')
            trackMc = self.widget.mainMc.trackMc
            trackMc.visible = True
            trackMc.publishBtn.addEventListener(events.BUTTON_CLICK, self.onPublishBtnClick)
            trackMc.startBtn.bossId = str(self.currBossId)
            trackMc.startBtn.addEventListener(events.BUTTON_CLICK, self.onStartBtnClick)
            bossNameInfo = self.uiAdapter.zmjActivityBg.getBossInfo(fbNo)
            trackMc.bossName.text = bossNameInfo.get('name', '')
            trackMc.zhanmoFameIcon.bonusType = 'zhanmo'
            bossType = 0
            bossDifficultyPhase = ZFCD.data.get('starBossDifficultyPhase', [])
            for i, (lowStar, highStar) in enumerate(bossDifficultyPhase):
                if star >= lowStar and star <= highStar:
                    bossType = i
                    break

            trackMc.bossIcon.gotoAndStop('type' + str(bossType))
            trackMc.zhanmoTxt.text = ZFCD.data.get('starBossCost', 0)
            self.refreshFounderInfo(bossInfo)
            self.refreshBossState()
            return

    def refreshBossState(self):
        p = BigWorld.player()
        bossInfo = p.zmjStarBoss.get(self.currBossId, None)
        trackMc = self.widget.mainMc.trackMc
        if not bossInfo:
            self.widget.mainMc.headMc.icon.loadImage('')
            trackMc.visible = False
            return
        else:
            trackMc.startBtn.enabled = utils.getNow() < bossInfo.tValid
            trackMc.publishBtn.visible = True
            if bossInfo.founder.gbId != p.gbId:
                trackMc.publishBtn.visible = False
                trackMc.publishInfo.htmlText = gameStrings.ZMJ_PUBLISHED
            elif bossInfo.star < ZFCD.data.get('starBossShareLevel', 0) or utils.getNow() >= bossInfo.tValid:
                trackMc.publishInfo.htmlText = gameStrings.ZMJ_PUBLISH_NOT_ALLOWED
                trackMc.publishBtn.visible = False
            else:
                trackMc.publishInfo.htmlText = ''
                trackMc.publishBtn.visible = True
            return

    def refreshFounderInfo(self, bossInfo):
        p = BigWorld.player()
        trackMc = self.widget.mainMc.trackMc
        founder = bossInfo.founder
        trackMc.playerName.text = founder.roleName
        trackMc.playerMc.level.text = founder.lv
        borderId = founder.borderId
        photo = founder.photo
        borderIcon = p.getPhotoBorderIcon(borderId, uiConst.PHOTO_BORDER_ICON_SIZE40)
        trackMc.playerMc.head.borderImg.fitSize = True
        trackMc.playerMc.head.borderImg.loadImage(borderIcon)
        trackMc.playerMc.head.icon.fitSize = True
        trackMc.playerMc.head.icon.imgType = uiConst.IMG_TYPE_NOS_FILE
        if uiUtils.isDownloadImage(photo):
            trackMc.playerMc.head.icon.url = photo
        else:
            trackMc.playerMc.head.icon.loadImage(photo)
        self.refreshBossState()

    def initFame(self):
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

    def handleChargeBtnClick(self, *arg):
        zhanmoFameMallId = ZFCD.data.get('zhanmoFameMallId', 0)
        self.uiAdapter.tianyuMall.mallBuyConfirm(zhanmoFameMallId, 1, 'zhanmo.0')

    def onShopBtnClick(self, *args):
        shopId = ZFCD.data.get('zmjStarBossShopId', 0)
        p = BigWorld.player()
        p.base.openPrivateShop(0, shopId)

    def refreshPushMsg(self):
        if not gameglobal.rds.configData.get('enableZMJStarBoss', False):
            self.removePushMsg()
            return
        if self.needPushMsg():
            self.addPushMsg()
            self.addRefreshPushCallBack()
        else:
            self.removePushMsg()

    def addRefreshPushCallBack(self):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
            self.callback = None
        if gameglobal.rds.GameState != gametypes.GS_PLAYGAME:
            return
        else:
            p = BigWorld.player()
            minInterval = -1
            for bossInfo in p.zmjStarBoss.values():
                if bossInfo.tValid > utils.getNow():
                    interval = bossInfo.tValid - utils.getNow()
                    minInterval = min(interval, minInterval) if minInterval > 0 else interval

            BigWorld.callback(minInterval, self.refreshPushMsg)
            return

    def needPushMsg(self):
        p = BigWorld.player()
        if not p.zmjStarBoss:
            return False
        for bossInfo in p.zmjStarBoss.values():
            if bossInfo.tValid > utils.getNow() and not bossInfo.killer:
                return True

        return False

    def addPushMsg(self):
        if uiConst.MESSAGE_TYPE_ZMJ_ACTIVITY_BOSS not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_ZMJ_ACTIVITY_BOSS)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_ZMJ_ACTIVITY_BOSS, {'click': self.onPushMsgClick})

    def removePushMsg(self):
        if uiConst.MESSAGE_TYPE_ZMJ_ACTIVITY_BOSS in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_ZMJ_ACTIVITY_BOSS)

    def onPushMsgClick(self):
        gameglobal.rds.ui.zmjActivityBg.show(zmjActivityBgProxy.TAB_THREE_IDX)
