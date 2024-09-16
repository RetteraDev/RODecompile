#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impSummonSpriteWingWorld.o
import wingWorldUtils
import gameglobal
import utils
import gamelog
from guis import uiConst
from callbackHelper import Functor
from data import wing_world_config_data as WWCD

class ImpSummonSpriteWingWorld(object):

    def onGetSpriteWingWorldRes(self, slots, resDictCurrent, unlockedSlots, specialRareLv, specialCntDay, maxSpeed, resTotalDay):
        """
        \xe4\xb8\x8a\xe7\xba\xbf\xe6\x97\xb6/\xe9\x87\x8d\xe8\xa6\x81\xe6\x93\x8d\xe4\xbd\x9c\xe6\x97\xb6\xef\xbc\x8c\xe5\x85\xa8\xe9\x87\x8f\xe5\x8f\x91\xe9\x80\x81\xe6\x88\x98\xe7\x81\xb5\xe7\xbf\xbc\xe4\xb8\x96\xe7\x95\x8c\xe8\xb5\x84\xe6\xba\x90\xe6\x95\xb0\xe6\x8d\xae
        :param slots: {slotIndex:spriteIndex, ...} \xe8\xbf\x99\xe4\xb8\xaa\xe7\xbb\x93\xe6\x9e\x84\xe5\x92\x8c\xe6\x9c\x8d\xe5\x8a\xa1\xe7\xab\xaf\xe7\x9a\x84\xe4\xb8\x8d\xe4\xb8\x80\xe6\xa0\xb7
        :param resDictCurrent: {resId:resNum, ...}
        :param unlockedSlots: set([1,2,3,...])
        :return: 
        """
        self.spriteWingWorldRes.spriteInSlots = slots
        self.spriteWingWorldRes.resDictCurrent = resDictCurrent
        self.spriteWingWorldRes.unlockedSlots = unlockedSlots
        self.spriteWingWorldRes.specialRareLv = specialRareLv
        self.spriteWingWorldRes.specialCntDay = specialCntDay
        self.spriteWingWorldRes.maxSpeed = maxSpeed
        self.spriteWingWorldRes.resTotalDay = resTotalDay
        self.spriteWingWorldRes.fameCurrent = wingWorldUtils.getFameByResourceCollectVal(sum(resDictCurrent.itervalues()))
        collectPanel = gameglobal.rds.ui.wingWorldResource.collectPanel
        if collectPanel:
            collectPanel.onShow()

    def onSpriteWingWorldResSyncRes(self, resDictCurrent, resTotalDay):
        """
        \xe6\xaf\x8f\xe9\x9a\x9410\xe5\x88\x86\xe9\x92\x9f\xe7\xbb\x93\xe7\xae\x97\xe4\xb8\x80\xe6\xac\xa1\xe8\xb5\x84\xe6\xba\x90/\xe6\x8f\x90\xe4\xba\xa4\xe4\xb9\x8b\xe5\x90\x8e\xe7\x9a\x84\xe8\xb5\x84\xe6\xba\x90\xe9\x87\x8f\xe5\x88\xb7\xe6\x96\xb0
        :param resDictCurrent: 
        """
        self.spriteWingWorldRes.resDictCurrent = resDictCurrent
        self.spriteWingWorldRes.fameCurrent = wingWorldUtils.getFameByResourceCollectVal(sum(resDictCurrent.itervalues()))
        self.spriteWingWorldRes.resTotalDay = resTotalDay
        collectPanel = gameglobal.rds.ui.wingWorldResource.collectPanel
        if collectPanel:
            collectPanel.onShow()

    def onApplySpriteWingWorldResCollectSucc(self, slotIndex, spriteIndex):
        """
        \xe6\x88\x90\xe5\x8a\x9f\xe5\xb0\x86\xe6\x88\x98\xe7\x81\xb5\xe6\x8c\x82\xe6\x9c\xba\xe5\x88\xb0\xe6\x8c\x87\xe5\xae\x9a\xe5\x9d\x91\xe4\xbd\x8d
        :param slotIndex: 
        :param spriteIndex: 
        """
        self.spriteWingWorldRes.spriteInSlots[slotIndex] = spriteIndex
        collectPanel = gameglobal.rds.ui.wingWorldResource.collectPanel
        if collectPanel:
            collectPanel.onShow()

    def onCancelSpriteWingWorldResCollectSucc(self, slotIndex):
        """
        \xe6\x88\x90\xe5\x8a\x9f\xe5\x8f\x96\xe6\xb6\x88\xe4\xba\x86\xe6\x88\x98\xe7\x81\xb5\xe6\x8c\x82\xe6\x9c\xba
        :param slotIndex: 
        """
        self.spriteWingWorldRes.spriteInSlots.pop(slotIndex, None)
        collectPanel = gameglobal.rds.ui.wingWorldResource.collectPanel
        if collectPanel:
            collectPanel.onShow()

    def onSpriteWingWorldResSlotUnlockChange(self, unlockedSlots):
        """
        \xe8\xa7\xa3\xe9\x94\x81\xe5\x9d\x91\xe4\xbd\x8d\xe5\x8f\x91\xe7\x94\x9f\xe5\x8f\x98\xe5\x8c\x96\xe6\x97\xb6
        :param unlockedSlots:\xe6\x96\xb0\xe7\x9a\x84\xe5\x9d\x91\xe4\xbd\x8dindex\xe9\x9b\x86\xe5\x90\x88
        :return: 
        """
        self.spriteWingWorldRes.unlockedSlots = unlockedSlots
        collectPanel = gameglobal.rds.ui.wingWorldResource.collectPanel
        if collectPanel:
            collectPanel.onShow()

    def onSpriteWingWorldResRandomEvent(self, eIds):
        """
        \xe6\x88\x98\xe7\x81\xb5\xe6\x8c\x82\xe6\x9c\xba\xe8\xb5\x84\xe6\xba\x90\xe6\x8f\x90\xe4\xba\xa4\xe6\x97\xb6\xe8\xa7\xa6\xe5\x8f\x91\xe7\x9a\x84\xe9\x9a\x8f\xe6\x9c\xba\xe4\xba\x8b\xe4\xbb\xb6
        :param eIds:\xe4\xba\x8b\xe4\xbb\xb6id\xe5\x88\x97\xe8\xa1\xa8 
        """
        collectPanel = gameglobal.rds.ui.wingWorldResource.collectPanel
        if collectPanel:
            collectPanel.updateCollectResRandom(eIds, utils.getNow())

    def onSpriteWingWorldResSyncSpecialRareLvAndSpeed(self, rareLv, maxSpeed):
        """
        \xe6\x9b\xb4\xe6\x96\xb0\xe5\xa5\x87\xe9\x81\x87\xe7\xad\x89\xe7\xba\xa7\xef\xbc\x88\xe7\x9b\xae\xe5\x89\x8d\xe4\xb8\xba1,2,3\xe6\x98\xaf\xe5\x9c\xa8\xe8\x8b\xb1\xe7\x81\xb5\xe6\x8c\x96\xe7\x9f\xbf\xe9\x9a\x8f\xe6\x9c\xba\xe4\xba\x8b\xe4\xbb\xb6\xe8\xa1\xa8\xe9\x87\x8c\xe9\x9d\xa2\xe9\x85\x8d\xe7\x9a\x84\xef\xbc\x89\xef\xbc\x8c\xe6\x9c\x80\xe5\xa4\xa7\xe9\x80\x9f\xe5\xba\xa6
        :param rareLv: 
        :param maxSpeed: 
        """
        self.spriteWingWorldRes.specialRareLv = rareLv
        self.spriteWingWorldRes.maxSpeed = maxSpeed
        collectPanel = gameglobal.rds.ui.wingWorldResource.collectPanel
        if collectPanel:
            collectPanel.onShow()

    def onSpriteWingWorldResNotifyNotFullWhenLogon(self, slotNum, spriteNum):
        """
        \xe4\xb8\x8a\xe7\xba\xbf\xe6\x97\xb6\xe6\xa3\x80\xe6\x9f\xa5\xe6\x8c\x82\xe6\x9c\xba\xe5\x9d\x91\xe4\xbd\x8d\xe5\x92\x8c\xe6\x94\xbe\xe7\xbd\xae\xe8\x8b\xb1\xe7\x81\xb5\xe6\x95\xb0\xef\xbc\x8c\xe6\xb2\xa1\xe6\x94\xbe\xe6\xbb\xa1\xe6\x97\xb6\xe6\x9c\x89\xe6\xad\xa4\xe5\x9b\x9e\xe8\xb0\x83
        :param slotNum: \xe5\xbd\x93\xe5\x89\x8d\xe5\x9d\x91\xe4\xbd\x8d\xe6\x95\xb0
        :param spriteNum: \xe5\xbd\x93\xe5\x89\x8d\xe6\x8c\x82\xe6\x9c\xba\xe8\x8b\xb1\xe7\x81\xb5\xe6\x95\xb0
        """
        if self.isInBlanceArenaWaitRoom():
            return
        if uiConst.MESSAGE_TYPE_SPRITE_SLOTS_NOT_FULL not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_SPRITE_SLOTS_NOT_FULL)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_SPRITE_SLOTS_NOT_FULL, {'click': self.onPushNotFullSpriteClick})

    def onPushNotFullSpriteClick(self):
        gameglobal.rds.ui.wingWorld.show(uiConst.WING_WORLD_TAB_RESOURCE)
        if uiConst.MESSAGE_TYPE_SPRITE_SLOTS_NOT_FULL in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_SPRITE_SLOTS_NOT_FULL)

    def onSpriteWingWorldResNotifyWhenRemoveBySys(self):
        """
        \xe6\x8c\x82\xe6\x9c\xba\xe8\x8b\xb1\xe7\x81\xb5\xe8\xa2\xab\xe7\xb3\xbb\xe7\xbb\x9f\xe6\x94\xb6\xe5\x9b\x9e\xe6\x97\xb6\xef\xbc\x8c\xe6\x9c\x89\xe6\xad\xa4\xe5\x9b\x9e\xe8\xb0\x83
        """
        if self.isInBlanceArenaWaitRoom():
            return
        if uiConst.MESSAGE_TYPE_CLEAR_SPRITE_SLOTS not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_CLEAR_SPRITE_SLOTS)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_CLEAR_SPRITE_SLOTS, {'click': self.onPushClearSpriteClick})

    def onPushClearSpriteClick(self):
        msg = WWCD.data.get('clearSpriteSlotsMsg', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(gameglobal.rds.ui.wingWorld.show, uiConst.WING_WORLD_TAB_RESOURCE))
        if uiConst.MESSAGE_TYPE_CLEAR_SPRITE_SLOTS in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_CLEAR_SPRITE_SLOTS)
