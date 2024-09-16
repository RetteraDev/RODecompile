#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/skillMacroOverviewProxy.o
import BigWorld
import gameglobal
import gametypes
import uiUtils
import uiConst
import events
import skillDataInfo
import const
import utils
import logicInfo
from ui import gbk2unicode
from Scaleform import GfxValue
from guis import asObject
from guis import hotkey
from guis import ui
from guis import richTextUtils
from gameclass import SkillInfo
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis.asObject import ASUtils
from gameStrings import gameStrings
import skillMacro
from callbackHelper import Functor
from uiProxy import SlotDataProxy
from data import skill_macro_icon_data as SMID
from data import skill_macro_template_data as SMTTD
from data import skill_macro_qte_data as SMQD
from data import chat_channel_data as CCD
from data import skill_macro_arg_data as SMAD
from data import skill_macro_command_data as SMCD
from data import sys_config_data as SCD
from cdata import skill_macro_type_data as SMTD
from cdata import game_msg_def_data as GMDD
MIN_SKILL_TIME = 0.2
MAX_OFFICIAL_RECOMMAND_NUM = 4
RIGHT_MENU = 'SkillMacroOverview_SkillMacro_Right_Menu'
WEB_MACRO = 'SkillMacroOverview_SkillMacro_Web_Recomm'
INIT_WEB_Y = 193
INIT_WEB_X = 10
WEB_Y_OFFSET = 64
MAX_WEB_PAGE = 10
INIT_TXT_COLOR = '#FFFFE6'
ERROR_TXT_COLOR = '#CC2929'
SPRITE_TELEPORT_SKILL_ID = 100001
SPRITE_AWAKE_SKILL_ID = 100002
SKILL_MACRO_ERROR_DICT = {gametypes.SKILL_MACRO_TYPE_ERROR: GMDD.data.SKILL_MACRO_TYPE_ERROR,
 gametypes.SKILL_MACRO_ARG_ERROR: GMDD.data.SKILL_MACRO_ARG_ERROR,
 gametypes.SKILL_MACRO_FORMAT_ERROR: GMDD.data.SKILL_MACRO_FORMAT_ERROR,
 gametypes.SKILL_MACRO_LEN_ERROR: GMDD.data.SKILL_MACRO_LEN_ERROR,
 gametypes.SKILL_MACRO_SINGLE_LENGTH_ERROR: GMDD.data.SKILL_MACRO_SINGLE_LENGTH_ERROR,
 gametypes.SKILL_MACRO_CONDITION_NUM_ERROR: GMDD.data.SKILL_MACRO_CONDITION_NUM_ERROR,
 gametypes.SKILL_MACRO_CONDITION_NOT_AVALIABLE: GMDD.data.SKILL_MACRO_CONDITION_NOT_AVALIABLE,
 gametypes.SKILL_MACRO_CONDITION_FORMAT_ERROR: GMDD.data.SKILL_MACRO_CONDITION_FORMAT_ERROR,
 gametypes.SKILL_MACRO_REPEAT_ERROR: GMDD.data.SKILL_MACRO_REPEAT_ERROR,
 gametypes.SKILL_MACRO_ARG_NUM_ERROR: GMDD.data.SKILL_MACRO_ARG_NUM_ERROR,
 gametypes.SKILL_MACRO_CHAT_REPEAT: GMDD.data.SKILL_MACRO_CHAT_REPEAT}
WEB_ROOT_ADDRESS = 'http://hd.tianyu.163.com'
SKILL_MACRO_WEB_LINKS_DICT = {gametypes.SKILL_MACRO_PUT_OUT_WEB_TYPE: '/skillmacros/updateForGame?token=%s&id=%d&gbId=%d',
 gametypes.SKILL_MACRO_QUERY_WEB_TYPE: '/skillmacros/detailForGame?id=%d&token=%s&gbId=%d'}
MACRO_NUM_TXT = '%d/%d'
SKILL_MACRO_WEB_MODE_TXT = (gameStrings.MACRO_WEB_HOTTEST, gameStrings.MACRO_WE_LASTEST)
SKILL_MACRO_WEB_MODES = (gametypes.MACRO_WEB_HOTTEST, gametypes.MACRO_WE_LASTEST)
SKILL_MACRO_WEB_REVERT_MODES = {gametypes.MACRO_WEB_HOTTEST: 0,
 gametypes.MACRO_WE_LASTEST: 1}

class SkillMacroOverviewProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(SkillMacroOverviewProxy, self).__init__(uiAdapter)
        self.type = 'skillMacro'
        self.widget = None
        self.mySkillMacroInfo = None
        self.mySkillMacroPage = 1
        self.bindType = 'skillMacro'
        self.needShow = False
        self.macroNum = 0
        self.selectedMacroId = 0
        self.isSaving = False
        self.webQueryMode = gametypes.MACRO_WEB_HOTTEST
        self.webPage = 1
        self.webSkillMacroList = []
        self.isSevereError = 0
        self.editMode = uiConst.NO_EDIT
        self.isAutoSaving = False
        self.webMacroNum = 0
        self.isSkillUseSuccess = False
        self.useSelfSkill = False
        self.isOnlySel = False
        self.webUI = None
        self.selectedWebId = 0
        self.switchSkill = set([])
        self.skillCdIdDict = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_SKILL_MACRO_OVERVIEW, self.hidePanel)

    def getSkillCdIdDict(self):
        p = BigWorld.player()
        if self.skillCdIdDict.get(p.school, 0):
            return self.skillCdIdDict
        else:
            self.skillCdIdDict[p.school] = {}
            for k, v in SMID.data.iteritems():
                if v.get('school', 0) == p.school:
                    icon = v.get('icon', '')
                    cdId = v.get('cdId', 0)
                    self.skillCdIdDict[p.school][icon] = cdId

            return self.skillCdIdDict

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.refreshOverviewPanel()

    def queryOverviewData(self):
        p = BigWorld.player()
        p.base.queryMySkillMacros()

    def getActionInfoByPos(self, page, slot):
        p = BigWorld.player()
        targetMacro = None
        for macroId, macroInfo in p.mySkillMacroInfo.iteritems():
            if macroInfo.slot == slot and macroInfo.page == page:
                targetMacro = macroInfo
                break

        if targetMacro:
            checkResult, resultType = skillMacro.checkMacroFormat(targetMacro.macroList)
            if checkResult:
                return targetMacro.macroId
        tip = uiUtils.getTextFromGMD(GMDD.data.SKILL_MACRO_TO_ACTION_BAR_ERROR_TIP)
        gameglobal.rds.ui.messageBox.showMsgBox(tip)
        return 0

    def getInforFromTemplateId(self, templateId):
        templateMacroInfo = SMTTD.data.get(templateId, {})
        if not templateMacroInfo:
            BigWorld.player().showGameMsg(GMDD.data.SKILL_MACRO_NOT_EXIST, ())
            return []
        macroList = templateMacroInfo.get('commandList', []).split('\n')
        return self.getInforFromMacroList(macroList)

    def getInforFromCommands(self, macroId):
        mySkillMacroInfo = BigWorld.player().mySkillMacroInfo.get(macroId, None)
        if not mySkillMacroInfo:
            BigWorld.player().showGameMsg(GMDD.data.SKILL_MACRO_NOT_EXIST, ())
            return []
        else:
            macroList = mySkillMacroInfo.macroList
            return self.getInforFromMacroList(macroList)

    def getInforFromMacroList(self, macroList):
        checkResult, resultType = skillMacro.checkMacroFormat(macroList)
        if not checkResult:
            BigWorld.player().showGameMsg(SKILL_MACRO_ERROR_DICT.get(resultType, ''), ())
            return []
        macroInfor = []
        for command in macroList:
            infor = {'condition': '',
             'type': 0,
             'args': []}
            command = command.replace('/', '')
            if not command:
                continue
            rawArgs = command.split(' ')
            infor['type'] = SMTD.data.get(rawArgs[0], {}).get('type', 0)
            if infor['type'] == gametypes.MACRO_TYPE_SKILL and rawArgs[1] == gameStrings.SPRITE_AWAKE_NAME:
                infor['type'] = 4
            if infor['type'] == gametypes.MACRO_TYPE_SPRITE:
                tmpSplit = ['', '', '']
                if len(rawArgs) < 2:
                    return (False, gametypes.SKILL_MACRO_ARG_NUM_ERROR)
                for i in xrange(0, len(rawArgs)):
                    if i < 2:
                        tmpSplit[i] = rawArgs[i]
                    elif i == 2:
                        tmpSplit[i] = rawArgs[i]
                    else:
                        tmpSplit[2] = tmpSplit[2] + ' ' + rawArgs[i]

                rawArgs = tmpSplit
            for i in xrange(0, len(rawArgs)):
                if -1 != rawArgs[i].find('['):
                    condition = rawArgs[i].replace('[', '').replace(']', '')
                    conditionDeal = skillMacro.SkillMacroCondition.getInstance()
                    _, condition = conditionDeal.preDealWithCondition(condition)
                    _, condition = conditionDeal.dealWithCondition(condition)
                    infor['condition'] = condition
                    del rawArgs[i]
                    break

            i = 0
            while i < len(rawArgs):
                if not rawArgs[i]:
                    del rawArgs[i]
                else:
                    i += 1

            for idx, arg in enumerate(rawArgs):
                if arg:
                    if idx:
                        if infor['type'] == gametypes.MACRO_TYPE_SKILL:
                            for argName, argItem in SMAD.data.iteritems():
                                if argName == arg:
                                    if type(argItem.get('arg')) == list:
                                        infor['args'] = argItem.get('arg')
                                    else:
                                        infor['args'].append(argItem.get('arg'))

                        elif infor['type'] == gametypes.MACRO_TYPE_ITEM:
                            for argName, argItem in SMAD.data.iteritems():
                                if argName == arg:
                                    if type(argItem.get('arg')) == list:
                                        infor['args'] = argItem.get('arg')
                                    else:
                                        infor['args'].append(argItem.get('arg'))

                        elif infor['type'] == gametypes.MACRO_TYPE_EMOTE:
                            for argName, argItem in SMAD.data.iteritems():
                                if argName == arg:
                                    if type(argItem.get('arg')) == list:
                                        infor['args'] = argItem.get('arg')
                                    else:
                                        infor['args'].append(argItem.get('arg'))

                        elif infor['type'] == gametypes.MACRO_TYPE_CHAT:
                            if idx == 1:
                                for channelId, item in CCD.data.iteritems():
                                    if item.get('comment', '') == arg:
                                        infor['args'].append(channelId)

                            elif idx == 2:
                                infor['args'].append(arg)
                        elif infor['type'] == gametypes.MACRO_TYPE_SPRITE:
                            for argName, argItem in SMAD.data.iteritems():
                                if argName == arg:
                                    infor['args'].append(argItem.get('arg'))

            macroInfor.append(infor)

        return macroInfor

    def showOverviewPanel(self):
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableSkillMacro', False):
            self.needShow = True
            if hasattr(p, 'mySkillMacroInfo'):
                self.openOverviewPanel()
            else:
                self.queryOverviewData()

    def openOverviewPanel(self):
        if not gameglobal.rds.configData.get('enableOpenSkillMacroEntry', True):
            return
        if not self.widget:
            if self.needShow:
                self.uiAdapter.loadWidget(uiConst.WIDGET_SKILL_MACRO_OVERVIEW)
        else:
            self.clearWidget()

    def refreshOverviewPanel(self):
        p = BigWorld.player()
        self.widget.helpPic.visible = False
        self.refreshMySkillMacroArea()
        ASUtils.setHitTestDisable(self.widget.titlePic, True)
        self.initRightPanel()
        self.setOfficialRecommandArea()
        self.setWebModeDropDown()
        self.widget.stage.addEventListener(events.MOUSE_CLICK, self.handleClickStage)
        self.widget.save.addEventListener(events.MOUSE_CLICK, self.handleClickSave)
        self.widget.cancel.addEventListener(events.MOUSE_CLICK, self.handleClickCancel)
        self.widget.createMacroLib.addEventListener(events.MOUSE_CLICK, self.handleCreateMacroLib)
        self.widget.createSkillMacro.addEventListener(events.MOUSE_CLICK, self.handleCreateSkillMacro)
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleHidePanel)
        self.widget.deleteMacro.addEventListener(events.MOUSE_CLICK, self.handleClickDeleteMacro)
        self.widget.check.addEventListener(events.MOUSE_CLICK, self.handleClickCheckMacro)
        self.widget.recommArea.addEventListener(events.SCROLL, self.handleScroll)
        self.widget.webLink.addEventListener(events.MOUSE_CLICK, self.handleClickWebLink)
        self.widget.helpBtn.addEventListener(events.MOUSE_CLICK, self.handleClickHelpBtn)
        if p.lv < gametypes.SKILL_MACRO_PUT_OUT_LV_REQUIRE:
            self.widget.putOutBtn.disabled = True
            TipManager.addTip(self.widget.putOutBtn, gameStrings.SKILL_MACRO_PUT_OUT_LV_REQUIRE)
        else:
            self.widget.putOutBtn.addEventListener(events.MOUSE_CLICK, self.handlePutOut)
        self.widget.shareBtn.addEventListener(events.MOUSE_CLICK, self.handleShare)
        self.widget.deleteBtn.addEventListener(events.MOUSE_CLICK, self.handleDelete)

    def setWebModeDropDown(self):
        p = BigWorld.player()
        macroInputFilterData = []
        for filterTxt in SKILL_MACRO_WEB_MODE_TXT:
            macroInputFilterData.append({'label': filterTxt})

        self.widget.recommArea.canvas.hotBtn.data = SKILL_MACRO_WEB_MODES[0]
        self.widget.recommArea.canvas.newBtn.data = SKILL_MACRO_WEB_MODES[1]
        self.widget.recommArea.canvas.hotBtn.addEventListener(events.EVENT_SELECT, self.handleChangeWebMode)
        self.widget.recommArea.canvas.newBtn.addEventListener(events.EVENT_SELECT, self.handleChangeWebMode)
        self.widget.recommArea.canvas.hotBtn.selected = True
        self.widget.recommArea.canvas.newBtn.selected = False
        p.base.queryWebSkillMacros(self.webPage, self.webQueryMode)

    def updateWebApplyNum(self, id, voteCount):
        if not self.widget:
            return
        idx = 0
        for webList in self.webSkillMacroList:
            skillMacrosList = webList.get('skillmacrosList', [])
            for skillMacro in skillMacrosList:
                if int(id) == int(skillMacro.get('id')):
                    webMacro = self.widget.recommArea.canvas.getChildByName('recomm%d' % idx)
                    if webMacro:
                        webMacro.useNum.text = str(gameStrings.WEB_MACRO_COUNT % voteCount)
                        return
                idx += 1

    def refreshWebArea(self, webSkillMacroList, page = 0):
        if not self.widget:
            return
        if not self.widget.recommArea:
            return
        p = BigWorld.player()
        self.webPage = page
        index = self.webPage - 1
        if len(self.webSkillMacroList) <= index:
            self.webSkillMacroList.append(p.dealWithRawWebSkillMacroList(webSkillMacroList))
        else:
            self.webSkillMacroList[index] = p.dealWithRawWebSkillMacroList(webSkillMacroList)
        webY = INIT_WEB_Y
        idx = 0
        for webList in self.webSkillMacroList:
            skillMacrosList = webList.get('skillmacrosList', [])
            for skillMacro in skillMacrosList:
                macrosContent = skillMacro.get('macrosContent', {})
                if not macrosContent:
                    continue
                webMacro = self.widget.recommArea.canvas.getChildByName('recomm%d' % idx)
                if not webMacro:
                    webMacro = self.widget.getInstByClsName(WEB_MACRO)
                    webMacro.name = 'recomm%d' % idx
                    self.widget.recommArea.canvas.addChild(webMacro)
                idx += 1
                webMacro.useNum.text = gameStrings.WEB_MACRO_COUNT % skillMacro.get('voteCount', 0)
                if skillMacro.get('gameNickName', ''):
                    webMacro.author.text = skillMacro.get('gameNickName', '').encode(utils.defaultEncoding())
                webMacro.macroName.text = macrosContent.get('name', '')
                macrosContent['id'] = skillMacro.get('id')
                webMacro.useBtn.data = macrosContent
                webMacro.webBtn.data = macrosContent
                data = {}
                iconName = p.getIconNameFromRawIcon(macrosContent.get('iconPath', ''))
                data['iconPath'] = uiConst.MACRO_ICON_DICT.get(macrosContent.get('iconType', ''), '%s') % iconName
                webMacro.slot.setItemSlotData(data)
                webMacro.slot.dragable = False
                webMacro.y = webY
                webMacro.x = INIT_WEB_X
                webY += WEB_Y_OFFSET
                ASUtils.setHitTestDisable(webMacro.author, True)
                ASUtils.setHitTestDisable(webMacro.useNum, True)
                ASUtils.setHitTestDisable(webMacro.macroName, True)
                webMacro.webBtn.addEventListener(events.MOUSE_CLICK, self.handleClickWebBtn)
                webMacro.useBtn.addEventListener(events.MOUSE_CLICK, self.handleClickWebUseBtn)

        if idx < self.webMacroNum:
            for i in xrange(idx, self.webMacroNum):
                webMacro = self.widget.recommArea.canvas.getChildByName('recomm%d' % i)
                if webMacro:
                    self.widget.recommArea.canvas.removeChild(webMacro)

        self.webMacroNum = idx
        self.widget.recommArea.refreshHeight()

    def setOfficialRecommandArea(self):
        p = BigWorld.player()
        templateNum = 0
        for templateId, item in SMTTD.data.iteritems():
            if not item.get('isRecomm', 1):
                continue
            if item.get('school', 0) == p.school:
                officialSlot = self.widget.recommArea.canvas.getChildByName('officialSlot%d' % templateNum)
                data = {}
                data['macroList'] = item.get('commandList', []).split('\n')
                data['rawIcon'] = item.get('icon', '')
                data['iconType'] = item.get('iconType', 0)
                iconName = p.getIconNameFromRawIcon(item.get('icon', ''))
                data['iconPath'] = uiConst.MACRO_ICON_DICT.get(item.get('iconType', 0), '%s') % iconName
                data['macroName'] = item.get('name', '')
                officialSlot.canvas.slot.setItemSlotData(data)
                officialSlot.canvas.slot.dragable = False
                officialSlot.canvas.macroName.text = data['macroName']
                officialSlot.canvas.useBtn.data = data
                officialSlot.canvas.useBtn.addEventListener(events.MOUSE_CLICK, self.handleClickUseBtn)
                templateNum += 1

        if templateNum < MAX_OFFICIAL_RECOMMAND_NUM:
            for i in xrange(templateNum, MAX_OFFICIAL_RECOMMAND_NUM):
                officialSlot = self.widget.recommArea.canvas.getChildByName('officialSlot%d' % i)
                officialSlot.visible = False

    def refreshOverviewData(self):
        p = BigWorld.player()
        self.mySkillMacroInfo = p.mySkillMacroInfo

    def getSkillWithoutGcd(self, commandList, autoAttack = False):
        p = BigWorld.player()
        for command in commandList:
            if command.get('type', 0) == gametypes.MACRO_TYPE_SKILL:
                skillId = command.get('args', [])[0]
                if self.checkSkillCanUse(skillId, autoAttack=autoAttack) and self.isWithoutGcd(skillId) and not self.isQteSkillIgnoreGcd(skillId):
                    skillId = self.getRealQteSkillId(skillId, commandList)
                    if not self.checkSkillCanUse(skillId, autoAttack=autoAttack):
                        continue
                    return (skillId, command)
            elif command.get('type', 0) == gametypes.MACRO_TYPE_SPRITE:
                arg = command.get('args', [])[0]
                canUse, skillId = self.getSpriteCanUseSkillId(arg)
                if canUse:
                    return (skillId, command)

        return (0, {})

    def getSpriteCanUseSkillId(self, arg):
        p = BigWorld.player()
        if p.summonedSpriteInWorld:
            if arg == SPRITE_TELEPORT_SKILL_ID:
                nextTime = logicInfo.spriteTeleportSkillCoolDown
                if (not nextTime or utils.getNow() >= nextTime) and not getattr(self, 'isUsingTeleportSkill', False):
                    return (True, 0)
            elif arg == SPRITE_AWAKE_SKILL_ID:
                awakeSkill = utils.getAwakeSkillBySprite()
                spriteInfo = p.summonSpriteList.get(p.lastSpriteBattleIndex, {})
                if awakeSkill and spriteInfo.get('props', {}).get('juexing', False):
                    if getattr(p, 'summonedSpriteInWorld', None) and p.summonedSpriteInWorld.mode != gametypes.SP_MODE_NOATK:
                        nextTime = logicInfo.spriteManualSkillCoolDown
                        if (not nextTime or utils.getNow() >= nextTime) and self.checkSpriteAwakeSkillCanUse():
                            return (True, awakeSkill)
        return (False, 0)

    def checkSpriteAwakeSkillCanUse(self):
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(p.lastSpriteBattleIndex, {})
        famiEfflv = spriteInfo.get('props', {}).get('famiEffLv', 1)
        lv = utils.getEffLvBySpriteFamiEffLv(famiEfflv, 'awake', const.DEFAULT_SKILL_LV_SPRITE)
        skillInfo = SkillInfo(utils.getAwakeSkillBySprite(), lv)
        return skillDataInfo.checkTargetRelationRequest(skillInfo, False, True)

    def changeTeleportSkillStatus(self):
        self.isUsingTeleportSkill = False

    def isWsEquiped(self, skillId):
        for equipItem in gameglobal.rds.ui.skill.equipSkills:
            if skillId in equipItem:
                return True

        return False

    def checkSkillCanUse(self, skillId, autoAttack = False):
        p = BigWorld.player()
        if not p.wsSkills.has_key(skillId) and not p.skills.has_key(skillId):
            return False
        if p.wsSkills.has_key(skillId):
            if not self.isWsEquiped(skillId):
                return False
        skillLv = self._getSkillLv(skillId)
        skillInfo = p.getSkillInfo(skillId, skillLv)
        self.dealWithSelSkill(skillInfo)
        isCanUseSkill = p.checkSkillCanUse(skillInfo, needBlockMsg=True, autoAttack=autoAttack)
        self.resetTargetLock()
        return isCanUseSkill

    def checkMacroSkillCanUse(self):
        p = BigWorld.player()
        return True

    def isWithoutGcd(self, skillId):
        p = BigWorld.player()
        if p.skillQteData.has_key(skillId):
            skillId = p.skillQteData[skillId].qteSkills[0]
        skillInfo = self._getSkillInfo(skillId)
        gcd = skillDataInfo.getCommonCoolDown(skillInfo, 0)
        if not gcd:
            return True
        return False

    @ui.callFilter(0.1, False)
    def executeCommandStart(self, commandList, isDown, isKeyMode, autoAttack = False):
        if not self.checkMacroSkillCanUse():
            return
        p = BigWorld.player()
        if hasattr(p, 'useSkillMacroToday') and not p.useSkillMacroToday:
            p.useSkillMacroToday = True
            p.base.useSkillMacro()
        if not commandList:
            return
        self.commandList = commandList
        skillId, command = self.getSkillWithoutGcd(commandList, autoAttack=autoAttack)
        self.isOnlySel = False
        if command.has_key('type'):
            condition = command.get('condition', '')
            conditionDeal = skillMacro.SkillMacroCondition.getInstance()
            if not condition or condition and conditionDeal.execCondition(condition):
                self.useMacroSkillById(skillId, isDown, isKeyMode, autoAttack=autoAttack)
            BigWorld.callback(MIN_SKILL_TIME, Functor(self.executeCommands, commandList, isDown, isKeyMode, autoAttack))
            return
        self.executeCommands(commandList, isDown, isKeyMode, autoAttack=autoAttack)

    def getRealQteSkillId(self, skillId, commandList):
        p = BigWorld.player()
        if not self.isQteSkillUse(skillId):
            return skillId
        originSkillId = self.getOriginSkillId(skillId)
        qteSkillId = 0
        if p.skillQteData.has_key(originSkillId):
            qteSkillId = p.skillQteData[originSkillId].qteSkills[0]
        if not qteSkillId:
            qteSkillId = originSkillId
        for command in commandList:
            if command.get('type', 0) == gametypes.MACRO_TYPE_SKILL:
                skill = command.get('args', [])[0]
                if skill == qteSkillId:
                    return skill

        return 0

    def isQteSkillUse(self, skillId):
        p = BigWorld.player()
        qteSkillId = skillId
        originSkillId = self.getOriginSkillId(skillId)
        if p.skillQteData.has_key(originSkillId):
            qteSkillId = p.skillQteData[originSkillId].qteSkills[0]
        else:
            qteSkillId = originSkillId
        return qteSkillId != skillId

    def getOriginSkillId(self, skillId):
        if SMQD.data.get(skillId, {}):
            preSkillId = SMQD.data.get(skillId, {}).get('preSkillId', 0)
            if type(preSkillId) == tuple:
                preSkillId = preSkillId[0]
            if skillId == preSkillId:
                return skillId
            return self.getOriginSkillId(preSkillId)
        return skillId

    def useSkillById(self, skillId, isDown, isKeyMode, autoUseSkill, autoAttack = False):
        p = BigWorld.player()
        if gameglobal.rds.ui.skill.inAirBattleState() and skillId not in p.airSkills and not isDown:
            p.showGameMsg(GMDD.data.SKILL_CANT_USE_IN_FLY, ())
            return
        if not skillId:
            return
        if skillId != BigWorld.player().circleEffect.skillID:
            BigWorld.player().circleEffect.cancel()
        if skillId != BigWorld.player().chooseEffect.skillID:
            BigWorld.player().chooseEffect.cancel()
        skillLevel = self._getSkillLv(skillId)
        skillInfo = p.getSkillInfo(skillId, skillLevel)
        if skillInfo.getSkillData('castType', gametypes.SKILL_FIRE_NORMAL) == gametypes.SKILL_FIRE_SWITCH and isDown:
            self.switchSkill.add((skillInfo.getSkillData('switchState', 0), skillId))
        if not isKeyMode:
            p.useSkillByMouseUp(isDown, skillInfo, autoAttack=autoAttack)
        if isKeyMode:
            p.useSkillByKeyDown(isDown, skillInfo, autoAttack=autoAttack)
        needCircle = skillDataInfo.isSkillneedCircle(skillInfo)
        if needCircle:
            p.circleEffect.updateEffect(True)
            p.circleEffect.run()

    def resetTargetLock(self):
        p = BigWorld.player()
        if self.useSelfSkill:
            temp = p.targetLocked
            oldOptionalTarget = p.optionalTargetLocked
            p.targetLocked = p.lastTargetLocked
            if not p.targetLocked:
                p.optionalTargetLocked = oldOptionalTarget
            if temp == p and p.targetLocked != p:
                p.optionalTargetLocked = oldOptionalTarget
        self.useSelfSkill = False

    def getIconPathByInfo(self, info):
        p = BigWorld.player()
        iconName = p.getIconNameFromRawIcon(info.iconPath)
        return uiConst.MACRO_ICON_DICT.get(info.iconType, '%s') % iconName

    def getBagPagePosByItemId(self, itemId):
        if not BigWorld.player()._isSoul():
            fromBag = const.RES_KIND_INV
            bagPage, bagPos = BigWorld.player().inv.findItemInPages(itemId, includeExpired=True, includeLatch=True, includeShihun=True)
            if (bagPage == const.CONT_NO_PAGE or bagPos == const.CONT_NO_POS) and gameglobal.rds.configData.get('enableUseCrossInv', False):
                fromBag = const.RES_KIND_CROSS_INV
                bagPage, bagPos = BigWorld.player().crossInv.findItemInPages(itemId, includeExpired=True, includeLatch=True, includeShihun=True)
        else:
            if gameglobal.rds.configData.get('enableCrossServerBag', False):
                fromBag = const.RES_KIND_CROSS_INV
            else:
                fromBag = const.RES_KIND_INV
            bagPage, bagPos = BigWorld.player().realInv.findItemInPages(itemId, includeExpired=True, includeLatch=True, includeShihun=True)
        return (bagPage, bagPos, fromBag)

    def dealWithSelSkill(self, skillInfo):
        p = BigWorld.player()
        isCastSelfKeyDown = hotkey.isCastSelfKeyDown()
        skillTargetType, skillTargetValue = p.getSkillTargetType(skillInfo)
        beastSkill = skillInfo.getSkillData('beastSkill', 0)
        beast = p.getBeast()
        if beastSkill and not beast:
            p.showGameMsg(GMDD.data.SKILL_CANT_USE_NO_BEAST, ())
            return
        else:
            if skillTargetValue:
                if p.getOperationMode() == gameglobal.ACTION_MODE and p.optionalTargetLocked and not isCastSelfKeyDown and not self.isOnlySel:
                    pass
                elif skillTargetType == gametypes.SKILL_TARGET_SELF or skillTargetType == gametypes.SKILL_TARGET_SELF_FRIEND and (isCastSelfKeyDown or p.targetLocked == None or not p.isFriend(p.targetLocked) or utils.instanceof(p.targetLocked, 'OreSpawnPoint') or self.isOnlySel) or skillTargetType == gametypes.SKILL_TARGET_SELF_ENERMY and (isCastSelfKeyDown or p.targetLocked == None or not p.isEnemy(p.targetLocked) or self.isOnlySel) or skillTargetType == gametypes.SKILL_TARGET_ALL_TYPE and (isCastSelfKeyDown or p.targetLocked == None or not p.targetLocked.IsCombatUnit or self.isOnlySel):
                    if not (gameglobal.NEED_CHOOSE_EFFECT and p.getOperationMode() == gameglobal.ACTION_MODE):
                        p.lastTargetLocked = p.targetLocked
                        if beastSkill and not isCastSelfKeyDown:
                            p.targetLocked = beast
                        else:
                            p.targetLocked = p
                        self.useSelfSkill = True
            return

    def setSkillOnlySel(self):
        self.isOnlySel = True
        return True

    def useMacroSkillById(self, skillId, isDown, isKeyMode, autoAttack = False):
        p = BigWorld.player()
        currentSkillUseSuccess = False
        if not skillId:
            BigWorld.player().spriteTeleportBack(True)
            self.isUsingTeleportSkill = True
            BigWorld.callback(2, Functor(self.changeTeleportSkillStatus))
            self.isSkillUseSuccess = True
            currentSkillUseSuccess = True
        elif skillId == utils.getAwakeSkillBySprite():
            if self.checkSpriteAwakeSkillCanUse():
                BigWorld.player().spriteUseManualSkill(True)
                self.isSkillUseSuccess = True
                currentSkillUseSuccess = True
        else:
            skillLv = self._getSkillLv(skillId)
            skillInfo = p.getSkillInfo(skillId, skillLv)
            if self.checkSkillCanUse(skillId, autoAttack=autoAttack) or p.chargeSkillId == skillInfo.num and p.isChargeKeyDown:
                self.isSkillUseSuccess = True
                currentSkillUseSuccess = True
                self.dealWithSelSkill(skillInfo)
                self.useSkillById(skillId, isDown, isKeyMode, False, autoAttack=autoAttack)
        self.resetTargetLock()
        self.isOnlySel = False
        return currentSkillUseSuccess

    def executeCommands(self, commandList, isDown, isKeyMode, autoAttack = False):
        p = BigWorld.player()
        isSkillInUse = False
        conditionDeal = skillMacro.SkillMacroCondition.getInstance()
        for command in commandList:
            condition = command.get('condition', '')
            if condition and not conditionDeal.execCondition(condition):
                continue
            if command.get('type', 0) == gametypes.MACRO_TYPE_SKILL:
                skillId = command.get('args', [])[0]
                if isSkillInUse:
                    continue
                if not skillId or self.isQteSkillUse(skillId):
                    continue
                if self.isWithoutGcd(skillId) and not self.isQteSkillIgnoreGcd(skillId):
                    continue
                if self.useMacroSkillById(skillId, isDown, isKeyMode, autoAttack=autoAttack):
                    isSkillInUse = True
            elif command.get('type', 0) == gametypes.MACRO_TYPE_SPRITE:
                canUse, skillId = self.getSpriteCanUseSkillId(command.get('args', [])[0])
                if isSkillInUse:
                    continue
                if canUse and self.useMacroSkillById(skillId, isDown, isKeyMode, autoAttack=autoAttack):
                    isSkillInUse = True
            elif command.get('type', 0) == gametypes.MACRO_TYPE_ITEM:
                fromBag = const.RES_KIND_INV
                bagPage, bagPos = const.CONT_NO_PAGE, const.CONT_NO_POS
                for itemId in command.get('args', []):
                    bagPage, bagPos, fromBag = self.getBagPagePosByItemId(itemId)
                    if bagPage != const.CONT_NO_PAGE:
                        p.useActionBarItem(bagPage, bagPos, fromBag)
                        continue

            elif command.get('type', 0) == gametypes.MACRO_TYPE_EMOTE:
                if command.get('args', []):
                    emoteId = command.get('args', [])[0]
                    if emoteId == uiConst.HORSE_RIDING:
                        gameglobal.rds.ui.actionbar.horseRide()
                    elif emoteId == uiConst.WING_FLYING:
                        gameglobal.rds.ui.skill.enterWingFly()
                    else:
                        p.wantToDoEmote(emoteId)
            elif command.get('type', 0) == gametypes.MACRO_TYPE_CHAT:
                if command.get('args', []):
                    channelId = command.get('args', [])[0]
                    msg = command.get('args', [])[1]
                    self.submitMessage(channelId, msg)

        if not self.isSkillUseSuccess:
            p.showGameMsg(GMDD.data.SKILL_MACRO_USE_NOT_AVALIABLE, ())
        self.isSkillUseSuccess = False

    @ui.callFilter(5, False)
    def submitMessage(self, channelId, msg):
        gameglobal.rds.ui.chat.submitMessage(channelId, msg)

    def isQteSkillIgnoreGcd(self, skillId):
        return SMQD.data.get(skillId, {}).get('isIgnoreGcd', 0)

    def _getSkillLv(self, skillId):
        curLv = 1
        sVal = BigWorld.player().getSkills().get(skillId, None)
        if sVal:
            curLv = sVal.level
        return curLv

    def _getSkillInfo(self, skillId):
        skillLv = self._getSkillLv(skillId)
        return BigWorld.player().getSkillInfo(skillId, skillLv)

    def refreshMySkillMacroArea(self):
        if not self.widget:
            return
        self.macroNum = 0
        self.refreshOverviewData()
        for macroId, info in self.mySkillMacroInfo.iteritems():
            self.macroNum += 1
            self.info = info
            slot = self.widget.mySkillMacroArea.getChildByName('slot%d' % info.slot)
            slot.addEventListener(events.MOUSE_CLICK, self.handleSkillMacroSelected)
            self.setMacroSlotData(info, slot)

        self.widget.macroNum.text = MACRO_NUM_TXT % (self.macroNum, gametypes.MAX_SLOT_NUM)
        self.clearMySkillMacroArea()
        if self.isAutoSaving or self.selectedMacroId:
            self.isAutoSaving = False
            self.selectMacroById()

    def clearMySkillMacroArea(self):
        for idx in xrange(0, gametypes.MAX_SLOT_NUM):
            slot = self.widget.mySkillMacroArea.getChildByName('slot%d' % idx)
            slot.binding = 'skillMacro.slot%d' % idx
            data = slot.data
            if data:
                if not self.mySkillMacroInfo.get(long(data['macroId']), None) or idx != self.mySkillMacroInfo[long(data['macroId'])].slot:
                    self.clearSkillMacroSlot(slot)

    def clearSkillMacroSlot(self, slot):
        slot.setItemSlotData(None)
        slot.removeEventListener(events.MOUSE_CLICK, self.handleSkillMacroSelected)

    def setMacroSlotData(self, info, slot):
        p = BigWorld.player()
        data = {}
        data['macroList'] = info.macroList
        data['iconType'] = info.iconType
        data['iconPath'] = self.getIconPathByInfo(info)
        data['macroId'] = info.macroId
        data['macroName'] = info.name
        data['rawIcon'] = info.iconPath
        slot.setItemSlotData(data)

    def initRightPanel(self):
        self.widget.skillMacroItem.visible = False
        self.widget.inputArea.visible = False
        self.widget.errorTip.visible = False
        self.widget.noScriptT.visible = False
        self.widget.skillMacroItem.macroSlot.dragable = False
        self.setEditVisible(False)
        TipManager.addTip(self.widget.check, gameStrings.SKILL_MACRO_CHECK)
        TipManager.addTip(self.widget.deleteMacro, gameStrings.SKILL_MACRO_DELETE)
        TipManager.addTip(self.widget.createMacroLib, gameStrings.SKILL_MACRO_OPEN_INPUT)

    def getSlotID(self, key):
        _, idItem = key.split('.')
        nItem = int(idItem[4:])
        return (self.mySkillMacroPage, nItem)

    def onGetToolTip(self, *args):
        key = args[3][0].GetString()
        p = BigWorld.player()
        page, pos = self.getSlotID(key)
        if self.widget:
            slot = self.widget.mySkillMacroArea.getChildByName('slot%d' % pos)
            tip = "<font size = \'%d\'>%s</font>" % (gametypes.MACRO_TIP_SIZE, slot.data.macroName)
            return GfxValue(gbk2unicode(tip))

    def handleChangeWebMode(self, *args):
        p = BigWorld.player()
        targetBtn = ASObject(args[3][0]).currentTarget
        if targetBtn.selected:
            if self.webQueryMode != targetBtn.data:
                self.webQueryMode = targetBtn.data
                self.webPage = 1
                self.webSkillMacroList = []
                p.base.queryWebSkillMacros(self.webPage, self.webQueryMode)

    def handleClickWebUseBtn(self, *args):
        p = BigWorld.player()
        if self.checkMacroFull():
            return
        e = ASObject(args[3][0])
        targetSkill = e.currentTarget
        macrosContent = targetSkill.data
        p.base.applyWebSkillMacro(macrosContent['id'])
        p.base.addMySkillMacro(macrosContent['iconType'], macrosContent['iconPath'], macrosContent['name'], macrosContent['macroList'], gametypes.SKILL_MACRO_ADD_FROM_APPLY)

    def handleClickWebBtn(self, *args):
        e = ASObject(args[3][0])
        targetSkill = e.currentTarget
        macrosContent = targetSkill.data
        self.selectedWebId = macrosContent['id']
        BigWorld.player().base.queryWebSkillDetail(macrosContent['id'])

    def handleSkillMacroSelected(self, *args):
        e = ASObject(args[3][0])
        targetSkill = e.currentTarget
        if targetSkill.data.macroId != self.selectedMacroId:
            if self.editMode == uiConst.MODIFYING or self.checkSelectedMacroChanged():
                if not self.tryAutoSave(targetSkill):
                    return
            self.selectMacro(targetSkill)
        if e.buttonIdx == events.RIGHT_BUTTON:
            self.addRightMenu()

    def handleClickStage(self, *args):
        e = ASObject(args[3][0])
        if e.buttonIdx == events.LEFT_BUTTON:
            self.removeRightMenu()

    def handlePutOut(self, *args):
        p = BigWorld.player()
        if p.lv < gametypes.SKILL_MACRO_PUT_OUT_LV_REQUIRE:
            return
        macroId = long(self.selectedMacroId)
        skillMacroInfo = self.mySkillMacroInfo.get(macroId)
        macroList = skillMacroInfo.macroList
        checkResult, resultType = skillMacro.checkMacroFormat(macroList)
        if not checkResult:
            p.showGameMsg(GMDD.data.SKILL_MACRO_PUBLISH_FORMAT_ERROR, ())
            self.checkMacroList()
            return
        if self.formatMacroList(macroList):
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.SKILL_MACRO_PUT_OUT_CONFIRM, yesCallback=Functor(self.skillMacroPutOutConfirm, macroId))
        else:
            p.showGameMsg(GMDD.data.SKILL_MACRO_PUBLISH_EMPTY_ERROR, ())

    def skillMacroPutOutConfirm(self, macroId):
        BigWorld.player().base.publishWebSkillMacro(macroId)

    def handleDelete(self, *args):
        self.deleteMacroById(long(self.selectedMacroId))

    def handleShare(self, *args):
        p = BigWorld.player()
        if BigWorld.player()._isSoul():
            BigWorld.player().showGameMsg(GMDD.data.SKILL_MACRO_SHARE_UNAVALIABLE_CROSS, ())
            return
        selectedMacroId = long(self.selectedMacroId)
        macroList = self.mySkillMacroInfo[selectedMacroId].macroList
        checkResult, resultType = skillMacro.checkMacroFormat(macroList)
        if not checkResult or not self.formatMacroList(macroList):
            BigWorld.player().showGameMsg(GMDD.data.SKILL_MACRO_SHARE_UNAVALIABLE_ERROR, ())
            return
        now = long(utils.getNow())
        p.base.shareSkillMacroToChat(selectedMacroId, now)

    def shareMacroLink(self):
        p = BigWorld.player()
        roleName = p.roleName
        selectedMacroId = long(self.selectedMacroId)
        now = long(utils.getNow())
        schoolName = const.SCHOOL_DICT[p.school]
        macroName = uiUtils.htmlToText(self.mySkillMacroInfo[selectedMacroId].name)
        msg = gameStrings.SHARE_SKILL_MACRO_TXT % (selectedMacroId,
         p.gbId,
         p.school,
         now,
         macroName,
         schoolName,
         roleName)
        gameglobal.rds.ui.sendLink(msg)

    def shareWebMacroLink(self, gbId, macroId, shareTime, macroName, school, roleName):
        p = BigWorld.player()
        schoolName = const.SCHOOL_DICT[p.school]
        msg = gameStrings.SHARE_SKILL_MACRO_TXT % (macroId,
         gbId,
         school,
         shareTime,
         macroName,
         schoolName,
         roleName)
        gameglobal.rds.ui.sendLink(msg)

    def removeRightMenu(self):
        if not self.widget:
            return
        rightMenu = self.widget.getChildByName('rightMenu')
        if rightMenu:
            self.widget.removeChild(rightMenu)

    def addRightMenu(self):
        p = BigWorld.player()
        rightMenu = self.widget.getChildByName('rightMenu')
        if not rightMenu:
            rightMenu = self.widget.getInstByClsName(RIGHT_MENU)
            rightMenu.name = 'rightMenu'
            rightMenu.x = self.widget.stage.mouseX - self.widget.x
            rightMenu.y = self.widget.stage.mouseY - self.widget.y
            self.widget.addChild(rightMenu)
            if p.lv < gametypes.SKILL_MACRO_PUT_OUT_LV_REQUIRE:
                rightMenu.putOutBtn.visible = False
                rightMenu.deleteBtn.y -= 24
                rightMenu.shareBtn.y -= 24
            else:
                rightMenu.putOutBtn.addEventListener(events.MOUSE_CLICK, self.handlePutOut)
            rightMenu.deleteBtn.addEventListener(events.MOUSE_CLICK, self.handleDelete)
            rightMenu.shareBtn.addEventListener(events.MOUSE_CLICK, self.handleShare)
        rightMenu.x = self.widget.stage.mouseX - self.widget.x
        rightMenu.y = self.widget.stage.mouseY - self.widget.y

    def setSelectedMacroId(self, macroId):
        if self.widget:
            self.selectedMacroId = str(macroId)
            self.setRightPanel()

    def selectMacro(self, slot):
        self.editMode = uiConst.NO_EDIT
        self.selectedMacroId = slot.data.macroId
        self.setRightPanel()
        gameglobal.rds.ui.skillMacroInput.show(isForceShow=True)

    def cancelSelectMacro(self):
        self.selectedMacroId = 0
        self.widget.inputArea.canvas.inputT.text = ''
        self.selectMacroById()

    def selectMacroById(self):
        for i in xrange(0, gametypes.MAX_SLOT_NUM):
            slot = self.widget.mySkillMacroArea.getChildByName('slot%d' % i)
            if slot.data and slot.data.macroId == self.selectedMacroId:
                slot.setSlotState(uiConst.MACRO_SELECTED)
            else:
                slot.setSlotState(uiConst.MACRO_NORMAL)

    def setRightPanel(self):
        if not self.widget:
            return
        else:
            self.hideErrorArea()
            if not self.mySkillMacroInfo.get(long(self.selectedMacroId), None):
                self.selectedMacroId = 0
                self.initRightPanel()
                self.selectMacroById()
                return
            skillMacroData = self.mySkillMacroInfo[long(self.selectedMacroId)]
            skillMacroItem = self.widget.skillMacroItem
            self.setEditVisible(True)
            self.setMacroSlotData(skillMacroData, skillMacroItem.macroSlot)
            skillMacroItem.macroName.text = skillMacroData.name
            skillMacroItem.modifyName.addEventListener(events.MOUSE_CLICK, self.handleModifySkillMacro)
            self.skillMacroData = skillMacroData
            macroList = skillMacroData.macroList
            if not len(macroList):
                self.widget.noScriptT.visible = True
                self.widget.inputArea.visible = False
                self.widget.inputBg.addEventListener(events.MOUSE_CLICK, self.handleClickInput)
            else:
                self.widget.inputArea.visible = True
                self.widget.noScriptT.visible = False
                macroText = self.getMacroTextFromList(macroList)
                self.widget.inputArea.canvas.inputT.text = macroText
            self.selectMacroById()
            return

    def setEditVisible(self, isVisible):
        skillMacroItem = self.widget.skillMacroItem
        skillMacroItem.visible = isVisible
        self.widget.check.visible = isVisible
        self.widget.deleteMacro.visible = isVisible
        self.widget.createMacroLib.visible = isVisible
        self.widget.createMacroT.visible = not isVisible
        self.widget.save.visible = isVisible
        self.widget.cancel.visible = isVisible
        self.widget.putOutBtn.visible = isVisible
        self.widget.shareBtn.visible = isVisible
        self.widget.deleteBtn.visible = isVisible

    def handleCreateMacroLib(self, *args):
        gameglobal.rds.ui.skillMacroInput.show()

    def handleClickInput(self, *args):
        self.widget.noScriptT.visible = False
        self.widget.inputArea.visible = True
        self.widget.inputArea.canvas.inputT.text = ''
        self.widget.inputBg.removeEventListener(events.MOUSE_CLICK, self.handleClickInput)

    def handleCreateSkillMacro(self, *args):
        if not BigWorld.player()._isSoul():
            gameglobal.rds.ui.skillMacroCreate.openCreateSkillMacro()
        else:
            BigWorld.player().showGameMsg(GMDD.data.SKILL_MACRO_CREATE_UNAVALIABLE_CROSS, ())

    def handleModifySkillMacro(self, *args):
        if BigWorld.player()._isSoul():
            BigWorld.player().showGameMsg(GMDD.data.SKILL_MACRO_MODIFY_UNAVALIABLE_CROSS, ())
            return
        if self.widget:
            skillMacroItem = self.widget.skillMacroItem
            macroName = skillMacroItem.macroName.text
            rawIcon = skillMacroItem.macroSlot.data.rawIcon
            gameglobal.rds.ui.skillMacroCreate.openCreateSkillMacro(macroName, rawIcon, True)

    def handleHidePanel(self, *args):
        self.hidePanel()

    def hidePanel(self):
        if self.editMode == uiConst.MODIFYING or self.checkSelectedMacroChanged():
            msg = uiUtils.getTextFromGMD(GMDD.data.SKILL_MACRO_CLOSE_CONFIRM)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.clearWidget)
        else:
            self.clearWidget()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        if self.widget:
            self.widget.stage.removeEventListener(events.MOUSE_CLICK, self.handleClickStage)
        self.widget = None
        self.mySkillMacroInfo = None
        self.needShow = False
        self.selectedMacroId = 0
        self.isSaving = False
        self.editMode = uiConst.NO_EDIT
        self.webPage = 1
        self.webQueryMode = gametypes.MACRO_WEB_HOTTEST
        self.webSkillMacroList = []
        self.isSevereError = 0
        self.isAutoSaving = False
        self.switchSkill = set([])
        self.selectedWebId = 0
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SKILL_MACRO_OVERVIEW)
        gameglobal.rds.ui.skillMacroInput.clearWidget()
        gameglobal.rds.ui.skillMacroCreate.clearWidget()

    def handleClickCancel(self, *args):
        skillMacroItem = self.widget.skillMacroItem
        if skillMacroItem.macroSlot.data:
            macroId = long(skillMacroItem.macroSlot.data.get('macroId', 0))
            macroList = self.mySkillMacroInfo[macroId].macroList
            self.widget.inputArea.canvas.inputT.text = self.getMacroTextFromList(macroList)
            self.hideErrorArea()
            self.editMode = uiConst.NO_EDIT

    def handleClickSave(self, *args):
        p = BigWorld.player()
        if BigWorld.player()._isSoul():
            p.showGameMsg(GMDD.data.SKILL_MACRO_SAVE_UNAVALIABLE_CROSS, ())
            return
        self.checkMacroList()
        if self.isSevereError:
            p.showGameMsg(SKILL_MACRO_ERROR_DICT[self.isSevereError], ())
            return
        self.saveMacro()

    def handleClickHelpBtn(self, *args):
        self.widget.helpPic.visible = not self.widget.helpPic.visible
        if gameglobal.rds.ui.skillMacroInput.widget:
            gameglobal.rds.ui.skillMacroInput.widget.helpPic.visible = self.widget.helpPic.visible
            gameglobal.rds.ui.skillMacroInput.initInputMacroLayout()
        elif self.widget.helpPic.visible:
            gameglobal.rds.ui.skillMacroInput.show(True)

    def tryAutoSave(self, targetSkill = None):
        p = BigWorld.player()
        self.checkMacroList()
        if self.isSevereError:
            msg = uiUtils.getTextFromGMD(GMDD.data.SKILL_MACRO_SERVER_ERROR)
            if targetSkill:
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.selectMacro, targetSkill))
            else:
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.setRightPanel)
            return False
        else:
            self.autoSave()
            return True

    def autoSave(self):
        self.isAutoSaving = True
        self.saveMacro()

    def saveMacro(self):
        self.isSaving = True
        self.editMode = uiConst.NO_EDIT
        skillMacroItem = self.widget.skillMacroItem
        macroName = skillMacroItem.macroName.text
        iconPath = skillMacroItem.macroSlot.data.rawIcon
        iconType = skillMacroItem.macroSlot.data.iconType
        macroList = self.widget.inputArea.canvas.inputT.text.replace('\r', '\n').split('\n')
        macroId = long(skillMacroItem.macroSlot.data.get('macroId', 0))
        if not macroId:
            BigWorld.player().base.addMySkillMacro(iconType, iconPath, macroName, macroList, gametypes.SKILL_MACRO_ADD_FROM_CREATE)
        else:
            BigWorld.player().base.modifyMySkillMacro(macroId, iconType, iconPath, macroName, macroList)

    def handleClickUseBtn(self, *args):
        p = BigWorld.player()
        if self.checkMacroFull():
            return
        targetBtn = ASObject(args[3][0]).currentTarget
        data = targetBtn.data
        BigWorld.player().base.addMySkillMacro(data['iconType'], data['rawIcon'], data['macroName'], data['macroList'], gametypes.SKILL_MACRO_ADD_FROM_APPLY)

    def checkMacroFull(self):
        p = BigWorld.player()
        if self.macroNum >= gametypes.MAX_SLOT_NUM:
            p.showGameMsg(GMDD.data.SKILL_MACRO_FULL_TIP, ())
            return True
        return False

    def deleteMacro(self, page, slot):
        p = BigWorld.player()
        for macroId, info in p.mySkillMacroInfo.iteritems():
            if info.page == page and info.slot == slot:
                self.deleteMacroById(macroId)

    def deleteMacroById(self, macroId):
        p = BigWorld.player()
        if BigWorld.player()._isSoul():
            BigWorld.player().showGameMsg(GMDD.data.SKILL_MACRO_DELETE_UNAVALIABLE_CROSS, ())
            return
        else:
            if p.mySkillMacroInfo.get(macroId, None):
                deleteConfirmTxt = uiUtils.getTextFromGMD(GMDD.data.SKILL_MACRO_DELETE_CONFIRM)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(deleteConfirmTxt, Functor(p.base.delMySkillMacro, macroId))
            return

    def handleClickDeleteMacro(self, *args):
        if self.widget:
            self.hideErrorArea()
            self.widget.inputArea.canvas.inputT.text = ''

    def handleClickCheckMacro(self, *args):
        self.checkMacroList()

    def handleClickCheckButton(self, *args):
        self.hideErrorArea()

    def handleClickWebLink(self, *args):
        BigWorld.openUrl(SCD.data.get('skillMacroWebLink', ''))

    def handleScroll(self, *args):
        if self.widget:
            canvas = self.widget.recommArea.canvas
            canvasMask = self.widget.recommArea.canvasMask
            if canvas.y <= canvasMask.height - canvas.height + 20:
                self.queryNextWebPage()

    def handleClickCloseWebPanel(self, *args):
        if self.widget:
            self.widget.webPanel.visible = False

    @ui.callFilter(1, False)
    def queryNextWebPage(self):
        if self.webPage >= MAX_WEB_PAGE:
            return
        p = BigWorld.player()
        if len(self.webSkillMacroList) >= self.webPage:
            self.webPage += 1
            p.base.queryWebSkillMacros(self.webPage, self.webQueryMode)

    def hideErrorArea(self):
        self.clearErrorArea()
        self.widget.inputArea.canvas.inputT.visible = True
        self.widget.errorTip.visible = False
        self.widget.inputArea.refreshHeight()

    def clearErrorArea(self):
        numChildren = self.widget.inputArea.canvas.errorArea.numChildren
        for i in xrange(0, numChildren):
            self.widget.inputArea.canvas.errorArea.removeChildAt(0)

    def formatMacroList(self, macroList):
        newMacroList = []
        for item in macroList:
            item = richTextUtils.htmlToPlaneText(item)
            if item:
                newMacroList.append(item)

        return newMacroList

    def getMacroTextFromList(self, macroList):
        macroText = ''
        for text in macroList:
            if text:
                macroText = macroText + text + '\n'

        return macroText

    def checkSelectedMacroChanged(self):
        if not self.widget:
            return
        else:
            data = self.widget.skillMacroItem.macroSlot.data
            if not data:
                return False
            macroId = long(data.get('macroId', 0))
            if not macroId:
                return False
            if not self.mySkillMacroInfo.get(macroId, None):
                return False
            oldMacroList = self.mySkillMacroInfo.get(macroId, None).macroList
            oldMacroList = self.formatMacroList(oldMacroList)
            newMacroList = self.widget.inputArea.canvas.inputT.text.replace('\r', '\n').split('\n')
            newMacroList = self.formatMacroList(newMacroList)
            if len(newMacroList) != len(oldMacroList):
                return True
            for i in xrange(0, len(newMacroList)):
                if newMacroList[i] != oldMacroList[i]:
                    return True

            return False

    def checkMacroList(self):
        self.clearErrorArea()
        macroList = self.widget.inputArea.canvas.inputT.text.replace('\r', '\n').split('\n')
        macroList = self.formatMacroList(macroList)
        if not len(macroList):
            return
        self.widget.inputArea.canvas.inputT.text = self.getMacroTextFromList(macroList)
        self.widget.inputArea.canvas.inputT.visible = False
        positionY = 0
        errorNum = 0
        isError = False
        self.isSevereError = 0
        checkResult, resultType = skillMacro.checkMacroFormat(macroList)
        checkedMacroList = []
        if resultType in gametypes.SKILL_MACRO_SEVERE_ERRORS:
            self.isSevereError = resultType
        for macroCommand in macroList:
            checkResult, resultType = skillMacro.checkMacroFormat(macroCommand, macroList, checkedMacroList)
            checkedMacroList.append(macroCommand)
            checkButton = self.widget.getInstByClsName('SkillMacroOverview_SkillMacro_CheckButton')
            if not checkResult:
                isError = True
                color = ERROR_TXT_COLOR
                errorNum += 1
                tip = uiUtils.getTextFromGMD(SKILL_MACRO_ERROR_DICT.get(resultType, ''))
                TipManager.addTip(checkButton, tip)
                if resultType in gametypes.SKILL_MACRO_SEVERE_ERRORS:
                    self.isSevereError = resultType
            else:
                color = INIT_TXT_COLOR
            checkButton.command.htmlText = "<font color = \'%s\'>%s</font>" % (color, macroCommand)
            checkButton.addEventListener(events.MOUSE_CLICK, self.handleClickCheckButton)
            self.widget.inputArea.canvas.errorArea.addChild(checkButton)
            checkButton.x = 0
            checkButton.y = positionY
            positionY += checkButton.height

        if isError:
            self.widget.errorTip.visible = True
            self.widget.errorTip.txt.text = gameStrings.SKILL_MACRO_ERROR_TIP % errorNum
        self.widget.inputArea.refreshHeight()

    def shareConfirm(self, macroId, gbId, now):
        p = BigWorld.player()
        if self.editMode == uiConst.MODIFYING or self.checkSelectedMacroChanged():
            if not self.tryAutoSave():
                return
        p.base.getSkillMacroFromChat(gbId, macroId, now)

    def openWebPanel(self, webType, token = '', id = 0, gbId = 0):
        p = BigWorld.player()
        if webType == gametypes.SKILL_MACRO_PUT_OUT_WEB_TYPE:
            url = WEB_ROOT_ADDRESS + SKILL_MACRO_WEB_LINKS_DICT[webType] % (token, id, int(p.gbId))
            gameglobal.rds.ui.innerIE.show(url, code=3, enableKeyEvent=True, canGoBack=False, width=1105, height=640, enableGoBack=True, bInput=True)
        elif webType == gametypes.SKILL_MACRO_QUERY_WEB_TYPE:
            url = WEB_ROOT_ADDRESS + SKILL_MACRO_WEB_LINKS_DICT[webType] % (self.selectedWebId, token, p.gbId)
            gameglobal.rds.ui.innerIE.show(url, code=3, enableKeyEvent=True, canGoBack=False, width=1105, height=640, bInput=True)
