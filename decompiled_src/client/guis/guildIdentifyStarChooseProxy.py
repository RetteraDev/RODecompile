#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildIdentifyStarChooseProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import TipManager
from data import state_data as SD
from data import guild_mass_astrology_data as GMAD
from data import guild_config_data as GCD
from gameStrings import gameStrings
MAX_BUFF_LEN = 5

class GuildIdentifyStarChooseProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildIdentifyStarChooseProxy, self).__init__(uiAdapter)
        self.widget = None
        self.selectBuffId = 0
        self.isLast = False
        self.nowBuffId = 0
        self.currBuffIds = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_IDENTIFY_STAR_CHOOSE, self.hide)

    def reset(self):
        self.isLast = False
        self.nowBuffId = 0
        self.currBuffIds = []

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_IDENTIFY_STAR_CHOOSE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_IDENTIFY_STAR_CHOOSE)

    def setBuffs(self, selectBuffId, currBuffIds, isLast):
        self.nowBuffId = selectBuffId
        self.currBuffIds = currBuffIds
        self.isLast = isLast

    def show(self):
        if self.widget:
            self.refreshInfo()
            self.widget.swapPanelToFront()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_IDENTIFY_STAR_CHOOSE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleClickConfirmBtn, False, 0, True)
        self.widget.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleClickCancelBtn, False, 0, True)

    def refreshInfo(self):
        if self.widget:
            if not self.nowBuffId:
                self.hide()
                return
            if self.isLast:
                hint = gameStrings.GUILD_IDENTIFY_STAR_LAST_CHOOSE
            else:
                hint = gameStrings.GUILD_IDENTIFY_STAR_CHOOSE
            maxNum = GCD.data.get('guildMassAstrologyMaxBuffNum', 1)
            self.widget.hintField.text = hint
            buffList = []
            data = GMAD.data
            for id in self.currBuffIds:
                for idx in data:
                    buffIds = data[idx].get('buffId', (0,))
                    if id in buffIds:
                        index = idx

                baseData = GMAD.data.get(index, {})
                buffData = SD.data.get(baseData.get('buffId', (0,))[0], {})
                buffInfo = {}
                buffInfo['buffId'] = id
                buffInfo['quality'] = index[0]
                buffInfo['iconPath'] = 'state/48/%d.dds' % buffData.get('iconId', 0)
                buffInfo['tipDesc'] = baseData.get('buffDesc', '')
                buffList.append(buffInfo)

            for i in xrange(MAX_BUFF_LEN):
                itemMc = self.widget.getChildByName('buff' + str(i))
                itemMc.idx = i
                if i < maxNum:
                    if i < len(buffList):
                        itemMc.icon.visible = True
                        itemInfo = buffList[i]
                        itemMc.data = itemInfo
                        itemMc.quality.gotoAndStop('a' + str(itemInfo['quality']))
                        itemMc.icon.fitSize = True
                        itemMc.icon.loadImage(itemInfo['iconPath'])
                        TipManager.addTip(itemMc, itemInfo['tipDesc'])
                    else:
                        itemMc.data = {}
                        itemMc.data['buffId'] = 0
                        itemMc.icon.visible = False
                    itemMc.bg.gotoAndStop('normal')
                    itemMc.addEventListener(events.MOUSE_CLICK, self.handleClickBuff, False, 0, True)
                else:
                    itemMc.icon.visible = False
                    itemMc.bg.gotoAndStop('lock')
                    itemMc.quality.visible = False
                    itemMc.removeEventListener(events.MOUSE_CLICK, self.handleClickBuff)

            for idx in data:
                buffIds = data[idx].get('buffId', (0,))
                if self.nowBuffId in buffIds:
                    nowBuffIndex = idx

            baseData = GMAD.data.get(nowBuffIndex, {})
            buffId = self.nowBuffId
            buffData = SD.data.get(buffId, {})
            nowBuffIconPath = 'state/48/%d.dds' % buffData.get('iconId', 0)
            nowBuffTip = baseData.get('buffDesc', '')
            self.widget.nowBuff.icon.fitSize = True
            self.widget.nowBuff.quality.gotoAndStop('a' + str(nowBuffIndex[0]))
            self.widget.nowBuff.icon.loadImage(nowBuffIconPath)
            TipManager.addTip(self.widget.nowBuff, nowBuffTip)
            self.widget.chooseMc.gotoAndStop('noBuff')
            self.widget.confirmBtn.enabled = False

    def handleClickConfirmBtn(self, *args):
        BigWorld.player().cell.applyReplaceMassAstrologyBuff(self.selectBuffId)
        gameglobal.rds.ui.guildIdentifyStar.isLast = False
        self.hide()

    def handleClickCancelBtn(self, *args):
        BigWorld.player().cell.discardMassAstrologyBuff()
        gameglobal.rds.ui.guildIdentifyStar.isLast = False
        self.hide()

    def handleClickBuff(self, *args):
        e = ASObject(args[3][0])
        selectMc = e.currentTarget
        self.widget.chooseMc.gotoAndStop('buff' + str(selectMc.idx))
        self.widget.confirmBtn.enabled = True
        self.selectBuffId = selectMc.data['buffId']
