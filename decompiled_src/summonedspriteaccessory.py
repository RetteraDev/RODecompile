#Embedded file name: /WORKSPACE/data/entities/common/summonedspriteaccessory.o
import BigWorld
from userDictType import UserDictType
import const
import gametypes
import gamelog
import formula
import utils
from gameclass import StateInfo
from collections import Iterable
from data import prop_data as PD
from data import sys_config_data as SCD
from data import summon_sprite_info_data as SSID
from cdata import summon_sprite_accessory_data as SSAD
from cdata import prop_ref_reverse_data as PRRD
from cdata import game_msg_def_data as GMDD
from data import summon_sprite_skill_data as SSSD
from data import summon_sprite_accessory_skill_data as SSAKD
from data import state_data as SD
from cdata import prop_def_data as PDD
if BigWorld.component in ('base', 'cell'):
    import gameconfig
    import commcalc
    import gameconst
    import gameengine
    import serverlog
    import riskControl
    import sprite
    from spriteGrowth import SpriteGrowth
AccessorySpritePropIds = frozenset([PDD.data.PROPERTY_MHP,
 PDD.data.PROPERTY_PHY_ATK_ADD,
 PDD.data.PROPERTY_MAG_ATK_ADD,
 PDD.data.PROPERTY_EQUIP_PHY_DEF,
 PDD.data.PROPERTY_PHY_DEF_ADD,
 PDD.data.PROPERTY_EQUIP_MAG_DEF,
 PDD.data.PROPERTY_MGI_DEF_ADD])

class SummonedSpriteAccessory(UserDictType):
    """
    \xd5\xbd\xc1\xe9\xb8\xbd\xc9\xed/\xca\xd8\xbb\xa4/\xc8\xeb\xbb\xea \xb5\xc4\xca\xfd\xbe\xdd\xbd\xe1\xb9\xb9
    \xb1\xbe\xc0\xe0\xd0\xcd\xca\xc7\xbc\xcc\xb3\xd0\xd3\xda\xd7\xd6\xb5\xe4\xa3\xac\xca\xfd\xbe\xdd\xbd\xe1\xb9\xb9\xca\xc7 { part : data { props: xxx, spriteIndex: yyy, score: zzz, spriteIndex: www, spriteUuid: vvv} }
    \xc6\xe4\xd6\xd0 part \xca\xc7\xb4\xd3 1 \xb5\xbd SUMMONED_SPRITE_ACCESSORY_COUNT \xb5\xc4\xd5\xfb\xca\xfd
    """
    ACCESSORY_DUMMY_ENTITY_ID_OFFSET = 1000000000
    KEYS_SEND_TO_CLIENT = ('props', 'spriteIndex', 'spriteId', 'score')

    def __init__(self):
        super(SummonedSpriteAccessory, self).__init__()
        for i in xrange(const.SUMMONED_SPRITE_ACCESSORY_COUNT):
            self[i + 1] = {}

        self.templateId = 0
        self.learnedTemplate = []

    def _getSendToClientDict(self, accessoryPart):
        res = {}
        for key in self[accessoryPart].keys():
            if key in self.KEYS_SEND_TO_CLIENT:
                res[key] = self[accessoryPart][key]

        return res

    def isValid(self, part):
        return 0 < part <= const.SUMMONED_SPRITE_ACCESSORY_COUNT

    def hasEquiped(self):
        for i in xrange(const.SUMMONED_SPRITE_ACCESSORY_COUNT):
            if self[i + 1].has_key('spriteIndex'):
                return True

        return False

    def setTemplateId(self, owner, templateId, accSprites):
        gamelog.debug('@xzh templateId:{0} learnedTemplate:{1} accSprites:{2}'.format(templateId, self.learnedTemplate, accSprites))
        if templateId not in self.learnedTemplate:
            return
        self.templateId = templateId
        self.reEquipAllSummonedSprite(owner, accSprites)
        owner.client.onChangeAccessoryTemplateId(templateId)
        owner.client.showGameMsg(GMDD.data.CHANGE_ACCESSORY_TEMPLATE_SUCC, ())

    def _processDefaultData(self):
        if const.SUMMONED_SPRITE_ACCESSORY_DEFAULT_TEMPLATE not in self.learnedTemplate:
            self.learnedTemplate.append(const.SUMMONED_SPRITE_ACCESSORY_DEFAULT_TEMPLATE)
        if not self.templateId:
            self.templateId = const.SUMMONED_SPRITE_ACCESSORY_DEFAULT_TEMPLATE

    def transfer(self, owner):
        self._processDefaultData()
        owner.client.syncSpriteAccessory(self.templateId, self.getAccessorySpriteIndexDict(), self.learnedTemplate)
        for part, accessoryInfo in self.iteritems():
            spriteIndex = accessoryInfo.get('spriteIndex', None)
            if spriteIndex:
                owner.client.onEquipSummonedSpriteAccessory(part, self[part])
                owner.base.onEquipSummonedSpriteAccessory(spriteIndex, part)

        if not gameconfig.enableSummonedSprite() or not riskControl.checkFeature(None, gameconst.F_SPRITE_SHOUHU):
            return
        if self.hasEquiped():
            owner.base.restoreAccessorySkillEffectBase()

    def calcSpriteAccCombatScore(self):
        res = 0
        for part, accessoryInfo in self.iteritems():
            res += accessoryInfo.get('score', 0)

        return res

    def calcSpriteAccCombatScoreType(self):
        addTypes = [ accessoryInfo.get('scoreType', []) for accessoryInfo in self.itervalues() ]
        return formula.calcCombatScoreType([], [], addTypes, 0, const.COMBAT_SCORE_TYPE_OP_ADD)

    def _choseMaxValuePropId(self, propDict, srcPropIds):
        maxValue = -1
        retPropId = 0
        for propId in srcPropIds:
            propVal = propDict.get(propId, 0)
            if propVal > maxValue:
                maxValue = propVal
                retPropId = propId

        return retPropId

    def equipSummonedSprite(self, owner, spriteDict, accessoryPart, needCalc = True, needMsg = True):
        """
        \xd5\xbd\xc1\xe9\xb8\xbd\xc9\xed
        \xd5\xe2\xc0\xef\xbd\xf8\xd0\xd0\xc1\xcb\xd5\xbd\xc1\xe9\xb8\xbd\xc9\xed\xca\xfd\xbe\xdd\xbd\xe1\xb9\xb9\xd0\xde\xb8\xc4\xa1\xa2\xd6\xf7\xc8\xcb\xca\xf4\xd0\xd4\xb5\xc4\xd6\xd8\xd0\xc2\xbc\xc6\xcb\xe3
        \xbd\xab\xcd\xa8\xd6\xaabase\xba\xcdclient\xd5\xbd\xc1\xe9\xb5\xc4\xb8\xbd\xc9\xed
        :param owner:\xd6\xf7\xc8\xcb\xb5\xc4cellMailbox 
        :param spriteDict: \xd5\xbd\xc1\xe9\xca\xf4\xd0\xd4\xca\xfd\xbe\xdd\xbd\xe1\xb9\xb9
        :param accessoryPart: \xb8\xbd\xc9\xed\xce\xbb
        :param needCalc: \xca\xc7\xb7\xf1\xd0\xe8\xd2\xaa\xca\xf4\xd0\xd4\xbc\xc6\xcb\xe3\xa3\xa8\xd5\xeb\xb6\xd4\xbe\xc9\xca\xf4\xd0\xd4\xbc\xc6\xcb\xe3\xa3\xa9
        :param needMsg: \xca\xc7\xb7\xf1\xd0\xe8\xd2\xaa\xcc\xe1\xca\xbe\xd0\xc5\xcf\xa2\xa3\xa8\xc7\xf8\xb7\xd6\xca\xc7\xd6\xf7\xb6\xaf\xbb\xb9\xca\xc7\xb1\xbb\xb6\xaf\xb5\xc4\xb8\xbd\xc9\xed\xa3\xa9
        """
        if not self.isValid(accessoryPart):
            gameengine.reportCritical('@xzh equipSummonedSprite accessory Index Error.')
            return
        accessoryInfo = SSAD.data.get((self.templateId, accessoryPart, owner.school), None)
        if accessoryInfo is None:
            gameengine.reportCritical('@xzh equipSummonedSprite no accessoryInfo', self.templateId, accessoryPart)
            return
        if self[accessoryPart]:
            self.unEquipSummonedSprite(owner, accessoryPart)
        self[accessoryPart]['props'] = []
        accEnhRatio_p1 = spriteDict['skills']['accEnhRatio'] + 1
        accScore = 0
        accScoreType = [0,
         0,
         0,
         0]
        if gameconfig.enableCardSys():
            cardParams = owner._getCardSpecialEffectParam(gametypes.CARD_SE_SUMMON_SPRITE_ACCESSORY_ENH_BY_POS)
            for (accParts, addRatio), _ in cardParams:
                if accessoryPart in accParts:
                    accEnhRatio_p1 += addRatio

        if gameconfig.enableSpriteGrowth():
            s = sprite.Sprite()
            s.setPersistentData(spriteDict)
            spriteGrowth, isBalanced = owner.rebalanceSpriteGrowth('specials', s)
            specialDict = SpriteGrowth.getSpecials(s, spriteGrowth, ignoreSpecialSprite=isBalanced)
            if gameconst.SPRITE_GROWTH_SPECIAL_ACCESSORY_ENH in specialDict:
                for lv, info in specialDict[gameconst.SPRITE_GROWTH_SPECIAL_ACCESSORY_ENH]:
                    parts, addRatio = info
                    if accessoryPart in parts:
                        accEnhRatio_p1 += addRatio

        propDict = spriteDict.get('aPropCacheDict', {})
        for srcPropIds, dstPropId, ratio in accessoryInfo['spriteAbilitys']:
            if not isinstance(srcPropIds, Iterable):
                srcPropId = srcPropIds
            else:
                srcPropId = self._choseMaxValuePropId(propDict, srcPropIds)
            if srcPropId not in AccessorySpritePropIds:
                continue
            dstPropRef = PRRD.data.get(dstPropId, [0,
             0,
             0,
             0])[0]
            value = propDict.get(srcPropId, 0) * ratio * accEnhRatio_p1
            self[accessoryPart]['props'].append((dstPropRef, gametypes.DATA_TYPE_NUM, value))
            propScoreVal = PD.data.get(dstPropId, {}).get('unitValue', 0) * value
            accScore += propScoreVal
            unitValueType = PD.data.get(dstPropId, {}).get('unitValueType', [])
            accScoreType = formula.calcCombatScoreType(accScoreType, unitValueType, [], propScoreVal, const.COMBAT_SCORE_TYPE_OP_COEFF)

        disableSkillIds = []
        for eachSkill in spriteDict['skills']['learns']:
            if eachSkill['id']:
                disableSkillIds.extend(list(SSSD.data.get(eachSkill['id'], {}).get('disableLearnSkillRefIds', ())))

        spriteLearnSkillIds = [ eachSkill['id'] for eachSkill in spriteDict['skills']['learns'] if eachSkill['id'] and eachSkill['id'] not in disableSkillIds ]
        if spriteDict['skills']['trait']:
            spriteLearnSkillIds.append(spriteDict['skills']['trait'])
        if spriteLearnSkillIds:
            accScore += self._calcAddAccessorySkillEffect(owner, spriteDict['props'], spriteLearnSkillIds, accessoryPart)
        accScore = accScore * SCD.data.get('spriteAccScoreCoef', 0)
        accScoreType = formula.calcCombatScoreType(accScoreType, [], [], SCD.data.get('spriteAccScoreCoef', 0), const.COMBAT_SCORE_TYPE_OP_MUL)
        self[accessoryPart]['spriteIndex'] = spriteDict['index']
        self[accessoryPart]['spriteId'] = spriteDict['spriteId']
        self[accessoryPart]['spriteUuid'] = spriteDict['uuid']
        self[accessoryPart]['score'] = accScore
        self[accessoryPart]['scoreType'] = accScoreType
        self.applySummonedSpriteAccessory(owner, accessoryPart)
        needCalc and owner.calcAllProp(gameconst.CALC_ALL_PROP_SRC_SPRITE_ACCESS)
        owner.base.onEquipSummonedSpriteAccessory(spriteDict['index'], accessoryPart)
        owner.client.onEquipSummonedSpriteAccessory(accessoryPart, self._getSendToClientDict(accessoryPart))
        needMsg and owner.client.showGameMsg(GMDD.data.EQUIP_SPRITE_SUCC, ())
        if gameconfig.enableSpriteStatLog() and needCalc:
            serverlog.genSpriteAccessoryLog(owner, const.SUMMON_SPRITE_ACCESSORY_EQUIP)
        needCalc and owner.updateCombatScore((const.SPRITE_ACC_SCORE,))

    def unEquipSummonedSprite(self, owner, accessoryPart, needCalc = True, needMsg = True):
        """
        \xbd\xe2\xb3\xfd\xd5\xbd\xc1\xe9\xb8\xbd\xc9\xed
        \xd5\xe2\xc0\xef\xbd\xf8\xd0\xd0\xc1\xcb\xd5\xbd\xc1\xe9\xb8\xbd\xc9\xed\xca\xfd\xbe\xdd\xbd\xe1\xb9\xb9\xd0\xde\xb8\xc4\xa1\xa2\xd6\xf7\xc8\xcb\xca\xf4\xd0\xd4\xb5\xc4\xd6\xd8\xd0\xc2\xbc\xc6\xcb\xe3
        \xbd\xab\xcd\xa8\xd6\xaabase\xba\xcdclient\xd5\xbd\xc1\xe9\xb5\xc4\xbd\xe2\xb3\xfd\xb8\xbd\xc9\xed
        :param owner:\xd6\xf7\xc8\xcb\xb5\xc4cellMailbox
        :param accessoryPart: \xb8\xbd\xc9\xed\xce\xbb
        :param needCalc: \xca\xc7\xb7\xf1\xd0\xe8\xd2\xaa\xca\xf4\xd0\xd4\xbc\xc6\xcb\xe3\xa3\xa8\xd5\xeb\xb6\xd4\xbe\xc9\xca\xf4\xd0\xd4\xbc\xc6\xcb\xe3\xa3\xa9
        """
        self._calcRemoveAccessorySkillEffect(owner, accessoryPart)
        self.unApplySummonedSpriteAccessory(owner, accessoryPart)
        self[accessoryPart].clear()
        needCalc and owner.calcAllProp(gameconst.CALC_ALL_PROP_SRC_SPRITE_ACCESS)
        owner.base.onEquipSummonedSpriteAccessory(0, accessoryPart)
        owner.client.onUnEquipSummonedSpriteAccessory(accessoryPart)
        needMsg and owner.client.showGameMsg(GMDD.data.UNEQUIP_SPRITE_SUCC, ())
        if gameconfig.enableSpriteStatLog() and needCalc:
            serverlog.genSpriteAccessoryLog(owner, const.SUMMON_SPRITE_ACCESSORY_UNEQUIP)
        needCalc and owner.updateCombatScore((const.SPRITE_ACC_SCORE,))

    def replaceEquipSummonedSprite(self, owner, newSpriteDict, accessoryPart):
        """
        \xcc\xe6\xbb\xbb\xd6\xb8\xb6\xa8\xb8\xbd\xc9\xed\xce\xbb\xb5\xc4\xb8\xbd\xc9\xed\xd5\xbd\xc1\xe9
        \xd0\xe8\xd2\xaa\xb4\xab\xc8\xeb\xd0\xc2\xd5\xbd\xc1\xe9\xb5\xc4\xca\xf4\xd0\xd4\xca\xfd\xbe\xdd\xa3\xac\xbe\xc9\xb5\xc4\xb2\xbb\xd3\xc3
        :param owner: \xd6\xf7\xc8\xcb\xb5\xc4cellMailbox
        :param newSpriteDict: \xd0\xc2\xd5\xbd\xc1\xe9\xb5\xc4\xca\xf4\xd0\xd4\xca\xfd\xbe\xdd
        :param accessoryPart: \xb8\xbd\xc9\xed\xce\xbb
        """
        self.unEquipSummonedSprite(owner, accessoryPart, needCalc=False, needMsg=False)
        self.equipSummonedSprite(owner, newSpriteDict, accessoryPart, needCalc=False, needMsg=False)
        owner.calcAllProp(gameconst.CALC_ALL_PROP_SRC_SPRITE_ACCESS)
        owner.client.showGameMsg(GMDD.data.REPLACE_EQUIPED_SPRITE_SUCC, ())
        if gameconfig.enableSpriteStatLog():
            serverlog.genSpriteAccessoryLog(owner, const.SUMMON_SPRITE_ACCESSORY_UNEQUIP)
        owner.updateCombatScore((const.SPRITE_ACC_SCORE,))

    def reEquipSummonedSprite(self, owner, sprite, accessoryPart):
        gamelog.debug('@xzh reEquipSummonedSprite', sprite.index, accessoryPart)
        self.unEquipSummonedSprite(owner, accessoryPart, needCalc=False, needMsg=False)
        self.equipSummonedSprite(owner, sprite.getPersistentDict(), accessoryPart, needCalc=False, needMsg=False)
        owner.calcAllProp(gameconst.CALC_ALL_PROP_SRC_SPRITE_ACCESS)
        if gameconfig.enableSpriteStatLog():
            serverlog.genSpriteAccessoryLog(owner, const.SUMMON_SPRITE_ACCESSORY_UNEQUIP)
        owner.updateCombatScore((const.SPRITE_ACC_SCORE,))

    def reEquipAllSummonedSprite(self, owner, accSprites):
        """
        \xd6\xd8\xd0\xc2\xb8\xbd\xc9\xed\xcb\xf9\xd3\xd0\xd5\xbd\xc1\xe9\xa3\xa8\xd5\xf3\xb7\xa8\xc7\xd0\xbb\xbb\xd6\xae\xba\xf3\xa3\xa9
        :param owner: \xd6\xf7\xc8\xcb\xb5\xc4cellMailbox
        :param accSprites: \xcb\xf9\xd3\xd0\xd0\xe8\xd2\xaa\xb8\xbd\xc9\xed\xb5\xc4\xd5\xbd\xc1\xe9\xca\xf4\xd0\xd4\xca\xfd\xbe\xdd\xa3\xac\xd3\xc9\xd6\xf7\xc8\xcb\xb5\xc4base\xb4\xab\xb9\xfd\xc0\xb4
        """
        for i in xrange(const.SUMMONED_SPRITE_ACCESSORY_COUNT):
            if self[i + 1].has_key('spriteIndex'):
                spriteIndex = self[i + 1].get('spriteIndex', None)
                if spriteIndex:
                    if spriteIndex not in accSprites:
                        if owner.IsAvatar:
                            gameengine.reportCritical('@xzh reEquipAllSummonedSprite spriteIndex:{0} not in accSprites:{1}'.format(spriteIndex, accSprites.keys()))
                        continue
                    self.unEquipSummonedSprite(owner, i + 1, needCalc=False, needMsg=False)
                    self.equipSummonedSprite(owner, accSprites[spriteIndex].getPersistentDict(), i + 1, needCalc=False, needMsg=False)

        owner.calcAllProp(gameconst.CALC_ALL_PROP_SRC_SPRITE_ACCESS)
        if gameconfig.enableSpriteStatLog():
            serverlog.genSpriteAccessoryLog(owner, const.SUMMON_SPRITE_ACCESSORY_UNEQUIP)
        owner.updateCombatScore((const.SPRITE_ACC_SCORE,))

    def applyAllAccessory(self, owner):
        if not gameconfig.enableNewPropCalc():
            return
        if not gameconfig.enableSummonedSprite() or not riskControl.checkFeature(None, gameconst.F_SPRITE_SHOUHU):
            return
        for part, accessoryInfo in self.iteritems():
            for attrId, attrType, attrVal in accessoryInfo.get('props', []):
                owner.combatProp.addPretreatProp(owner, attrId, attrType, attrVal)

    def applySummonedSpriteAccessory(self, owner, accessoryPart):
        if not gameconfig.enableNewPropCalc():
            return
        accessoryInfo = self[accessoryPart]
        for attrId, attrType, attrVal in accessoryInfo.get('props', []):
            owner.combatProp.addPretreatProp(owner, attrId, attrType, attrVal)

    def unApplySummonedSpriteAccessory(self, owner, accessoryPart):
        if not gameconfig.enableNewPropCalc():
            return
        accessoryInfo = self[accessoryPart]
        for attrId, attrType, attrVal in accessoryInfo.get('props', []):
            owner.combatProp.removePretreatProp(owner, attrId, attrType, attrVal)

    def mergeSummonedSpriteProp(self, owner, propAdd):
        if not gameconfig.enableSummonedSprite() or not riskControl.checkFeature(None, gameconst.F_SPRITE_SHOUHU):
            return propAdd
        if not owner._isValidPropSrc(gameconst.AVATAR_PROP_SRC_SUMMONED_SPRITE_ACCESSORY):
            return propAdd
        for part, accessoryInfo in self.iteritems():
            for attrId, attrType, attrVal in accessoryInfo.get('props', []):
                commcalc.attrMerge(owner, propAdd, attrId, attrType, attrVal)

        return propAdd

    def appendTemplate(self, templateId):
        if templateId in self.learnedTemplate:
            gameengine.reportCritical('@xzh appendTemplate templateId:{0} exist in learnedTemplate:{1}'.format(templateId, self.learnedTemplate))
            return
        self.learnedTemplate.append(templateId)

    def getAccessorySpriteIndexDict(self):
        dic = {}
        for i in xrange(const.SUMMONED_SPRITE_ACCESSORY_COUNT):
            dic[i + 1] = self[i + 1].get('spriteIndex', None)

        return dic

    def getAccessorySpriteIds(self):
        ret = []
        for i in xrange(const.SUMMONED_SPRITE_ACCESSORY_COUNT):
            relPos = i + 1
            if self[relPos]:
                spriteId = self[relPos].get('spriteId', 0)
                if spriteId:
                    ret.append(spriteId)

        return ret

    def _calcAddAccessorySkillEffect(self, owner, spriteProps, spriteLearnSkillIds, accessoryPart):
        """
        \xb4\xa6\xc0\xed\xb8\xbd\xc9\xed\xd0\xa7\xb9\xfb
        \xb8\xbd\xc9\xed\xd0\xa7\xb9\xfb\xbe\xdf\xd3\xd0\xc7\xb0\xd6\xc3\xcc\xf5\xbc\xfe\xbc\xec\xb2\xe9
        :param owner: \xd6\xf7\xc8\xcbcellMailbox
        :param spriteProps: \xd5\xbd\xc1\xe9\xca\xf4\xd0\xd4\xd7\xd6\xb5\xe4
        :param spriteLearnSkillIds: \xd5\xbd\xc1\xe9\xb5\xc4\xba\xf3\xcc\xec\xbc\xbc\xc4\xdc\xca\xfd\xbe\xdd\xbd\xe1\xb9\xb9\xc1\xd0\xb1\xed
        :param accessoryPart: \xb8\xbd\xc9\xed\xce\xbb
        """
        skScore = 0
        gamelog.debug('@xzh _calcAddAccessorySkillEffect', spriteLearnSkillIds, accessoryPart)
        if not self[accessoryPart].has_key('accEffect'):
            self[accessoryPart]['accEffect'] = {}
        for skillId in spriteLearnSkillIds:
            accessorySKills = SSSD.data.get(skillId, {}).get('accessoryPSkills', ())
            for accSkillId in accessorySKills:
                accData = SSAKD.data.get(accSkillId, {})
                skScore += self._addSingleAccessorySkillEffect(owner, spriteProps, accData, accessoryPart)

        return skScore

    def _addSingleAccessorySkillEffect(self, owner, spriteProps, accData, accessoryPart):
        """
        \xcc\xed\xbc\xd3\xb5\xa5\xb8\xf6\xb8\xbd\xc9\xed\xd0\xa7\xb9\xfb
        :param owner: \xd6\xf7\xc8\xcbcellMailbox
        :param spriteProps: \xd5\xbd\xc1\xe9\xca\xf4\xd0\xd4\xd7\xd6\xb5\xe4
        :param accData: \xb8\xbd\xc9\xed\xd0\xa7\xb9\xfb\xca\xfd\xbe\xdd
        :param accessoryPart: \xb8\xbd\xc9\xed\xce\xbb
        """
        if accData.has_key('condAccessoryPos') and accData['condAccessoryPos'] != accessoryPart:
            return 0
        self[accessoryPart]['accEffect'].setdefault('accessoryStates', [])
        if accData.has_key('accessoryStates'):
            for stateId in accData['accessoryStates']:
                sData = self._calcHijackSData(stateId, spriteProps)
                added, needCalcProp = owner._addStateCommonWithoutCalc(stateId, 1, 0, gametypes.ADD_STATE_FROM_SPRITE_EQUIP, self.ACCESSORY_DUMMY_ENTITY_ID_OFFSET + accessoryPart, 0, sData=sData)
                added and self[accessoryPart]['accEffect']['accessoryStates'].append(stateId)

        return accData.get('accessoryScore', 0)

    def _calcRemoveAccessorySkillEffect(self, owner, accessoryPart):
        """
        \xd2\xc6\xb3\xfd\xb8\xbd\xc9\xed\xd0\xa7\xb9\xfb
        :param owner: \xd6\xf7\xc8\xcbcellMailbox
        :param accessoryPart: \xb8\xbd\xc9\xed\xce\xbb
        """
        accEffectDict = self[accessoryPart].get('accEffect', {})
        if accEffectDict and accEffectDict.has_key('accessoryStates'):
            for stateId in accEffectDict['accessoryStates']:
                owner._removeSpecificStateWithoutCalc(stateId, self.ACCESSORY_DUMMY_ENTITY_ID_OFFSET + accessoryPart, gametypes.REMOVE_STATE_BY_SPRITE_UNEQUIP, self.ACCESSORY_DUMMY_ENTITY_ID_OFFSET + accessoryPart)

    def _calcHijackSData(self, stateId, spriteProps):
        stateInfo = StateInfo(stateId, 1)
        sData = {}
        enhanceDict = {}
        if stateInfo.getStateData('attrValueType') not in gametypes.DATA_TYPE_SPRITE_MODIFY:
            return sData
        if stateInfo.hasStateData('spriteLvAffectType'):
            spriteLvAffectType = stateInfo.getStateData('spriteLvAffectType')
            spriteLvAffectFormula = stateInfo.getStateData('spriteLvAffectFormula')
            if spriteLvAffectFormula:
                sData['attrFstValue'] = stateInfo.getStateData('attrFstValue')
                sData['attrContiValue'] = stateInfo.getStateData('attrContiValue')
                spriteLvAffectVal = spriteLvAffectFormula({'spriteLv': spriteProps.get('lv', 0)})
                self._mergeEnhanceDict(enhanceDict, {spriteLvAffectType: spriteLvAffectVal})
        spriteLvAffectAttrNoList = stateInfo.getStateData('spriteLvAffectList', [])
        if not spriteLvAffectAttrNoList:
            return sData
        for attrNo in spriteLvAffectAttrNoList:
            valueTypeStr = utils.getStateAttrValueTypeStr(attrNo)
            if not stateInfo.hasStateData(valueTypeStr):
                continue
            if stateInfo.getStateData(valueTypeStr) not in gametypes.DATA_TYPE_SPRITE_MODIFY:
                continue
            fstValueStr = utils.getStateAttrFstValueStr(attrNo)
            contiValueStr = utils.getStateAttrContiValueStr(attrNo)
            attrFstValue = stateInfo.getStateData(fstValueStr)
            attrContiValue = stateInfo.getStateData(contiValueStr)
            if enhanceDict.has_key(gametypes.PARAM_TYPE_SUMMONED_SPRITE_NUMBER):
                addVal = enhanceDict.get(gametypes.PARAM_TYPE_SUMMONED_SPRITE_NUMBER, 0)
                sData[fstValueStr] = max((sData[fstValueStr] if sData.has_key(fstValueStr) else attrFstValue) + addVal, 0)
                sData[contiValueStr] = max((sData[contiValueStr] if sData.has_key(contiValueStr) else attrContiValue) + addVal, 0)
            if enhanceDict.has_key(gametypes.PARAM_TYPE_SUMMONED_SPRITE_PERSENT):
                persentVal = enhanceDict.get(gametypes.PARAM_TYPE_SUMMONED_SPRITE_PERSENT, 0)
                sData[fstValueStr] = max((sData[fstValueStr] if sData.has_key(fstValueStr) else attrFstValue) * (1 + persentVal), 0)
                sData[contiValueStr] = max((sData[contiValueStr] if sData.has_key(contiValueStr) else attrContiValue) * (1 + persentVal), 0)

        return sData

    def _mergeEnhanceDict(self, enhanceDict, toMergeDict):
        for key, value in toMergeDict.iteritems():
            enhanceDict[key] = enhanceDict.get(key, 0) + value

    def restoreAccessorySkillEffect(self, owner, accSprites):
        for accessoryPart in self.iterkeys():
            if not self[accessoryPart].has_key('spriteIndex'):
                continue
            spriteIndex = self[accessoryPart]['spriteIndex']
            accEffectDict = self[accessoryPart].get('accEffect', {})
            if accEffectDict and accEffectDict.has_key('accessoryStates'):
                unvalidStates = []
                for stateId in accEffectDict['accessoryStates']:
                    sData = self._calcHijackSData(stateId, accSprites[spriteIndex].getPersistentDict())
                    added, needCalcProp = owner._addStateCommonWithoutCalc(stateId, 1, 0, gametypes.ADD_STATE_FROM_SPRITE_EQUIP, self.ACCESSORY_DUMMY_ENTITY_ID_OFFSET + accessoryPart, 0, sData=sData)
                    if not added:
                        unvalidStates.append(stateId)

                for unvalidStateId in unvalidStates:
                    accEffectDict['accessoryStates'].remove(unvalidStateId)

        owner.calcAllProp(gameconst.CALC_ALL_PROP_SRC_SPRITE_ACCESS)
