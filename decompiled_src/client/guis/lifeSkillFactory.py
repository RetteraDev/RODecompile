#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/lifeSkillFactory.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
import uiConst
import gamelog
import uiUtils
import const
import utils
import commQuest
from item import Item
from gameclass import Singleton
from Scaleform import GfxValue
from ui import gbk2unicode
from sMath import limit
from callbackHelper import Functor
from data import life_skill_data as LSD
from data import life_skill_subtype_data as LSSD
from data import life_skill_subtype_reverse_data as LSSRD
from data import life_skill_collection_reverse_data as LSCRD
from data import life_skill_resource_data as LSRD
from data import life_skill_manufacture_data as LSMD
from data import life_skill_sub_manufacture_reverse_data as LSSMRD
from data import life_skill_top_sub_manufacture_reverse_data as LSTSMRD
from cdata import life_skill_mix_data as LSMIXD
from data import item_data as ID
from data import fishing_lv_data as FLD
from data import explore_lv_data as ELD
from data import life_skill_expertise_data as LSED
from data import quest_data as QD
from data import fish_data as FD
from data import kuiling_config_data as KCD
from data import sys_config_data as SCD
from data import life_skill_config_data as LSCD
from data import ability_tree_phase_data as ATPD
from data import life_skill_prototype_data as LSPD
from data import kuiling_quest_data as KQD
from cdata import life_skill_quality_data as LSQD
from data import life_skill_prop_tips_data as LSPTD
from data import life_skill_equip_data as LSEPD
from cdata import prop_def_data as PDD
from cdata import game_msg_def_data as GMDD
from data import state_client_data as SECD
from data import fame_data as FAD
LIFE_SKILL_BIGER_ICON_PATH = 'lifeSkill/icon110/'
LIFE_SKILL_BIG_ICON_PATH = 'lifeSkill/icon64/'
LIFE_SKILL_SMALL_ICON_PATH = 'lifeSkill/icon40/'
LV_INTERVAL = 5
MAX_NUM = 9999999999999L
NAME_TAG_MAP = {gameStrings.TEXT_LIFESKILLFACTORY_60: 'chadao',
 gameStrings.TEXT_LIFESKILLFACTORY_60_1: 'chushi',
 gameStrings.TEXT_LIFESKILLFACTORY_60_2: 'gongyi',
 gameStrings.TEXT_LIFESKILLFACTORY_60_3: 'jiguan',
 gameStrings.TEXT_LIFESKILLFACTORY_60_4: 'jianzhu',
 gameStrings.TEXT_LIFESKILLFACTORY_61: 'lianjin',
 gameStrings.TEXT_LIFESKILLFACTORY_61_1: 'jiuniang',
 gameStrings.TEXT_LIFESKILLFACTORY_61_2: 'qiju',
 gameStrings.TEXT_FASHIONPROPTRANSFERPROXY_279: 'shizhuang',
 gameStrings.TEXT_LIFESKILLFACTORY_61_3: 'tiejiang',
 gameStrings.TEXT_LIFESKILLFACTORY_61_4: 'yijiang',
 gameStrings.TEXT_LIFESKILLFACTORY_62: 'yinjiang',
 gameStrings.TEXT_LIFESKILLFACTORY_62_1: 'yinjiang',
 gameStrings.TEXT_LIFESKILLFACTORY_62_2: 'zhiyao',
 gameStrings.TEXT_LIFESKILLFACTORY_62_3: 'zhiyao',
 gameStrings.TEXT_ACTIONBARPROXY_1867: 'diaoyu',
 gameStrings.TEXT_ACTIONBARPROXY_1869: 'tanmi',
 gameStrings.TEXT_LIFESKILLFACTORY_62_4: 'caicao',
 gameStrings.TEXT_LIFESKILLFACTORY_62_5: 'famu',
 gameStrings.TEXT_LIFESKILLFACTORY_62_6: 'wakuang'}
CLASS_IDS_OF_FURNITURE = (21, 32)

class ILifeSkillInfo(object):

    def __init__(self):
        self.type = 0
        self.val2Index = {}
        self.reset()

    def reset(self):
        self.firstMenuIndex = 0
        self.secondMenuIndex = 0
        self.firstMenuVal = []
        self.secondMenuVal = []

    def resLv2Index(self, lv):
        return (lv - 1) / LV_INTERVAL

    def getManuInfo(self):
        return uiUtils.dict2GfxDict({})

    def genSuccProbColorDesc(self, val):
        val = int(val / 100)
        if val < 60:
            return 'low'
        elif val >= 60 and val < 90:
            return 'mid'
        else:
            return 'high'

    def _genDescWithColor(self, skLv, tgtLv, resName, num = 1, ext = ''):
        fixVal = utils.getLifeFixVal(skLv - tgtLv)
        color = fixVal.get('color', 'FFFFE7')
        numStr = ''
        if num:
            fromString = uiUtils.getTextFromGMD(GMDD.data.LIFE_SKILL_NUMS_STRING, gameStrings.TEXT_LIFESKILLFACTORY_101)
            numStr = fromString % num
        desc = "<font color = \'#%s\'>" % (color,) + resName + numStr + ext + '</font>'
        return desc

    def _getSubMenuInfo(self, subMenuVals):
        ret = []
        subMenuVal = []
        for index, item in enumerate(subMenuVals):
            gamelog.debug('@hjx lifeSkill#_getSubMenuInfo:', item)
            if not item['open']:
                continue
            obj = {}
            obj['desc'] = item['name']
            obj['icon'] = LIFE_SKILL_SMALL_ICON_PATH + str(item['icon']) + '.dds'
            obj['open'] = item['open']
            obj['subType'] = item['id']
            obj['descTag'] = item.get('descTag', NAME_TAG_MAP.get(item['name'], ''))
            ret.append(obj)
            subMenuVal.append(item['id'])

        self.secondMenuVal.append(subMenuVal)
        return ret

    def getLeftListMenuInfo(self):
        gamelog.debug('@hjx lifeSkill#getLeftListMenuInfo:', self.type)
        ret = []
        lifeSkillData = LSSRD.data[self.type]
        self.firstMenuVal = []
        self.secondMenuVal = []
        p = BigWorld.player()
        for lifeSkillId, lifeSkillVal in lifeSkillData.items():
            self.firstMenuVal.append(lifeSkillId)
            curLifeSkillId = uiUtils.getCurLifeSkill(lifeSkillId)
            if curLifeSkillId[0] is None:
                continue
            lifeSkillItemData = LSD.data.get(curLifeSkillId, {})
            firstMenuName = lifeSkillItemData.get('name', '')
            itemLv = lifeSkillItemData.get('lv', 0)
            lvUpExp = lifeSkillItemData.get('lvUpExp', 0)
            obj = {}
            obj['itemDesc'] = firstMenuName
            obj['itemLv'] = 'Lv.' + str(itemLv)
            obj['stageLv'] = lifeSkillItemData.get('stageLv', 0)
            obj['itemTrueLv'] = itemLv
            obj['curVal'] = p.lifeSkill[lifeSkillId]['exp']
            obj['maxVal'] = lvUpExp
            obj['lifeSkillId'] = lifeSkillId
            obj['icon'] = {'iconPath': LIFE_SKILL_BIG_ICON_PATH + str(lifeSkillItemData.get('icon', '')) + uiUtils.ICON_FILE_EXT}
            obj['data'] = self._getSubMenuInfo(lifeSkillVal)
            obj['skillType'] = uiConst.LIFE_SKILL_PANEL_PRODUCE
            ret.append(obj)

        return uiUtils.array2GfxAarry(ret, True)

    def getAssistInfo(self, subType):
        p = BigWorld.player()
        skillId = utils.getLifeSkillIdBySubType(subType)
        limitCnt = utils.getLifeCanEquipCnt(p, skillId)
        info = {}
        info['limitCnt'] = limitCnt
        info['desc'] = gameStrings.TEXT_LIFESKILLFACTORY_181
        info['data'] = []
        for key, val in p.lifeEquipment.iteritems():
            itemInfo = {}
            if not val:
                continue
            srcSubType, _ = key
            if srcSubType != subType:
                continue
            itemId = val.id
            iconPath = uiUtils.getItemIconFile40(itemId)
            itemInfo['icon'] = {'iconPath': iconPath,
             'itemId': itemId,
             'srcType': 'roleInfoLifeSkill'}
            itemInfo['itemId'] = itemId
            itemInfo['part'] = val.part
            info['data'].append(itemInfo)

        if info.get('data'):
            info['data'].sort(cmp=lambda x, y: cmp(x['part'], y['part']))
        if len(info['data']) == 0:
            info['desc'] = gameStrings.TEXT_LIFESKILLFACTORY_206
        return uiUtils.dict2GfxDict(info, True)

    def leftVal2Index(self, lType, lifeSkillId):
        if not self.val2Index.has_key(lType):
            return 0
        try:
            return self.val2Index[lType].index(lifeSkillId)
        except:
            return 0

    def getLeftFirstId(self):
        return self.firstMenuVal[self.firstMenuIndex]

    def getLeftSecondId(self):
        if self.firstMenuIndex >= len(self.secondMenuVal):
            return None
        if self.secondMenuIndex >= len(self.secondMenuVal[self.firstMenuIndex]):
            return None
        return self.secondMenuVal[self.firstMenuIndex][self.secondMenuIndex]

    def clickSubMenu(self, firstMenuIndex, secondMenuIndex):
        self.firstMenuIndex = firstMenuIndex
        self.secondMenuIndex = secondMenuIndex

    def getExpertiseInfo(self):
        expertiseInfo = []
        p = BigWorld.player()
        for expertiseId in p.expertiseReverseInfo[self.type]:
            expertiseData = LSED.data[expertiseId]
            expertiseInfo.append({'iconPath': LIFE_SKILL_SMALL_ICON_PATH + str(expertiseData['icon']) + '.dds'})

        return uiUtils.array2GfxAarry(expertiseInfo)

    def getLabourInfo(self):
        p = BigWorld.player()
        labourTips = LSPTD.data.get(uiConst.LABOUR_TIPS_INDEX, {}).get('tips', gameStrings.TEXT_IMPQUEST_2707_1)
        mentalTips = LSPTD.data.get(uiConst.MENTAL_TIPS_INDEX, {}).get('tips', gameStrings.TEXT_IMPQUEST_2707_1)
        if uiUtils.hasVipBasic():
            mLabour = 2 * p.mLabour / 10
            mMental = 2 * p.mMental / 10
        else:
            mLabour = p.mLabour / 10
            mMental = p.mMental / 10
        labourDict = {'curLabour': p.labour / 10,
         'maxLabour': mLabour,
         'curMental': p.mental / 10,
         'maxMental': mMental,
         'labourTips': labourTips,
         'mentalTips': mentalTips}
        return uiUtils.dict2GfxDict(labourDict, True)

    def checkValid(self, resource):
        reqSkills = resource['reqSkills']
        for skill in reqSkills:
            reqSkillId, reqSkillLv = skill
            _, curSkillLv = uiUtils.getCurLifeSkill(reqSkillId)
            if curSkillLv is None:
                return False
            if reqSkillLv > curSkillLv:
                return False

        return True

    def getLvSubPropTips(self, rData, skLv):
        tgtLv = rData.get('lv', 1)
        probAdd3 = (tgtLv - skLv) * (tgtLv - skLv + 5) * 100
        probAdd3 = limit(probAdd3, 0, 5000)
        if tgtLv - skLv > 0:
            subLv = tgtLv - skLv
            successTips = uiUtils.getTextFromGMD(GMDD.data.LIFE_SKILL_SUCCESS_TIPS, gameStrings.TEXT_LIFESKILLFACTORY_288) % (subLv, probAdd3 / 100)
        else:
            successTips = uiUtils.getTextFromGMD(GMDD.data.LIFE_SKILL_SUCCESS_NO_SUB_TIPS, gameStrings.TEXT_LIFESKILLFACTORY_290)
        return successTips

    def _calcLifeSkillSuccProb(self, rData, props, skLv):
        baseSuccProb = rData.get('succProb', 0)
        tgtLv = rData.get('lv', 1)
        propA = props.get('propA', 0)
        resPropA = props.get('resPropA', 0)
        delta = max(propA - resPropA, 0)
        probAdd1 = delta ** 0.6 * 150
        probAdd2 = BigWorld.player().socProp.lucky ** 0.3 / (int(tgtLv / 20.0) + 2) * 700
        if tgtLv > skLv:
            probAdd3 = (tgtLv - skLv) * (tgtLv - skLv + 5) * 100
        else:
            probAdd3 = 0
        dstSubType = props.get('subType')
        toolAdd = 0
        for part in gametypes.LIFE_EQUIPMENT_PART:
            equ = BigWorld.player().lifeEquipment.get(dstSubType, part)
            if equ:
                toolAdd += equ.getLifeEquSuccProb()

        probAdd3 = limit(probAdd3, 0, 5000)
        prob = int(baseSuccProb + probAdd1 + probAdd2 - probAdd3 + toolAdd)
        return limit(prob, 0, 10000)

    def _calcGenerateIdentifiedQuality(self, skillId, rData, props, subType, userSpecifiedItems):
        p = BigWorld.player()
        dstSubType = subType
        mixId = rData.get('formula')
        fData = LSMIXD.data.get(mixId, None)
        baseQuality = fData.get('identifyQuality', 0)
        propA = props.get('propA', 0)
        resPropA = props.get('resPropA', 0)
        delta = max(propA - resPropA, 0)
        propAdd = max(delta ** 0.3 * 400, 0)
        toolQuality = 0
        for part in gametypes.LIFE_EQUIPMENT_PART:
            equ = p.lifeEquipment.get(dstSubType, part)
            if equ:
                toolQuality += equ.getLifeEquToolQuality()

        itemQuality = 0
        consumeItems = fData.get('consumeItems', [])
        identifyProbQuality = fData.get('identifyProbQuality', [])
        if identifyProbQuality:
            for itemInfo, probQuality in zip(consumeItems, identifyProbQuality):
                itemId, itemNum = itemInfo
                prob, quality = probQuality
                fineItemId = LSQD.data.get(itemId, {}).get('fineItemId', 0)
                if fineItemId and fineItemId in userSpecifiedItems:
                    itemQuality += quality

        qualityUpLimit = limit(int(baseQuality * (1000 + propAdd + toolQuality) / 1000.0), 0, 100)
        return (qualityUpLimit, itemQuality)

    def _calcGenerateIdentifiedProb(self, skillId, rData, props, subType, userSpecifiedItems):
        p = BigWorld.player()
        dstSubType = subType
        mixId = rData.get('formula')
        fData = LSMIXD.data.get(mixId, None)
        baseProb = fData.get('identifyProb', 0)
        tgtLv = rData.get('lv', 1)
        luckProb = max((p.socProp.lucky ** 0.3 - 0.05 * tgtLv) * 400, 0)
        toolProb = 0
        for part in gametypes.LIFE_EQUIPMENT_PART:
            equ = p.lifeEquipment.get(dstSubType, part)
            if equ:
                toolProb += equ.getLifeEquToolProb()

        itemProb = 0
        consumeItems = fData.get('consumeItems', [])
        identifyProbQuality = fData.get('identifyProbQuality', [])
        if identifyProbQuality:
            for itemInfo, probQuality in zip(consumeItems, identifyProbQuality):
                itemId, itemNum = itemInfo
                prob, quality = probQuality
                fineItemId = LSQD.data.get(itemId, {}).get('fineItemId', 0)
                if fineItemId and fineItemId in userSpecifiedItems:
                    itemProb += prob

        prob = int(baseProb + luckProb + toolProb + itemProb)
        return limit(prob, 0, 10000)

    def getIdentified(self):
        identifiedQuality, identifiedExtraQuality, identifiedProb = (0, 0, 0)
        detailId = self.getDetailId()
        ret = []
        if detailId is None:
            return uiUtils.array2GfxAarry(ret)
        resourceId = LSMD.data[detailId]['resourceId']
        resource = LSRD.data[resourceId]
        subType = LSMD.data[detailId]['subType']
        lifeSkillId = LSSD.data[subType]['lifeSkillId']
        props = self._calcLifeSkillProps(lifeSkillId, subType, resource)
        mixId = resource.get('formula')
        fData = LSMIXD.data.get(mixId, None)
        if not fData:
            return (identifiedQuality, identifiedExtraQuality, identifiedProb / 100)
        skillType = LSD.data.get((lifeSkillId, 0), {}).get('type', 0)
        if skillType == gametypes.LIFE_SKILL_TYPE_MANUFACTURE and fData.get('needIdentify', 0):
            if props:
                identifiedQuality, identifiedExtraQuality = self._calcGenerateIdentifiedQuality(lifeSkillId, resource, props, self.getLeftSecondId(), self.collectFineItems())
                identifiedProb = self._calcGenerateIdentifiedProb(lifeSkillId, resource, props, self.getLeftSecondId(), self.collectFineItems())
        return (identifiedQuality, identifiedExtraQuality, identifiedProb / 100)

    def _getLifeEquipPropsAdd(self, dstSubType):
        props = {}
        for key, val in BigWorld.player().lifeEquipment.iteritems():
            if not val:
                continue
            srcSubType, _ = key
            if srcSubType != dstSubType:
                continue
            if val.cdura == 0:
                continue
            eData = LSEPD.data.get(val.id)
            if not eData:
                continue
            curProps = eData.get('props', [])
            for item2 in curProps:
                if props.get(item2[0]):
                    props[item2[0]] += item2[1]
                else:
                    props[item2[0]] = item2[1]

        return props

    def _calcLifeSkillProps(self, skillId, subType, rData):
        props = {}
        equipAdd = self._getLifeEquipPropsAdd(subType)
        for pId in PDD.data.SOCIAL_PRIMARY_PROPERTIES:
            bVal = BigWorld.player().getSocPrimaryPropValue(pId)
            props[pId] = bVal + equipAdd.get(pId, 0)

        lv = rData['lv']
        ppId = rData.get('ppId')
        reqProps = LSPD.data.get(ppId, {}).get('reqProps')
        lessPropList = []
        lessPropNeedList = []
        if reqProps:
            for i, v in enumerate(reqProps):
                if props.get(PDD.data.SOCIAL_PRIMARY_PROPERTIES[i], 0) < v[lv - 1]:
                    lessPropList.append(PDD.data.SOCIAL_PRIMARY_PROPERTIES[i])
                    lessPropNeedList.append(v[lv - 1])

        ppId = rData.get('ppId', 0)
        pData = LSPD.data.get(ppId)
        if not pData:
            return props
        lv = rData['lv']
        pIdA = pData.get('majorAttrb', 0)
        pIdB = pData.get('minorAttrb', 0)
        resPorps = {}
        for i, val in enumerate(pData.get('resProps', [])):
            resPorps[PDD.data.SOCIAL_PRIMARY_PROPERTIES[i]] = val[lv - 1]

        props['propA'] = props.get(pIdA, 0)
        props['propB'] = props.get(pIdB, 0)
        props['resPropA'] = resPorps.get(pIdA, 0)
        props['resPropB'] = resPorps.get(pIdB, 0)
        props['resPorps'] = resPorps
        props['lv'] = lv
        props['skillId'] = skillId
        props['subType'] = subType
        return props


YUE_LI_TIPS_INDEX = 8
WEI_WANG_TIPS_INDEX = 9

class LifeSkillOverview(ILifeSkillInfo):

    def __init__(self):
        super(LifeSkillOverview, self).__init__()

    def _getIconList(self, val):
        ret = []
        for item in val:
            if item.get('open', 1) == 0:
                continue
            obj = {}
            obj['name'] = item['name']
            obj['icon'] = LIFE_SKILL_SMALL_ICON_PATH + str(item['icon']) + uiUtils.ICON_FILE_EXT
            ret.append(obj)

        return ret

    def lv2Title(self, lv):
        levelToTitle = LSCD.data.get('levelToTitle', {})
        for key, val in levelToTitle.iteritems():
            lvMin, lvMax = key
            if lv >= lvMin and lv <= lvMax:
                return val

        return 0

    def _getLifeSkillInfo(self, lifeSkillType):
        lifeSkillReverseData = LSSRD.data[lifeSkillType]
        ret = []
        p = BigWorld.player()
        if not self.val2Index.has_key(lifeSkillType):
            self.val2Index[lifeSkillType] = []
        for lifeSkillId, lifeSkillVal in lifeSkillReverseData.items():
            obj = {}
            curLifeSkillId = uiUtils.getCurLifeSkill(lifeSkillId)
            if curLifeSkillId[0] is None:
                continue
            if len(self._getIconList(lifeSkillVal)) == 0:
                continue
            self.val2Index[lifeSkillType].append(lifeSkillId)
            lifeSkillData = LSD.data.get(curLifeSkillId, {})
            obj['itemDesc'] = lifeSkillData.get('name', '')
            obj['id'] = lifeSkillData.get('id', 0)
            obj['stageLv'] = lifeSkillData.get('stageLv', 0)
            obj['lifeSkillId'] = lifeSkillId
            obj['itemLv'] = 'Lv.' + str(curLifeSkillId[1])
            obj['itemTrueLv'] = curLifeSkillId[1]
            obj['curVal'] = p.lifeSkill[lifeSkillId]['exp']
            obj['maxVal'] = lifeSkillData['lvUpExp']
            obj['icon'] = {'iconPath': LIFE_SKILL_BIG_ICON_PATH + str(lifeSkillData.get('icon', '')) + uiUtils.ICON_FILE_EXT}
            obj['lvInterval'] = self.lv2Title(curLifeSkillId[1])
            obj['iconList'] = self._getIconList(lifeSkillVal)
            obj['isLevelUp'] = self.isSkillLevelUp(lifeSkillId)
            obj['levelUpTips'] = gameStrings.TEXT_LIFESKILLFACTORY_556
            ret.append(obj)

        return uiUtils.array2GfxAarry(ret, True)

    def isSkillLevelUp(self, lifeSkillId):
        p = BigWorld.player()
        curLifeSkillId = uiUtils.getCurLifeSkill(lifeSkillId)
        lifeSkillData = LSD.data.get(curLifeSkillId, {})
        curExpVal = p.lifeSkill[lifeSkillId]['exp']
        maxExpVal = lifeSkillData['lvUpExp']
        lifeSkilllv = curLifeSkillId[1]
        if curExpVal >= maxExpVal and lifeSkilllv % 10 == 9:
            return True
        else:
            return False

    def _getSpecialSkillInfo(self):
        specialDict = {}
        p = BigWorld.player()
        fData = FLD.data.get(p.fishingLv, {})
        FISH_MAX_LV = max(FLD.data.keys())
        specialDict['fishSkill'] = {'id': 99,
         'icon': {'iconPath': LIFE_SKILL_BIG_ICON_PATH + '1.dds'},
         'desc': fData.get('name', gameStrings.TEXT_LIFESKILLFACTORY_583),
         'stageLv': fData.get('stageLv', 0),
         'level': gameStrings.TEXT_LIFESKILLFACTORY_585 if p.fishingLv >= FISH_MAX_LV else 'Lv.' + str(p.fishingLv),
         'itemTrueLv': p.fishingLv,
         'curExp': p.fishingExp,
         'maxExp': fData['exp'],
         'lvInterval': self.lv2Title(p.fishingLv),
         'isLevelUp': p.fishingLv % 10 == 9 and p.fishingExp >= fData['exp'],
         'levelUpTips': gameStrings.TEXT_LIFESKILLFACTORY_556}
        EXPLORE_MAX_LV = max(ELD.data.keys())
        eData = ELD.data.get(p.exploreLv, {})
        specialDict['exploreSkill'] = {'id': 98,
         'icon': {'iconPath': LIFE_SKILL_BIG_ICON_PATH + '2.dds'},
         'desc': eData.get('name', gameStrings.TEXT_LIFESKILLFACTORY_599),
         'stageLv': eData.get('stageLv', 0),
         'lvInterval': self.lv2Title(p.exploreLv),
         'level': gameStrings.TEXT_LIFESKILLFACTORY_585 if p.exploreLv >= EXPLORE_MAX_LV else 'Lv.' + str(p.exploreLv),
         'itemTrueLv': p.exploreLv,
         'curExp': p.xiangyaoExp + p.xunbaoExp + p.zhuizongExp,
         'maxExp': p.xiangyaoExp + p.xunbaoExp + p.zhuizongExp if p.exploreLv >= EXPLORE_MAX_LV else eData['exp'],
         'tips': gameStrings.TEXT_LIFESKILLFACTORY_606 + str(p.xiangyaoExp) + '/' + str(eData.get('maxXiangyaoExp', '-')) + '\n' + gameStrings.TEXT_LIFESKILLFACTORY_607 + str(p.xunbaoExp) + '/' + str(eData.get('maxXunbaoExp', '-')) + '\n' + gameStrings.TEXT_LIFESKILLFACTORY_608 + str(p.zhuizongExp) + '/' + str(eData.get('maxZhuizongExp', '-')),
         'isLevelUp': p.exploreLv % 10 == 9 and p.xiangyaoExp + p.xunbaoExp + p.zhuizongExp >= p.xiangyaoExp + p.xunbaoExp + p.zhuizongExp,
         'levelUpTips': gameStrings.TEXT_LIFESKILLFACTORY_556}
        return uiUtils.dict2GfxDict(specialDict, True)

    def getPanelInfo(self):
        ret = gameglobal.rds.ui.movie.CreateObject()
        ret.SetMember('produceSkill', self._getLifeSkillInfo(gametypes.LIFE_SKILL_TYPE_COLLECTION))
        ret.SetMember('makeSkill', self._getLifeSkillInfo(gametypes.LIFE_SKILL_TYPE_MANUFACTURE))
        ret.SetMember('specialSkill', self._getSpecialSkillInfo())
        p = BigWorld.player()
        weiWangTips = LSPTD.data.get(WEI_WANG_TIPS_INDEX, {}).get('tips', gameStrings.TEXT_IMPQUEST_2707_1)
        ret.SetMember('weiWang', GfxValue(p.getCurXueShiVal()))
        ret.SetMember('weiWangTips', GfxValue(gbk2unicode(weiWangTips)))
        value = p.getCurYueLiVal()
        valueMax = 0
        phase = 1
        for id, data_item in ATPD.data.iteritems():
            reqValue = data_item.get('reqValue', 0)
            if value >= valueMax + reqValue:
                phase = id
                valueMax += reqValue
            else:
                break

        ret.SetMember('descName', GfxValue(gbk2unicode(ATPD.data.get(phase, {}).get('name', ''))))
        ret.SetMember('descStage', GfxValue(phase))
        if phase < max(ATPD.data.keys()):
            yueLiValue = valueMax + ATPD.data.get(phase + 1, {}).get('reqValue', 0)
        else:
            yueLiValue = valueMax
        yueLi = '%d/%d' % (value, yueLiValue)
        yueLiTips = LSPTD.data.get(YUE_LI_TIPS_INDEX, {}).get('tips', gameStrings.TEXT_IMPQUEST_2707_1)
        ret.SetMember('yueLi', GfxValue(yueLi))
        ret.SetMember('yueLiNow', GfxValue(value))
        ret.SetMember('yueLiMax', GfxValue(yueLiValue))
        ret.SetMember('yueLiTips', GfxValue(gbk2unicode(yueLiTips)))
        bindingRelevanceList = []
        bindingRelevanceListProduction = []
        bindingRelevanceListSpecial = []
        bindingRelevance = LSCD.data.get('LIFE_SKILL_ICON_RELEVANCE_BINDING', None)
        bindingRelevance = sorted(bindingRelevance.iteritems(), key=lambda d: d[1], reverse=False)
        for binding, path in bindingRelevance:
            bindingRelevanceMap = {}
            bindingRelevanceMap['binding'] = binding
            bindingRelevanceMap['path'] = {'iconPath': LIFE_SKILL_BIGER_ICON_PATH + str(path) + uiUtils.ICON_FILE_EXT,
             'smallIconPath': LIFE_SKILL_SMALL_ICON_PATH + str(path) + uiUtils.ICON_FILE_EXT}
            bindingRelevanceList.append(bindingRelevanceMap)

        bindingRelevance = LSCD.data.get('LIFE_SKILL_ICON_RELEVANCE_BINDING_PRODUCTION', None)
        bindingRelevance = sorted(bindingRelevance.iteritems(), key=lambda d: d[1], reverse=False)
        for binding, path in bindingRelevance:
            bindingRelevanceMap = {}
            bindingRelevanceMap['binding'] = binding
            bindingRelevanceMap['path'] = {'iconPath': LIFE_SKILL_BIGER_ICON_PATH + str(path) + uiUtils.ICON_FILE_EXT,
             'smallIconPath': LIFE_SKILL_SMALL_ICON_PATH + str(path) + uiUtils.ICON_FILE_EXT}
            bindingRelevanceListProduction.append(bindingRelevanceMap)

        bindingRelevance = LSCD.data.get('LIFE_SKILL_ICON_RELEVANCE_BINDING_SPECIAL', None)
        bindingRelevance = sorted(bindingRelevance.iteritems(), key=lambda d: d[1], reverse=False)
        for binding, path in bindingRelevance:
            bindingRelevanceMap = {}
            bindingRelevanceMap['binding'] = binding
            bindingRelevanceMap['path'] = {'iconPath': LIFE_SKILL_BIGER_ICON_PATH + str(path) + uiUtils.ICON_FILE_EXT,
             'smallIconPath': LIFE_SKILL_SMALL_ICON_PATH + str(path) + uiUtils.ICON_FILE_EXT}
            bindingRelevanceListSpecial.append(bindingRelevanceMap)

        ret.SetMember('bindingRelevance', uiUtils.array2GfxAarry(bindingRelevanceList, False))
        ret.SetMember('bindingRelevanceProduction', uiUtils.array2GfxAarry(bindingRelevanceListProduction, False))
        ret.SetMember('bindingRelevanceSpecial', uiUtils.array2GfxAarry(bindingRelevanceListSpecial, False))
        gamelog.debug('@hjx lifeSkill#getPanelInfo:', ret)
        return ret


class ProduceSkillInfo(ILifeSkillInfo):

    def __init__(self):
        super(ProduceSkillInfo, self).__init__()
        self.type = gametypes.LIFE_SKILL_TYPE_COLLECTION

    def getDetailInfo(self):
        ret = []
        for i in xrange(const.MAX_LIFE_SKILL_RES_LEVEL / LV_INTERVAL):
            ret.append({'titleDesc': gameStrings.TEXT_LIFESKILLFACTORY_696 % (i * LV_INTERVAL + 1, (i + 1) * LV_INTERVAL),
             'data': []})

        detailData = LSCRD.data.get(self.getLeftSecondId(), {})
        p = BigWorld.player()
        lifeSkillId = self.getLeftFirstId()
        _, skLv = uiUtils.getCurLifeSkill(lifeSkillId)
        for item in detailData:
            obj = {}
            resourceId = item['resourceId']
            targetId = item.get('targetId', 0)
            resource = LSRD.data[resourceId]
            if gameglobal.rds.ui.lifeSkillNew.hideInfo[1]:
                if not p.getAbilityData(gametypes.ABILITY_LS_COLLECTION_SUB_ON, item['id']):
                    continue
                if resource.get('needShow') == 0:
                    continue
            elif resource.get('needShow') == 0:
                continue
            props = self._calcLifeSkillProps(lifeSkillId, item['subType'], resource)
            successTips = uiUtils.getTextFromGMD(GMDD.data.LIFE_SKILL_SUCCESS_NO_SUB_TIPS, gameStrings.TEXT_LIFESKILLFACTORY_290)
            if props:
                success = min(100, int(self._calcLifeSkillSuccProb(resource, props, skLv) / 100))
                successTips = self.getLvSubPropTips(resource, skLv)
            else:
                success = 0
            formulaId = resource['formula']
            formualData = LSMIXD.data[formulaId]
            if not formualData.has_key('targetItems'):
                continue
            consumeLabour = utils.calcLabourConsume(p, lifeSkillId, resource, props) / 10.0
            consumeMental = utils.calcMentalConsume(p, lifeSkillId, resource, props) / 10.0
            itemId = targetId
            iconPath = uiUtils.getItemIconFile40(itemId)
            pinXing = uiUtils.getPinXing(itemId)
            color = uiUtils.getItemColor(itemId)
            obj['color'] = color
            obj['icon'] = {'iconPath': iconPath,
             'itemId': itemId,
             'pinXing': pinXing}
            obj['itemId'] = itemId
            obj['desc'] = resource['name']
            obj['difficulty'] = resource.get('difficulty', 0)
            obj['consumeLabour'] = str(consumeLabour)
            obj['consumeMental'] = str(consumeMental)
            obj['success'] = gameStrings.TEXT_LIFESKILLFACTORY_749 % success
            obj['successTips'] = successTips
            index = self.resLv2Index(resource['lv'])
            ret[index]['data'].append(obj)

        return uiUtils.array2GfxAarry(ret, True)


class MakeSkillInfo(ILifeSkillInfo):

    def __init__(self):
        super(MakeSkillInfo, self).__init__()
        self.type = gametypes.LIFE_SKILL_TYPE_MANUFACTURE
        self.reset()

    def reset(self):
        super(MakeSkillInfo, self).reset()
        self.midFirstMenuIndex = 0
        self.midSecondMenuIndex = 0
        self.midFirstMenuVal = []
        self.midSecondMenuVal = []
        self.curPage = 1
        self.needFineItem = {}
        self.invCountCache = {}

    def getDetailId(self):
        if self.midFirstMenuIndex >= len(self.midSecondMenuVal):
            return None
        if self.midSecondMenuIndex >= len(self.midSecondMenuVal[self.midFirstMenuIndex]):
            return None
        return self.midSecondMenuVal[self.midFirstMenuIndex][self.midSecondMenuIndex]

    def clickMidSubMenu(self, firstMenuIndex, secondMenuIndex):
        self.midFirstMenuIndex = firstMenuIndex
        self.midSecondMenuIndex = secondMenuIndex

    def getCanBuildNum(self, detailId):
        resourceId = LSMD.data[detailId]['resourceId']
        resource = LSRD.data[resourceId]
        subType = LSMD.data[detailId]['subType']
        lifeSkillId = LSSD.data[subType]['lifeSkillId']
        props = self._calcLifeSkillProps(lifeSkillId, subType, resource)
        if not props:
            return 0
        p = BigWorld.player()
        consumeLabour = utils.calcLabourConsume(p, lifeSkillId, resource, props) / 10.0
        consumeMental = utils.calcMentalConsume(p, lifeSkillId, resource, props) / 10.0
        curLabour = p.labour / 10
        curMental = p.mental / 10
        if consumeLabour:
            labourNum = int(curLabour / consumeLabour)
        else:
            labourNum = MAX_NUM
        if consumeMental:
            mentalNum = int(curMental / consumeMental)
        else:
            mentalNum = MAX_NUM
        minNum = min(labourNum, mentalNum)
        formulaId = resource['formula']
        formualData = LSMIXD.data[formulaId]
        enableParentCheck = True
        p = BigWorld.player()
        userSpecifiedItems = self.collectFineItems()
        consumeItems = formualData.get('consumeItems', [])
        tDict = {}
        for itemId, num in consumeItems:
            tDict[itemId] = tDict.setdefault(itemId, 0) + num

        targetDict = utils.getRealConsumeLifeSkillItems(tDict, userSpecifiedItems)
        if not targetDict:
            targetDict = tDict
        for itemId, num in targetDict.iteritems():
            itemHasNum = self._getNeedItemsCountById(itemId)
            fineItemId = LSQD.data.get(itemId, {}).get('fineItemId', 0)
            if not itemHasNum and fineItemId:
                itemHasNum = self._getNeedItemsCountById(fineItemId)
            canMake = int(itemHasNum / num)
            minNum = min(minNum, canMake)

        return minNum

    def _getMidSubMenuInfo(self, midMenuVal):
        ret = []
        gamelog.debug('@hjx lifeSkill#_getMidSubMenuInfo#midMenuVal:', midMenuVal)
        midSubMenuVal = []
        p = BigWorld.player()
        lifeSkillId = self.getLeftFirstId()
        _, skLv = uiUtils.getCurLifeSkill(lifeSkillId)
        for item in midMenuVal:
            resourceData = LSRD.data.get(item['resourceId'], {})
            if resourceData.get('needShow') == 0:
                continue
            isLearned = True
            if item.get('defaultCanDo', 0):
                pass
            elif gameglobal.rds.ui.lifeSkillNew.hideInfo[0]:
                if not p.getAbilityData(gametypes.ABILITY_LS_MANUFACTURE_SUB_ON, item['id']):
                    continue
            elif not p.getAbilityData(gametypes.ABILITY_LS_MANUFACTURE_SUB_ON, item['id']):
                isLearned = False
            obj = {}
            num = self.getCanBuildNum(item['id'])
            if isLearned == False:
                obj['desc'] = self._genDescWithColor(skLv, resourceData['lv'], item['name'] + '[' + str(resourceData['lv']) + gameStrings.TEXT_LIFESKILLFACTORY_869, 0, gameStrings.TEXT_LIFESKILLFACTORY_869_1)
            else:
                obj['desc'] = self._genDescWithColor(skLv, resourceData['lv'], item['name'] + '[' + str(resourceData['lv']) + gameStrings.TEXT_LIFESKILLFACTORY_869, num)
            obj['icon'] = LIFE_SKILL_SMALL_ICON_PATH + str(item['icon']) + '.dds'
            obj['manuId'] = item['id']
            obj['isLearned'] = isLearned
            ret.append(obj)
            midSubMenuVal.append(item['id'])

        ret.sort(key=lambda x: x['manuId'])
        midSubMenuVal.sort()
        self.midSecondMenuVal.append(midSubMenuVal)
        return ret

    def isAllMidMenuNotValid(self, midMenuVals):
        p = BigWorld.player()
        for midMenu in midMenuVals:
            if midMenu.get('defaultCanDo', 0):
                return False
            if p.getAbilityData(gametypes.ABILITY_LS_MANUFACTURE_SUB_ON, midMenu['id']):
                return False
            if not gameglobal.rds.ui.lifeSkillNew.hideInfo[0]:
                resourceData = LSRD.data.get(midMenu['resourceId'], {})
                if resourceData.get('needShow') != 0:
                    return False

        return True

    def getMidListInfo(self):
        ret = []
        subType = self.getLeftSecondId()
        if subType is None:
            return uiUtils.array2GfxAarry(ret)
        self.midFirstMenuVal = []
        self.midSecondMenuVal = []
        for classId in LSTSMRD.data[subType]:
            midMenuVals = LSSMRD.data[subType, classId]
            if self.isAllMidMenuNotValid(midMenuVals):
                continue
            if classId in CLASS_IDS_OF_FURNITURE and not gameglobal.rds.configData.get('enableHome', False):
                continue
            self.midFirstMenuVal.append(classId)
            midFirstMenuName = midMenuVals[0].get('className', '')
            obj = {}
            obj['keyName'] = midFirstMenuName
            obj['data'] = self._getMidSubMenuInfo(midMenuVals)
            ret.append(obj)

        return ret

    def _getProduceItems(self):
        detailId = self.getDetailId()
        ret = []
        if detailId is None:
            return uiUtils.array2GfxAarry(ret)
        resourceId = LSMD.data[detailId]['resourceId']
        resource = LSRD.data[resourceId]
        formulaId = resource['formula']
        formualData = LSMIXD.data[formulaId]
        resourceId = LSMD.data[detailId]['resourceId']
        resource = LSRD.data[resourceId]
        subType = LSMD.data[detailId]['subType']
        lifeSkillId = LSSD.data[subType]['lifeSkillId']
        _, skLv = uiUtils.getCurLifeSkill(lifeSkillId)
        props = self._calcLifeSkillProps(lifeSkillId, subType, resource)
        successTips = uiUtils.getTextFromGMD(GMDD.data.LIFE_SKILL_SUCCESS_NO_SUB_TIPS, gameStrings.TEXT_LIFESKILLFACTORY_290)
        quality, extraQuality, prob = (0, 0, 0)
        if props:
            success = int(min(100, self._calcLifeSkillSuccProb(resource, props, skLv) / 100))
            successTips = self.getLvSubPropTips(resource, skLv)
            skillType = LSD.data.get((lifeSkillId, 0), {}).get('type', 0)
            mixId = resource.get('formula')
            fData = LSMIXD.data.get(mixId, None)
            if not fData:
                return
            if skillType == gametypes.LIFE_SKILL_TYPE_MANUFACTURE and fData.get('needIdentify', 0):
                quality, extraQuality = self._calcGenerateIdentifiedQuality(lifeSkillId, resource, props, self.getLeftSecondId(), self.collectFineItems())
                prob = self._calcGenerateIdentifiedProb(lifeSkillId, resource, props, self.getLeftSecondId(), self.collectFineItems())
        else:
            success = 0
        p = BigWorld.player()
        consumeLabour = utils.calcLabourConsume(p, lifeSkillId, resource, props) / 10.0
        consumeMental = utils.calcMentalConsume(p, lifeSkillId, resource, props) / 10.0
        gamelog.debug('@jinjj lifeSkill#_getProduceItems:', detailId, resourceId, formulaId)
        for item in formualData.get('targetItems', []):
            obj = {}
            iconPath = uiUtils.getItemIconFile40(item[0])
            iconPath2 = uiUtils.getItemIconFile64(item[0])
            pinXing = uiUtils.getPinXing(item[0])
            color = uiUtils.getItemColor(item[0])
            obj['icon'] = {'iconPath': iconPath,
             'itemId': item[0],
             'pinXing': pinXing,
             'quality': color}
            obj['icon2'] = {'iconPath': iconPath2,
             'itemId': item[0],
             'pinXing': pinXing,
             'quality': color}
            obj['itemId'] = item[0]
            obj['count'] = gameStrings.TEXT_LIFESKILLFACTORY_988 % item[1]
            obj['color'] = uiUtils.getItemColor(item[0])
            obj['desc'] = ID.data.get(item[0], {}).get('name', '')
            obj['difficulty'] = resource.get('difficulty', 0)
            obj['consumeLabour'] = str(consumeLabour)
            obj['consumeMental'] = str(consumeMental)
            obj['success'] = gameStrings.TEXT_LIFESKILLFACTORY_749 % success
            obj['successTips'] = successTips
            obj['identifiedQuality'] = quality
            obj['identifiedExtraQuality'] = extraQuality
            obj['identifiedProb'] = prob / 100
            ret.append(obj)

        return uiUtils.array2GfxAarry(ret, True)

    def _genReqDesc(self, detailId):
        desc = ''
        canMake = True
        if not LSMD.data.has_key(detailId):
            return desc
        p = BigWorld.player()
        cData = LSMD.data[detailId]
        for itemId, num in cData.get('reqItems', ()):
            itemName = ID.data.get(itemId, {}).get('name', '')
            if BigWorld.player().inv.hasItemInPages(itemId, num, enableParentCheck=True):
                desc += gameStrings.TEXT_LIFESKILLFACTORY_1014 % (itemName, num)
            else:
                desc += uiUtils.toHtml(gameStrings.TEXT_LIFESKILLFACTORY_1014 % (itemName, num), '#a60000')
                canMake = False

        if cData.has_key('reqBuff'):
            buffId, msgId = cData['reqBuff']
            if SECD.data.has_key(buffId):
                name = SECD.data[buffId].get('name')
                state = getattr(p, 'statesServerAndOwn', {})
                if state.has_key(buffId):
                    desc += gameStrings.TEXT_LIFESKILLFACTORY_1026 % name
                else:
                    desc += uiUtils.toHtml(gameStrings.TEXT_LIFESKILLFACTORY_1026 % name, '#a60000')
                    canMake = False
        if cData.has_key('reqFames'):
            reqFames = cData['reqFames']
            for fId, num in reqFames:
                fname = FAD.data.get(fId).get('name')
                self._getFameLv(fId, num)
                if p.fame.get(fId) >= num:
                    desc += gameStrings.TEXT_LIFESKILLFACTORY_1037 % fname
                else:
                    desc += uiUtils.toHtml(gameStrings.TEXT_LIFESKILLFACTORY_1037 % fname, '#a60000')
                    canMake = False

        resourceId = LSMD.data[detailId]['resourceId']
        resource = LSRD.data[resourceId]
        subType = LSMD.data[detailId]['subType']
        reqSkills = resource.get('reqSkills', [])
        for skId, lv in reqSkills:
            if lv == 0:
                continue
            nowLv = uiUtils.getCurLifeSkill(skId)
            addLv = uiUtils.getLifeSkillEquipAdd(subType)
            if nowLv[1] + addLv >= lv:
                desc += gameStrings.TEXT_LIFESKILLFACTORY_1052 + LSD.data[skId, lv]['name'] + gameStrings.TEXT_LIFESKILLFACTORY_1052_1 % lv
            else:
                desc += uiUtils.toHtml(gameStrings.TEXT_LIFESKILLFACTORY_1052 + LSD.data[skId, lv]['name'] + gameStrings.TEXT_LIFESKILLFACTORY_1052_1 % lv, '#a60000')
                canMake = False

        if resource.get('ppId', 0) == 0:
            return desc
        ppId = resource['ppId']
        if not LSPD.data.has_key(ppId):
            return desc
        socProp = [gameStrings.TEXT_LIFESKILLFACTORY_1064,
         gameStrings.TEXT_LIFESKILLFACTORY_1064_1,
         gameStrings.TEXT_LIFESKILLFACTORY_1064_2,
         gameStrings.TEXT_LIFESKILLFACTORY_1064_3,
         gameStrings.TEXT_LIFESKILLFACTORY_1064_4,
         gameStrings.TEXT_LIFESKILLFACTORY_1064_5,
         gameStrings.TEXT_LIFESKILLFACTORY_1064_6]
        socNameArray = ['str',
         'dex',
         'know',
         'sense',
         'study',
         'charm',
         'lucky']
        socPropArray = [PDD.data.PROPERTY_STR,
         PDD.data.PROPERTY_DEX,
         PDD.data.PROPERTY_KNOW,
         PDD.data.PROPERTY_SENSE,
         PDD.data.PROPERTY_STUDY,
         PDD.data.PROPERTY_CHARM,
         PDD.data.PROPERTY_LUCKY]
        lv = resource['lv']
        reqProps = LSPD.data.get(ppId, {}).get('reqProps', ())
        equipAdd = self._getLifeEquipPropsAdd(subType)
        descArray = []
        for i, v in enumerate(reqProps):
            if v[lv - 1] == 0:
                continue
            p = BigWorld.player()
            if getattr(p.socProp, socNameArray[i]) + equipAdd.get(socPropArray[i], 0) >= v[lv - 1]:
                descArray.append([v[lv - 1], gameStrings.TEXT_LIFESKILLFACTORY_1082 + socProp[i] + gameStrings.TEXT_LIFESKILLFACTORY_1082_1 + str(v[lv - 1]) + '\n'])
            else:
                destText = uiUtils.toHtml(gameStrings.TEXT_LIFESKILLFACTORY_1082 + socProp[i] + gameStrings.TEXT_LIFESKILLFACTORY_1082_1 + str(v[lv - 1]) + '\n', '#FB0000')
                descArray.append([v[lv - 1], destText])
                canMake = False

        descArray.sort(cmp=lambda x, y: cmp(x[0], y[0]))
        descArray.reverse()
        for item in descArray:
            desc += item[1]

        self.canMake = canMake
        return desc

    def _getLifeEquipPropsAdd(self, dstSubType):
        props = {}
        for key, val in BigWorld.player().lifeEquipment.iteritems():
            if not val:
                continue
            srcSubType, _ = key
            if srcSubType != dstSubType:
                continue
            if val.cdura == 0:
                continue
            eData = LSEPD.data.get(val.id)
            if not eData:
                continue
            curProps = eData.get('props', [])
            for item2 in curProps:
                if props.get(item2[0]):
                    props[item2[0]] += item2[1]
                else:
                    props[item2[0]] = item2[1]

        return props

    def _getFameLv(self, fameId, fameVal):
        fd = FAD.data.get(fameId)
        ret = 1
        if fd.has_key('lvUpCondition'):
            lvUpCondition = fd.get('lvUpCondition', [])
            if lvUpCondition:
                lvArray = lvUpCondition[1].items()
            else:
                lvArray = []
        else:
            lvArray = fd.get('lvUpNeed', {}).items()
        lvArray.sort(key=lambda k: k[1], reverse=True)
        for key, val in lvArray:
            if fameVal >= val:
                ret = key + 1
                break

        return ret

    def _genNeedItem(self, itemId, num):
        itemObj = {}
        p = BigWorld.player()
        item = Item(itemId)
        iconPath = uiUtils.getItemIconFile64(itemId)
        pinXing = uiUtils.getPinXing(itemId)
        itemNum = self._getNeedItemsCountById(itemId)
        itemObj['icon'] = {'iconPath': iconPath,
         'itemId': itemId,
         'pinXing': pinXing,
         'count': str(itemNum) + '/' + str(num)}
        itemObj['color'] = uiUtils.getItemColor(itemId)
        itemObj['itemId'] = itemId
        itemObj['itemNum'] = gameStrings.TEXT_LIFESKILLFACTORY_1159 + str(itemNum) + '/' + str(num)
        itemObj['desc'] = item.getName()
        itemObj['isEnough'] = itemNum >= num
        lifeSkillOtherSmallBtnType = ID.data.get(itemId, {}).get('lifeSkillOtherSmallBtnType', ())
        gamelog.debug('@lvc lifeSkillOtherSmallBtnType:', lifeSkillOtherSmallBtnType)
        if lifeSkillOtherSmallBtnType:
            itemObj['otherSmallBtnName'] = uiConst.SMALL_BTN_TYPE_LABEL[lifeSkillOtherSmallBtnType[0]]
            itemObj['getItemId'] = lifeSkillOtherSmallBtnType[1]
        else:
            itemObj['otherSmallBtnName'] = ''
        return itemObj

    def updateSelectNeedItem(self, itemId, val):
        if not self.needFineItem.has_key(itemId):
            return
        self.needFineItem[itemId] = val

    def _getNeedItems(self):
        detailId = self.getDetailId()
        ret = {}
        self.canMake = True
        if detailId is None:
            return uiUtils.dict2GfxDict(ret)
        ret['reqDesc'] = self._genReqDesc(detailId)
        ret['data'] = []
        resourceId = LSMD.data[detailId]['resourceId']
        resource = LSRD.data[resourceId]
        formulaId = resource['formula']
        formualData = LSMIXD.data[formulaId]
        gamelog.debug('@hjx lifeSkill#_getNeedItems:', detailId, self._genReqDesc(detailId))
        self.needFineItem = {}
        index = 0
        for itemId, num in formualData.get('consumeItems', []):
            item = Item(itemId)
            obj = {}
            obj['isIdentity'] = LSQD.data.has_key(itemId) and self._checkIdentifyProbQuality(formualData, index)
            obj['data'] = []
            obj['data'].append(self._genNeedItem(itemId, num))
            if obj['isIdentity']:
                itemObj = self._genNeedItem(LSQD.data[itemId]['fineItemId'], num)
                if item.getIdentifyQuality():
                    identifyQualityDesc = gameStrings.TEXT_LIFESKILLFACTORY_1208 + str(item.getIdentifyQuality())
                else:
                    identifyQualityDesc = ''
                itemObj.update({'identifyQualityDesc': gameStrings.TEXT_LIFESKILLFACTORY_1212 + identifyQualityDesc})
                obj['data'].append(itemObj)
                self.needFineItem[LSQD.data[itemId]['fineItemId']] = 0
                identityData = formualData.get('identifyProbQuality', [])[index]
                obj['isIdentityTip'] = gameStrings.TEXT_LIFESKILLFACTORY_1218 % (identityData[0] / 100, identityData[1])
            ret['data'].append(obj)
            index += 1

        return uiUtils.dict2GfxDict(ret, True)

    def _getNeedItemsCountById(self, itemId):
        curFrame = BigWorld.getCurFrameNum()
        oldFrame = self.invCountCache.get('curFrame', 0)
        if oldFrame == curFrame:
            if self.invCountCache.has_key(itemId):
                return self.invCountCache[itemId]
        else:
            self.invCountCache.clear()
            self.invCountCache['curFrame'] = curFrame
        p = BigWorld.player()
        itemNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
        if gameglobal.rds.configData.get('enableMaterialBagManualLifeSkill', False) and p.getAbilityData(gametypes.ABILITY_MATERIAL_BAG_ON):
            materialBagNum = p.materialBag.getMaterialBagItemCount(itemId, enableParentCheck=True)
            itemNum += materialBagNum
        self.invCountCache[itemId] = itemNum
        return itemNum

    def _checkIdentifyProbQuality(self, data, num):
        if data.has_key('identifyProbQuality'):
            length = len(data.get('identifyProbQuality', []))
            if num < length:
                if data.get('identifyProbQuality', [])[num] != (0, 0):
                    return True
        else:
            return False

    def calTotalCnt(self):
        detailId = self.getDetailId()
        if detailId is None:
            return 0
        resourceId = LSMD.data[detailId]['resourceId']
        resource = LSRD.data[resourceId]
        formulaId = resource['formula']
        formualData = LSMIXD.data[formulaId]
        p = BigWorld.player()
        cnt = 100000
        for item in formualData.get('consumeItems', []):
            itemNum = self._getNeedItemsCountById(item[0])
            produceNum = itemNum / item[1]
            if produceNum < cnt:
                cnt = produceNum

        return cnt

    def getStepperInfo(self, direc):
        totalPage = self.calTotalCnt()
        if self.curPage == 1 and direc == -1:
            pass
        else:
            self.curPage += direc
        self.curPage = max(1, min(totalPage, self.curPage))
        stepperDict = {'totalPage': totalPage,
         'curPage': self.curPage}
        return uiUtils.dict2GfxDict(stepperDict)

    def getDetailInfo(self):
        ret = {}
        ret['produceItems'] = self._getProduceItems()
        ret['needItems'] = self._getNeedItems()
        ret['manuId'] = self.getDetailId()
        ret['showMakeBtn'] = gameglobal.rds.ui.lifeSkillNew.isLearnedAbility()
        ret['isShowGoAbilityBtn'] = gameglobal.rds.ui.lifeSkillNew.isShowGoAbilityBtn()
        ret['hintDesc'] = gameglobal.rds.ui.lifeSkillNew.getShowHintDesc()
        ret['canMake'] = self.isItemCanMake()
        return uiUtils.dict2GfxDict(ret, True)

    def isItemCanMake(self):
        if self.canMake:
            return self.getCanBuildNum(self.getDetailId())
        else:
            return 0

    def makeAllClick(self, num):
        detailId = self.getDetailId()
        if detailId is None:
            return
        p = BigWorld.player()
        userSpecifiedItems = self.collectFineItems()
        func = Functor(p.cell.useManuLifeSkill, detailId, num, [], userSpecifiedItems)
        if self.needBindAlert(detailId):
            self.showBindAlert(func)
        else:
            func()
        p.tLastMoving = utils.getNow()

    def collectFineItems(self):
        userSpecifiedItems = []
        for key, val in self.needFineItem.iteritems():
            if val:
                userSpecifiedItems.append(key)

        return userSpecifiedItems

    def getMakeAllInfo(self):
        ret = gameglobal.rds.ui.movie.CreateObject()
        detailId = self.getDetailId()
        if detailId is None:
            return ret
        ret.SetMember('data', self._getProduceItems())
        ret.SetMember('totalCnt', GfxValue(self.getCanBuildNum(detailId)))
        return ret

    def makeClick(self):
        detailId = self.getDetailId()
        if detailId is None:
            return
        p = BigWorld.player()
        if self.curPage == 0:
            return
        userSpecifiedItems = self.collectFineItems()
        func = Functor(p.cell.useManuLifeSkill, detailId, self.curPage, [], userSpecifiedItems)
        if self.needBindAlert(detailId):
            self.showBindAlert(func)
        else:
            func()

    def needBindAlert(self, detailId):
        resourceId = LSMD.data.get(detailId, {}).get('resourceId', 0)
        resource = LSRD.data.get(resourceId, {})
        mixId = resource.get('formula', 0)
        fData = LSMIXD.data.get(mixId, None)
        if fData.get('needBind', 0):
            return True
        return False

    def showBindAlert(self, callback):
        msg = SCD.data.get('USE_LIFE_SKILL_MSG', gameStrings.TEXT_LIFESKILLFACTORY_1371)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, callback)

    def getManuUsingLifeSkillInfo(self):
        p = BigWorld.player()
        usingLifeSkillInfo = {'curVal': int(utils.getNow() - p.manuSkillStartTimeStamp),
         'maxVal': int(p.manuSpellTime)}
        return usingLifeSkillInfo

    def getManuInfo(self):
        p = BigWorld.player()
        detailId = self.getDetailId()
        if p.curLifeSkillType == gametypes.LIFE_SKILL_TYPE_MANUFACTURE and p.usingLifeSkill:
            detailId = p.manuId
        else:
            detailId = 0
        if not detailId:
            return uiUtils.dict2GfxDict({})
        mData = LSMD.data[detailId]
        manuDict = {'desc': mData.get('name', ''),
         'manuId': detailId}
        manuDict.update(self.getManuUsingLifeSkillInfo())
        return uiUtils.dict2GfxDict(manuDict, True)

    def usingManuLifeSkillInfo(self):
        p = BigWorld.player()
        usingManuLifeSkillDict = {'usingManuLifeSkill': False if p.curLifeSkillType == gametypes.LIFE_SKILL_TYPE_COLLECTION else p.usingLifeSkill}
        if p.curLifeSkillType == gametypes.LIFE_SKILL_TYPE_MANUFACTURE and p.usingLifeSkill:
            usingManuLifeSkillDict.update(self.getManuUsingLifeSkillInfo())
        else:
            usingManuLifeSkillDict.update({'curVal': 0,
             'maxVal': 0})
        return uiUtils.dict2GfxDict(usingManuLifeSkillDict)


LIFE_SKILL_TYPE_PRODUCE = 0
LIFE_SKILL_TYPE_FISH = 1
LIFE_SKILL_TYPE_EXPLORE = 2

class SpecailSkillInfo(ILifeSkillInfo):

    def __init__(self):
        super(SpecailSkillInfo, self).__init__()
        self.FISH_MAX_LV = 0

    def getLeftListMenuInfo(self):
        ret = []
        p = BigWorld.player()
        fData = FLD.data.get(p.fishingLv)
        self.FISH_MAX_LV = max(FLD.data.keys())
        info = {'icon': {'iconPath': LIFE_SKILL_BIG_ICON_PATH + '1.dds'},
         'itemDesc': gameStrings.TEXT_ACTIONBARPROXY_1867 if p.fishingLv == self.FISH_MAX_LV else fData['name'],
         'itemLv': gameStrings.TEXT_LIFESKILLFACTORY_585 if p.fishingLv == self.FISH_MAX_LV else 'Lv.' + str(p.fishingLv),
         'itemTrueLv': p.fishingLv,
         'curVal': p.fishingExp,
         'stageLv': fData.get('stageLv', 0),
         'maxVal': fData['exp'],
         'data': [{'desc': gameStrings.TEXT_ACTIONBARPROXY_1867,
                   'icon': LIFE_SKILL_BIG_ICON_PATH + '1.dds',
                   'open': 1,
                   'descTag': 'diaoyu'}],
         'skillType': LIFE_SKILL_TYPE_FISH}
        ret.append(info)
        EXPLORE_MAX_LV = max(ELD.data.keys())
        eData = ELD.data.get(p.exploreLv, {})
        info = {'icon': {'iconPath': LIFE_SKILL_BIG_ICON_PATH + '2.dds'},
         'itemDesc': gameStrings.TEXT_ACTIONBARPROXY_1869 if p.exploreLv == EXPLORE_MAX_LV else eData['name'],
         'itemLv': gameStrings.TEXT_LIFESKILLFACTORY_585 if p.exploreLv == EXPLORE_MAX_LV else 'Lv.' + str(p.exploreLv),
         'itemTrueLv': p.exploreLv,
         'curVal': p.xiangyaoExp + p.xunbaoExp + p.zhuizongExp,
         'stageLv': eData.get('stageLv', 0),
         'maxVal': eData['exp'],
         'data': [{'desc': gameStrings.TEXT_ACTIONBARPROXY_1869,
                   'icon': LIFE_SKILL_BIG_ICON_PATH + '2.dds',
                   'open': 1,
                   'descTag': 'tanmi'}],
         'skillType': LIFE_SKILL_TYPE_EXPLORE}
        ret.append(info)
        self.firstMenuVal = [LIFE_SKILL_TYPE_FISH, LIFE_SKILL_TYPE_EXPLORE]
        self.secondMenuVal = [[LIFE_SKILL_TYPE_FISH]]
        return uiUtils.array2GfxAarry(ret, True)

    def clickHelp(self, skillType):
        if skillType == LIFE_SKILL_TYPE_FISH:
            gameglobal.rds.ui.lifeSkillGuide.show(uiConst.GUIDE_TYPE_FISHING)
        elif skillType == LIFE_SKILL_TYPE_EXPLORE:
            gameglobal.rds.ui.lifeSkillGuide.show(uiConst.GUIDE_TYPE_EXPLORE)

    def getDetailInfo(self):
        print '@hjx lifeSkill#SpecailSkillInfo#getDetailInfo0:'
        ret = []
        for i in xrange(self.FISH_MAX_LV / LV_INTERVAL):
            ret.append({'titleDesc': gameStrings.TEXT_LIFESKILLFACTORY_1482 % (i * LV_INTERVAL + 1, (i + 1) * LV_INTERVAL),
             'data': []})

        lifeSkillType = self.getLeftFirstId()
        if lifeSkillType == LIFE_SKILL_TYPE_FISH:
            for itemId, val in FD.data.iteritems():
                obj = {}
                if val.get('visible', 0) == 0:
                    continue
                if val['lv'] > self.FISH_MAX_LV:
                    continue
                iconPath = uiUtils.getItemIconFile40(itemId)
                pinXing = uiUtils.getPinXing(itemId)
                color = uiUtils.getItemColor(itemId)
                obj['icon'] = {'iconPath': iconPath,
                 'itemId': itemId,
                 'pinXing': pinXing}
                obj['color'] = color
                obj['itemId'] = itemId
                obj['desc'] = val['name']
                obj['difficulty'] = val.get('difficulty', 1)
                index = self.resLv2Index(val['lv'])
                ret[index]['data'].append(obj)

        elif lifeSkillType == LIFE_SKILL_TYPE_EXPLORE:
            pass
        print '@hjx lifeSkill#getDetailInfo1:', ret
        return uiUtils.array2GfxAarry(ret, True)


class KuiLingInfo(ILifeSkillInfo):

    def __init__(self, klId):
        self.kuiLingId = klId
        self.questTabType = 1
        self.questIds = []

    def reset(self):
        pass

    def getMaxFame(self, fame):
        dspMax = KCD.data[self.kuiLingId].get('dspMax', (200, 1000, 5000, 20000))
        for m in dspMax:
            if fame <= m:
                return m

        return 0

    def getKuiLingInfo(self):
        kData = KCD.data[self.kuiLingId]
        p = BigWorld.player()
        fameId = KCD.data[self.kuiLingId].get('fameId', 440)
        fame = p.fame.get(fameId, 0)
        info = {}
        info['id'] = self.kuiLingId
        info['desc'] = kData['description']
        info['curFame'] = fame
        info['maxFame'] = self.getMaxFame(fame)
        kuilingReduceFame = LSCD.data.get('kuilingReduceFame', 100)
        kuilingAddLabour = LSCD.data.get('kuilingAddLabour', 600)
        info['labourTips'] = gameStrings.TEXT_LIFESKILLFACTORY_1544 % (kuilingReduceFame, kuilingAddLabour / 10)
        gamelog.debug('@hjx kl#getKuiLingInfo:', info)
        return uiUtils.dict2GfxDict(info, True)

    def getQuestStatus(self, questId):
        p = BigWorld.player()
        qVal = p.kuilingQuests[questId]
        if p.getQuestData(questId, const.QD_FAIL):
            return (const.QUEST_STATUS_FAILED, gameStrings.TEXT_UICONST_3235_2)
        elif questId in p.quests:
            return (const.QUEST_STATUS_ACCEPTED, gameStrings.TEXT_LIFESKILLFACTORY_1555)
        elif qVal.status == const.QUEST_STATUS_DEFAULT:
            return (const.QUEST_STATUS_DEFAULT, '')
        elif qVal.status == const.QUEST_STATUS_SUCC:
            return (const.QUEST_STATUS_SUCC, gameStrings.TEXT_CC_286)
        else:
            gamelog.error('@hjx kuiling error quest status is not correct!!!')
            return (const.QUEST_STATUS_DEFAULT, '')

    def getBtnEnable(self, questId):
        if self.getQuestStatus(questId)[0] == const.QUEST_STATUS_DEFAULT:
            return True
        else:
            return False

    def getQuestDura(self, questId):
        qd = QD.data[questId]
        p = BigWorld.player()
        timeout = 0
        if qd.has_key('timeLimit') and not p.getQuestData(questId, const.QD_FAIL):
            limit = qd['timeLimit']
            timeout = p.getQuestData(questId, const.QD_BEGIN_TIME) + limit - p.getServerTime()
        return timeout

    def getLeftList(self):
        leftList = []
        p = BigWorld.player()
        index = 0
        self.questIds = []
        for questId, qVal in p.kuilingQuests.iteritems():
            self.questIds.append(questId)
            qData = QD.data[questId]
            info = {}
            info['name'] = qData['name']
            info['index'] = index
            info['status'], info['statusDesc'] = self.getQuestStatus(questId)
            if info['status'] == const.QUEST_STATUS_ACCEPTED:
                info['duration'] = self.getQuestDura(questId)
            leftList.append(info)
            index += 1

        gamelog.debug('@hjx kl#getLeftList:', leftList)
        return uiUtils.array2GfxAarry(leftList, True)

    def getCurItemCnt(self, questId, itemId):
        p = BigWorld.player()
        qd = p.getQuestData(questId, self.getQuestType(questId))
        if qd:
            return qd.get(itemId, 0)
        else:
            return 0

    def getQuestType(self, questId):
        questData = QD.data[questId]
        items = questData.get('needLifeSkillCollection', [])
        if items:
            return const.QD_QUEST_LIFESKILL_COLLECTION
        else:
            return const.QD_QUEST_LIFESKILL_MANUFACTURE

    def getStatsDesc(self, questId, itemId, maxCnt):
        if self.getQuestType(questId) == const.QD_QUEST_LIFESKILL_COLLECTION:
            desc = gameStrings.TEXT_ITEMTOOLTIPUTILS_123
        else:
            desc = gameStrings.TEXT_LIFESKILLFACTORY_1627
        desc += ID.data[itemId]['name']
        return desc

    def getKuilingFame(self, questId):
        for quest in KQD.data[self.kuiLingId]:
            if quest['questId'] == questId:
                return quest['fameAdd']

        return 0

    def getDetailInfo(self, index):
        if index >= len(self.questIds):
            return uiUtils.dict2GfxDict({})
        questId = self.questIds[index]
        questData = QD.data[questId]
        if self.getQuestType(questId) == const.QD_QUEST_LIFESKILL_COLLECTION:
            items = questData.get('needLifeSkillCollection', [])
        else:
            items = questData.get('needLifeSkillManufacture', [])
        info = {}
        info['desc'] = questData['desc']
        info['stats'] = []
        for item in items:
            info['stats'].append({'statsDesc': self.getStatsDesc(questId, item[0], item[1]),
             'curVal': self.getCurItemCnt(questId, item[0]),
             'maxVal': item[1]})

        info['awardItems'] = []
        rewardItems = questData.get('rewardItems', [])
        rewardItems = utils.filtItemByConfig(rewardItems, lambda e: e[0])
        for itemId, cnt in rewardItems:
            iconPath = uiUtils.getItemIconFile40(itemId)
            info['awardItems'].append({'iconPath': iconPath,
             'itemId': itemId,
             'count': cnt})

        info['btnEnabled'] = self.getBtnEnable(questId)
        totalExp, cashBonus, _, _ = commQuest.calcReward(BigWorld.player(), questId)
        info['money'] = gameStrings.TEXT_LIFESKILLFACTORY_1671 + str(cashBonus)
        info['exp'] = gameStrings.TEXT_LIFESKILLFACTORY_1672 + str(totalExp)
        info['fame'] = gameStrings.TEXT_LIFESKILLFACTORY_1673 + str(self.getKuilingFame(questId))
        return uiUtils.dict2GfxDict(info, True)

    def acceptQuest(self, index):
        p = BigWorld.player()
        if index >= len(self.questIds):
            return
        questId = self.questIds[index]
        p.cell.autoAcceptQuest(questId)

    def getRefreshTime(self):
        p = BigWorld.player()
        duration = SCD.data.get('kuilingRefreshCD', 600)
        if p.kuilingQuests.refreshTime:
            duration = p.kuilingQuests.refreshTime + duration - p.getServerTime()
            if duration <= 0:
                return 0
            else:
                return duration
        else:
            return 0


class LifeSkillFactory(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.resetLifeSkillIns()
        self.createLifeSkillIns()

    def createLifeSkillIns(self):
        try:
            self.lifeSkillIns[uiConst.PANEL_TYPE_LIFE_SKILL_OVERVIEW] = LifeSkillOverview()
            self.lifeSkillIns[uiConst.PANEL_TYPE_PRODUCE_SKILL] = ProduceSkillInfo()
            self.lifeSkillIns[uiConst.PANEL_TYPE_MAKE_SKILL] = MakeSkillInfo()
            self.lifeSkillIns[uiConst.PANEL_TYPE_SPECIAL_SKILL] = SpecailSkillInfo()
        except:
            print '@hjx error createLifeSkillIns'

    def resetLifeSkillIns(self):
        self.lifeSkillIns = {}

    def createKuiLingIns(self, kuiLingId):
        self.lifeSkillIns[uiConst.PANEL_TYPE_KUI_LING] = KuiLingInfo(kuiLingId)

    def getCurLifeSkillIns(self, pType):
        if self.lifeSkillIns.has_key(pType):
            return self.lifeSkillIns[pType]
        else:
            return None

    def getKuiLingOverview(self):
        overviewInfo = {}
        overviewInfo['desc'] = LSCD.data.get('kuilingOverviewInfo', '')
        kuiLing = []
        for key, val in KCD.data.iteritems():
            info = {}
            info['id'] = key
            info['name'] = val['name']
            info['desc'] = val['description']
            info['isOpen'] = val['isOpen']
            kuiLing.append(info)

        overviewInfo['kuiLing'] = kuiLing
        return uiUtils.dict2GfxDict(overviewInfo, True)

    def reset(self):
        for val in self.lifeSkillIns.itervalues():
            val.reset()


def getInstance():
    return LifeSkillFactory.getInstance()
