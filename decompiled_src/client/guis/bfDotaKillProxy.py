#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bfDotaKillProxy.o
import BigWorld
from Queue import Queue
import gameglobal
import uiConst
from guis import uiUtils
from guis.asObject import ASUtils
from data import duel_config_data as DCD
BF_DOTA_KILL_FRAMES = ['kill1',
 'kill2',
 'kill3',
 'kill4',
 'kill5']
DELAY_HIDE_TIME = 2
SELF_SIDE_KILLED_IDX = 0
ENEMY_SIDE_KILLED_IDX = 1
from uiProxy import UIProxy
TYPE_FIRST_BLOOD = 0
TYPE_COMBO_KILL = 1
TYPE_SHUT_DOWN = 2
TYPE_ACCMULATE_KILL = 3
TYPE_KILL_NORMAL = 4
TYPE_ACE = 5
MAX_ACCMULAT_CNT = 7
MAX_COMBO_KILL_CNT = 5
TEXT_COLOR_BLUE = '#43B9F0'
TEXT_COLOR_RED = '#FF471C'

class BfDotaKillProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BfDotaKillProxy, self).__init__(uiAdapter)
        self.killInfo = {}
        self.reset()

    def reset(self):
        self.timer = 0
        self.normalKillWidget = None
        self.normalKillWidgetId = 0
        self.aceWidget = None
        self.aceWidgetId = 0
        self.bfDotaNormalKillQueue = Queue()
        self.bfDotaAceQueue = Queue()

    def _registerASWidget(self, widgetId, widget):
        if not self.normalKillWidget:
            self.normalKillWidget = widget
            self.normalKillWidget.mainMc.ace.visible = False
            self.setNormalKillVisible(False)
        elif not self.aceWidget:
            self.aceWidget = widget
            self.aceWidget.mainMc.normalKill.visible = False
            self.setAceVisible(False)

    def setNormalKillVisible(self, visible):
        if self.normalKillWidget:
            self.normalKillWidget.visible = visible
            if visible:
                self.normalKillWidget.mainMc.normalKill.gotoAndPlay(1)

    def setAceVisible(self, visible):
        if self.aceWidget:
            self.aceWidget.visible = visible
            if visible:
                self.aceWidget.y = self.normalKillWidget.y - DCD.data.get('bfDotaKillWidgetOffset', 200)
                self.aceWidget.mainMc.ace.gotoAndPlay(1)

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(self.aceWidgetId)
        self.uiAdapter.unLoadWidget(self.normalKillWidgetId)
        self.reset()

    def show(self):
        if self.normalKillWidgetId and self.aceWidgetId:
            return
        self.normalKillWidgetId = self.uiAdapter.loadWidget(uiConst.WIDGET_BF_DOTA_KILL)
        self.aceWidgetId = self.uiAdapter.loadWidget(uiConst.WIDGET_BF_DOTA_KILL)

    def addFirstBloodInfo(self, killerGbId, killeeGbId):
        info = {}
        info['type'] = TYPE_FIRST_BLOOD
        info['killInfo'] = (killerGbId, killeeGbId)
        self.bfDotaNormalKillQueue.put(info)
        if self.normalKillWidget and not self.normalKillWidget.visible:
            self.refreshNormalKill()

    def addNormalKillInfo(self, killerGbId, killeeGbId, killerAccmulateKill, killeeAccmulateKill, comboKill):
        killerAccmulateKill = min(MAX_ACCMULAT_CNT, killerAccmulateKill)
        comboKill = min(MAX_COMBO_KILL_CNT, comboKill)
        info = {}
        if comboKill > 1:
            info['type'] = TYPE_COMBO_KILL
            info['cnt'] = comboKill
            info['killInfo'] = (killerGbId, killeeGbId)
        elif killeeAccmulateKill >= 3:
            info['type'] = TYPE_SHUT_DOWN
            info['killInfo'] = (killerGbId, killeeGbId)
        elif killerAccmulateKill >= 3:
            info['type'] = TYPE_ACCMULATE_KILL
            info['killInfo'] = (killerGbId, killeeGbId)
            info['cnt'] = killerAccmulateKill
        else:
            info['type'] = TYPE_KILL_NORMAL
            info['killInfo'] = (killerGbId, killeeGbId)
        self.bfDotaNormalKillQueue.put(info)
        if self.normalKillWidget and not self.normalKillWidget.visible:
            self.refreshNormalKill()

    def addAceKillInfo(self):
        info = {}
        info['type'] = TYPE_ACE
        self.bfDotaAceQueue.put(info)
        if self.aceWidget and not self.aceWidget.visible:
            self.refreshAceKill()

    def getColorfulRoleName(self, roleName, gbId):
        p = BigWorld.player()
        if p.bfSideNUID == p.getMemInfoByGbId(gbId).get('sideNUID', 0):
            return uiUtils.toHtml(roleName, TEXT_COLOR_BLUE)
        else:
            return uiUtils.toHtml(roleName, TEXT_COLOR_RED)

    def refreshNormalKill(self):
        p = BigWorld.player()
        if not self.normalKillWidget or self.bfDotaNormalKillQueue.empty():
            self.setNormalKillVisible(False)
            return
        info = self.bfDotaNormalKillQueue.get()
        if not info:
            self.setNormalKillVisible(False)
            return
        self.setNormalKillVisible(True)
        type = info['type']
        killerGbId, killeeGbId = info['killInfo']
        killerMemInfo = p.getMemInfoByGbId(killerGbId)
        killeeMemInfo = p.getMemInfoByGbId(killeeGbId)
        killerMemName = killerMemInfo.get('roleName', '')
        killerMemName = self.getColorfulRoleName(killerMemName, killerGbId)
        self.normalKillWidget.mainMc.normalKill.leftName.txtName.htmlText = killerMemName
        ASUtils.autoSizeWithFont(self.normalKillWidget.mainMc.normalKill.leftName.txtName, 14)
        killeeMemName = killeeMemInfo.get('roleName', '')
        killeeMemName = self.getColorfulRoleName(killeeMemName, killeeGbId)
        self.normalKillWidget.mainMc.normalKill.rightName.txtName.htmlText = killeeMemName
        ASUtils.autoSizeWithFont(self.normalKillWidget.mainMc.normalKill.rightName, 14)
        self.normalKillWidget.mainMc.normalKill.leftIcon.icon.fitSize = True
        self.normalKillWidget.mainMc.normalKill.leftIcon.icon.loadImage(uiUtils.getZaijuLittleHeadIconPathById(p.bfDotaZaijuRecord.get(killerGbId, 0)))
        self.normalKillWidget.mainMc.normalKill.rightIcon.icon.fitSize = True
        self.normalKillWidget.mainMc.normalKill.rightIcon.icon.loadImage(uiUtils.getZaijuLittleHeadIconPathById(p.bfDotaZaijuRecord.get(killeeGbId, 0)))
        soundId = 0
        soundMaps = DCD.data.get('bfDotaKillSoundMaps', {})
        selfSideKilled = p.getMemInfoByGbId(killeeGbId).get('sideNUID', 0) == p.bfSideNUID
        if not selfSideKilled:
            selfKill = soundMaps.get('selfKill', 5669)
            gameglobal.rds.sound.playSound(selfKill)
        else:
            selfKilled = soundMaps.get('selfKilled', 5670)
            gameglobal.rds.sound.playSound(selfKilled)
        if type == TYPE_FIRST_BLOOD:
            self.normalKillWidget.mainMc.normalKill.effCombo.gotoAndPlay('kill1')
            self.normalKillWidget.mainMc.normalKill.effComboBg.visible = False
            self.setKillInfoFrameLabel(self.normalKillWidget.mainMc.normalKill, 'firstBlood')
            soundId = soundMaps.get('firstBlood', 0)
        if type == TYPE_COMBO_KILL:
            self.normalKillWidget.mainMc.normalKill.effComboBg.visible = True
            self.normalKillWidget.mainMc.normalKill.effCombo.gotoAndPlay('kill%d' % info['cnt'])
            self.normalKillWidget.mainMc.normalKill.effComboBg.gotoAndPlay('kill%d' % info['cnt'])
            self.setKillInfoFrameLabel(self.normalKillWidget.mainMc.normalKill, 'comboKill%d' % info['cnt'])
            sounds = soundMaps.get('comboKill', {}).get(info['cnt'], ())
            if sounds:
                soundId = sounds[SELF_SIDE_KILLED_IDX] if selfSideKilled else sounds[ENEMY_SIDE_KILLED_IDX]
        else:
            self.normalKillWidget.mainMc.normalKill.effCombo.gotoAndPlay('kill1')
            self.normalKillWidget.mainMc.normalKill.effComboBg.visible = False
        if type == TYPE_SHUT_DOWN:
            self.setKillInfoFrameLabel(self.normalKillWidget.mainMc.normalKill, 'shutDown')
            gameglobal.rds.sound.playSound(DCD.data.get('bfDotaKillSoundMaps', {}).get('shutDown', 0))
            soundId = soundMaps.get('shutDown', 0)
        if type == TYPE_ACCMULATE_KILL:
            self.setKillInfoFrameLabel(self.normalKillWidget.mainMc.normalKill, 'accmulateKill%d' % info['cnt'])
            sounds = soundMaps.get('accmulateKill', {}).get(info['cnt'], ())
            if sounds:
                soundId = sounds[SELF_SIDE_KILLED_IDX] if selfSideKilled else sounds[ENEMY_SIDE_KILLED_IDX]
        if type == TYPE_KILL_NORMAL:
            if selfSideKilled:
                sounds = soundMaps.get('selfSideKilled', ())
                if sounds:
                    if killeeGbId == p.gbId:
                        soundId = sounds.get('self', 0)
                    else:
                        soundId = sounds.get('others', 0)
            else:
                sounds = soundMaps.get('enemySideKilled', ())
                if sounds:
                    if killerGbId == p.gbId:
                        soundId = sounds.get('self', 0)
                    else:
                        soundId = sounds.get('others', 0)
        gameglobal.rds.sound.playSound(soundId)
        self.normalKillWidget.mainMc.normalKill.killInfo.visible = type != TYPE_KILL_NORMAL
        self.normalKillWidget.mainMc.normalKill.killInfo2.visible = type != TYPE_KILL_NORMAL
        BigWorld.callback(DCD.data.get('bfDotaKillShowTime', (5, 5))[0], self.refreshNormalKill)

    def setKillInfoFrameLabel(self, parentMc, frameLabel):
        parentMc.killInfo.gotoAndPlay(frameLabel)
        parentMc.killInfo2.gotoAndPlay(frameLabel)

    def refreshAceKill(self):
        if not self.aceWidget or self.bfDotaAceQueue.empty():
            self.setAceVisible(False)
            return
        info = self.bfDotaAceQueue.get()
        if not info:
            self.setAceVisible(False)
            return
        self.setAceVisible(True)
        self.setKillInfoFrameLabel(self.aceWidget.mainMc.ace, 'ace')
        gameglobal.rds.sound.playSound(DCD.data.get('bfDotaKillSoundMaps', {}).get('ace', 0))
        BigWorld.callback(DCD.data.get('bfDotaKillShowTime', (5, 5))[0], self.refreshAceKill)

    def testFun(self):
        p = BigWorld.player()
        p.battleFieldTeam[0] = {'sideNUID': p.bfSideNUID}
        p.battleFieldTeam[1] = {'sideNUID': p.bfSideNUID - 1}
        p.bfDotaZaijuRecord[0] = 10000
        p.bfDotaZaijuRecord[1] = 10001
        self.addFirstBloodInfo(0, 1)
        self.addNormalKillInfo(0, 1, 3, 2, 2)
        self.addNormalKillInfo(0, 1, 3, 2, 3)
        self.addNormalKillInfo(0, 1, 3, 2, 4)
        self.addNormalKillInfo(0, 1, 3, 2, 5)
        self.addNormalKillInfo(1, 0, 3, 2, 2)
        self.addNormalKillInfo(1, 0, 3, 2, 3)
        self.addNormalKillInfo(1, 0, 3, 2, 4)
        self.addNormalKillInfo(1, 0, 3, 2, 5)
        self.addNormalKillInfo(0, 1, 1, 3, 1)
        self.addNormalKillInfo(0, 1, 2, 0, 1)
        self.addNormalKillInfo(0, 1, 3, 0, 1)
        self.addNormalKillInfo(0, 1, 4, 0, 1)
        self.addNormalKillInfo(0, 1, 5, 0, 1)
        self.addNormalKillInfo(0, 1, 6, 0, 1)
        self.addNormalKillInfo(0, 1, 7, 0, 1)
        self.addNormalKillInfo(0, 1, 8, 0, 1)
        self.addNormalKillInfo(1, 0, 2, 0, 1)
        self.addNormalKillInfo(1, 0, 3, 0, 1)
        self.addNormalKillInfo(1, 0, 4, 0, 1)
        self.addNormalKillInfo(1, 0, 5, 0, 1)
        self.addNormalKillInfo(1, 0, 6, 0, 1)
        self.addNormalKillInfo(1, 0, 7, 0, 1)
        self.addNormalKillInfo(1, 0, 8, 0, 1)
        self.addAceKillInfo()
