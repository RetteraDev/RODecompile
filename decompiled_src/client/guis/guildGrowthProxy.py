#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildGrowthProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import utils
import commGuild
import gameconfigCommon
from ui import gbk2unicode
from callbackHelper import Functor
from guis import uiConst
from uiProxy import SlotDataProxy
from guis import uiUtils
from gamestrings import gameStrings
from data import guild_config_data as GCD
from data import guild_growth_data as GGD
from data import guild_growth_volumn_data as GGVD
from data import guild_growth_prop_data as GGPD
from data import prop_ref_data as PRD
from data import guild_pskill_data as GPD
from data import skill_client_data as SKCD
from cdata import pskill_data as PD
from cdata import pskill_template_data as PSTD
from data import jingjie_config_data as JJCD
from data import guild_technology_data as GTD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
RESEARCH_PSKILL_PANEL = 0
LEARN_GROWTH_BASE_PANEL = 1
LEARN_GROWTH_ADVANCE_PANEL = 2
ACTIVATE_GROWTH_PANEL = 3
LEARN_GROWTH_BASE_IDX = 0
LEARN_GROWTH_ADVANCE_IDX = 1
LEARN_ADVANCE_OPEN_VOLUMN = 10004

class GuildGrowthProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(GuildGrowthProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickManager': self.onClickManager,
         'regress': self.onRegress,
         'confirm': self.onConfirm,
         'getInitData': self.onGetInitData,
         'getPSkillBaseData': self.onGetPSkillBaseData,
         'getGrowthBaseData': self.onGetGrowthBaseData,
         'getLearnGrowthBtnState': self.onGetLearnGrowthBtnState,
         'getResearchPSkillDetail': self.onGetResearchPSkillDetail,
         'getLearnGrowthDetail': self.onGetLearnGrowthDetail,
         'getActivateGrowthDetail': self.onGetActivateGrowthDetail,
         'getTabIdx': self.onGetTabIdx,
         'clickFly': self.onClickFly,
         'clickGetReward': self.onClickGetReward,
         'enableGuildGrowthScoreReward': self.onEnableGuildGrowthScoreReward,
         'getRewardBtnRedPot': self.onGetRewardBtnRedPot}
        self.mediator = None
        self.bindType = 'guildGrowth'
        self.type = 'guildGrowth'
        self.markerId = 0
        self.buildLv = 0
        self.learnMoney = 0
        self.learnExp = 0
        self.selectItem = {}
        self.checkAllPSkillTimer = False
        self.isNPCFlag = False
        self.useNPCTab = False
        self.tabIdx = 0
        self.learnGrowthStageMap = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_GROWTH, self.hide)

    def reset(self):
        self.markerId = 0
        self.buildLv = 0
        self.selectItem = {}
        self.checkAllPSkillTimer = False
        self.isNPCFlag = False
        self.useNPCTab = False
        self.tabIdx = 0
        self.learnGrowthStageMap = {}

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_GROWTH:
            self.mediator = mediator
            self.updateAuthorization()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_GROWTH)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def needChangeToGuild(self):
        p = BigWorld.player()
        if not p.guildNUID:
            return (False, 0)
        guild = p.guild
        markerId = commGuild.getMarkerIdByBuildingId(guild, gametypes.GUILD_BUILDING_GROWTH_ID)
        if markerId:
            buildingNUID = guild.marker[markerId].buildingNUID
        else:
            buildingNUID = 0
        buildValue = guild.building.get(buildingNUID) if buildingNUID else None
        if buildValue and buildValue.level > 0:
            return (True, buildValue.markerId)
        else:
            return (False, 0)

    def show(self, markerId, tabIdx = 0, isNPCFlag = False, needChange = True):
        if isNPCFlag:
            useNPCTab = True
            if needChange:
                need, newMarkerId = self.needChangeToGuild()
                if need:
                    isNPCFlag = False
                    markerId = newMarkerId
        else:
            useNPCTab = False
        gameglobal.rds.ui.guild.hideAllGuildBuilding()
        self.markerId = markerId
        self.tabIdx = tabIdx
        self.isNPCFlag = isNPCFlag
        self.useNPCTab = useNPCTab
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_GROWTH)

    def onGetInitData(self, *arg):
        info = {}
        info['isNPCFlag'] = self.isNPCFlag
        info['useNPCTab'] = self.useNPCTab
        if self.isNPCFlag:
            self.buildLv = 0
        else:
            guild = BigWorld.player().guild
            marker = guild.marker.get(self.markerId)
            buildValue = guild.building.get(marker.buildingNUID) if marker else None
            self.buildLv = buildValue.level if buildValue else 0
        info['level'] = gameStrings.TEXT_GUILDACTIVITYPROXY_153 % self.buildLv
        _, info['showAdvanceTab'] = self.getVolumnData(LEARN_ADVANCE_OPEN_VOLUMN)
        return uiUtils.dict2GfxDict(info, True)

    def onGetTabIdx(self, *arg):
        return GfxValue(self.tabIdx)

    def updateAuthorization(self):
        if self.mediator:
            self.mediator.Invoke('updateAuthorization', GfxValue(gameglobal.rds.ui.guild.checkAuthorization(gametypes.GUILD_ACTION_SKILL_LEARN, False)))

    def onClickManager(self, *arg):
        gameglobal.rds.ui.guildResidentManager.showOrHide(self.markerId)

    def onRegress(self, *arg):
        if not self.mediator:
            return
        else:
            idx = int(arg[3][0].GetNumber())
            p = BigWorld.player()
            type = int(arg[3][1].GetNumber())
            propId = int(arg[3][2].GetNumber())
            playerVolumn = p.guildGrowth.getVolumn(type)
            growthVal = playerVolumn.getGrowth(propId)
            level = growthVal.level
            propName = PRD.data.get(propId, {}).get('name', '')
            gData = GGD.data.get((playerVolumn.volumnId, propId, level))
            exp = gData.get('exp', 0)
            contrib = p.guildGressLearnContribData.get((playerVolumn.volumnId, propId, level), 0)
            if not contrib:
                contrib = gData.get('contrib', 0)
            item = gData.get('item', None)
            itemId = 0
            itemNum = 0
            if item:
                itemId, itemNum = item[0]
            msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_GROWTH_REGRESS_CONFIRM_MSG, '%s %d %d %d %d') % (propName,
             level - 1,
             exp,
             contrib,
             itemNum)
            if not gameglobal.rds.ui.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_GUILD_GROWTH_REGRESS_CONFIRM):
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(p.cell.guildGrowthRegress, playerVolumn.volumnId, propId), yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL, isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_GUILD_GROWTH_REGRESS_CONFIRM)
            else:
                p.cell.guildGrowthRegress(playerVolumn.volumnId, propId)
            return

    def onConfirm(self, *arg):
        idx = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if idx == RESEARCH_PSKILL_PANEL:
            sid = int(arg[3][1].GetNumber())
            research = arg[3][2].GetBool()
            if research:
                msg = gameStrings.TEXT_GUILDGROWTHPROXY_200
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.researchGuildPSkill, sid))
            else:
                guild = p.guild
                nowLevel = 0
                if guild.pskill.has_key(sid):
                    nowLevel = guild.pskill[sid].level
                pSkillData = GPD.data.get((sid, nowLevel + 1), {})
                if pSkillData.get('bindCash', 0) + guild.bindCash > guild._getMaxBindCash() or pSkillData.get('mojing', 0) + guild.mojing > guild._getMaxMojing() or pSkillData.get('xirang', 0) + guild.xirang > guild._getMaxXirang() or pSkillData.get('wood', 0) + guild.wood > guild._getMaxWood():
                    msg = gameStrings.TEXT_GUILDGROWTHPROXY_213
                else:
                    msg = gameStrings.TEXT_GUILDGROWTHPROXY_215
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.cancelResearchGuildPSkill, sid))
        elif idx == LEARN_GROWTH_BASE_PANEL or idx == LEARN_GROWTH_ADVANCE_PANEL:
            type = int(arg[3][1].GetNumber())
            propId = int(arg[3][2].GetNumber())
            playerVolumn = p.guildGrowth.getVolumn(type)
            playerLevel = 0
            if playerVolumn.has_key(propId):
                playerLevel = playerVolumn[propId].level
            noRegressPropList = p.guildGrowthNoRegress.get(playerVolumn.volumnId, [])
            guildGrowthCanBackReturnProps = SCD.data.get('guildGrowthCanBackReturnProps', {})
            returnPropsList = guildGrowthCanBackReturnProps.get(type, ())
            if propId not in noRegressPropList and propId in returnPropsList and gameconfigCommon.enableGuildGrowthRegress():
                msg = gameStrings.GUILD_GROWTH_LEARN_CONFIRM_REGRESS_MSG
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(gameglobal.rds.ui.skill.gotoGetSkillEnhancePoint, self.learnExp, self.learnMoney, Functor(self.gotoLearnGuildGrowth, type, propId, playerLevel + 1)))
            elif not gameglobal.rds.ui.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_PLAYER_XIU_LIAN_SURE):
                msg = gameStrings.GUILD_GROWTH_LEARN_CONFIRM_MSG
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(gameglobal.rds.ui.skill.gotoGetSkillEnhancePoint, self.learnExp, self.learnMoney, Functor(self.gotoLearnGuildGrowth, type, propId, playerLevel + 1)), isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_PLAYER_XIU_LIAN_SURE)
            else:
                gameglobal.rds.ui.skill.gotoGetSkillEnhancePoint(self.learnExp, self.learnMoney, Functor(self.gotoLearnGuildGrowth, type, propId, playerLevel + 1))
        elif idx == ACTIVATE_GROWTH_PANEL:
            type = int(arg[3][1].GetNumber())
            propId = int(arg[3][2].GetNumber())
            canActivate = arg[3][3].GetBool()
            if canActivate:
                msg = gameStrings.TEXT_GUILDGROWTHPROXY_250
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.activateGuildGrowth, type, propId))
            else:
                msg = gameStrings.TEXT_GUILDGROWTHPROXY_253
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.deactivateGuildGrowth, type, propId))

    def refreshInfo(self):
        if not self.mediator:
            return
        self.mediator.Invoke('refreshInfo')

    def gotoLearnGuildGrowth(self, type, propId, slv):
        p = BigWorld.player()
        if not self.isNPCFlag:
            p.cell.learnGuildGrowth(type, propId, slv, 0, 0)
        else:
            p.cell.learnNPCGrowth(type, propId, slv, 0, 0)

    def onGetLearnGrowthBtnState(self, *arg):
        btnType = arg[3][0].GetNumber()
        if btnType == LEARN_GROWTH_ADVANCE_IDX:
            ret = self.checkLearnGrowthAdvanceBtnState()
        else:
            ret = self.checkLearnGrowthBaseBtnState()
        return uiUtils.array2GfxAarry(ret, True)

    def checkLearnGrowthBaseBtnState(self):
        p = BigWorld.player()
        LEARN_GROWTH_JINGJIE_LIMIT = JJCD.data.get('LEARN_GROWTH_JINGJIE_LIMIT', 3)
        if p.jingJie < LEARN_GROWTH_JINGJIE_LIMIT:
            jName = utils.jingJie2Name(LEARN_GROWTH_JINGJIE_LIMIT)
            ret = [False, gameStrings.TEXT_GUILDGROWTHPROXY_282 % jName]
        else:
            ret = [True, '']
        return ret

    def checkLearnGrowthAdvanceBtnState(self):
        baseState = self.checkLearnGrowthBaseBtnState()
        if baseState[0]:
            tips, advanceTabState = self.getVolumnData(LEARN_ADVANCE_OPEN_VOLUMN)
            if not advanceTabState:
                name = GGVD.data.get(LEARN_ADVANCE_OPEN_VOLUMN, {}).get('name', '')
                advance = [False, gameStrings.GUILD_GROWTH_LEARN_ADVANCE_NAME + tips[len(name):]]
                return advance
        return baseState

    def onGetPSkillBaseData(self, *arg):
        p = BigWorld.player()
        sortData = []
        pskill = {}
        for value in GPD.data.itervalues():
            sid = value.get('skillId', 0)
            if sid not in pskill:
                sortData.append([sid, value.get('sortId', 0)])
                pskill[sid] = {}
                if value.get('type', 1) == gametypes.GUILD_PSKILL_TYPE_ACTIVE:
                    pskill[sid]['iconPath'] = 'skill/icon/%d.dds' % SKCD.data.get((sid, 1), {}).get('icon', 0)
                else:
                    pskill[sid]['iconPath'] = 'skill/icon/%d.dds' % PSTD.data.get(sid, {}).get('icon', 0)

        sortData.sort(key=lambda x: x[1])
        sortId = 0
        for sid, _ in sortData:
            pskill[sid]['sortId'] = sortId
            pskill[sid]['x'] = 4 + sortId % 4 * 55
            pskill[sid]['y'] = sortId / 4 * 55
            sortId += 1

        for sid in pskill.iterkeys():
            if p.guildMemberSkills.has_key(sid):
                pskill[sid]['nowLevel'] = p.guildMemberSkills[sid].level
            else:
                pskill[sid]['nowLevel'] = 0
            if p.guild.pskill.has_key(sid):
                pskill[sid]['maxLevel'] = p.guild.pskill[sid].level
            else:
                pskill[sid]['maxLevel'] = 0
            techId = GPD.data.get((sid, 1), {}).get('techId', 0)
            techVal = p.guild.technology.get(techId, None)
            if techVal and not techVal.isAvail():
                pskill[sid]['techTips'] = gameStrings.TEXT_GUILDFACTORYPROXY_127 % GTD.data.get(techId, {}).get('name', '')
            else:
                pskill[sid]['techTips'] = ''

        return uiUtils.dict2GfxDict(pskill, True)

    def onGetGrowthBaseData(self, *arg):
        p = BigWorld.player()
        dataList = []
        for key, value in GGVD.data.iteritems():
            if not self.isNPCFlag:
                guildvolumn = p.guild.getGrowthVolumn(key)
            playerVolumn = p.guildGrowth.getVolumn(key)
            dataItem = {}
            dataItem['type'] = key
            dataItem['name'] = value.get('name', '')
            dataItem['tips'], dataItem['btnState'] = self.getVolumnData(key)
            dataItem['children'] = []
            dataItem['stageIdx'] = value.get('stageIdx', '')
            self.learnGrowthStageMap[key] = dataItem['stageIdx']
            props = value.get('props', ())
            for propId in props:
                if not self.isNPCFlag:
                    growthData = self.getTreeNodeData(guildvolumn, playerVolumn, key, propId)
                else:
                    growthData = self.getNPCTreeNodeData(playerVolumn, key, propId)
                dataItem['children'].append(growthData)

            dataList.append(dataItem)

        return uiUtils.array2GfxAarry(dataList, True)

    def getGrowthMaxLevel(self, type, propId, nowLv):
        maxLevel = 0
        reqLv = 0
        while 1:
            growthData = GGD.data.get((type, propId, maxLevel + 1), {})
            if not growthData:
                reqLv = -1
                break
            reqLv = growthData.get('reqLv', 0)
            if reqLv == -1 or nowLv < reqLv:
                break
            maxLevel += 1

        if self.isNPCFlag:
            NPCMaxLevel = GGVD.data.get(type, {}).get('npcMaxLv', 0)
            if NPCMaxLevel and NPCMaxLevel < maxLevel:
                reqLv = -1
                return (NPCMaxLevel, reqLv)
        return (maxLevel, reqLv)

    def getTreeNodeData(self, guildvolumn, playerVolumn, type, propId):
        p = BigWorld.player()
        growthData = {}
        growthData['type'] = type
        growthData['propId'] = propId
        growthData['name'] = PRD.data.get(propId, {}).get('name', '')
        growthData['extraProps'] = self.getExtraPropsName(playerVolumn.volumnId, propId)
        maxLevel, _ = self.getGrowthMaxLevel(type, propId, p.realLv)
        if playerVolumn.has_key(propId) and maxLevel > 0:
            growthData['levelState'] = '%d/%d' % (playerVolumn[propId].level, maxLevel)
            growthData['currentValue'] = 100.0 * playerVolumn[propId].level / maxLevel
        else:
            growthData['levelState'] = '0/%d' % maxLevel
            growthData['currentValue'] = 0
        if guildvolumn.has_key(propId) and guildvolumn.get(propId).active:
            growthData['activateState'] = 'light'
            growthData['activateIconText'] = gameStrings.TEXT_GUILDGROWTHPROXY_406
        else:
            growthData['activateState'] = 'gray'
            growthData['activateIconText'] = gameStrings.TEXT_GUILDGROWTHPROXY_409
        return growthData

    def getExtraPropsName(self, volumnId, propId):
        if not gameconfigCommon.enableGuildGrowthExtraPropsAdd():
            return []
        propInfo = GGD.data.get((volumnId, propId, 1), {})
        attachNameList = []
        attaches = propInfo.get('extraProps', ())
        for id, _ in attaches:
            attachNameList.append(PRD.data.get(id, {}).get('name', ''))

        return '/'.join(attachNameList)

    def getNPCTreeNodeData(self, playerVolumn, type, propId):
        p = BigWorld.player()
        growthData = {}
        growthData['type'] = type
        growthData['propId'] = propId
        growthData['name'] = PRD.data.get(propId, {}).get('name', '')
        growthData['extraProps'] = self.getExtraPropsName(playerVolumn.volumnId, propId)
        maxLevel, _ = self.getGrowthMaxLevel(type, propId, p.realLv)
        if playerVolumn.has_key(propId):
            growthData['levelState'] = '%d/%d' % (playerVolumn[propId].level, maxLevel)
            growthData['currentValue'] = 100.0 * playerVolumn[propId].level / maxLevel
        else:
            growthData['levelState'] = '0/%d' % maxLevel
            growthData['currentValue'] = 0
        growthData['activateState'] = 'light'
        growthData['activateIconText'] = gameStrings.TEXT_EQUIPSOULPROXY_1042
        return growthData

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        sid = int(key[11:])
        p = BigWorld.player()
        level = p.guild.pskill[sid].level if p.guild.pskill.has_key(sid) else 0
        return gameglobal.rds.ui.skill.getGuildSkillTip(sid, level)

    def researchPSkillTimer(self, skillId, level, leftTime):
        if self.mediator:
            totleTime = GPD.data.get((skillId, level), {}).get('time', 0)
            currentValue = 100.0
            if totleTime >= leftTime:
                currentValue = currentValue * (totleTime - leftTime) / totleTime
            leftTimeText = uiUtils.formatTime(leftTime)
            self.mediator.Invoke('setResearchPSkillTimer', (GfxValue(skillId), GfxValue(gbk2unicode(leftTimeText)), GfxValue(int(currentValue))))

    def onGetResearchPSkillDetail(self, *arg):
        sid = int(arg[3][0].GetNumber())
        self.selectItem[RESEARCH_PSKILL_PANEL] = sid
        self.updateResearchPSkillDetail(sid)

    def updateResearchPSkillNode(self, sid):
        p = BigWorld.player()
        if self.mediator:
            info = {}
            info['sid'] = sid
            maxLevel = 0
            if p.guild.pskill.has_key(sid):
                maxLevel = p.guild.pskill[sid].level
            info['maxLevel'] = maxLevel
            techId = GPD.data.get((sid, 1), {}).get('techId', 0)
            techVal = p.guild.technology.get(techId, None)
            if techVal and not techVal.isAvail():
                info['techTips'] = gameStrings.TEXT_GUILDFACTORYPROXY_127 % GTD.data.get(techId, {}).get('name', '')
            else:
                info['techTips'] = ''
            self.mediator.Invoke('updateResearchPSkillNode', uiUtils.dict2GfxDict(info, True))
        self.updateResearchPSkillDetail(sid)

    def updateResearchPSkillDetail(self, sid):
        if self.selectItem.get(RESEARCH_PSKILL_PANEL, 0) != sid:
            return
        else:
            if self.mediator:
                p = BigWorld.player()
                guild = p.guild
                dataDict = {}
                dataDict['sid'] = sid
                dataDict['skillName'] = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_660 % GPD.data.get((sid, 1), {}).get('name', '')
                nowLevel = 0
                if guild.pskill.has_key(sid):
                    nowLevel = guild.pskill[sid].level
                dataDict['pskillNowLv'] = gameStrings.TEXT_GUILDGROWTHPROXY_501 % nowLevel
                dataDict['pskillNextLv'] = gameStrings.TEXT_GUILDGROWTHPROXY_502 % (nowLevel + 1)
                pSkillData = GPD.data.get((sid, nowLevel + 1), {})
                if GPD.data.get((sid, 1), {}).get('type', 1) == gametypes.GUILD_PSKILL_TYPE_ACTIVE:
                    dataDict['iconPath'] = 'skill/icon/%d.dds' % SKCD.data.get((sid, 1), {}).get('icon', 0)
                    if nowLevel == 0:
                        dataDict['pskillNowDesc'] = gameStrings.TEXT_BATTLEFIELDPROXY_1605
                    else:
                        dataDict['pskillNowDesc'] = p.getSkillTipsInfo(sid, nowLevel).getSkillData('mainEff', '')
                    if pSkillData:
                        dataDict['pskillNextDesc'] = p.getSkillTipsInfo(sid, nowLevel + 1).getSkillData('mainEff', '')
                else:
                    dataDict['iconPath'] = 'skill/icon/%d.dds' % PSTD.data.get(sid, {}).get('icon', 0)
                    if nowLevel == 0:
                        dataDict['pskillNowDesc'] = gameStrings.TEXT_BATTLEFIELDPROXY_1605
                    else:
                        dataDict['pskillNowDesc'] = PD.data.get((sid, nowLevel), {}).get('mainEff', '')
                    if pSkillData:
                        dataDict['pskillNextDesc'] = PD.data.get((sid, nowLevel + 1), {}).get('mainEff', '')
                if not pSkillData:
                    dataDict['isMaxLevel'] = True
                else:
                    dataDict['isMaxLevel'] = False
                    enabledState = True
                    level = gameStrings.TEXT_GUILDACTIVITYPROXY_153 % pSkillData.get('bldLv', 0)
                    levelHave = gameStrings.TEXT_GUILDACTIVITYPROXY_153 % self.buildLv
                    if pSkillData.get('bldLv', 0) > self.buildLv:
                        levelHave = uiUtils.toHtml(levelHave, '#F43804')
                        enabledState = False
                    dataDict['level'] = level
                    dataDict['levelHave'] = levelHave
                    dataDict['cashName'] = gameStrings.TEXT_GUILDGROWTHPROXY_537
                    cash = format(pSkillData.get('bindCash', 0), ',')
                    cashHave = format(guild.bindCash, ',')
                    if pSkillData.get('bindCash', 0) > guild.bindCash:
                        cashHave = uiUtils.toHtml(cashHave, '#F43804')
                        enabledState = False
                    dataDict['cash'] = cash
                    dataDict['cashHave'] = cashHave
                    dataDict['woodName'] = gameStrings.TEXT_CONST_7489
                    wood = format(pSkillData.get('wood', 0), ',')
                    woodHave = format(guild.wood, ',')
                    if pSkillData.get('wood', 0) > guild.wood:
                        woodHave = uiUtils.toHtml(woodHave, '#F43804')
                        enabledState = False
                    dataDict['wood'] = wood
                    dataDict['woodHave'] = woodHave
                    dataDict['mojingName'] = gameStrings.TEXT_CONST_7487
                    mojing = format(pSkillData.get('mojing', 0), ',')
                    mojingHave = format(guild.mojing, ',')
                    if pSkillData.get('mojing', 0) > guild.mojing:
                        mojingHave = uiUtils.toHtml(mojingHave, '#F43804')
                        enabledState = False
                    dataDict['mojing'] = mojing
                    dataDict['mojingHave'] = mojingHave
                    dataDict['xirangName'] = gameStrings.TEXT_CONST_7488
                    xirang = format(pSkillData.get('xirang', 0), ',')
                    xirangHave = format(guild.xirang, ',')
                    if pSkillData.get('xirang', 0) > guild.xirang:
                        xirangHave = uiUtils.toHtml(xirangHave, '#F43804')
                        enabledState = False
                    dataDict['xirang'] = xirang
                    dataDict['xirangHave'] = xirangHave
                    techId = GPD.data.get((sid, 1), {}).get('techId', 0)
                    tech = GTD.data.get(techId, {}).get('name', '')
                    if tech != '':
                        techVal = guild.technology.get(techId, None)
                        if techVal and not techVal.isAvail():
                            techHave = uiUtils.toHtml(gameStrings.TEXT_GUILDGROWTHPROXY_578, '#F43804')
                            enabledState = False
                        else:
                            techHave = gameStrings.TEXT_GUILDGROWTHPROXY_581
                    else:
                        tech = gameStrings.TEXT_BATTLEFIELDPROXY_1605
                        techHave = gameStrings.TEXT_GUILDGROWTHPROXY_581
                    dataDict['tech'] = tech
                    dataDict['techHave'] = techHave
                    dataDict['enabledState'] = enabledState
                    pskillVal = guild.pskill.get(sid, None)
                    dataDict['time'] = gameStrings.TEXT_GUILDGROWTHPROXY_591 % uiUtils.formatTime(pskillVal.getResearchTime(guild)) if pskillVal else ''
                self.mediator.Invoke('updateDetail', (GfxValue(RESEARCH_PSKILL_PANEL), uiUtils.dict2GfxDict(dataDict, True)))
                if self.checkAllPSkillTimer:
                    if guild.pskill.has_key(sid):
                        if guild.pskill[sid].isUpgrading():
                            guild.pskill[sid].start()
                else:
                    self.checkAllPSkillTimer = True
                    for _sid in guild.pskill.iterkeys():
                        if guild.pskill[_sid].isUpgrading():
                            guild.pskill[_sid].start()

            return

    def onGetLearnGrowthDetail(self, *arg):
        type = int(arg[3][0].GetNumber())
        propId = int(arg[3][1].GetNumber())
        stage = self.learnGrowthStageMap.get(type, -1)
        if stage == -1:
            return
        if stage == LEARN_GROWTH_BASE_IDX:
            self.selectItem[LEARN_GROWTH_BASE_PANEL] = (type, propId)
        elif stage == LEARN_GROWTH_ADVANCE_IDX:
            self.selectItem[LEARN_GROWTH_ADVANCE_PANEL] = (type, propId)
        self.updateLearnGrowthDetail(type, propId, stage)

    def updateLearnGrowthTree(self, type, propId):
        p = BigWorld.player()
        playerVolumn = p.guildGrowth.getVolumn(type)
        stage = self.learnGrowthStageMap.get(type, -1)
        if stage == -1:
            return
        if not self.isNPCFlag:
            guildvolumn = p.guild.getGrowthVolumn(type)
            growthData = self.getTreeNodeData(guildvolumn, playerVolumn, type, propId)
        else:
            growthData = self.getNPCTreeNodeData(playerVolumn, type, propId)
        if self.mediator:
            learnBtnState = self.checkLearnGrowthAdvanceBtnState()
            self.mediator.Invoke('updatetLearnAdvanceBtnState', uiUtils.array2GfxAarry(learnBtnState, True))
            growthData['stageIdx'] = stage
            self.mediator.Invoke('updateTreeSecondNodeData', uiUtils.dict2GfxDict(growthData, True))
            volumnList = []
            for key, value in GGVD.data.iteritems():
                volumnData = {}
                volumnData['type'] = key
                volumnData['tips'], volumnData['btnState'] = self.getVolumnData(key)
                volumnData['stageIdx'] = value.get('stageIdx', 0)
                volumnList.append(volumnData)

            self.mediator.Invoke('updateTreeFirstNodeData', uiUtils.array2GfxAarry(volumnList, True))
        self.updateLearnGrowthDetail(type, propId, stage)

    def updateLearnGrowthDetail(self, type, propId, stage):
        if stage == LEARN_GROWTH_BASE_IDX:
            if self.selectItem.get(LEARN_GROWTH_BASE_PANEL, ()) != (type, propId):
                return
        elif stage == LEARN_GROWTH_ADVANCE_IDX:
            if self.selectItem.get(LEARN_GROWTH_ADVANCE_PANEL, ()) != (type, propId):
                return
        if self.mediator:
            p = BigWorld.player()
            guild = p.guild
            dataDict = {}
            dataDict['partScore'] = gameStrings.TEXT_GUILDGROWTHPROXY_663 % (GGVD.data.get(type, {}).get('name', ''), p.guildGrowth.getVolumn(type).score)
            totalScore = 0
            for key in p.guildGrowth:
                totalScore += p.guildGrowth[key].score

            dataDict['totalScore'] = gameStrings.TEXT_GUILDGROWTHPROXY_667 % totalScore
            playerVolumn = p.guildGrowth.getVolumn(type)
            maxLevel, reqLv = self.getGrowthMaxLevel(type, propId, p.realLv)
            playerLevel = 0
            if playerVolumn.has_key(propId):
                playerLevel = playerVolumn[propId].level
            growthName = PRD.data.get(propId, {}).get('name', '')
            nowGrowthData = GGD.data.get((type, propId, playerLevel), {})
            nextGrowthData = GGD.data.get((type, propId, playerLevel + 1), {})
            extraProps = nowGrowthData.get('extraProps', ())
            nextExtraProps = nextGrowthData.get('extraProps', ())
            extraPropsInfo = []
            if gameconfigCommon.enableGuildGrowthExtraPropsAdd():
                for nextId, nextVal in nextExtraProps:
                    extraPropName = PRD.data.get(nextId, {}).get('name', '')
                    nowValue = 0
                    for id, value in extraProps:
                        if id == nextId:
                            nowValue = value
                            break

                    extraPropNowDesc = '+%d' % nowValue
                    extraPropNextDesc = '+%d' % nextVal
                    extraPropsInfo.append((extraPropName, extraPropNowDesc, extraPropNextDesc))

            dataDict['extraPropsInfo'] = extraPropsInfo
            reqSkillEnhancePoint = nextGrowthData.get('skillEnhancePoint', 0)
            guildGrowthCanBackReturnProps = SCD.data.get('guildGrowthCanBackReturnProps', {})
            noRegressPropList = p.guildGrowthNoRegress.get(type, [])
            dataDict['canRegress'] = playerLevel and propId in guildGrowthCanBackReturnProps.get(playerVolumn.volumnId, ()) and gameconfigCommon.enableGuildGrowthRegress()
            dataDict['grayRegress'] = propId in noRegressPropList
            dataDict['growthNowLevel'] = playerLevel
            dataDict['growthNowLevelField'] = gameStrings.TEXT_GUILDGROWTHPROXY_501 % playerLevel
            dataDict['growthNowNameField'] = growthName
            dataDict['growthNowDescField'] = '+%d' % int(nowGrowthData.get('value', 0))
            if playerLevel >= maxLevel:
                dataDict['isMaxLevel'] = True
                if reqLv == -1:
                    if not self.isNPCFlag:
                        dataDict['MaxLevelText'] = gameStrings.TEXT_GUILDGROWTHPROXY_712
                    else:
                        dataDict['MaxLevelText'] = gameStrings.TEXT_GUILDGROWTHPROXY_714
                elif maxLevel == 0:
                    dataDict['MaxLevelText'] = gameStrings.TEXT_GUILDGROWTHPROXY_717 % reqLv
                else:
                    dataDict['MaxLevelText'] = gameStrings.TEXT_GUILDGROWTHPROXY_719 % reqLv
            elif utils.getTotalSkillEnhancePoint(p) < reqSkillEnhancePoint:
                dataDict['isMaxLevel'] = True
                dataDict['MaxLevelText'] = gameStrings.GUILD_GROWTH_REQ_SKILL_ENHANCE_POINT_HINT % reqSkillEnhancePoint
            else:
                dataDict['isMaxLevel'] = False
                param = nextGrowthData.get('paramDefault', 1)
                dataDict['growthNextLevelField'] = gameStrings.TEXT_GUILDGROWTHPROXY_502 % (playerLevel + 1)
                dataDict['growthNextNameField'] = growthName
                dataDict['growthNextDescField'] = '+%d' % int(nextGrowthData.get('value', 0))
                enabledState = True
                if not self.isNPCFlag:
                    extraPara = 1
                    guildvolumn = guild.getGrowthVolumn(type)
                    if guildvolumn.has_key(propId) and guildvolumn[propId].active:
                        dataDict['activateState'] = 'light'
                    else:
                        dataDict['activateState'] = 'gray'
                        dataDict['MaxLevelText'] = gameStrings.GUILD_GROWTH_LEARN_NODE_NOT_ACTIVE
                        if playerLevel < GGVD.data.get(type, {}).get('npcMaxLv', 0):
                            dataDict['MaxLevelText'] = SCD.data.get('learnGrowthActiveTips', '')
                        enabledState = False
                else:
                    extraPara = nextGrowthData.get('npcfactor', 1)
                    dataDict['activateState'] = 'light'
                dataDict['expName'] = gameStrings.TEXT_GETSKILLPOINTPROXY_174
                self.learnExp = int(nextGrowthData.get('exp', 0) * param * extraPara)
                exp = format(self.learnExp, ',')
                expHave = format(p.expXiuWei, ',')
                if self.learnExp > p.expXiuWei + p.exp:
                    expHave = uiUtils.toHtml(expHave, '#F43804')
                    expLack = gameStrings.TEXT_GUILDGROWTHPROXY_758 % format(self.learnExp - p.expXiuWei, ',')
                    expHint = gameStrings.TEXT_GUILDGROWTHPROXY_759 % (uiUtils.toHtml(expLack, '#F43804'), uiUtils.toHtml(gameStrings.TEXT_GUILDGROWTHPROXY_759_1, '#F43804'))
                    enabledState = False
                elif self.learnExp > p.expXiuWei:
                    expHave = uiUtils.toHtml(expHave, '#F43804')
                    expLack = gameStrings.TEXT_GUILDGROWTHPROXY_758 % format(self.learnExp - p.expXiuWei, ',')
                    expHint = gameStrings.TEXT_GUILDGROWTHPROXY_764 % uiUtils.toHtml(expLack)
                else:
                    expHint = ''
                dataDict['exp'] = exp
                dataDict['expHave'] = expHave
                dataDict['expHint'] = expHint
                if not self.isNPCFlag:
                    growthVal = playerVolumn.getGrowth(propId)
                    if nextGrowthData.get('contrib', 0) > 0:
                        dataDict['contribName'] = gameStrings.TEXT_CONST_7558
                        contrib = growthVal.getLearnContrib(guild, int(nextGrowthData.get('contrib', 0)))
                        contribHave = format(guild.memberMe.contrib, ',')
                        if contrib > guild.memberMe.contrib:
                            contribHave = uiUtils.toHtml(contribHave, '#F43804')
                            enabledState = False
                        dataDict['contrib'] = format(contrib, ',')
                        dataDict['contribHave'] = contribHave
                        dataDict['contribVisible'] = True
                    else:
                        dataDict['contribVisible'] = False
                    _, needItems, learnMoney = commGuild.calcGrowthItemAndMoney(p, True, nextGrowthData)
                    self.learnMoney = growthVal.getLearnMoney(guild, learnMoney)
                    if needItems and nextGrowthData.get('item', None) != None:
                        dataDict['yutangguoName'] = gameStrings.TEXT_GUILDGROWTHPROXY_789
                        yutangguoId, yutangguo = nextGrowthData.get('item')[0]
                        yutangguoHave = p.inv.countItemInPages(yutangguoId, enableParentCheck=True)
                        if yutangguo > yutangguoHave:
                            yutangguoHave = uiUtils.toHtml(format(yutangguoHave, ','), '#F43804')
                            moneyLack = gameStrings.TEXT_GUILDGROWTHPROXY_794 % format(self.learnMoney, ',')
                            if self.learnMoney > p.bindCash + p.cash:
                                yutangguoHint = gameStrings.TEXT_GUILDGROWTHPROXY_796 % (uiUtils.toHtml(moneyLack, '#F43804'), uiUtils.toHtml(gameStrings.TEXT_FUBENPROXY_353, '#F43804'))
                                enabledState = False
                            else:
                                yutangguoHint = gameStrings.TEXT_GUILDGROWTHPROXY_799 % uiUtils.toHtml(moneyLack)
                        else:
                            yutangguoHave = format(yutangguoHave, ',')
                            yutangguoHint = ''
                        dataDict['yutangguo'] = format(yutangguo, ',')
                        dataDict['yutangguoHave'] = yutangguoHave
                        dataDict['yutangguoHint'] = yutangguoHint
                        dataDict['yutangguoSeekHint'] = GCD.data.get('yutangguoSeekHint', '')
                        dataDict['yutangguoVisible'] = True
                    else:
                        dataDict['yutangguoVisible'] = False
                else:
                    dataDict['bindCashName'] = gameStrings.TEXT_INVENTORYPROXY_3297
                    self.learnMoney = int(nextGrowthData.get('money', 0) * param)
                    bindCash = format(self.learnMoney, ',')
                    bindCashHave = format(p.bindCash, ',')
                    if self.learnMoney > p.bindCash + p.cash:
                        bindCashHave = uiUtils.toHtml(bindCashHave, '#F43804')
                        bindCashLack = gameStrings.TEXT_GUILDGROWTHPROXY_818 % format(self.learnMoney - p.bindCash, ',')
                        bindCashHint = gameStrings.TEXT_GUILDGROWTHPROXY_819 % (uiUtils.toHtml(bindCashLack, '#F43804'), uiUtils.toHtml(gameStrings.TEXT_GUILDGROWTHPROXY_819_1, '#F43804'))
                        enabledState = False
                    elif self.learnMoney > p.bindCash:
                        bindCashHave = uiUtils.toHtml(bindCashHave, '#F43804')
                        bindCashLack = gameStrings.TEXT_GUILDGROWTHPROXY_818 % format(self.learnMoney - p.bindCash, ',')
                        bindCashHint = gameStrings.TEXT_GUILDGROWTHPROXY_824 % uiUtils.toHtml(bindCashLack)
                    else:
                        bindCashHint = ''
                    dataDict['bindCash'] = bindCash
                    dataDict['bindCashHave'] = bindCashHave
                    dataDict['bindCashHint'] = bindCashHint
                dataDict['enabledState'] = enabledState
            if stage == LEARN_GROWTH_BASE_IDX:
                self.mediator.Invoke('updateDetail', (GfxValue(LEARN_GROWTH_BASE_PANEL), uiUtils.dict2GfxDict(dataDict, True)))
            elif stage == LEARN_GROWTH_ADVANCE_IDX:
                self.mediator.Invoke('updateDetail', (GfxValue(LEARN_GROWTH_ADVANCE_PANEL), uiUtils.dict2GfxDict(dataDict, True)))

    def onGetActivateGrowthDetail(self, *arg):
        type = int(arg[3][0].GetNumber())
        propId = int(arg[3][1].GetNumber())
        self.selectItem[ACTIVATE_GROWTH_PANEL] = (type, propId)
        self.updateActivateGrowthDetail(type, propId)

    def updateActivateGrowthTree(self, type, propId):
        p = BigWorld.player()
        playerVolumn = p.guildGrowth.getVolumn(type)
        if not self.isNPCFlag:
            guildvolumn = p.guild.getGrowthVolumn(type)
            growthData = self.getTreeNodeData(guildvolumn, playerVolumn, type, propId)
        else:
            growthData = self.getNPCTreeNodeData(playerVolumn, type, propId)
        if self.mediator:
            self.mediator.Invoke('updateTreeSecondNodeData', uiUtils.dict2GfxDict(growthData, True))
        self.updateActivateGrowthDetail(type, propId)

    def updateActivateGrowthDetail(self, type, propId):
        if self.selectItem.get(ACTIVATE_GROWTH_PANEL, ()) != (type, propId):
            return
        if self.mediator:
            p = BigWorld.player()
            guild = p.guild
            dataDict = {}
            dataDict['partScore'] = gameStrings.TEXT_GUILDGROWTHPROXY_663 % (GGVD.data.get(type, {}).get('name', ''), p.guildGrowth.getVolumn(type).score)
            totalScore = 0
            for key in p.guildGrowth:
                totalScore += p.guildGrowth[key].score

            dataDict['totalScore'] = gameStrings.TEXT_GUILDGROWTHPROXY_667 % totalScore
            dataDict['desc'] = GGVD.data.get(type, {}).get('desc', '')
            guildvolumn = guild.getGrowthVolumn(type)
            if guildvolumn.has_key(propId) and guildvolumn[propId].active:
                dataDict['isActivate'] = True
            else:
                dataDict['isActivate'] = False
            descDetail = PRD.data.get(propId, {}).get('name', '')
            dataDict['nameDetail'] = gameStrings.TEXT_GUILDGROWTHPROXY_878 % (GGVD.data.get(type, {}).get('name', ''), descDetail)
            dataDict['descDetail'] = gameStrings.TEXT_GUILDGROWTHPROXY_879 % descDetail
            propData = GGPD.data.get((type, propId), {})
            enabledState = True
            level = gameStrings.TEXT_GUILDACTIVITYPROXY_153 % propData.get('bldLv', 0)
            levelHave = gameStrings.TEXT_GUILDACTIVITYPROXY_153 % self.buildLv
            if propData.get('bldLv', 0) > self.buildLv:
                levelHave = uiUtils.toHtml(levelHave, '#F43804')
                enabledState = False
            dataDict['level'] = level
            dataDict['levelHave'] = levelHave
            dataDict['cashName'] = gameStrings.TEXT_GUILDGROWTHPROXY_537
            cash = format(propData.get('bindCash', 0), ',')
            cashHave = format(guild.bindCash, ',')
            if propData.get('bindCash', 0) > guild.bindCash:
                cashHave = uiUtils.toHtml(cashHave, '#F43804')
                enabledState = False
            dataDict['cash'] = cash
            dataDict['cashHave'] = cashHave
            dataDict['woodName'] = gameStrings.TEXT_CONST_7489
            wood = format(propData.get('wood', 0), ',')
            woodHave = format(guild.wood, ',')
            if propData.get('wood', 0) > guild.wood:
                woodHave = uiUtils.toHtml(woodHave, '#F43804')
                enabledState = False
            dataDict['wood'] = wood
            dataDict['woodHave'] = woodHave
            dataDict['mojingName'] = gameStrings.TEXT_CONST_7487
            mojing = format(propData.get('mojing', 0), ',')
            mojingHave = format(guild.mojing, ',')
            if propData.get('mojing', 0) > guild.mojing:
                mojingHave = uiUtils.toHtml(mojingHave, '#F43804')
                enabledState = False
            dataDict['mojing'] = mojing
            dataDict['mojingHave'] = mojingHave
            dataDict['xirangName'] = gameStrings.TEXT_CONST_7488
            xirang = format(propData.get('xirang', 0), ',')
            xirangHave = format(guild.xirang, ',')
            if propData.get('xirang', 0) > guild.xirang:
                xirangHave = uiUtils.toHtml(xirangHave, '#F43804')
                enabledState = False
            dataDict['xirang'] = xirang
            dataDict['xirangHave'] = xirangHave
            dataDict['enabledState'] = enabledState
            dataDict['maintainBindCash'] = propData.get('maintainBindCash', 0)
            self.mediator.Invoke('updateDetail', (GfxValue(ACTIVATE_GROWTH_PANEL), uiUtils.dict2GfxDict(dataDict, True)))

    def getVolumnData(self, type):
        p = BigWorld.player()
        value = GGVD.data.get(type, {})
        btnState = True
        tips = gameStrings.TEXT_GUILDGROWTHPROXY_937 % value.get('name', '')
        reqJingJie = value.get('reqJingJie', 0)
        if p.jingJie >= reqJingJie:
            tips += gameStrings.TEXT_GUILDGROWTHPROXY_941 % utils.jingJie2Name(reqJingJie)
        else:
            tips += gameStrings.TEXT_GUILDGROWTHPROXY_943 % utils.jingJie2Name(reqJingJie)
            btnState = False
        reqLv = value.get('reqLv', 0)
        if p.realLv >= reqLv:
            tips += gameStrings.TEXT_GUILDGROWTHPROXY_948 % reqLv
        else:
            tips += gameStrings.TEXT_GUILDGROWTHPROXY_950 % reqLv
            btnState = False
        reqSkillEnhancePoint = value.get('skillEnhancePoint', 0)
        if utils.getTotalSkillEnhancePoint(p) >= reqSkillEnhancePoint:
            tips += gameStrings.TEXT_GUILDGROWTHPROXY_955 % reqSkillEnhancePoint
        else:
            tips += gameStrings.TEXT_GUILDGROWTHPROXY_957 % reqSkillEnhancePoint
            btnState = False
        condition = value.get('condition', ((),))
        if condition != ((),):
            for _key, _vale in condition:
                _name = GGVD.data.get(_key, {}).get('name', '')
                _score = p.guildGrowth.getVolumn(_key).score
                if _score >= _vale:
                    tips += gameStrings.TEXT_GUILDGROWTHPROXY_966 % (_name, _vale)
                else:
                    tips += gameStrings.TEXT_GUILDGROWTHPROXY_968 % (_name, _vale)
                    btnState = False

        return (tips, btnState)

    def onClickFly(self, *arg):
        seekId = GCD.data.get('yutangguoSeekId', ())
        uiUtils.gotoTrack(seekId)
        gameglobal.rds.uiLog.addFlyLog(seekId)

    def onClickGetReward(self, *args):
        gameglobal.rds.ui.xiuLianScoreReward.show()

    def onEnableGuildGrowthScoreReward(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableGuildGrowthScoreReward', False))

    def onGetRewardBtnRedPot(self, *args):
        return GfxValue(gameglobal.rds.ui.xiuLianScoreReward.getXiuLianScoreRewardRedPot())

    def updateRewardBtnRedPot(self):
        if not self.mediator:
            return
        self.mediator.Invoke('updateRewardBtnRedPot', GfxValue(gameglobal.rds.ui.xiuLianScoreReward.getXiuLianScoreRewardRedPot()))
