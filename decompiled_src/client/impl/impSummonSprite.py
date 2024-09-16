#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impSummonSprite.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gamelog
import logicInfo
import gametypes
import const
import Sound
import utils
import SummonedSprite
from guis import ui
from guis import uiUtils
from guis import uiConst
from helpers import cgPlayer
from guis import events
from appSetting import SoundSettingObj
from helpers.eventDispatcher import Event
from callbackHelper import Functor
from data import sys_config_data as SCD
from data import formula_client_data as FCD
from data import prop_data as PD
from data import summon_sprite_skin_data as SSSD
from data import summon_sprite_foot_dust_data as SSFDD
from data import summon_sprite_info_data as SSID
from data import summon_sprite_data as SPD
from data import sprite_upgrade_data as SUD
from cdata import game_msg_def_data as GMDD

class ImpSummonSprite(object):
    spriteBaseArgNames = ('lv', 'famiEffLv', 'growthRatio', 'aptitudePw', 'aptitudeAgi', 'aptitudeSpr', 'aptitudePhy', 'aptitudeInt', 'famiExp', 'famiMaxExp', 'familiar')
    spriteBasePropEnhVarName = ('baseMhpEnhRatio', 'basePhyAtkEnhRatio', 'baseMagAtkEnhRatio', 'basePhyDefEnhRatio', 'baseMagDefEnhRatio')

    def summonSpriteUpdate(self, nextIndex, updateDict, isNewFromItem, isNewFromQuest):
        """
        \xe6\x95\xb4\xe4\xb8\xaa\xe6\x88\x98\xe7\x81\xb5\xe4\xbf\xa1\xe6\x81\xaf\xe7\x9a\x84\xe5\x90\x8c\xe6\xad\xa5\xef\xbc\x8c\xe5\x8f\xaf\xe8\x83\xbd\xe6\x98\xaf1\xe4\xb8\xaa\xe4\xb9\x9f\xe5\x8f\xaf\xe8\x83\xbd\xe6\x98\xaf\xe5\xa4\x9a\xe4\xb8\xaa\xe6\x88\x98\xe7\x81\xb5
        updateDict \xe6\x95\xb0\xe6\x8d\xae\xe7\xbb\x93\xe6\x9e\x84\xe4\xb8\xba { index : spriteDict } \xe8\x80\x8c spriteDict \xe6\x98\xaf Sprite \xe7\x9a\x84\xe5\xb1\x9e\xe6\x80\xa7\xe5\xad\x97\xe5\x85\xb8\xe6\x88\x96 None\xef\xbc\x88\xe8\xa1\xa8\xe7\xa4\xba\xe5\x88\xa0\xe9\x99\xa4\xef\xbc\x89
        """
        gamelog.debug('@yj summonSpriteUpdate', nextIndex)
        for index, v in updateDict.iteritems():
            if not v and index in self.summonSpriteList:
                rmSpriteDict = self.summonSpriteList.pop(index)
                gameglobal.rds.ui.actionbar.refreshSummonedSprite(index)
                gameglobal.rds.ui.summonedWarSpriteMine.removeSpriteSucc(index)
                gameglobal.rds.ui.summonedWarSpriteLunhuiItems.turnItemsSucc(index)
                if rmSpriteDict and rmSpriteDict.get('spriteId', None):
                    spriteId = rmSpriteDict.get('spriteId', None)
                    if spriteId in self.summonSpriteSkin:
                        self.summonSpriteSkin[spriteId].curUseDict.pop(index, None)
                    if spriteId in self.summonSpriteFootDust:
                        self.summonSpriteFootDust[spriteId].curUseDict.pop(index, None)
                    self.spriteChats.onDeleteSprite(index)
                continue
            if v:
                self.summonSpriteList[index] = v
                gameglobal.rds.ui.actionbar.refreshSummonedSprite(index)
            if v and isNewFromItem:
                spriteId = v.get('spriteId', 0)
                name = v.get('name', '')
                p = BigWorld.player()
                everSignedSpriteIds = list(p.spriteExtraDict.get('everSignedSpriteIds', set()))
                if spriteId not in everSignedSpriteIds:
                    self.spritePlayMovie(spriteId, name, index)
                else:
                    self.openSummonedWarSprite(index)
            elif v and isNewFromQuest:
                self.openSummonedWarSprite(index)

        if self.summonSpriteListCache:
            self.summonSpriteDictUpdate(self.summonSpriteListCache)
            self.summonSpriteListCache = {}
        self._refreshSpriteBasePropTipsData(updateDict)
        gameglobal.rds.ui.summonedWarSprite.refreshInfo()
        gameglobal.rds.ui.summonedWarSpriteMine.checkSpriteHungry()
        if self.summonSpriteList and not gameglobal.rds.ui.summonedSpriteUnitFrameV2.widget:
            gameglobal.rds.ui.summonedSpriteUnitFrameV2.show()
        e = Event(events.EVENT_SUMMON_SPRITE_LIST_CHANGED, (nextIndex, updateDict))
        gameglobal.rds.ui.dispatchEvent(e)

    def spritePlayMovie(self, spriteId, name, index):
        global cgMovie
        cgName = SSID.data.get(spriteId, {}).get('playMovieName', '')
        if not cgName:
            return
        p = BigWorld.player()
        p.ap.stopMove()
        p.ap.forceAllKeysUp()
        p.lockKey(gameglobal.KEY_POS_UI, False)
        BigWorld.worldDrawEnabled(False)
        cgMovie = cgPlayer.CGPlayer()
        config = {'position': (0, 0, 0),
         'w': 2,
         'h': 2,
         'loop': False,
         'callback': Functor(self.callBackPlayMovieEnd, name)}
        cgMovie.playMovie(cgName, config)
        Sound.enableMusic(False)
        p.base.signNewSprite(spriteId)
        self.openSummonedWarSprite(index)

    def callBackPlayMovieEnd(self, name):
        global cgMovie
        Sound.enableMusic(True)
        if cgMovie:
            cgMovie.endMovie()
            cgMovie = None
        p = BigWorld.player()
        p.unlockKey(gameglobal.KEY_POS_UI)
        p.showGameMsg(GMDD.data.SPRITE_PALY_MOVIE_END_DESC, (name,))

    def openSummonedWarSprite(self, index):
        gameglobal.rds.ui.summonedWarSprite.show(uiConst.WAR_SPRITE_TAB_INDEX0, index)

    def startSummonSprite(self, index, spriteId):
        gamelog.debug('@yj startSummonSprite', index, spriteId)

    def summonSpriteDictUpdate(self, updateDicts):
        """
        \xe5\xbf\x85\xe9\xa1\xbb\xe4\xbf\x9d\xe8\xaf\x81\xe8\xbf\x99\xe4\xb8\xaa\xe6\x88\x98\xe7\x81\xb5\xe7\x9a\x84\xe6\x95\xb0\xe6\x8d\xae\xe6\x98\xaf\xe5\xb7\xb2\xe7\xbb\x8f\xe5\xad\x98\xe5\x9c\xa8\xe7\x9a\x84
            updateDicts \xe7\xbb\x93\xe6\x9e\x84\xef\xbc\x9a {index : { key: value }}
        """
        gamelog.debug('@yj summonSpriteDictUpdate', updateDicts)
        for index, updateDict in updateDicts.iteritems():
            if index in self.summonSpriteList:
                for k, v in updateDict.iteritems():
                    if k in self.summonSpriteList[index] and isinstance(v, dict):
                        self.summonSpriteList[index][k].update(v)
                        gameglobal.rds.ui.summonedWarSpriteMine.checkSpriteHungry()
                    else:
                        self.summonSpriteList[index][k] = v

            else:
                if index not in self.summonSpriteListCache:
                    self.summonSpriteListCache[index] = {}
                for k, v in updateDict.iteritems():
                    if k in self.summonSpriteListCache[index] and isinstance(v, dict):
                        self.summonSpriteListCache[index][k].update(v)
                    else:
                        self.summonSpriteListCache[index][k] = v

            if updateDict.has_key('propsReRand'):
                gameglobal.rds.ui.summonedWarSpriteReRandom.updateSpriteInfo(index)
            if updateDict.has_key('propsLunhui'):
                gameglobal.rds.ui.summonedWarSpriteLunhui.updateSpriteLunhui(index)

        self._refreshSpriteBasePropTipsData(updateDicts)
        gameglobal.rds.ui.summonedWarSprite.refreshInfo()
        gameglobal.rds.ui.summonedSpriteUnitFrameV2.initAwakeSkill()
        e = Event(events.EVENT_SUMMON_SPRITE_INFO_CHANGED, updateDicts)
        gameglobal.rds.ui.dispatchEvent(e)

    def onSummonedSprite(self, isCalledOut, objId, index, calledbackReason):
        gamelog.debug('@zhangkuo onSummonedSprite', isCalledOut, objId, index, calledbackReason)
        if isCalledOut:
            self.spriteObjId = objId
            self.spriteBattleIndex = index
            self.updateLastSummonedSpriteIndex(index)
            gameglobal.rds.ui.summonedSpriteUnitFrameV2.initAwakeSkill()
        else:
            if not self.spriteBattleIndex:
                return
            if getattr(self, 'inCombat', False):
                if calledbackReason in (gametypes.SSPRITE_DISMISS_ACTIVE, gametypes.SSPRITE_DISMISS_PASSIVE):
                    self.spriteBattleCallBackList.append(self.spriteBattleIndex)
                    gameglobal.rds.ui.summonedWarSpriteMine.updateSpriteLifeState()
            self.updateLastSummonedSpriteIndex(self.spriteBattleIndex)
            self.spriteObjId = 0
            self.spriteBattleIndex = 0
        gameglobal.rds.ui.summonedWarSpriteMine.updateSpriteBattleState(index)
        gameglobal.rds.ui.summonedWarSpriteMine.checkSpriteHungry()
        gameglobal.rds.ui.actionbar.refreshSummonedSprite(index)
        gameglobal.rds.ui.zmjSpriteBuff.afterSummonedSprite()

    def updateLastSummonedSpriteIndex(self, index):
        self.lastSpriteBattleIndex = index
        gameglobal.rds.ui.summonedSpriteUnitFrameV2.refreshLastSpriteIcon()

    def onReRandomSummonSpritePropDone(self, index):
        pass

    def onAbandonSpriteCleverForItemDone(self, index):
        gamelog.debug('@xzh onAbandonSpriteCleverForItemDone', index)
        self.summonSpriteList[index].pop('propsReRand', None)
        gameglobal.rds.ui.summonedWarSpriteReRandom.hideNewMC()

    def onSubmitReRandomPropDone(self, index):
        gamelog.debug('@yj onReRandomSummonSpritePropDone', index)
        self.summonSpriteList[index].pop('propsReRand', None)
        gameglobal.rds.ui.summonedWarSpriteReRandom.hideNewMC()
        self.showGameMsg(GMDD.data.SUMMON_SPRITE_RERANDOM_PROP_SUCC, ())

    def onSpriteBoneDone(self, index):
        gamelog.debug('@yj onSpriteBoneDone', index)
        self.showGameMsg(GMDD.data.SUMMON_SPRITE_USE_BONE_SUCC, ())
        gameglobal.rds.ui.summonedWarSpriteUp.refreshInfo()

    def onSpriteBoneWithdraw(self, index):
        gamelog.debug('@yj onSpriteBoneWithdraw', index)
        gameglobal.rds.ui.summonedWarSpriteUp.refreshInfo()

    def onGetSpritePropList(self, index, propList):
        props = {}
        for propId, value in propList.iteritems():
            props[PD.data.get(propId, {}).get('name', '')] = value

        p = BigWorld.player()
        props.update(p.summonSpriteVirtualBaseProps.get(index, {}))
        p.summonSpriteProps[index] = props
        gamelog.debug('@yj ImpSummonSprite.onGetSpritePropList', index, props)
        e = Event(events.EVENT_SPRITE_PROPS_CHANGED, index)
        gameglobal.rds.ui.dispatchEvent(e)

    def _refreshSpriteBasePropTipsData(self, updateDicts):
        if not updateDicts:
            return
        else:
            p = BigWorld.player()
            for index, updateDict in updateDicts.iteritems():
                if not updateDict:
                    continue
                needRefresh = False
                if updateDict.has_key('skillEnhBaseProp'):
                    needRefresh = True
                if updateDict.has_key('props'):
                    for var in self.spriteBaseArgNames:
                        if var in updateDict.get('props', {}):
                            needRefresh = True

                if not needRefresh:
                    continue
                props = p.summonSpriteVirtualBaseProps.get(index, {})
                p = BigWorld.player()
                argDict = {}
                for key, value in p.summonSpriteList[index]['props'].iteritems():
                    if key in self.spriteBaseArgNames:
                        argDict[key] = value

                for i, val in enumerate(p.summonSpriteList[index]['skillEnhBaseProp']):
                    argDict[self.spriteBasePropEnhVarName[i]] = val

                spriteBaseSetValFormualParams = SCD.data.get('spriteBaseSetValFormualParams', ())
                for name, formulaId, virtualId in spriteBaseSetValFormualParams:
                    argDict[name] = 0
                    func = FCD.data.get(formulaId, {}).get('formula', None)
                    if func:
                        props[virtualId] = int(func(argDict))
                    else:
                        props[virtualId] = 0

                p.summonSpriteVirtualBaseProps[index] = props
                if p.summonSpriteProps.has_key(index):
                    p.summonSpriteProps[index].update(props)

            return

    def syncSpriteAccessory(self, templateId, accSpriteIndexDic, learnedTemplate):
        """
        \xe4\xb8\x8a\xe7\xba\xbf\xe6\x97\xb6\xe5\x90\x8c\xe6\xad\xa5summonedSpriteAccessory\xe7\x9a\x84\xe4\xbf\xa1\xe6\x81\xaf\xef\xbc\x8c\xe5\xb9\xb6\xe6\x81\xa2\xe5\xa4\x8d\xe4\xb8\x8b\xe7\xba\xbf\xe5\x89\x8d\xe7\x9a\x84\xe9\x99\x84\xe8\xba\xab
        :param templateId: \xe9\x98\xb5\xe6\xb3\x95id
        :param accSpriteIndexDic: \xe9\x99\x84\xe8\xba\xab\xe4\xbd\x8d\xe5\x92\x8c\xe6\x88\x98\xe7\x81\xb5index\xe7\x9a\x84\xe5\xad\x97\xe5\x85\xb8 
        :param learnedTemplate: \xe5\xb7\xb2\xe5\xad\xa6\xe4\xb9\xa0\xe7\x9a\x84\xe9\x98\xb5\xe6\xb3\x95id\xe5\x88\x97\xe8\xa1\xa8 
        :return: 
        """
        gamelog.debug('@xzh synSpriteAccessory templateId:{0} accSpriteIndexDic:{1} ' + 'learnedTemplate:{2}'.format(templateId, accSpriteIndexDic, learnedTemplate))
        self.summonedSpriteAccessory.learnedTemplate = learnedTemplate
        self.summonedSpriteAccessory.templateId = templateId

    def onLearnAccessoryTemplate(self, templateId):
        """
        \xe6\x88\x90\xe5\x8a\x9f\xe5\xad\xa6\xe4\xb9\xa0\xe9\x98\xb5\xe6\xb3\x95\xe4\xb9\xa6\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param templateId: \xe6\x9c\xac\xe6\xac\xa1\xe5\xad\xa6\xe5\x88\xb0\xe7\x9a\x84\xe9\x98\xb5\xe6\xb3\x95id
        :return: 
        """
        gamelog.debug('@xzh onLearnAccessoryTemplate', templateId)
        self.summonedSpriteAccessory.appendTemplate(templateId)

    def onChangeAccessoryTemplateId(self, templateId):
        gamelog.debug('@yj onChangeAccessoryTemplateId', templateId)
        self.summonedSpriteAccessory.templateId = templateId
        gameglobal.rds.ui.summonedWarSpriteGuard.updateRightGuardMc()

    def onEquipSummonedSpriteAccessory(self, accessoryPart, accessoryDict):
        """
            spriteIndex: \xe6\x88\x98\xe7\x81\xb5\xe5\x9c\xa8\xe4\xba\xba\xe8\xba\xab\xe4\xb8\x8a\xe7\x9a\x84index
            accessoryPart: \xe6\x88\x98\xe7\x81\xb5\xe9\x99\x84\xe8\xba\xab\xe4\xbd\x8d\xe7\x9a\x84Index
        """
        gamelog.debug('@yj onEquipSummonedSpriteAccessory', accessoryPart, accessoryDict)
        self.summonedSpriteAccessory[accessoryPart].update(accessoryDict)
        gameglobal.rds.ui.summonedWarSpriteGuard.addSpriteGuardSlot(accessoryDict['spriteIndex'], accessoryPart)
        gameglobal.rds.ui.actionbar.refreshSummonedSprite(accessoryDict['spriteIndex'])

    def onUnEquipSummonedSpriteAccessory(self, accessoryPart):
        """
        Args:
            accessoryPart: \xe6\x88\x98\xe7\x81\xb5\xe9\x99\x84\xe8\xba\xab\xe4\xbd\x8d\xe7\x9a\x84Index
        """
        gamelog.debug('@yj onUnEquipSummonedSpriteAccessory', accessoryPart)
        spriteIdx = self.summonedSpriteAccessory[accessoryPart]['spriteIndex']
        self.summonedSpriteAccessory[accessoryPart].clear()
        gameglobal.rds.ui.summonedWarSpriteGuard.removeSpriteGuardSlot(accessoryPart)
        gameglobal.rds.ui.actionbar.refreshSummonedSprite(spriteIdx)

    def onUseFoodExpRes(self, spriteIndex, lvExp, famiExp, famiEffLv):
        gamelog.debug('@yj onUnEquipSummonedSpriteAccessory', spriteIndex, lvExp, famiExp)
        gameglobal.rds.ui.summonedWarSpriteMine.playSoundAndAction('spriteSoundList3', 'spriteActionList3', 'spriteActionPro3')
        gameglobal.rds.ui.summonedWarSpriteMine.updateFeedMoreFoodMc()
        if famiEffLv > 0:
            self.showGameMsg(GMDD.data.SUMMON_SPRITE_FAMI_SPECIAL_FOOD_SUCC, ())

    def onLearnedSpriteTextBook(self, index, slot, newRefID, oldRefID):
        gamelog.debug('@yj onLearnedSpriteTextBook', index, slot)
        gameglobal.rds.ui.summonedWarSpriteMine.showLearnedSpriteSkillMsg(index, newRefID, oldRefID)
        gameglobal.rds.ui.summonedWarSpriteMine.refreshLearnedSkillSfx(index, slot)

    def onUsedSpriteTextBookReplaceSkill(self, index, slot, newRefID, oldRefID):
        gameglobal.rds.ui.summonedWarSpriteMine.updateSpriteSkillReplaceSucc(index, slot, newRefID, oldRefID)

    def onUsedSpriteAwakeSkill(self, manualSkillID):
        gamelog.debug('m.l@ImpSummonSprite.onUsedSpriteAwakeSkill', manualSkillID)

    def onSpriteAwakeSkillNextTime(self, cdTime):
        logicInfo.spriteManualSkillCoolDown = cdTime + utils.getNow()
        gamelog.debug('m.l@ImpSummonSprite.onSpriteAwakeSkillNextTime', logicInfo.spriteManualSkillCoolDown)
        gameglobal.rds.ui.summonedSpriteUnitFrameV2.updateManualSkillCooldown()

    def onUsedSpriteBackSkill(self, backSkillID):
        gamelog.debug('@smj onUsedSpriteBackSkill', backSkillID)

    def onSpriteBackSkillNextTime(self, nextTime):
        logicInfo.spriteTeleportSkillCoolDown = nextTime
        gamelog.debug('m.l@ImpSummonSprite.onSpriteBackSkillNextTime', nextTime)
        gameglobal.rds.ui.summonedSpriteUnitFrameV2.updateTeleportCooldown()

    def onSynSummonSpriteSkinAndFootDust(self, skinData, footDustData):
        """
        \xe7\x99\xbb\xe5\xbd\x95\xe6\x97\xb6\xe6\x88\x98\xe7\x81\xb5\xe7\x9a\xae\xe8\x82\xa4\xe5\x92\x8c\xe6\xad\xa5\xe5\xb0\x98\xe6\x95\xb0\xe6\x8d\xae\xe5\x90\x8c\xe6\xad\xa5
        :param skinData: 
        :param footDustData: 
        """
        self.summonSpriteSkin = skinData
        self.summonSpriteFootDust = footDustData

    def onUnlockSummonSpriteSkin(self, spriteId, skinId, tExpire):
        """
        \xe8\xa7\xa3\xe9\x94\x81\xef\xbc\x88\xe8\x8e\xb7\xe5\xbe\x97\xef\xbc\x89\xe6\x88\x98\xe7\x81\xb5\xe7\x9a\xae\xe8\x82\xa4\xe5\x9b\x9e\xe8\xb0\x83
        :param spriteId: \xe6\x88\x98\xe7\x81\xb5id
        :param skinId: \xe7\x9a\xae\xe8\x82\xa4id
        """
        gamelog.debug('@xzh onUnlockSummonSpriteSkin', spriteId, skinId)
        if tExpire:
            self.summonSpriteSkin[spriteId].tempDict[skinId] = tExpire
        else:
            self.summonSpriteSkin[spriteId].hasList.append(skinId)
        self.showGameMsg(GMDD.data.SUMMON_SPRITE_SKIN_UNLOCK_SUCC, (SSSD.data.get(skinId, {}).get('skinName', ''),))
        gameglobal.rds.ui.summonedWarSpriteMine.changeSkinProxy.refreshWidget()

    def onUnlockSummonSpriteFootDust(self, spriteId, footDustId, tExpire):
        """
        \xe8\xa7\xa3\xe9\x94\x81\xef\xbc\x88\xe8\x8e\xb7\xe5\xbe\x97\xef\xbc\x89\xe6\x88\x98\xe7\x81\xb5\xe6\xad\xa5\xe5\xb0\x98\xe5\x9b\x9e\xe8\xb0\x83
        :param spriteId: \xe6\x88\x98\xe7\x81\xb5id
        :param footDustId: \xe6\xad\xa5\xe5\xb0\x98id
        """
        if tExpire:
            self.summonSpriteFootDust[spriteId].tempDict[footDustId] = tExpire
        else:
            self.summonSpriteFootDust[spriteId].hasList.append(footDustId)
        self.showGameMsg(GMDD.data.SUMMON_SPRITE_DUST_UNLOCK_SUCC, (SSFDD.data.get(footDustId, {}).get('footDustName', ''),))
        gameglobal.rds.ui.summonedWarSpriteMine.changeSkinProxy.refreshWidget()

    def onRemoveSummonSpriteSkin(self, spriteId, removeSkinId, newUseDict):
        """
        \xe5\x88\xa0\xe9\x99\xa4\xe4\xb8\x80\xe4\xb8\xaa\xe6\x88\x98\xe7\x81\xb5\xe7\x9a\xae\xe8\x82\xa4
        :param spriteId: 
        :param removeSkinId: 
        :param newUseDict:\xe5\x88\xa0\xe9\x99\xa4\xe5\x90\x8e\xe7\x94\xa8\xe5\x93\xaa\xe4\xb8\x80\xe4\xb8\xaa\xe7\x9a\xae\xe8\x82\xa4\xef\xbc\x8c\xe7\x8e\xb0\xe5\x9c\xa8\xe6\x98\xaf\xe6\x8d\xa2\xe5\x9b\x9e\xe9\xbb\x98\xe8\xae\xa4\xe7\x9a\xae\xe8\x82\xa4 
        """
        skinInfo = self.summonSpriteSkin[spriteId]
        if removeSkinId in skinInfo.hasList:
            skinInfo.hasList.remove(removeSkinId)
        if skinInfo.curUseDict != newUseDict:
            skinInfo.curUseDict = newUseDict

    def onExpireSummonSpriteSkin(self, spriteId, expireSkinId, newUseDict):
        """
        \xe6\x88\x98\xe7\x81\xb5\xe9\x99\x90\xe6\x97\xb6\xe7\x9a\xae\xe8\x82\xa4\xe8\xbf\x87\xe6\x9c\x9f
        :param spriteId:
        :param expireSkinId:
        :param newUseDict:
        :return:
        """
        skinInfo = self.summonSpriteSkin[spriteId]
        if expireSkinId in skinInfo.tempDict:
            skinInfo.tempDict.pop(expireSkinId)
        if skinInfo.curUseDict != newUseDict:
            skinInfo.curUseDict = newUseDict
        gameglobal.rds.ui.summonedWarSpriteMine.changeSkinProxy.refreshWidget()

    def onRemoveSummonSpriteFootDust(self, spriteId, removeFootDustId, newUseDict):
        """
        \xe5\x88\xa0\xe9\x99\xa4\xe4\xb8\x80\xe4\xb8\xaa\xe6\x88\x98\xe7\x81\xb5\xe6\xad\xa5\xe5\xb0\x98
        :param spriteId: 
        :param removeFootDustId: 
        :param newUseDict: \xe5\x88\xa0\xe9\x99\xa4\xe5\x90\x8e\xe7\x94\xa8\xe5\x93\xaa\xe4\xb8\x80\xe4\xb8\xaa\xe6\xad\xa5\xe5\xb0\x98\xef\xbc\x8c\xe7\x8e\xb0\xe5\x9c\xa8\xe6\x98\xaf\xe6\x8d\xa2\xe5\x9b\x9e\xe9\xbb\x98\xe8\xae\xa4\xe6\xad\xa5\xe5\xb0\x98 
        """
        dustInfo = self.summonSpriteFootDust[spriteId]
        if removeFootDustId in dustInfo.hasList:
            dustInfo.hasList.remove(removeFootDustId)
        if dustInfo.curUseDict != newUseDict:
            dustInfo.curUseDict = newUseDict

    def onExpireSummonSpriteFootDust(self, spriteId, expireFootDustId, newUseDict):
        """
        \xe6\x88\x98\xe7\x81\xb5\xe9\x99\x90\xe6\x97\xb6\xe6\xad\xa5\xe5\xb0\x98\xe8\xbf\x87\xe6\x9c\x9f
        :param spriteId:
        :param expireFootDustId:
        :param newUseDict:
        :return:
        """
        dustInfo = self.summonSpriteFootDust[spriteId]
        if expireFootDustId in dustInfo.tempDict:
            dustInfo.tempDict.pop(expireFootDustId)
        if dustInfo.curUseDict != newUseDict:
            dustInfo.curUseDict = newUseDict
        gameglobal.rds.ui.summonedWarSpriteMine.changeSkinProxy.refreshWidget()

    def onUseSummonSpriteSkinSucc(self, index, spriteId, skinId):
        """
        \xe4\xbd\xbf\xe7\x94\xa8\xef\xbc\x88\xe8\xa3\x85\xe5\xa4\x87\xef\xbc\x89\xe6\x88\x98\xe7\x81\xb5\xe7\x9a\xae\xe8\x82\xa4\xe5\x9b\x9e\xe8\xb0\x83
        :param index: \xe6\x88\x98\xe7\x81\xb5index
        :param spriteId: \xe6\x88\x98\xe7\x81\xb5id
        :param skinId: \xe7\x9a\xae\xe8\x82\xa4id
        """
        self.summonSpriteSkin[spriteId].curUseDict[index] = skinId
        gameglobal.rds.ui.summonedWarSpriteMine.updateSpriteSkinOrFootDust()
        p = BigWorld.player()
        if p.summonedSpriteInWorld:
            p.summonedSpriteInWorld.changeSpriteSkinModelSucc()

    def onUseSummonSpriteFootDustSucc(self, index, spriteId, dustId):
        """
        \xe4\xbd\xbf\xe7\x94\xa8\xef\xbc\x88\xe8\xa3\x85\xe5\xa4\x87\xef\xbc\x89\xe6\x88\x98\xe7\x81\xb5\xe6\xad\xa5\xe5\xb0\x98\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param index: \xe6\x88\x98\xe7\x81\xb5index
        :param spriteId: \xe6\x88\x98\xe7\x81\xb5id
        :param dustId: \xe6\xad\xa5\xe5\xb0\x98id
        """
        self.summonSpriteFootDust[spriteId].curUseDict[index] = dustId
        gameglobal.rds.ui.summonedWarSpriteMine.updateSpriteSkinOrFootDust()

    def _hasSpriteSkin(self, spriteId, skinId):
        if self.summonSpriteSkin.has_key(spriteId) and skinId in self.summonSpriteSkin[spriteId].totalList:
            return True
        return False

    def _hasSpriteFootDust(self, spriteId, footDustId):
        if self.summonSpriteFootDust.has_key(spriteId) and footDustId in self.summonSpriteFootDust[spriteId].totalList:
            return True
        return False

    def buySpriteSkin(self, spriteId, skinId, payType):
        """
        \xe8\xb4\xad\xe4\xb9\xb0\xe6\x88\x98\xe7\x81\xb5\xe7\x9a\xae\xe8\x82\xa4
        :param spriteId: 
        :param skinId: 
        :param payType:\xe6\x94\xaf\xe4\xbb\x98\xe6\x96\xb9\xe5\xbc\x8f 1-\xe4\xba\x91\xe5\x88\xb8\xef\xbc\x8c2-\xe4\xba\x91\xe5\xb8\x81\xef\xbc\x8c3-\xe4\xba\x91\xe5\x9e\x82\xe7\xa7\xaf\xe5\x88\x86
        """
        if self._hasSpriteSkin(spriteId, skinId):
            self.showGameMsg(GMDD.data.SUMMON_SPRITE_SKIN_ALREADY_HAD, ())
            return
        else:
            if payType == gametypes.SPRITE_COST_TYPE_BIND_CASH:
                needBindCash = SSSD.data.get((spriteId, skinId), {}).get('bindCashPrice', None)
                if not needBindCash or self.bindCash < needBindCash:
                    return
            elif payType == gametypes.SPRITE_COST_TYPE_CASH:
                needCash = SSSD.data.get((spriteId, skinId), {}).get('cashPrice', None)
                if not needCash or self.cash < needCash:
                    return
            elif payType == gametypes.SPRITE_COST_TYPE_YUNCHUI_SCORE:
                needFame = SSSD.data.get((spriteId, skinId), {}).get('yunchuiScorePrice', None)
                if not needFame or self.fame.get(const.YUN_CHUI_JI_FEN_FAME_ID, 0) < needFame:
                    return
            self.cell.buySummonSpriteSkin(spriteId, skinId, payType)
            return

    def buySpriteFootDust(self, spriteId, footDustId, payType):
        """
        \xe8\xb4\xad\xe4\xb9\xb0\xe6\x88\x98\xe7\x81\xb5\xe6\xad\xa5\xe5\xb0\x98
        :param spriteId: 
        :param footDustId: 
        :param payType:\xe6\x94\xaf\xe4\xbb\x98\xe6\x96\xb9\xe5\xbc\x8f 1-\xe4\xba\x91\xe5\x88\xb8\xef\xbc\x8c2-\xe4\xba\x91\xe5\xb8\x81\xef\xbc\x8c3-\xe4\xba\x91\xe5\x9e\x82\xe7\xa7\xaf\xe5\x88\x86
        """
        if self._hasSpriteFootDust(spriteId, footDustId):
            self.showGameMsg(GMDD.data.SUMMON_SPRITE_DUST_ALREADY_HAD, ())
            return
        else:
            if payType == gametypes.SPRITE_COST_TYPE_BIND_CASH:
                needBindCash = SSFDD.data.get((spriteId, footDustId), {}).get('bindCashPrice', None)
                if not needBindCash or self.bindCash < needBindCash:
                    return
            elif payType == gametypes.SPRITE_COST_TYPE_CASH:
                needCash = SSFDD.data.get((spriteId, footDustId), {}).get('cashPrice', None)
                if not needCash or self.cash < needCash:
                    return
            elif payType == gametypes.SPRITE_COST_TYPE_YUNCHUI_SCORE:
                needFame = SSFDD.data.get((spriteId, footDustId), {}).get('yunchuiScorePrice', None)
                if not needFame or self.fame.get(const.YUN_CHUI_JI_FEN_FAME_ID, 0) < needFame:
                    return
            self.cell.buySummonSpriteFootDust(spriteId, footDustId, payType)
            return

    def onUpdateClientExpFamiliar(self, index, newExp, newFamiExp):
        if index not in self.summonSpriteList:
            return
        oldExp = self.summonSpriteList[index].get('props', {}).get('exp', 0)
        oldFamiExp = self.summonSpriteList[index].get('props', {}).get('famiExp', 0)
        if oldExp == newExp and oldFamiExp == newFamiExp:
            return
        self.summonSpriteList[index]['props']['exp'] = newExp
        self.summonSpriteList[index]['props']['famiExp'] = newFamiExp
        gameglobal.rds.ui.summonedWarSpriteMine.updateSpriteExpBar()
        gameglobal.rds.ui.summonedWarSpriteMine.updateSpritePrivityBar()

    def onPreSummonSpriteJuexing(self, index, isFirst, awakeSkillRefId):
        """
        \xe6\x98\xaf\xe5\x90\xa6\xe6\x98\xaf\xe7\xac\xac\xe4\xb8\x80\xe5\x8f\xaa\xe8\xa7\x89\xe9\x86\x92\xe7\x9a\x84\xe6\xad\xa4\xe7\xb1\xbb\xe6\x88\x98\xe7\x81\xb5
        :param index: 
        :param isFirst:\xe6\x98\xaf\xe5\x90\xa6\xe6\x98\xaf\xe9\xa6\x96\xe6\xac\xa1\xe8\xa7\x89\xe9\x86\x92 
        :param awakeSkillRefId:\xe8\xa7\x89\xe9\x86\x92\xe5\x90\x8e\xe7\x9a\x84\xe8\xa7\x89\xe9\x86\x92\xe6\x8a\x80\xef\xbc\x88\xe6\x88\x98\xe7\x81\xb5\xe6\x8a\x80\xe8\x83\xbd\xe8\xa1\xa8\xe9\x87\x8c\xe9\x9d\xa2\xe7\x9a\x84id\xef\xbc\x89
        """
        gamelog.debug('@xzh onPreSummonSpriteJuexing', index, isFirst, awakeSkillRefId)
        gameglobal.rds.ui.summonedWarSpriteAwake.show(index, isFirst, awakeSkillRefId)
        gameglobal.rds.ui.summonedWarSpriteMine.updateAwakeBtnRedPot()
        gameglobal.rds.ui.summonedWarSpriteMine.updateSpriteItemRedPot()
        gameglobal.rds.ui.summonedWarSprite.updateSpriteTab0RedPot()

    def onSpriteJuexingSucc(self, index, spriteId):
        juexingSkinId = 0
        unlockTypeJunxing = 3
        for sId, skinId in SSSD.data:
            if sId == spriteId:
                unlockType = SSSD.data.get((sId, skinId), {}).get('unlockType', ())
                for typeV in unlockType:
                    if typeV == unlockTypeJunxing:
                        juexingSkinId = skinId
                        break

                if juexingSkinId:
                    break

        p = BigWorld.player()
        if juexingSkinId:
            p.base.useSummonSpriteSkin(index, spriteId, juexingSkinId)
        if p.summonedSpriteInWorld:
            gameglobal.rds.ui.summonedSpriteUnitFrameV2.initAwakeSkill()
        gameglobal.rds.ui.summonedWarSpriteMine.updateAwakeBtnRedPot()
        gameglobal.rds.ui.summonedWarSpriteMine.updateSpriteItemRedPot()
        gameglobal.rds.ui.summonedWarSprite.updateSpriteTab0RedPot()

    def updateTriderSpriteState(self, isMoving):
        """
        \xe6\x9b\xb4\xe6\x96\xb0\xe5\xa4\x9a\xe4\xba\xba\xe5\x9d\x90\xe9\xaa\x91\xe4\xb8\x8a\xe9\x98\x9f\xe5\x91\x98\xe7\x9a\x84\xe5\x9d\x90\xe9\xaa\x91\xe7\x8a\xb6\xe6\x80\x81
        :param isMoving:\xe6\x98\xaf\xe5\x90\xa6\xe5\x9c\xa8\xe7\xa7\xbb\xe5\x8a\xa8
        """
        p = BigWorld.player()
        if p.summonedSpriteInWorld:
            if self.id == p.tride.header or getattr(p.getCoupleRideHorse(), 'id', 0) == self.id:
                p.spriteOwnerMoving(isMoving)

    def updateSummonSpriteExtraDict(self, updateExtraDict):
        """
        \xe6\x9b\xb4\xe6\x96\xb0\xe9\xa2\x9d\xe5\xa4\x96\xe7\x9a\x84\xe5\x86\x85\xe5\xae\xb9\xe5\xad\x97\xe5\x85\xb8
        :param updateExtraDict: \xe4\xb8\x8d\xe4\xb8\x80\xe5\xae\x9a\xe6\x98\xaf\xe5\x85\xa8\xe9\x87\x8f\xe6\x9b\xb4\xe6\x96\xb0\xef\xbc\x8c\xe5\x8f\xaa\xe6\x9c\x89\xe9\x9c\x80\xe8\xa6\x81\xe6\x9b\xb4\xe6\x96\xb0\xe7\x9a\x84key\xe6\x89\x8d\xe5\x9c\xa8\xe8\xbf\x99\xe4\xb8\xaa\xe5\xad\x97\xe5\x85\xb8\xe9\x87\x8c\xe9\x9d\xa2\xef\xbc\x8c\xe6\x89\x80\xe4\xbb\xa5\xe5\x90\x8e\xe9\x9d\xa2\xe7\x94\xa8\xe7\x9a\x84\xe6\x98\xafupdate
        """
        gamelog.debug('@xzh updateSummonSpriteExtraDict', updateExtraDict)
        for k, v in updateExtraDict.iteritems():
            if k in self.spriteExtraDict and isinstance(v, dict):
                self.spriteExtraDict[k].update(v)
            else:
                self.spriteExtraDict[k] = v

        gameglobal.rds.ui.summonedWarSpriteExploreState.refreshInfo()
        gameglobal.rds.ui.summonedWarSpriteExploreState.checkExploreTimeEndPush()
        gameglobal.rds.ui.summonedWarSpriteExplorePlan.refreshInfo()
        gameglobal.rds.ui.summonedWarSpriteItemSubmit.refreshInfo()
        gameglobal.rds.ui.summonedWarSpriteItemRefresh.refreshInfo()
        gameglobal.rds.ui.summonedWarSpriteExplore.refreshInfo()
        if updateExtraDict.has_key('pendingList'):
            gameglobal.rds.ui.summonedWarSpriteMine.refreshInfo()

    def onSpriteGetSkillWhenLvUp(self, index, skillIdList):
        gamelog.debug('@xzh onSpriteGetSkillWhenLvUp', index, skillIdList)
        for _, skillId in skillIdList:
            gameglobal.rds.ui.summonedWarSpriteSkillNotify.show(index, skillId)

    def checkSpriteCanPlaySound(self, spriteObjId):
        if SoundSettingObj.isMuteOtherSprite():
            return self.summonedSpriteInWorld and self.summonedSpriteInWorld.id == spriteObjId
        return True

    def getSpriteInWorld(self):
        if self == BigWorld.player():
            return self.summonedSpriteInWorld
        else:
            return BigWorld.entities.get(self.spriteObjId, None)

    def openTrainSprite(self):
        trainingList = list(self.spriteExtraDict.get('trainingIndexSet', set()))

    def openExploreSprite(self):
        if not gameglobal.rds.configData.get('enableExploreSprite', False):
            return
        p = BigWorld.player()
        p.cell.exploreSpriteSyncData()
        exploringList = list(p.spriteExtraDict['exploreSprite'].exploringIndexSet)
        if exploringList:
            gameglobal.rds.ui.summonedWarSpriteExploreState.show(exploringList)
        else:
            gameglobal.rds.ui.summonedWarSpriteExplore.show()

    def onLunhuiSummonSpriteDone(self, index, isBonus):
        gamelog.debug('@xzh onLunhuiSummonSpriteDone', index)
        gameglobal.rds.ui.summonedWarSpriteLunhui.updateSpriteLunhui(index)
        gameglobal.rds.ui.summonedWarSpriteLunhui.appearBonusPlayEffect(index, isBonus)

    def onSubmitLunhuiDone(self, index):
        gamelog.debug('@xzh onSubmitLunhuiDone', index)
        self.summonSpriteList[index].pop('propsLunhui', None)
        gameglobal.rds.ui.summonedWarSpriteLunhui.updateSpriteLunhui(index)

    def onSpriteFamiCoverSucc(self, inIndex, outIndex):
        """
        \xe4\xba\xb2\xe5\xaf\x86\xe8\xa6\x86\xe7\x9b\x96\xe6\x88\x90\xe5\x8a\x9f\xe5\x90\x8e\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param inIndex:\xe8\xbd\xac\xe5\x85\xa5\xe6\x88\x98\xe7\x81\xb5index 
        :param outIndex: \xe8\xbd\xac\xe5\x87\xba\xe6\x88\x98\xe7\x81\xb5index
        """
        self.showGameMsg(GMDD.data.SUMMON_SPRITE_FAMI_COUVER_SUCC, ())

    def onSyncSpriteChats(self, spriteChats):
        self.spriteChats = spriteChats

    def onSetSpriteChat(self, index, chatNo, text):
        self.spriteChats.setChatText(index, chatNo, text)
        gameglobal.rds.ui.summonedWarSpriteChat.saveChatSucc(index, chatNo, text)

    def onResetSpriteChat(self, index, chatNo):
        self.spriteChats.resetChatText(index, chatNo)
        gameglobal.rds.ui.summonedWarSpriteChat.resetChatSucc(index, chatNo)

    def onResetSpriteManuallyAddedPropPoint(self, index):
        self.showGameMsg(GMDD.data.SUMMON_SPRITE_ADD_PROP_POINT_SUCC, ())

    def onSpriteLvUp(self, index, newLv):
        spriteName = self.summonSpriteList[index]['name']
        self.showGameMsg(GMDD.data.SUMMON_SPRITE_LV_UP_SUCC, (spriteName, newLv))

    def onSpriteFamiLvUp(self, index, newFamiLv, newFamiEffLv):
        spriteName = self.summonSpriteList[index]['name']
        self.showGameMsg(GMDD.data.SUMMON_SPRITE_FAMI_LV_UP_SUCC, (spriteName, newFamiEffLv))

    def onForgetSpriteLearnedSkill(self, index, forgetSkillRefId):
        self.showGameMsg(GMDD.data.SUMMON_SPRITE_FORGET_SKILL_SUCC, ())

    def constructSpriteInfo(self, index):
        self.base.constructSpriteInfo(index)

    def onGetSpriteLink(self, linkStr):
        gamelog.debug('@ljh get sprite hyper link string:', linkStr)
        if linkStr is None or linkStr[:6] != 'sprite':
            return
        else:
            linkInfos = linkStr[len('sprite'):].split(':')
            if len(linkInfos) < 3:
                return
            NUID = ':'.join(linkInfos[:-2])
            spriteInfoNUID = str(utils.strToUint64(NUID))
            link = "<font color=\'%s\'>[<a href = \'event:sprite%s\'><u>%s</u></a>]</font>" % (linkInfos[-1], spriteInfoNUID, linkInfos[-2])
            gameglobal.rds.ui.sendLink(link)
            return

    def onExploreSpriteOpenHelpPanelCheck(self, isOK, askerGbId, index, itemId, itemNum, groupId, daySecond, roleName):
        gamelog.debug('@hqx_onExploreSpriteOpenHelpPanelCheck', isOK)
        if isOK:
            gameglobal.rds.ui.summonedWarSpriteExploreHelp.show(int(askerGbId), int(index), int(itemId), int(itemNum), int(groupId), int(daySecond), roleName)

    def afterExploreSpriteHelpItem(self, isOK):
        if isOK:
            gameglobal.rds.ui.summonedWarSpriteExploreHelp.hide()

    def onTransferSpriteLearnSkills(self, sourceSpriteIndex, destSpriteIndex, destSpriteLearnSkillIdList):
        """
        \xe8\x8b\xb1\xe7\x81\xb5\xe8\xbd\xac\xe7\xa7\xbb\xe5\x90\x8e\xe5\xa4\xa9\xe6\x8a\x80\xe8\x83\xbd\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param sourceSpriteIndex: \xe6\xba\x90\xe8\x8b\xb1\xe7\x81\xb5\xe7\x9a\x84index
        :param destSpriteIndex: \xe7\x9b\xae\xe6\xa0\x87\xe8\x8b\xb1\xe7\x81\xb5\xe7\x9a\x84index
        :param destSpriteLearnSkillIdList: \xe7\x9b\xae\xe6\xa0\x87\xe8\x8b\xb1\xe7\x81\xb5\xe8\xbd\xac\xe7\xa7\xbb\xe5\x90\x8e\xe7\x9a\x84\xe6\x8a\x80\xe8\x83\xbdID\xe5\x88\x97\xe8\xa1\xa8
        :return:
        """
        gamelog.debug('@zhangkuo onTransferSpriteLearnSkills: sourceSpriteIndex, destSpriteIndex, destSpriteLearnSkillIdList', sourceSpriteIndex, destSpriteIndex, destSpriteLearnSkillIdList)
        gameglobal.rds.ui.summonedWarSpriteSkillTransfer.transferSpriteSkillSuccess(sourceSpriteIndex)

    def onUpgradeSprite(self, spriteIndex, upgradeStage, rareLv):
        """
        \xe8\x8b\xb1\xe7\x81\xb5\xe8\xbf\x9b\xe9\x98\xb6\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param spriteIndex: \xe8\x8b\xb1\xe7\x81\xb5\xe7\x9a\x84index
        :param upgradeStage: \xe8\x8b\xb1\xe7\x81\xb5\xe8\xbf\x9b\xe9\x98\xb6\xe4\xb9\x8b\xe5\x90\x8e\xe7\x9a\x84\xe9\x98\xb6\xe6\x95\xb0
        :param rareLv: \xe8\x8b\xb1\xe7\x81\xb5\xe8\xbf\x9b\xe9\x98\xb6\xe4\xb9\x8b\xe5\x90\x8e\xe7\x9a\x84\xe7\xa8\x80\xe6\x9c\x89\xe5\xba\xa6
        :return:
        """
        gamelog.debug('@zhangkuo onUpgradeSprite [spriteIndex][upgradeStage][rareLv]', spriteIndex, upgradeStage, rareLv)
        spriteName = self.summonSpriteList[spriteIndex]['name']
        spriteId = self.summonSpriteList[spriteIndex]['spriteId']
        subData = SUD.data.get((spriteId, upgradeStage), {})
        upGradeName = subData.get('upGradeNmae', '')
        self.showGameMsg(GMDD.data.SUMMON_SPRITE_UP_GRADE_SUCC, (spriteName, upGradeName))
        gameglobal.rds.ui.summonedWarSpriteUpGrade.refreshInfo()

    def onSpriteRareTransfer(self, isOK):
        """
        \xe8\xb6\x85\xe8\x8b\xb1\xe7\x81\xb5\xe8\xbd\xac\xe6\x8d\xa2\xe5\x9b\x9e\xe8\xb0\x83
        :param isOK: True: \xe8\xb6\x85\xe8\x8b\xb1\xe7\x81\xb5\xe8\xbd\xac\xe6\x8d\xa2\xe6\x88\x90\xe5\x8a\x9f, False: \xe8\xb6\x85\xe8\x8b\xb1\xe7\x81\xb5\xe8\xbd\xac\xe6\x8d\xa2\xe5\xa4\xb1\xe8\xb4\xa5
        :return:
        """
        gamelog.debug('@zmm onSpriteRareTransfer ')
        if isOK:
            gameglobal.rds.ui.summonedWarSpriteRareTransfer.transferSuccess()

    def onUsedSpriteTextBookReplaceOldSkill(self, index, slot, newRefID, oldRefID):
        skillProxy = gameglobal.rds.ui.summonedWarSpriteMine.skillProxy
        if skillProxy:
            skillProxy.usedSkillBesetSucc(index, slot, newRefID, oldRefID)

    def onSpriteExploreResetDaily(self):
        gameglobal.rds.ui.summonedWarSpriteExplore.resetRecordState()

    def onApplySpritePrayLunhui(self, index, bonusId):
        gameStrings.TEXT_IMPSUMMONSPRITE_796
        gamelog.debug('@zhangkuo onApplySpritePrayLunhui [index][bonusId]', index, bonusId)
        gameglobal.rds.ui.summonedWarSpriteLunhui.updateSpriteLunhui(index)
        gameglobal.rds.ui.summonedWarSpriteLunhui.appearBonusPlayEffect(index, True)

    def onUnlockPendingListSlot(self, index):
        gameStrings.TEXT_IMPSUMMONSPRITE_802
        gamelog.debug('@zhangkuo onUnlockPendingListSlot [index]', index)
        gameglobal.rds.ui.summonedWarSpriteFight.refreshInfo()

    def onInsertPendingSprite(self, index, pos):
        gameStrings.TEXT_IMPSUMMONSPRITE_807
        gamelog.debug('@zhangkuo onInsertPendingSprite [index][pos]', index, pos)
        gameglobal.rds.ui.summonedWarSpriteFight.insertSpriteSuccess(index, pos)

    def onResetPendingListSlot(self, index):
        """\xe6\x9c\x80\xe5\x90\x8e\xe4\xb8\x80\xe4\xb8\xaa\xe5\xa4\x87\xe6\x88\x98\xe6\xa7\xbd\xe4\xbd\x8d\xe7\x94\xb1\xe4\xba\x8eVIP\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x88\xb0\xe6\x9c\x9f\xe5\xa4\xb1\xe6\x95\x88"""
        gamelog.debug('@zhangkuo onResetPendingListSlot')
        gameglobal.rds.ui.summonedWarSpriteFight.refreshInfo()

    def onRemovePendingSprite(self, index, pos):
        """\xe7\xa7\xbb\xe9\x99\xa4\xe6\x8c\x87\xe5\xae\x9a\xe6\xa7\xbd\xe4\xbd\x8d\xe7\x9a\x84\xe5\xa4\x87\xe6\x88\x98\xe8\x8b\xb1\xe7\x81\xb5"""
        gamelog.debug('@zhangkuo onRemovePendingSprite', index, pos)
        gameglobal.rds.ui.summonedWarSpriteFight.removeSpriteSuccess(index, pos)

    def onExpandSpriteSlot(self, curSpriteSlotNum):
        """\xe6\x88\x90\xe5\x8a\x9f\xe6\x89\xa9\xe5\xb1\x95\xe8\x8b\xb1\xe7\x81\xb5\xe6\xa7\xbd\xe4\xbd\x8d\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83"""
        gamelog.debug('@zhangkuo onExpandSpriteSlot [curSpriteSlotNum]', curSpriteSlotNum)
        self.spriteExtraDict['spriteSlotNum'] = curSpriteSlotNum
        gameglobal.rds.ui.summonedWarSpriteMine.refreshInfo()

    def onGetSptiteItemStateData(self, data):
        gamelog.debug('yedawang### onGetSptiteItemStateData', data)
        gameglobal.rds.ui.zmjSpriteBuff.setSptiteItemStateData(data)

    def onQuerySpriteSummonProps(self, index, propList):
        """\xe8\x8b\xb1\xe7\x81\xb5\xe5\x87\xba\xe6\x88\x98\xe5\xb1\x9e\xe6\x80\xa7,\xe5\x90\x8conGetSpritePropList"""
        props = {}
        for propId, value in propList.iteritems():
            props[PD.data.get(propId, {}).get('name', '')] = value

        p = BigWorld.player()
        props.update(p.summonSpriteVirtualBaseProps.get(index, {}))
        p.summonSpritePropsWithFami[index] = props
        e = Event(events.EVENT_SPRITE_PROPS_CHANGED, index)
        gameglobal.rds.ui.dispatchEvent(e)

    def updateSpriteSEOrder(self, orderDict):
        gamelog.debug('xjw## updateSpriteSEOrder', orderDict)
        self.summonSpriteSEOrder = orderDict
        gameglobal.rds.ui.tianZhaoSummonedSpriteSkillSet.onSpriteChange()
