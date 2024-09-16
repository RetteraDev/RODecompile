#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/worldBossMapProxy.o
import BigWorld
import utils
import gameglobal
import uiUtils
import Math
import uiConst
from guis import events
from guis.asObject import TipManager
from guis.asObject import ASObject
from helpers import tickManager
from uiProxy import UIProxy
from data import clan_war_fort_data as CWFD
from guis import worldBossHelper
from guis.asObject import ASUtils
from gamestrings import gameStrings

class WorldBossMapProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WorldBossMapProxy, self).__init__(uiAdapter)
        self.widget = None
        self.bossInfos = {}
        self.tickId = 0
        self.reset()
        self.isResult = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_WORLD_BOSS_MAP, self.hide)

    def reset(self):
        self.bossInfos = {}
        self.isResult = False

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WORLD_BOSS_MAP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WORLD_BOSS_MAP)
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.tickId = 0

    def show(self, isResult = False):
        self.isResult = isResult
        worldBossHelper.getInstance().queryWorldBossInfo()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WORLD_BOSS_MAP)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        ASUtils.callbackAtFrame(self.widget, 38, self.refreshMarks)

    def refreshInfo(self):
        if not self.widget:
            return
        self.bossInfos = worldBossHelper.getInstance().getWorldBossInfos()
        self.refreshMarks()
        self.refreshGuildInfo()
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.tickId = tickManager.addTick(1, self.refreshTick)

    def refreshTick(self):
        self.refreshMarks()

    def refreshMarks(self, *args):
        if self.widget.currentFrame < 38:
            return
        for fortId in CWFD.data.keys():
            markMc = self.widget.getChildByName('mark%d' % fortId)
            if markMc:
                markMc.visible = False

        for refId in self.bossInfos:
            bossInfo = self.bossInfos.get(refId, {})
            fortId = bossInfo.get('fortId', 0)
            if not fortId:
                continue
            markMc = self.widget.getChildByName('mark%d' % fortId)
            markMc.visible = True
            self.setMarkDetail(markMc, bossInfo)

    def setMarkDetail(self, markMc, bossInfo):
        startTime = bossInfo.get('startTime', 0)
        now = utils.getNow()
        markMc.timeInfo.textField.text = ''
        markMc.guildName.textField.text = ''
        markMc.killIcon.content.visible = False
        markMc.bg.content.visible = False
        markMc.teleBtn.content.visible = False
        markMc.teleBtn1.content.visible = False
        markMc.goldBorder.content.visible = False
        markMc.head.icon.fitSize = True
        markMc.head.icon.loadImage(bossInfo.get('bossRoundIcon', ''))
        TipManager.addTip(markMc.head, bossInfo.get('bossName', ''))
        markMc.teleBtn.content.addEventListener(events.BUTTON_CLICK, self.onGotoBtnClick)
        markMc.teleBtn1.content.addEventListener(events.BUTTON_CLICK, self.onGotoBtnClick)
        if bossInfo.get('rareWorldBoss', False):
            markMc.goldBorder.content.visible = True
            TipManager.addTip(markMc.goldBorder, bossInfo.get('bossName', ''))
        if bossInfo.get('firstKiller', {}):
            guildName = bossInfo['firstKiller'].get('guildName', '')
            if guildName:
                markMc.guildName.textField.text = guildName
                markMc.bg.content.visible = True
            markMc.killIcon.content.visible = True
            ASUtils.setMcEffect(markMc.head, 'gray')
        elif not bossInfo.get('isLive', False):
            ASUtils.setMcEffect(markMc.head.icon, 'gray')
        else:
            ASUtils.setMcEffect(markMc.head.icon, '')
            if now < startTime:
                remainTime = startTime - now
                markMc.timeInfo.textField.text = self.formateTime(remainTime)
                markMc.bg.content.visible = True
                markMc.teleBtn1.content.visible = True
                markMc.teleBtn1.content.refId = bossInfo.get('refId', 0)
            else:
                markMc.teleBtn.content.visible = True
                markMc.teleBtn.content.refId = bossInfo.get('refId', 0)

    def formateTime(self, time):
        minute = int(time / 60)
        sec = time - minute * 60
        return '%02d:%02d' % (minute, sec)

    def refreshGuildInfo(self):
        p = BigWorld.player()
        resultVisible = self.isResult and getattr(p, 'worldBossAccount', None)
        self.widget.result0.mc.visible = resultVisible
        self.widget.result1.mc.visible = resultVisible
        self.widget.result2.mc.visible = resultVisible
        self.widget.result3.mc.visible = resultVisible
        if resultVisible:
            self.widget.result0.mc.txt.textField.text = gameStrings.GUILD_TOTAL_DMG % p.worldBossAccount[1]
            self.widget.result1.mc.txt.textField.text = gameStrings.GUILD_TOTAL_KILL % p.worldBossAccount[3]
            self.widget.result2.mc.txt.textField.text = gameStrings.SELF_TOTAL_DMG % p.worldBossAccount[2]
            self.widget.result3.mc.txt.textField.text = gameStrings.SELF_TOTAL_KILL % p.worldBossAccount[4]

    def onGotoBtnClick(self, *args):
        e = ASObject(args[3][0])
        refId = e.currentTarget.refId
        bossInfo = self.bossInfos.get(refId, {})
        position = bossInfo.get('position', None)
        if position:
            pos = Math.Vector3(position[0], position[1], position[2])
            uiUtils.findPosByPos(1, pos)
