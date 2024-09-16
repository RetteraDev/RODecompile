#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/dyingProxy.o
import BigWorld
import Sound
from Scaleform import GfxValue
import gameglobal
import gamelog
import gametypes
import ui
from uiProxy import SlotDataProxy
from guis import uiConst
from ui import gbk2unicode
from callbackHelper import Functor
from sfx import sfx
from sfx import screenEffect
from data import monster_bianshi_data as MBD
from data import item_data as ID
from cdata import font_config_data as FCD
SCREEN_EFFECT_TUPLE = ((gameglobal.EFFECT_TAG_BIANSHI_GREEN, [1006]),
 (gameglobal.EFFECT_TAG_BIANSHI_BLUE, [1007]),
 (gameglobal.EFFECT_TAG_BIANSHI_YELLOW, [1008]),
 (gameglobal.EFFECT_TAG_BIANSHI_RED, [1009]))

class DyingProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(DyingProxy, self).__init__(uiAdapter)
        self.modelMap = {'getNum': self.onGetNum,
         'getDuration': self.onGetDuration,
         'playMusic': self.onPlayMusic,
         'getTotalStage': self.onGetTotalStage}
        self.mediator = None
        self.comboMediator = None
        self.critiMediator = None
        self.rewardMediator = None
        self.noticeMediator = None
        self.num = None
        self.isOpen = False
        self.time = None
        self.stage = None
        self.fx = None
        self.entityId = 0
        self.effect = []
        self.stageEff = [13005,
         13007,
         13009,
         13011]
        self.endEff = [13006,
         13008,
         13010,
         13012]
        self.totalStage = 4
        self.bsData = None
        self.recordStage = None
        self.showFinal = False

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DYING:
            self.mediator = mediator
        elif widgetId == uiConst.WIDGET_BIANSHI_COMBO:
            self.comboMediator = mediator
        elif widgetId == uiConst.WIDGET_BIANSHI_CRITICAL:
            self.critiMediator = mediator
            self.critiMediator.Invoke('setVisible', GfxValue(False))
        elif widgetId == uiConst.WIDGET_BIANSHI_REWARD:
            self.rewardMediator = mediator
        elif widgetId == uiConst.WIDGET_BIANSHI_NOTICE:
            self.noticeMediator = mediator

    def onGetNum(self, *arg):
        return GfxValue(self.num)

    def onGetDuration(self, *arg):
        return GfxValue(self.time)

    def onPlayMusic(self, *arg):
        pass

    def onGetTotalStage(self, *arg):
        return GfxValue(self.totalStage)

    @ui.checkWidgetLoaded(uiConst.WIDGET_BIANSHI_NOTICE)
    def showNotice(self, notice):
        if self.noticeMediator:
            self.noticeMediator.Invoke('showNotice', GfxValue(notice))

    def show(self, extendId = 1, entityId = 0):
        ent = BigWorld.entities.get(entityId, None)
        if ent:
            ent.playBossMusic(False)
        Sound.playMusic('music/fb/boss_corpse_beat')
        self.fx = gameglobal.rds.sound.playFx('fx/effect/boss_blood', BigWorld.player().position, True, BigWorld.player())
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DYING)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BIANSHI_COMBO)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BIANSHI_CRITICAL)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BIANSHI_REWARD)
        self.showNotice('enter')
        self.isOpen = True
        self.stage = None
        self.entityId = entityId
        self.bsData = MBD.data.get(extendId, {})
        if self.bsData:
            self.time = self.bsData[0]['time']
        else:
            self.time = 0
        self.totalStage = len(MBD.data[extendId])
        self.showFinal = False
        self.recordStage = None
        screenEffect.startEffects(SCREEN_EFFECT_TUPLE[0][0], SCREEN_EFFECT_TUPLE[0][1], False, BigWorld.player())
        if self.effect:
            for item in self.effect:
                item.stop()

        if ent:
            self.effect = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, [ent.getBasicEffectLv(),
             ent.getBasicEffectPriority(),
             ent.model,
             self.stageEff[0],
             sfx.EFFECT_UNLIMIT])
            for key, id in enumerate(gameglobal.rds.ui.teamComm.memberId):
                hitNum = ent.dyingAtkDict.get(id, 0)
                gameglobal.rds.ui.teamComm.setHit(id, hitNum)

    def close(self, isShowNotice = False):
        ent = BigWorld.entities.get(self.entityId, None)
        if isShowNotice and ent:
            if ent.life == gametypes.LIFE_DEAD:
                self.showNotice('success')
            else:
                self.showNotice('fail')
        if self.stage:
            screenEffect.delEffect(SCREEN_EFFECT_TUPLE[self.stage - 1][0])
        else:
            screenEffect.delEffect(SCREEN_EFFECT_TUPLE[0][0])
        if self.fx:
            Sound.stopFx(self.fx)
            self.fx = None
        Sound.stopMusic()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DYING)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BIANSHI_COMBO)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BIANSHI_CRITICAL)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BIANSHI_REWARD)
        gameglobal.rds.ui.teamComm.endHit()
        self.isOpen = False
        if self.effect:
            for item in self.effect:
                item.stop()

        if self.recordStage and self.recordStage < len(self.endEff) and self.endEff[self.recordStage] and not self.showFinal:
            self.showFinal = True
            if ent:
                self.effect = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (ent.getBasicEffectLv(),
                 ent.getBasicEffectPriority(),
                 ent.model,
                 self.endEff[self.recordStage],
                 sfx.EFFECT_UNLIMIT,
                 gameglobal.EFFECT_LAST_TIME))

    def hit(self, num):
        Sound.playSimple('hit')
        if self.mediator != None:
            self.mediator.Invoke('setHit', GfxValue(num))

    def thump(self):
        if self.mediator != None:
            self.mediator.Invoke('thump')

    def shakeCamera(self, shakeId):
        pass

    def setTeamHit(self, stage, num, maxNum, totalHit, hasBonus = False):
        if self.comboMediator != None:
            if self.stage != stage:
                if self.stage != None:
                    Sound.playSimple('bonus_a')
                    BigWorld.callback(1, Functor(Sound.playSimple, 'bonus_b'))
                    self.comboMediator.Invoke('showFire')
                    if self.effect:
                        for item in self.effect:
                            item.stop()

                    ent = BigWorld.entities.get(self.entityId, None)
                    self.recordStage = self.stage
                    if ent and self.recordStage:
                        self.effect = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, [ent.getBasicEffectLv(),
                         ent.getBasicEffectPriority(),
                         ent.model,
                         self.stageEff[self.recordStage],
                         sfx.EFFECT_UNLIMIT])
                    screenEffect.delEffect(SCREEN_EFFECT_TUPLE[self.stage - 1][0])
                else:
                    screenEffect.delEffect(SCREEN_EFFECT_TUPLE[0][0])
                self.stage = stage
                if self.stage != 1:
                    self.shakeCamera(6)
                screenEffect.startEffects(SCREEN_EFFECT_TUPLE[self.stage - 1][0], SCREEN_EFFECT_TUPLE[self.stage - 1][1], False, BigWorld.player())
            else:
                maxHit = self.bsData[self.totalStage - 1]['hitRange'][1]
                if totalHit >= maxHit:
                    self.stage = self.totalStage
                    self.recordStage = self.stage
                    if self.effect:
                        for item in self.effect:
                            item.stop()

                    ent = BigWorld.entities.get(self.entityId, None)
                    if ent:
                        self.effect = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (ent.getBasicEffectLv(),
                         ent.getBasicEffectPriority(),
                         ent.model,
                         self.endEff[self.recordStage - 1],
                         sfx.EFFECT_UNLIMIT))
            self.comboMediator.Invoke('setBloodScale', (GfxValue(num), GfxValue(maxNum)))
            if hasBonus:
                self.comboMediator.Invoke('showBombFire')
                Sound.playSimple('boss_blood_effect')

    def showCritical(self):
        if self.critiMediator != None:
            self.critiMediator.SetVisible(True)
            self.critiMediator.Invoke('showCritical')

    def showReward(self, key, itemId):
        gamelog.debug('wy:showReward', key)
        if self.rewardMediator != None:
            arr = self.movie.CreateArray()
            obj = self.movie.CreateArray()
            itemData = ID.data.get(itemId, {})
            if itemData:
                quality = itemData.get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                obj.SetMember('iconPath', GfxValue(uiConst.ITEM_ICON_IMAGE_RES_40 + str(itemData['icon']) + '.dds'))
                arr.SetElement(0, obj)
                arr.SetElement(1, GfxValue(color))
                arr.SetElement(2, GfxValue(gbk2unicode(itemData['name'])))
                self.rewardMediator.Invoke('showReward', (GfxValue(key), arr))

    def getSlotID(self, key):
        idCon, idItem = key.split('.')
        return (0, int(idItem[4:]))

    def clearWidget(self):
        self.mediator = None
        self.comboMediator = None
        self.critiMediator = None
        self.rewardMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DYING)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BIANSHI_COMBO)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BIANSHI_CRITICAL)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BIANSHI_REWARD)

    def reset(self):
        self.num = None
        self.isOpen = False
        self.time = None
        self.stage = None
        self.fx = None
        self.entityId = 0
        self.effect = []
        self.totalStage = 4
        self.bsData = None
        self.recordStage = None
        self.showFinal = False
