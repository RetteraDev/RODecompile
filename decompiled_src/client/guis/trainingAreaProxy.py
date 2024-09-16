#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/trainingAreaProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import gamelog
from ui import gbk2unicode
from uiProxy import SlotDataProxy
import const
import uiUtils
import tipUtils
import skillDataInfo
from gameclass import SkillInfo
from callbackHelper import Functor
from data import school_switch_ws_data as SSWD
from data import school_switch_general_data as SSGD
from data import school_switch_equipment_data as SSED
from data import training_monster_ref_data as TMRD
from data import school_data as SD
from data import monster_model_client_data as MMCD
from data import sys_config_data as SCD
SCHOOL_PATH_PREFIX = 'trainingArea/school/'
BOSS_PATH_PREFIX = 'trainingArea/boss/backGround/'
BOSS_ICON_PREFIX = 'trainingArea/boss/icon/'
EQUIP_ITEM_SET = set(['leftWeapon',
 'rightWeapon',
 'head',
 'body',
 'hand',
 'leg',
 'shoe',
 'ring1',
 'ring2',
 'necklace',
 'bullet',
 'trap',
 'earring1',
 'earring2'])
EQUIP_NUM = 16

class TrainingAreaProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(TrainingAreaProxy, self).__init__(uiAdapter)
        self.bindType = 'trainingArea'
        self.type = 'trainingArea'
        self.modelMap = {'getLeftInfo': self.onGetLeftInfo,
         'getRightInfo': self.onGetRightInfo,
         'leaveTrain': self.onLeaveTrain,
         'enterTrain': self.onEnterTrain,
         'chooseSchool': self.onChooseSchool,
         'chooseMonster': self.onChooseMonster,
         'clickReward': self.onClickReward,
         'getYeChaEnable': self.onGetYeChaEnable,
         'getTianZhaoEnable': self.onGetTianZhaoEnable}
        self.equip = []
        self.wushuangSkill = []
        self.schoolIndex = 1
        self.monsterId = 0
        self.totalMonster = len(TMRD.data)
        self.leftMediator = None
        self.rightMediator = None
        self.destroyOnHide = True
        self.npcId = None
        self.monsterIcon = []
        self.bossHistory = [0] * self.totalMonster
        self.bossScores = {}
        self.bossWeekScores = {}
        self.isShow = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_TRAINING_AREA_LEFT, Functor(self.onLeaveTrain, None))
        uiAdapter.registerEscFunc(uiConst.WIDGET_TRAINING_AREA_RIGHT, Functor(self.onLeaveTrain, None))
        uiAdapter.registerEscFunc(uiConst.WIDGET_TRAINING_AREA_MIDDLE, Functor(self.onLeaveTrain, None))

    def getMonsterIcon(self):
        self.monsterIcon = []
        for key in self.bossHistory:
            if key == 0:
                self.monsterIcon.append('')
            else:
                value = TMRD.data[key]
                self.monsterIcon.append(BOSS_ICON_PREFIX + value.get('monsterPath', 'Mohuamudeng') + '.dds')

        return self.monsterIcon

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_TRAINING_AREA_LEFT:
            self.leftMediator = mediator
            self.isShow = True
        elif widgetId == uiConst.WIDGET_TRAINING_AREA_RIGHT:
            self.rightMediator = mediator

    def getSlotID(self, key):
        gamelog.debug('bgf:getSlotID', key)
        _, pos = key.split('.')
        return (None, int(pos[4:]))

    def getSlotValue(self, movie, idItem, idCon):
        gamelog.debug('getSlotValue', idItem)
        if idItem < EQUIP_NUM:
            obj = movie.CreateObject()
            if self.equip and idItem < len(self.equip):
                obj.SetMember('iconPath', GfxValue(uiUtils.getItemIconFile64(self.equip[idItem])))
            return obj

    def show(self, npcId):
        self.setNpc(npcId)
        self.uiAdapter.loadWidget(uiConst.WIDGET_TRAINING_AREA_BG)
        self.uiAdapter.loadWidget(uiConst.WIDGET_TRAINING_AREA_LEFT)
        self.uiAdapter.loadWidget(uiConst.WIDGET_TRAINING_AREA_MIDDLE)
        self.uiAdapter.loadWidget(uiConst.WIDGET_TRAINING_AREA_RIGHT)
        p = BigWorld.player()
        p.ap.stopMove(True)
        p.ap.forceAllKeysUp()
        p.lockKey(gameglobal.KEY_POS_TRAINING_AREA)

    def clearWidget(self):
        self.isShow = False
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_TRAINING_AREA_BG)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_TRAINING_AREA_LEFT)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_TRAINING_AREA_MIDDLE)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_TRAINING_AREA_RIGHT)

    def reset(self):
        self.equip = []
        self.wushuangSkill = []
        self.leftMediator = None
        self.rightMediator = None
        self.npcId = None
        self.monsterIcon = []

    def getDataIndex(self):
        transData = SCD.data.get('training_area_school_additional', (1, 2, 3, 4, 5, 6, 1007))
        if self.schoolIndex < len(transData) + 1:
            return transData[self.schoolIndex - 1]
        return 0

    def onGetLeftInfo(self, *arg):
        obj = {}
        dataIndex = self.getDataIndex()
        ssgd = SSGD.data.get(dataIndex, {})
        school = ssgd['school']
        equipId = ssgd['equipmentId']
        obj['schoolName'] = SD.data.get(school, {})['name']
        ssed = SSED.data.get(equipId, {})
        obj['mabi'] = ssed.get('mabi', 0)
        obj['qijue'] = ssed.get('qijue', 0)
        obj['shuimian'] = ssed.get('shuimian', 0)
        obj['pohuai'] = ssed.get('pohuai', 0)
        obj['yinhou'] = ssed.get('yinhou', 0)
        obj['schoolPath'] = SCHOOL_PATH_PREFIX + str(school) + '.dds'
        obj['schoolIndex'] = self.schoolIndex
        obj['equip'] = []
        self.equip = []
        for item in EQUIP_ITEM_SET:
            equip = ssed.get(item, 0)
            if equip:
                self.equip.append(equip)
                equipObj = self.movie.CreateObject()
                equipObj.SetMember('iconPath', GfxValue(uiUtils.getItemIconFile64(equip)))
                obj['equip'].append([equipObj, uiUtils.getItemColor(equip)])

        obj.update(self.getWushuangSkillAndEquipDesc())
        return uiUtils.dict2GfxDict(obj, True)

    def getWushuangSkillAndEquipDesc(self):
        ret = {'equipDesc': gameStrings.TEXT_TRAININGAREAPROXY_165,
         'wushuangSkill': []}
        for i in xrange(0, 6):
            skillObj = self.movie.CreateObject()
            skillObj.SetMember('iconPath', GfxValue('skill/icon/error.dds'))
            ret['wushuangSkill'].append([skillObj, 0])

        if self.schoolIndex and self.monsterId:
            bossId = TMRD.data[self.monsterId]['id']
            sswd = SSWD.data.get((bossId, self.getDataIndex()), {})
            ret['equipDesc'] = sswd.get('equipDesc', '')
            self.wushuangSkill = sswd.get('wushuangSkills', [])
            for i, (skillId, skillLv) in enumerate(self.wushuangSkill):
                skillObj = self.movie.CreateObject()
                path = self._getSkillIcon(skillId, skillLv)
                skillObj.SetMember('iconPath', GfxValue(path))
                wsNeed = self._getWsSkillStar(skillId, skillLv)
                ret['wushuangSkill'][i] = [skillObj, wsNeed]

        return ret

    def _getSkillIcon(self, skillId, skillLv = 1):
        sd = skillDataInfo.ClientSkillInfo(skillId, skillLv)
        icon = sd.getSkillData('icon', 'error')
        return 'skill/icon/' + str(icon) + '.dds'

    def _getWsSkillStar(self, skillId, skillLv):
        if skillId == 0:
            return 0
        return skillDataInfo.getWsStarLv(SkillInfo(skillId, skillLv))

    def getKillMonsterNum(self):
        num = 0
        for schoolIndex in self.bossScores:
            for monsterId in self.bossScores[schoolIndex]:
                if self.bossScores[schoolIndex][monsterId] > 0:
                    num += 1

        return num

    def getPassedMonster(self):
        array = []
        for item in self.bossHistory:
            if item == 0:
                array.append(1)
            else:
                schoolScore = self.bossScores.get(self.getDataIndex(), {})
                array.append(schoolScore.get(item, 0))

        return array

    def getSchoolNum(self):
        num = 6
        if self._getEnableTrainingAreaYeCha():
            num += 1
        return num

    def onGetRightInfo(self, *arg):
        ret = {}
        monsterName = MMCD.data.get(self.monsterId, {}).get('name', gameStrings.TEXT_GAME_1747)
        bossData = TMRD.data.get(self.monsterId, {})
        star = bossData.get('star', 0)
        monsterDesc = bossData.get('monsterDesc', gameStrings.TEXT_GAME_1747)
        ret['monsterName'] = monsterName
        ret['star'] = star
        ret['monsterDesc'] = monsterDesc
        ret['totalMonster'] = self.totalMonster * self.getSchoolNum()
        killedMonster = self.getKillMonsterNum()
        ret['killedMonster'] = killedMonster
        score = self.bossScores.get(self.getDataIndex(), {}).get(self.monsterId, 0)
        weekScore = self.bossWeekScores.get(self.getDataIndex(), {}).get(self.monsterId, 0)
        ret['score'] = score
        ret['weekScore'] = weekScore
        monsterPath = BOSS_PATH_PREFIX + bossData.get('monsterPath', 'Mohuamudeng') + '.dds'
        ret['monsterPath'] = monsterPath
        ret['monsterIcon'] = self.getMonsterIcon()
        ret['bossId'] = self.bossHistory.index(self.monsterId)
        ret['monsterPassed'] = self.getPassedMonster()
        ret['tips'] = self.getTips()
        return uiUtils.dict2GfxDict(ret, True)

    def getTips(self):
        ret = []
        for key, value in sorted(TMRD.data.items(), key=lambda d: d[1].get('id', 0)):
            ret.append(value.get('tips', gameStrings.TEXT_GAME_1747))

        return ret

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        _, pos = self.getSlotID(key)
        if pos < EQUIP_NUM and pos < len(self.equip):
            equip = self.equip[pos]
            if equip:
                return tipUtils.getItemTipById(equip)
        if pos >= EQUIP_NUM and pos - EQUIP_NUM < len(self.wushuangSkill):
            skillId, skillLv = self.wushuangSkill[pos - EQUIP_NUM]
            if skillId != 0:
                tooltip = gameglobal.rds.ui.actionbar.formatToolTip(skillId, skillLv, True)
                return tooltip

    def onChooseSchool(self, *arg):
        self.schoolIndex = int(arg[3][0].GetString())
        if self.leftMediator:
            obj = self.onGetLeftInfo()
            self.leftMediator.Invoke('refreshLeftInfo', obj)
            for i in xrange(0, EQUIP_NUM):
                slotName = self.bindType + '.slot' + str(i)
                if slotName in self.binding:
                    slotData = self.movie.CreateObject()
                    if self.equip and i < len(self.equip):
                        slotData.SetMember('iconPath', GfxValue(uiUtils.getItemIconFile64(self.equip[i])))
                    self.binding[slotName][1].InvokeSelf(slotData)

        if self.rightMediator:
            obj = self.onGetRightInfo()
            self.rightMediator.Invoke('refreshRightInfo', obj)

    def getMonsterId(self, bossId):
        for key, value in TMRD.data.iteritems():
            if value['id'] == bossId:
                return key

    def onChooseMonster(self, *arg):
        bossId = int(arg[3][0].GetString())
        self.monsterId = self.bossHistory[bossId]
        if self.rightMediator:
            obj = self.onGetRightInfo()
            self.rightMediator.Invoke('refreshRightInfo', obj)
        if self.leftMediator:
            ret = self.getWushuangSkillAndEquipDesc()
            self.leftMediator.Invoke('setWushuangSkillAndEquipDesc', (GfxValue(gbk2unicode(ret['equipDesc'])), uiUtils.array2GfxAarry(ret['wushuangSkill'])))

    def onEnterTrain(self, *arg):
        dataIndex = self.getDataIndex()
        school = SSGD.data.get(dataIndex, {}).get('school', 0)
        if gameglobal.PIN_JIAN_TEST and school == const.SCHOOL_SHENTANG:
            gameglobal.rds.ui.systemTips.show(gameStrings.TEXT_TRAININGAREAPROXY_302)
            return
        if not self._getEnableTrainingAreaYeCha() and school == const.SCHOOL_YECHA:
            gameglobal.rds.ui.systemTips.show(gameStrings.TEXT_TRAININGAREAPROXY_305)
            return
        if not self.monsterId:
            return
        bossId = TMRD.data.get(self.monsterId, {}).get('id', 0)
        if self.npcId:
            npc = BigWorld.entity(self.npcId)
            if npc:
                npc.cell.executeTrainingFbAI(dataIndex, bossId)
        self.hide(True)
        BigWorld.player().unlockKey(gameglobal.KEY_POS_TRAINING_AREA)

    def onLeaveTrain(self, *arg):
        self.hide(True)
        BigWorld.player().unlockKey(gameglobal.KEY_POS_TRAINING_AREA)

    def setNpc(self, npcId):
        self.npcId = npcId
        npc = BigWorld.entity(npcId)
        if npc:
            self.uiAdapter.registerClear(npc)

    def initData(self, bossHistory, bossScores, bossWeekScores):
        self.bossHistory = list(bossHistory)
        res = [0] * self.totalMonster
        for item in self.bossHistory:
            res[TMRD.data.get(item, {}).get('id', 1) - 1] = item

        self.bossHistory = res
        self.monsterId = 0
        for item in self.bossHistory:
            if item:
                self.monsterId = item
                break

        self.bossScores = bossScores
        self.bossWeekScores = bossWeekScores

    def onClickReward(self, *arg):
        self.uiAdapter.trainingAreaAward.show()

    def onGetYeChaEnable(self, *arg):
        return GfxValue(self._getEnableTrainingAreaYeCha())

    def onGetTianZhaoEnable(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableNewSchoolTianZhao', False))

    def _getEnableTrainingAreaYeCha(self):
        if gameglobal.rds.configData.get('enableNewSchoolYeCha', False) and gameglobal.rds.configData.get('enableTrainingAreaYeCha', False):
            return True
        return False
