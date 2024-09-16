#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildIdentifyStarProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import uiUtils
import random
import gametypes
from uiProxy import UIProxy
from data import state_data as SD
from data import guild_mass_astrology_data as GMAD
from data import guild_config_data as GCD
from gameStrings import gameStrings
from guis.asObject import TipManager
from callbackHelper import Functor
BUFF_MAP = {0: 22,
 1: 23,
 2: 0,
 3: 1,
 4: 10,
 5: 11,
 6: 12,
 7: 13,
 8: 2,
 9: 3,
 10: 4,
 11: 5,
 12: 14,
 13: 15,
 14: 16,
 15: 17,
 16: 18,
 17: 19,
 18: 20,
 19: 21,
 20: 6,
 21: 7,
 22: 8,
 23: 9}
ROTATION_SPEED = 8

class GuildIdentifyStarProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildIdentifyStarProxy, self).__init__(uiAdapter)
        self.widget = None
        self.allRotate = 0
        self.curIndex = -1
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_IDENTIFY_STAR, self.hide)

    def reset(self):
        self.itemList = []
        self.needCloseMsgBox = False
        self.index = 0
        self.curRotate = 0
        self.needChangeBuff = False
        self.buffIdxs = []
        gameglobal.rds.sound.stopSound(gameglobal.SD_498)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_IDENTIFY_STAR:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_IDENTIFY_STAR)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def show(self):
        if not self.widget:
            gameglobal.rds.ui.guild.hideAllGuildBuilding()
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_IDENTIFY_STAR)
            self.refreshInfo()

    def initUI(self):
        self.widget.bg.diYun1.gotoAndStop('DiYun')
        self.widget.bg.diYun2.gotoAndStop('DiYun')
        self.widget.bg.renShi1.gotoAndStop('RenShi')
        self.widget.bg.renShi2.gotoAndStop('RenShi')
        self.widget.content.gotoAndStop('play')
        self.widget.content.visible = False
        for index in xrange(0, 24):
            self.itemList.append(self.widget.getChildByName('item' + str(index)))
            self.itemList[index].selectMc.visible = False
            self.itemList[index].icon.visible = False
            self.itemList[index].quality.visible = False

        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleClose, False, 0, True)
        self.widget.content.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleBeginIdentityStar, False, 0, True)

    def refreshInfo(self):
        if self.widget:
            self.refreshTimeInfo()

    def refreshTimeInfo(self):
        p = BigWorld.player()
        p.cell.getMassAstrologyInfo()

    def setTimeInfo(self, currState, dailyCnt):
        if not self.widget:
            return
        p = BigWorld.player()
        guild = p.guild
        marker = guild.marker.get(gametypes.GUILD_BUILDING_ASTROLOGY_ID)
        buildValue = guild.building.get(marker.buildingNUID)
        buildLv = buildValue.level if buildValue else 0
        MaxCntDaily = GCD.data.get('massAstrologyMaxCntDaily', {7: 15,
         8: 20,
         9: 25,
         10: 30}).get(buildLv, 0)
        guildMoney = BigWorld.player().guild.bindCash
        ConsumeMoney = GCD.data.get('massAstrologyConsumeMoney', {}).get(dailyCnt + 1, 0)
        if dailyCnt == MaxCntDaily:
            timeText = uiUtils.toHtml(gameStrings.GUILD_IDENTIFY_STAR_TIMES + ': %d/%d' % (dailyCnt, MaxCntDaily), '#F43804')
            self.widget.content.moneyText.visible = False
            self.widget.content.money.visible = False
            self.widget.content.moneyIcon.visible = False
            self.setConfirmBtn(False)
        else:
            timeText = uiUtils.toHtml(gameStrings.GUILD_IDENTIFY_STAR_TIMES + ': %d/%d' % (dailyCnt, MaxCntDaily), '#4D4339')
        if ConsumeMoney > guildMoney:
            money = uiUtils.toHtml(str(ConsumeMoney), '#F43804')
        else:
            money = uiUtils.toHtml(str(ConsumeMoney), '#4D4339')
        self.widget.content.timeNum.htmlText = timeText
        self.widget.content.moneyIcon.bonusType = 'bindCash'
        self.widget.content.money.htmlText = money
        self.widget.content.visible = True

    def setBuff(self, buffIdxs):
        buffList = []
        idx = 0
        for buffIdx in buffIdxs:
            baseData = GMAD.data.get(buffIdx, {})
            buffData = SD.data.get(baseData.get('buffId', (0,))[0], {})
            buffInfo = {}
            buffInfo['idx'] = BUFF_MAP.get(idx, 0)
            buffInfo['quality'] = buffIdx[0]
            buffInfo['iconPath'] = 'state/48/%d.dds' % buffData.get('iconId', 0)
            buffInfo['tipDesc'] = '%s<br>%s' % (buffData.get('name', ''), baseData.get('buffDesc', ''))
            buffList.append(buffInfo)
            idx += 1

        self.buffIdxs = buffIdxs
        for itemInfo in buffList:
            itemMc = self.itemList[itemInfo['idx']]
            itemMc.quality.gotoAndStop('a' + str(itemInfo['quality']))
            itemMc.icon.fitSize = True
            itemMc.icon.loadImage(itemInfo['iconPath'])
            TipManager.addTip(itemMc, itemInfo['tipDesc'])
            itemMc.selectMc.visible = False
            itemMc.icon.visible = False
            itemMc.quality.visible = False

    def handleBeginIdentityStar(self, *args):
        gameglobal.rds.sound.playSound(gameglobal.SD_2)
        p = BigWorld.player()
        p.cell.applyMassAstrology()

    def beginIdentifyStar(self, randomBuffList, selectIdx, selectBuffId, currBuffIds):
        if self.widget:
            if not selectIdx:
                gameglobal.rds.ui.guildIdentifyStarChoose.setBuffs(selectBuffId, currBuffIds, isLast=True)
                gameglobal.rds.ui.guildIdentifyStarChoose.show()
                self.setConfirmBtn(True)
            elif selectBuffId and currBuffIds:
                self.setBuff(randomBuffList)
                self.needChangeBuff = True
                self.setConfirmBtn(True)
                self.needCloseMsgBox = True
                idx = BUFF_MAP.get(self.buffIdxs.index(selectIdx), 0)
                self.index = random.choice([idx + 3, idx + 27])
                gameglobal.rds.sound.playSound(gameglobal.SD_498)
                self.widget.smallCircle.addEventListener(events.EVENT_ENTER_FRAME, self.onEnterFrame, False, 0, True)
                gameglobal.rds.ui.guildIdentifyStarChoose.setBuffs(selectBuffId, currBuffIds, isLast=False)
            else:
                self.setBuff(randomBuffList)
                self.setConfirmBtn(False)
                self.needCloseMsgBox = True
                idx = BUFF_MAP.get(self.buffIdxs.index(selectIdx), 0)
                self.index = random.choice([idx + 2, idx + 26])
                gameglobal.rds.sound.playSound(gameglobal.SD_498)
                self.widget.smallCircle.addEventListener(events.EVENT_ENTER_FRAME, self.onEnterFrame, False, 0, True)
            self.refreshTimeInfo()

    def onEnterFrame(self, *args):
        self.allRotate += ROTATION_SPEED
        self.widget.smallCircle.rotation += ROTATION_SPEED
        index = int((self.widget.smallCircle.rotation + 352) % 360 / 15)
        self.itemList[index].selectMc.visible = True
        self.curIndex = index
        if self.curIndex != -1 and self.allRotate <= 360 + 15 * self.index - 37.5 - self.curRotate:
            BigWorld.callback(0.3, Functor(self.setReliveItem, self.curIndex))
        if self.allRotate > 360 + 15 * self.index - 37.5 - self.curRotate:
            self.widget.smallCircle.removeEventListener(events.EVENT_ENTER_FRAME, self.onEnterFrame)
            self.widget.smallCircle.rotation = self.widget.smallCircle.rotation % 360
            self.curRotate = self.widget.smallCircle.rotation
            if self.needChangeBuff:
                gameglobal.rds.ui.guildIdentifyStarChoose.show()
            self.curIndex = -1
            self.allRotate = 0
            self.setConfirmBtn(True)
            self.needCloseMsgBox = False
            for i in xrange(24):
                self.itemList[i].icon.visible = True
                self.itemList[i].quality.visible = True

    def setReliveItem(self, idx):
        if self.widget:
            self.itemList[idx].selectMc.visible = False

    def handleClose(self, *args):
        if self.needCloseMsgBox:
            msg = gameStrings.GUILD_IDENTIFY_STAR_CLOSE_MSG
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.hide)
        else:
            self.hide()

    def setConfirmBtn(self, isConfirmBtnEnable = True):
        if self.widget.content.confirmBtn:
            self.widget.content.confirmBtn.focused = False
            self.widget.content.confirmBtn.enabled = isConfirmBtnEnable
        if isConfirmBtnEnable:
            gameglobal.rds.sound.stopSound(gameglobal.SD_498)
