#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/lifeSkillNewProxy.o
from gamestrings import gameStrings
import copy
import BigWorld
from Scaleform import GfxValue
import gamelog
import gameglobal
import gametypes
import utils
import uiUtils
import item
import const
import ui
from ui import gbk2unicode
from ui import unicode2gbk
from callbackHelper import Functor
from uiProxy import SlotDataProxy
from guis import uiConst
from guis import lifeSkillFactory
from guis import events
from guis import cursor
from guis import pinyinConvert
from data import sys_config_data as SCD
from data import life_skill_data as LSD
from cdata import game_msg_def_data as GMDD
from data import ability_tree_node_reverse_data as ATNRD
from data import ability_tree_data as ATD
from data import ability_tree_phase_data as ATPD
from data import ability_data as AD
from data import life_skill_resource_data as LSRD
from data import life_skill_collection_data as LSCD
from data import life_skill_manufacture_data as LSMD
from data import life_skill_prop_tips_data as LSPTD
from data import fame_data as FD
from data import life_skill_extra_ability_show_data as LSEASD
from data import life_skill_subtype_data as LSSD
from data import life_skill_config_data as LSCFD
from data import map_config_data as MCD
from data import fishing_lv_data as FLD
TA = None
BUTTON_POS_X = 4
BUTTON_POS_Y = 50
BUTTON_OFFSET_X = 210
BUTTON_OFFSET_Y = 48
MIN_LENGTH = 853
MAX_PAHSE = 9

class LifeSkillNewProxy(SlotDataProxy):
    SPECIAL_PANEL = 4
    PRODUCE_PANEL = 2

    def __init__(self, uiAdapter):
        super(LifeSkillNewProxy, self).__init__(uiAdapter)
        self.bindType = 'lifeSkill'
        self.type = 'lifeSkill'
        self.modelMap = {'getPanelInfo': self.onGetPanelInfo,
         'setCurPanelType': self.onSetCurPanelType,
         'getTreeBaseData': self.onGetTreeBaseData,
         'getTreeData': self.onGetTreeData,
         'clickActivate': self.onClickActivate,
         'getNowIdx': self.getNowIdx,
         'getHint': self.onGetHint,
         'refreshLabour': self.onRefreshLabour,
         'getProduceSelectPos': self.onGetProduceSelectPos,
         'getLeftListMenuInfo': self.onGetLeftListMenuInfo,
         'setSelectProductPos': self.onSetSelectProductPos,
         'setSelectMakePos': self.onSetSelectMakePos,
         'closePanel': self.closeWidget,
         'getDetailInfo': self.onGetDetailInfo,
         'clickToPanel': self.onClickToPanel,
         'clickToSpecial': self.onClickToSpecial,
         'clickHelpBtn': self.onClickHelpBtn,
         'getAssistInfo': self.onGetAssistInfo,
         'getAssistInfo2': self.onGetAssistInfo2,
         'repairClick': self.onRepairClick,
         'repairClick2': self.onRepairClick2,
         'getMidListInfo': self.onGetMidListInfo,
         'getOpenNode': self.onGetOpenNode,
         'setOpenNode': self.onSetOpenNode,
         'getRightDetailInfo': self.onGetRightDetailInfo,
         'updateSelectNeedItem': self.onUpdateSelectNeedItem,
         'makeAllClick': self.onMakeAllClick,
         'makeClick': self.onMakeClick,
         'getManuInfo': self.onGetManuInfo,
         'cancelMake': self.onCancelMake,
         'getExtraAbilityInfo': self.onGetExtraAbilityInfo,
         'getNowIsCancelState': self.onGetNowIsCancelState,
         'cancelAbility': self.onCancelAbility,
         'setCursor': self.onSetCursor,
         'getIsHideInfo': self.getIsHideInfo,
         'checkHide': self.checkHide,
         'goAbility': self.onGoAbility,
         'getDuraConfig': self.onGetDuraConfig,
         'getNodeNameList': self.onGetNodeNameList,
         'getUnopenedDesc': self.onGetUnopenedDesc,
         'isPinYin': self.onIsPinYin,
         'getHanZhiResult': self.onGetHanZhiResult,
         'getExtraAbilityPosInfo': self.onGetExtraAbilityPosInfo,
         'getMaxAtype': self.onGetMaxAtype,
         'clickLvUp': self.onClickLvUp,
         'buySmallBtnClick': self.onBuySmallBtnClick,
         'otherSmallBtnClick': self.onOtherSmallBtnClick}
        self.lifeSkillFactory = lifeSkillFactory.getInstance()
        self.reset()
        self.curLifeTypeIdx = -1
        self.selectPage = 0
        self.needShowHint = False
        self.hitAnNo = -1
        self.isShow = False
        self.openNode = {}
        self.mediator = None
        self.selectProducePos = {0: [0, 0],
         1: [0, 0]}
        self.selectMakePos = [0, 0, 0]
        self.messageBoxId = 0
        self.maxAtype = 0
        self.extraAbilityInfo = {}
        self.hideInfo = [True, True]
        self.hideProduceInfo = True
        self.curAbilityInfo = {}
        self.curAbilityInfoPhaseMap = {}
        self.nodeNameList = []
        self.extraAbilityPosInfo = []
        self.makeSkillSubIdxs = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_SKILL_PANEL_NEW, self.hide)

    def getIsHideInfo(self, *args):
        idx = int(args[3][0].GetNumber())
        return GfxValue(self.hideInfo[idx])

    def onGetDuraConfig(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableLifeDura', False))

    def defaultCanDo(self, mid):
        mData = LSMD.data.get(mid)
        if not mData:
            return False
        return not not mData.get('defaultCanDo')

    def isLearnedAbility(self):
        p = BigWorld.player()
        dId = self.lifeSkillFactory.getCurLifeSkillIns(uiConst.PANEL_TYPE_MAKE_SKILL).getDetailId()
        if self.defaultCanDo(dId):
            return True
        elif not p.getAbilityData(gametypes.ABILITY_LS_MANUFACTURE_SUB_ON, dId):
            return False
        else:
            return True

    def onGetUnopenedDesc(self, *args):
        unopenedDescText1 = SCD.data.get('unopenedDescText1', gameStrings.TEXT_LIFESKILLNEWPROXY_166)
        unopenedDescText2 = SCD.data.get('unopenedDescText2', gameStrings.TEXT_LIFESKILLNEWPROXY_167)
        arr = []
        for key in ATPD.data.keys():
            phaseName = ATPD.data.get(key, {}).get('name', '')
            arr.append(phaseName)

        return uiUtils.array2GfxAarry((unopenedDescText1, unopenedDescText2, arr), True)

    def onIsPinYin(self, *args):
        ret = False
        searchName = unicode2gbk(args[3][0].GetString())
        ret = utils.isPinyinAndHanzi(searchName) == const.STR_ONLY_PINYIN
        return GfxValue(ret)

    def onGetHanZhiResult(self, *args):
        result = []
        searchName = unicode2gbk(args[3][0].GetString())
        for i in self.nodeNameList:
            obj = {}
            itemName = i[0]['itemName']
            matchName = i[1]['itemName']
            if searchName in itemName:
                obj['label'] = itemName
                obj['id'] = i[2]
                result.append(obj)
            elif searchName in matchName:
                obj['label'] = itemName
                obj['id'] = i[2]
                result.append(obj)

        return uiUtils.array2GfxAarry(result, True)

    def isShowGoAbilityBtn(self):
        p = BigWorld.player()
        dId = self.lifeSkillFactory.getCurLifeSkillIns(uiConst.PANEL_TYPE_MAKE_SKILL).getDetailId()
        if self.defaultCanDo(dId):
            return False
        if not p.getAbilityData(gametypes.ABILITY_LS_MANUFACTURE_SUB_ON, dId):
            anNo = ATNRD.data.get((gametypes.ABILITY_LS_MANUFACTURE_SUB_ON, dId), 0)
            if anNo > 0:
                return True
            else:
                return False
        else:
            return False

    def getShowHintDesc(self):
        p = BigWorld.player()
        dId = self.lifeSkillFactory.getCurLifeSkillIns(uiConst.PANEL_TYPE_MAKE_SKILL).getDetailId()
        if self.defaultCanDo(dId):
            return ''
        if not p.getAbilityData(gametypes.ABILITY_LS_MANUFACTURE_SUB_ON, dId):
            anNo = ATNRD.data.get((gametypes.ABILITY_LS_MANUFACTURE_SUB_ON, dId), 0)
            if anNo == 0:
                extraAbilityInfo = self.getExtraAbilityInfo()
                for phaseId in extraAbilityInfo:
                    data = extraAbilityInfo[phaseId]
                    for aType in data:
                        abList = data[aType]
                        if not abList:
                            continue
                        if type(abList) != list:
                            continue
                        for i in xrange(len(abList)):
                            aId = abList[i]['abilityId']
                            aInfo = AD.data.get(aId)
                            if aInfo.get('sid') == dId:
                                msg = uiUtils.getTextFromGMD(GMDD.data.HINT_LEARN_FROM_EXTRA_ABILITY, gameStrings.TEXT_LIFESKILLNEWPROXY_232)
                                phaseName = ATPD.data.get(phaseId, {}).get('name', '')
                                atype = LSEASD.data[aId].get('skillType', 0)
                                typeName = LSSD.data.get(atype, {}).get('name', '')
                                msg = msg % (phaseName, typeName)
                                return msg

                return uiUtils.getTextFromGMD(GMDD.data.HINT_LEARN_FROM_CONSIGN, gameStrings.TEXT_LIFESKILLNEWPROXY_238)
        return ''

    def onGoAbility(self, *args):
        self.hintNoLearndAbility()

    def hintNoLearndAbility(self):
        p = BigWorld.player()
        dId = self.lifeSkillFactory.getCurLifeSkillIns(uiConst.PANEL_TYPE_MAKE_SKILL).getDetailId()
        if self.defaultCanDo(dId):
            return
        if not p.getAbilityData(gametypes.ABILITY_LS_MANUFACTURE_SUB_ON, dId):
            anNo = ATNRD.data.get((gametypes.ABILITY_LS_MANUFACTURE_SUB_ON, dId), 0)
            if anNo > 0:
                gameglobal.rds.ui.lifeSkillNew.hint(gametypes.ABILITY_LS_MANUFACTURE_SUB_ON, dId)
            else:
                extraAbilityInfo = self.getExtraAbilityInfo()
                for phaseId in extraAbilityInfo:
                    data = extraAbilityInfo[phaseId]
                    for aType in data:
                        abList = data[aType]
                        if abList:
                            if type(abList) == list:
                                for i in xrange(len(abList)):
                                    aId = abList[i]['abilityId']
                                    aInfo = AD.data.get(aId)
                                    if aInfo.get('sid') == dId:
                                        msg = uiUtils.getTextFromGMD(GMDD.data.HINT_LEARN_FROM_EXTRA_ABILITY, gameStrings.TEXT_LIFESKILLNEWPROXY_232)
                                        phaseName = ATPD.data.get(phaseId, {}).get('name')
                                        atype = LSEASD.data[aId].get('skillType', 0)
                                        typeName = LSSD.data.get(atype, {}).get('name', '')
                                        msg = msg % (phaseName, typeName)
                                        BigWorld.player().showGameMsg(GMDD.data.COMMON_MSG, msg)
                                        return

            return

    def checkHide(self, *args):
        idx = int(args[3][0].GetNumber())
        ret = args[3][1].GetBool()
        self.hideInfo[idx] = ret
        self.refreshPanel()

    def onSetCursor(self, *args):
        anNo = int(args[3][0].GetNumber())
        star = int(args[3][1].GetNumber())
        inOrOut = args[3][2].GetBool()
        if not inOrOut:
            if ui.get_cursor_state() == ui.CANCEL_ABILITY_STATE or ui.get_cursor_state() == ui.CANCEL_ABILITY_NODE_STATE:
                ui.lock_cursor(False)
                ui.set_cursor(cursor.equipCancelAbility)
                ui.lock_cursor(True)
                return
        else:
            isDis = False
            if ui.get_cursor_state() == ui.CANCEL_ABILITY_NODE_STATE and star != 0:
                isDis = True
            if ui.get_cursor_state() == ui.CANCEL_ABILITY_STATE and star == 0:
                isDis = True
            info = self.getNowAllNodeInfo()[0]
            if not info[anNo].get('star', []):
                isDis = True
            if star == 0:
                hasActiveNext = False
                for key in info[anNo].get('nextNodes', []):
                    stars = info[key].get('star', [])
                    if len(stars):
                        hasActiveNext = True
                        break

                if hasActiveNext:
                    isDis = True
            elif len(info[anNo].get('star', [])) == 0 or star not in info[anNo].get('star', []):
                isDis = True
            ui.lock_cursor(False)
            if isDis:
                ui.set_cursor(cursor.equipCancelAbilityDis)
            else:
                ui.set_cursor(cursor.equipCancelAbility)
            ui.lock_cursor(True)

    def onGetNowIsCancelState(self, *args):
        if ui.get_cursor_state() == ui.CANCEL_ABILITY_STATE or ui.get_cursor_state() == ui.CANCEL_ABILITY_NODE_STATE:
            return GfxValue(ui.get_cursor_state())
        else:
            return GfxValue(0)

    def onCancelAbility(self, *args):
        if ui.get_cursor_state() != ui.CANCEL_ABILITY_STATE and ui.get_cursor_state() != ui.CANCEL_ABILITY_NODE_STATE:
            return
        anNo = int(args[3][0].GetNumber())
        star = int(args[3][1].GetNumber())
        info = self.getNowAllNodeInfo()[0]
        hasActiveNext = False
        if len(info[anNo].get('star', [])) == 0:
            BigWorld.player().showGameMsg(GMDD.data.CANCEL_ABILITY_FAILED_NODE_NOT_ACTIVE, ())
            return
        if ui.get_cursor_state() == ui.CANCEL_ABILITY_NODE_STATE:
            if star == 0:
                for key in info[anNo].get('nextNodes', []):
                    stars = info[key].get('star', [])
                    if len(stars):
                        hasActiveNext = True
                        break

        if hasActiveNext:
            BigWorld.player().showGameMsg(GMDD.data.CANCEL_ABILITY_FAILED_NODE_HAS_NEXT, ())
            return
        itemPos = ui.get_bindItemPos()
        targetItem = BigWorld.player().inv.getQuickVal(itemPos[1], itemPos[2])
        if not targetItem:
            ui.reset_cursor()
            BigWorld.player().showGameMsg(GMDD.data.CANCEL_ABILITY_FAILED_NODE_NOT_ACTIVE, ())
            return
        if ui.get_cursor_state() == ui.CANCEL_ABILITY_STATE and getattr(targetItem, 'cstype', 0) != item.Item.SUBTYPE_2_RESET_ONE_ABILITY:
            BigWorld.player().showGameMsg(GMDD.data.NOT_SIGN_ITEM, ())
            return
        if ui.get_cursor_state() == ui.CANCEL_ABILITY_NODE_STATE and getattr(targetItem, 'cstype', 0) != item.Item.SUBTYPE_2_RESET_ONE_ABILITY_NODE:
            BigWorld.player().showGameMsg(GMDD.data.NOT_SIGN_ITEM, ())
            return
        if ui.get_cursor_state() == ui.CANCEL_ABILITY_STATE and getattr(targetItem, 'cstype', 0) == item.Item.SUBTYPE_2_RESET_ONE_ABILITY:
            if star == 0:
                return
            if star not in info[anNo].get('star', []):
                return
        if ui.get_cursor_state() == ui.CANCEL_ABILITY_NODE_STATE and getattr(targetItem, 'cstype', 0) == item.Item.SUBTYPE_2_RESET_ONE_ABILITY_NODE:
            if star != 0:
                return
        if not BigWorld.player().checkItemCanUse(targetItem):
            return
        hint = ''
        abName = ''
        if star == 0:
            hint = uiUtils.getTextFromGMD(GMDD.data.CANCEL_ABILITY_NODE_0_USE_HINT, gameStrings.TEXT_LIFESKILLNEWPROXY_379)
            abName = info[anNo]['name']
        else:
            hint = uiUtils.getTextFromGMD(GMDD.data.CANCEL_ABILITY_NODE_0_USE_HINT, gameStrings.TEXT_LIFESKILLNEWPROXY_382)
            ab = info[anNo]['abilities']
            tmp = 0
            usedAbilityId = 0
            for i in xrange(len(ab)):
                for ddId in ab[i]:
                    if tmp == star:
                        usedAbilityId = ddId
                        break
                    tmp = tmp + 1

                if usedAbilityId:
                    break

            abName = info[anNo][usedAbilityId]['name']
        msg = hint % (abName, uiUtils.getItemColorName(targetItem.id))
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.sendCancel, itemPos[1], itemPos[2], anNo, star))

    def sendCancel(self, page, pos, anNo, star):
        BigWorld.player().cell.useItemOfResetSingleAbility(const.RES_KIND_INV, page, pos, anNo, star)
        ui.reset_cursor()

    def onGetOpenNode(self, *args):
        return uiUtils.dict2GfxDict(self.openNode)

    def onSetOpenNode(self, *args):
        nodeName = args[3][0].GetString()
        state = int(args[3][1].GetNumber())
        self.openNode[nodeName] = state

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SKILL_PANEL_NEW:
            self.mediator = mediator
            BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.itemChangeFunc)
            BigWorld.player().registerEvent(const.EVENT_ITEM_REMOVE, self.itemChangeFunc)

    def itemChangeFunc(self, *args):
        self.refreshPanel()

    def getNowIdx(self, *args):
        return GfxValue(self.selectPage)

    def onGetProduceSelectPos(self, *args):
        idx = int(args[3][0].GetNumber())
        if idx == 0:
            return uiUtils.dict2GfxDict(self.selectProducePos, True)
        else:
            return uiUtils.array2GfxAarry(self.selectMakePos, True)

    def reset(self):
        self.needShowHint = False
        self.hitAnNo = -1
        self.mediator = None
        self.curLifeTypeIdx = -1
        self.selectPage = 0
        self.selectProducePos = {0: [0, 0],
         1: [0, 0]}
        self.selectMakePos = [0, 0, 0]
        self.lifeSkillFactory.reset()
        self.openNode = {}
        self.messageBoxId = 0
        self.extraAbilityInfo = {}
        self.curAbilityInfo = {}
        self.curAbilityInfoPhaseMap = {}
        self.nodeNameList = []
        self.extraAbilityPosInfo = []
        self.maxAtype = 0
        self.makeSkillSubIdxs = []

    def onSetSelectProductPos(self, *args):
        page = int(args[3][0].GetNumber())
        leftPos = int(args[3][1].GetNumber())
        leftSecond = int(args[3][2].GetNumber())
        if leftPos == -1:
            leftPos = self.selectProducePos[page][0]
        if leftSecond == -1:
            leftSecond = self.selectProducePos[page][1]
        self.selectProducePos[page] = [leftPos, leftSecond]

    def setSelectProductPos(self, page, leftPos, leftSecond):
        if leftPos == -1:
            leftPos = self.selectProducePos[page][0]
        if leftSecond == -1:
            leftSecond = self.selectProducePos[page][1]
        self.selectProducePos[page] = [leftPos, leftSecond]

    def setSelectMakePos(self, page, leftPos, leftSecond):
        if page == -1:
            page = self.selectMakePos[0]
        if leftPos == -1:
            leftPos = self.selectMakePos[1]
        if leftSecond == -1:
            leftSecond = self.selectMakePos[2]
        self.selectMakePos = [page, leftPos, leftSecond]

    def onSetSelectMakePos(self, *args):
        page = int(args[3][0].GetNumber())
        leftPos = int(args[3][1].GetNumber())
        leftSecond = int(args[3][2].GetNumber())
        if page == -1:
            page = self.selectMakePos[0]
        if leftPos == -1:
            leftPos = self.selectMakePos[1]
        if leftSecond == -1:
            leftSecond = self.selectMakePos[2]
        self.selectMakePos = [page, leftPos, leftSecond]

    def getMakeSkillIdxByPos(self, pos):
        if len(self.makeSkillSubIdxs) <= pos:
            return -1
        idx = self.makeSkillSubIdxs[pos]
        self.makeSkillSubIdxs[pos] = -1
        return idx

    def show(self, idx = 0):
        if BigWorld.player().lv < SCD.data.get('lifeSkillMinLv', 0):
            BigWorld.player().showGameMsg(GMDD.data.LIFE_SKILL_NEED_LV_NOT_ENOUGH, ())
            return
        self.selectPage = idx
        if not BigWorld.player().checkMapLimitUI(gametypes.MAP_LIMIT_UI_LIFE_SKILL):
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SKILL_PANEL_NEW)
        self.isShow = True

    def openProduceSkillPanel(self, idx, produceSkillSubIdxs = []):
        self.show(idx)
        secondTabIdx = -1
        firstTabIdx = produceSkillSubIdxs[0]
        if len(produceSkillSubIdxs) >= 2:
            secondTabIdx = produceSkillSubIdxs[1]
        if idx == 2:
            self.setSelectProductPos(0, firstTabIdx, secondTabIdx)
        else:
            self.setSelectProductPos(1, firstTabIdx, secondTabIdx)

    def openMakeSkillPanel(self, makeSkillSubIdxs = []):
        self.show(uiConst.LIFE_SKILL_MAKE_SKILL_TAB_IDX)
        self.makeSkillSubIdxs = makeSkillSubIdxs
        firstTabIdx = makeSkillSubIdxs[0]
        secondTabIdx = -1
        if len(makeSkillSubIdxs) >= 2:
            secondTabIdx = makeSkillSubIdxs[1]
        self.setSelectMakePos(firstTabIdx, secondTabIdx, -1)

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SKILL_PANEL_NEW)
        self.isShow = False
        self.mediator = None
        BigWorld.player().unRegisterEvent(const.EVENT_ITEM_CHANGE, self.itemChangeFunc)
        BigWorld.player().unRegisterEvent(const.EVENT_ITEM_REMOVE, self.itemChangeFunc)

    def closeWidget(self, *args):
        self.clearWidget()

    def onSetCurPanelType(self, *arg):
        oldType = self.curLifeTypeIdx
        self.curLifeTypeIdx = int(arg[3][0].GetNumber())
        if oldType != -1:
            oldLifeSkill = self.lifeSkillFactory.getCurLifeSkillIns(oldType)
            if oldLifeSkill:
                oldLifeSkill.reset()

    @ui.callAfterTime()
    def refreshPanel(self, stage = 0, refreshAll = False):
        if self.mediator:
            self.mediator.Invoke('refreshPanel', (GfxValue(stage), GfxValue(refreshAll)))

    def onGetPanelInfo(self, *arg):
        idx = int(arg[3][0].GetNumber())
        curLifeSkill = self.lifeSkillFactory.getCurLifeSkillIns(idx)
        if curLifeSkill:
            return curLifeSkill.getPanelInfo()
        else:
            return

    def onGetTreeData(self, *args):
        p = BigWorld.player()
        for key in p.abilityTree:
            self.setTreeNodeData(key, p.abilityTree[key])

    def setTreeNodeData(self, anNo, star):
        if self.mediator:
            self.mediator.Invoke('setTreeNodeData', (GfxValue(anNo), uiUtils.array2GfxAarry(star, True)))

    def onGetTreeBaseData(self, *args):
        info = self.getNowAllNodeInfo()
        return uiUtils.array2GfxAarry(info, True)

    def refreshAllData(self):
        if self.mediator:
            self.mediator.Invoke('refreshAllData', uiUtils.array2GfxAarry(self.getNowAllNodeInfo(), True))

    def setNodeNameList(self, itemName, matchName, id):
        tmp1 = {}
        tmp1['itemName'] = itemName if itemName else ''
        tmp1['pinyinFirst'] = pinyinConvert.strPinyinFirst(itemName)
        tmp1['pinyin'] = pinyinConvert.strPinyin(itemName)
        tmp2 = {}
        tmp2['itemName'] = matchName if matchName else ''
        tmp2['pinyinFirst'] = pinyinConvert.strPinyinFirst(matchName)
        tmp2['pinyin'] = pinyinConvert.strPinyin(matchName)
        self.nodeNameList.append((tmp1, tmp2, id))

    def onGetNodeNameList(self, *args):
        if self.extraAbilityPosInfo:
            self.nodeNameList = self.nodeNameList + self.extraAbilityPosInfo
            self.extraAbilityPosInfo = []
        return uiUtils.array2GfxAarry(self.nodeNameList, True)

    def onGetExtraAbilityPosInfo(self, *args):
        return uiUtils.array2GfxAarry(self.extraAbilityPosInfo, True)

    def getNowAllNodeInfo(self):
        if not self.curAbilityInfo:
            for id, data_item in ATD.data.iteritems():
                temp = copy.deepcopy(data_item)
                abilities = data_item.get('abilities', ())
                temp['abilities'] = list(abilities)
                temp['leftStar'] = list(xrange(0, len(abilities)))
                for i in xrange(len(abilities)):
                    temp['abilities'][i] = list(abilities[i])
                    for j in xrange(len(abilities[i])):
                        if abilities[i][j] in AD.data:
                            adInfo = AD.data.get(abilities[i][j], {})
                            if not adInfo.get('deleted', 0):
                                info = {}
                                info['name'] = adInfo.get('name', '')
                                info['description'] = adInfo.get('description', '')
                                info['description1'] = adInfo.get('description1', '')
                                info['item'] = adInfo.get('item', 0)
                                unripeName = adInfo.get('unripeName', '')
                                matchName = adInfo.get('lifeSkillMatchField', '')
                                self.setNodeNameList(unripeName, matchName, id)
                                info['icon'] = adInfo.get('icon', 0)
                                if adInfo:
                                    sid = adInfo.get('sid', 0)
                                    atype = adInfo.get('atype', 0)
                                    resourceId = 0
                                    if atype == gametypes.ABILITY_LS_COLLECTION_SUB_ON:
                                        resourceId = LSCD.data.get(sid, {}).get('resourceId', 0)
                                    elif atype == gametypes.ABILITY_LS_MANUFACTURE_SUB_ON:
                                        resourceId = LSMD.data.get(sid, {}).get('resourceId', 0)
                                    reqSkills = LSRD.data.get(resourceId, {}).get('reqSkills', [])
                                    if reqSkills:
                                        extraName = ''
                                        for key in reqSkills:
                                            skillInfo = LSD.data.get(key, {})
                                            extraName += gameStrings.TEXT_LIFESKILLNEWPROXY_650 % (skillInfo.get('name', ''), skillInfo.get('lv', ''))

                                        info['extraName'] = extraName
                                temp[abilities[i][j]] = info
                            else:
                                temp['abilities'][i].remove(abilities[i][j])

                temp['abilities'] = [ data for data in temp['abilities'] if data ]
                if len(temp['abilities']) > 0:
                    self.curAbilityInfo[id] = temp
                    phase = data_item.get('phase', 1)
                    self.curAbilityInfoPhaseMap.setdefault(phase, {}).setdefault('idArray', []).append(id)
                    startPos = BUTTON_POS_X + BUTTON_OFFSET_X * self.curAbilityInfo[id]['coordinate'][0]
                    minPos = self.curAbilityInfoPhaseMap[phase].get('startPos')
                    if phase == 1:
                        self.curAbilityInfoPhaseMap[phase]['startPos'] = 0
                        self.curAbilityInfoPhaseMap[phase]['startCoordinate'] = 0
                    else:
                        if minPos == None:
                            self.curAbilityInfoPhaseMap[phase]['startPos'] = startPos
                            self.curAbilityInfoPhaseMap[phase]['startCoordinate'] = self.curAbilityInfo[id]['coordinate'][0]
                        elif minPos > startPos:
                            self.curAbilityInfoPhaseMap[phase]['startPos'] = startPos
                            self.curAbilityInfoPhaseMap[phase]['startCoordinate'] = self.curAbilityInfo[id]['coordinate'][0]
                        if phase == MAX_PAHSE:
                            self.curAbilityInfoPhaseMap.setdefault(phase + 1, {})
                            nextPhaseStart = self.curAbilityInfoPhaseMap[phase + 1].get('startPos')
                            if nextPhaseStart == None:
                                self.curAbilityInfoPhaseMap[phase + 1]['startPos'] = startPos + BUTTON_OFFSET_X
                            elif self.curAbilityInfoPhaseMap[phase + 1]['startPos'] < startPos + BUTTON_OFFSET_X:
                                self.curAbilityInfoPhaseMap[phase + 1]['startPos'] = startPos + BUTTON_OFFSET_X

            if self.curAbilityInfoPhaseMap.get(MAX_PAHSE + 1, {}).get('startPos', 0) < self.curAbilityInfoPhaseMap[MAX_PAHSE]['startPos'] + MIN_LENGTH:
                self.curAbilityInfoPhaseMap.setdefault(MAX_PAHSE + 1, {})['startPos'] = self.curAbilityInfoPhaseMap[MAX_PAHSE]['startPos'] + MIN_LENGTH
            for key in self.curAbilityInfo:
                info = self.curAbilityInfo[key]
                info['reqNodes'] = [ data for data in info.get('reqNodes', ()) if data in self.curAbilityInfo ]
                for reqNodeId in info['reqNodes']:
                    self.curAbilityInfo[reqNodeId].setdefault('nextNodes', []).append(key)

        info = copy.deepcopy(self.curAbilityInfo)
        for key in BigWorld.player().abilityTree:
            if info.get(key):
                info[key]['star'] = BigWorld.player().abilityTree[key]

        return [info,
         self.curAbilityInfoPhaseMap,
         range(1, MAX_PAHSE + 1),
         self.getExtraAbilityInfo()]

    def onClickActivate(self, *args):
        needValue = int(args[3][0].GetNumber())
        anNo = int(args[3][1].GetNumber())
        star = int(args[3][2].GetNumber())
        name = FD.data.get(const.ABILITY_FAME_WEIWANG, {}).get('name', '')
        if needValue <= BigWorld.player().getCurXueShiVal():
            msg = gameStrings.TEXT_LIFESKILLNEWPROXY_705 % (name, needValue)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(BigWorld.player().cell.enableAbilityNode, anNo, star))
        else:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_LIFESKILLNEWPROXY_709 % name)

    def showTreeNodeEffect(self, anNo):
        if self.mediator:
            self.mediator.Invoke('showTreeNodeEffect', GfxValue(anNo))

    def hint(self, key1, key2):
        anNo = ATNRD.data.get((key1, key2), 0)
        if anNo > 0 and self.messageBoxId == 0:
            msg = uiUtils.getTextFromGMD(GMDD.data.IS_OPEN_ABILITIY_TREE, gameStrings.TEXT_LIFESKILLNEWPROXY_719)
            self.messageBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.showHint, anNo), gameStrings.TEXT_IMPPLAYERTEAM_644, Functor(self.clearMessageBoxId), gameStrings.TEXT_AVATAR_2876_1)

    def showHint(self, anNo):
        self.needShowHint = True
        self.hitAnNo = anNo
        if self.mediator:
            self.mediator.Invoke('setTabIndex', GfxValue(1))
        else:
            self.show(1)
        self.clearMessageBoxId()

    def clearMessageBoxId(self):
        self.messageBoxId = 0

    def onGetHint(self, *args):
        ret = [self.needShowHint, self.hitAnNo]
        self.hitAnNo = -1
        self.needShowHint = False
        return uiUtils.array2GfxAarry(ret, True)

    def onRefreshLabour(self, *args):
        self.setLabour()
        self.setMental()

    @ui.uiEvent(uiConst.WIDGET_SKILL_PANEL_NEW, events.EVENT_CHANGE_LABOUR)
    def setLabour(self):
        p = BigWorld.player()
        labourTips = LSPTD.data.get(uiConst.LABOUR_TIPS_INDEX, {}).get('tips', gameStrings.TEXT_LIFESKILLFACTORY_247)
        strLabourBackRate = LSCFD.data.get('strLabourBackRate', 0)
        value = (LSCFD.data.get('labourRegenVal', 1) + int(strLabourBackRate * int(BigWorld.player().socProp.str / 10))) / 10.0
        useTime = max(30, LSCFD.data.get('labourRegenInterval', 300) - BigWorld.player().getAbilityData(gametypes.ABILITY_LS_LABOUR_REGEN_INTERVAL))
        labourTips = labourTips % (useTime, value)
        if self.mediator:
            mLabour = 2 * p.mLabour / 10 if uiUtils.hasVipBasic() else p.mLabour / 10
            self.mediator.Invoke('setLabour', (GfxValue(str(p.labour / 10)),
             GfxValue(str(mLabour)),
             GfxValue(gbk2unicode(labourTips)),
             GfxValue(0)))

    @ui.uiEvent(uiConst.WIDGET_SKILL_PANEL_NEW, events.EVENT_CHANGE_MENTAL)
    def setMental(self):
        p = BigWorld.player()
        mentalTips = LSPTD.data.get(uiConst.MENTAL_TIPS_INDEX, {}).get('tips', gameStrings.TEXT_LIFESKILLFACTORY_247)
        strMentalBackRate = LSCFD.data.get('strMentalBackRate', 0)
        value = (LSCFD.data.get('mentalRegenVal', 1) + int(strMentalBackRate * int(BigWorld.player().socProp.know / 10))) / 10.0
        useTime = max(30, LSCFD.data.get('mentalRegenInterval', 300) - BigWorld.player().getAbilityData(gametypes.ABILITY_LS_LABOUR_REGEN_INTERVAL))
        mentalTips = mentalTips % (useTime, value)
        if self.mediator:
            mMental = 2 * p.mMental / 10 if uiUtils.hasVipBasic() else p.mMental / 10
            self.mediator.Invoke('setLabour', (GfxValue(p.mental / 10),
             GfxValue(mMental),
             GfxValue(gbk2unicode(mentalTips)),
             GfxValue(1)))

    def onGetLeftListMenuInfo(self, *arg):
        idx = int(arg[3][0].GetNumber())
        curLifeSkill = self.lifeSkillFactory.getCurLifeSkillIns(idx)
        if curLifeSkill:
            return curLifeSkill.getLeftListMenuInfo()
        else:
            return

    def onGetDetailInfo(self, *arg):
        idx = int(arg[3][0].GetNumber())
        curLifeSkill = self.lifeSkillFactory.getCurLifeSkillIns(idx)
        firstIndex = int(arg[3][1].GetNumber())
        secondIndex = int(arg[3][2].GetNumber())
        curLifeSkill.clickSubMenu(firstIndex, secondIndex)
        return curLifeSkill.getDetailInfo()

    def onClickToPanel(self, *args):
        lifeSkillId = int(args[3][0].GetNumber())
        curLifeSkillId = uiUtils.getCurLifeSkill(lifeSkillId)
        gamelog.debug('@jinjj lifeSkill#refreshPanel:', lifeSkillId, curLifeSkillId)
        if curLifeSkillId[0] is None:
            return
        else:
            lifeSkillData = LSD.data.get(curLifeSkillId, {})
            self.selectPage = lifeSkillData['type'] + 1
            lifeSkillIns = self.lifeSkillFactory.lifeSkillIns[uiConst.PANEL_TYPE_LIFE_SKILL_OVERVIEW]
            if self.selectPage == LifeSkillNewProxy.PRODUCE_PANEL:
                self.selectProducePos[0] = [lifeSkillIns.leftVal2Index(lifeSkillData['type'], lifeSkillId), 0]
            else:
                self.selectMakePos = [lifeSkillIns.leftVal2Index(lifeSkillData['type'], lifeSkillId), 0, 0]
            self.changeToTab(self.selectPage)
            return

    def onClickToSpecial(self, *args):
        typeName = args[3][0].GetString()
        if typeName == 'fish':
            self.selectPage = LifeSkillNewProxy.SPECIAL_PANEL
            self.selectProducePos[1] = [0, 0]
        else:
            self.selectPage = LifeSkillNewProxy.SPECIAL_PANEL
            self.selectProducePos[1] = [1, 0]
        self.changeToTab(self.selectPage)

    def changeToTab(self, idx):
        if self.mediator:
            self.mediator.Invoke('setTabIndex', GfxValue(idx))
        else:
            self.show(idx)

    def onClickHelpBtn(self, *args):
        idx = int(args[3][0].GetNumber())
        curLifeSkill = self.lifeSkillFactory.getCurLifeSkillIns(idx)
        skillType = int(args[3][1].GetNumber())
        curLifeSkill.clickHelp(skillType)

    def onGetMidListInfo(self, *arg):
        idx = int(arg[3][0].GetNumber())
        curLifeSkill = self.lifeSkillFactory.getCurLifeSkillIns(idx)
        firstIndex = int(arg[3][1].GetNumber())
        secondIndex = int(arg[3][2].GetNumber())
        curLifeSkill.clickSubMenu(firstIndex, secondIndex)
        initMenuIdx = self.getMakeSkillIdxByPos(2)
        midListInfo = curLifeSkill.getMidListInfo()
        if initMenuIdx >= 0:
            if initMenuIdx < len(midListInfo):
                self.openNode[gbk2unicode(midListInfo[initMenuIdx]['keyName'])] = 1
        initItemIdx = self.getMakeSkillIdxByPos(3)
        if initItemIdx >= 0:
            if initMenuIdx < len(midListInfo) and initItemIdx < len(midListInfo[initMenuIdx]['data']):
                initManuId = midListInfo[initMenuIdx]['data'][initItemIdx]['manuId']
                self.setSelectMakePos(-1, -1, initManuId)
        return uiUtils.array2GfxAarry(midListInfo, True)

    def onGetAssistInfo(self, *arg):
        idx = int(arg[3][0].GetNumber())
        subType = int(arg[3][1].GetNumber())
        curLifeSkill = self.lifeSkillFactory.getCurLifeSkillIns(idx)
        gamelog.debug('@hjx lifeSkill#onGetAssistInfo:', subType)
        return curLifeSkill.getAssistInfo(subType)

    def onGetAssistInfo2(self, *args):
        skillType = int(args[3][0].GetNumber())
        info = {}
        info['desc'] = gameStrings.TEXT_LIFESKILLFACTORY_181
        info['data'] = []
        p = BigWorld.player()
        container = None
        if skillType == 1:
            info['limitCnt'] = 3
            container = p.fishingEquip
        elif skillType == 2:
            info['limitCnt'] = 1
            container = p.exploreEquip
        if container:
            for i in xrange(info['limitCnt']):
                item = container[i]
                if item:
                    itemInfo = {}
                    itemId = item.id
                    iconPath = uiUtils.getItemIconFile40(itemId)
                    itemInfo['icon'] = {'iconPath': iconPath,
                     'itemId': itemId,
                     'srcType': 'roleInfoLifeSkill'}
                    itemInfo['itemId'] = itemId
                    itemInfo['part'] = i + 1
                    info['data'].append(itemInfo)

        if len(info['data']) == 0:
            info['desc'] = gameStrings.TEXT_LIFESKILLFACTORY_206
        info['skillType'] = skillType
        return uiUtils.dict2GfxDict(info, True)

    def onRepairClick(self, *arg):
        gameglobal.rds.ui.lifeSkill.repairSubtype = int(arg[3][0].GetNumber())
        gameglobal.rds.ui.lifeSkill.repairPart = int(arg[3][1].GetNumber())
        gameglobal.rds.ui.lifeSkill.isSpecialPart = False
        if gameglobal.rds.ui.lifeSkill.repairPart == 0:
            BigWorld.player().showGameMsg(GMDD.data.LIFE_EQUIPMENT_REPAIR_NO_SELECT, ())
            return
        self.showRepairPanel()

    def onRepairClick2(self, *arg):
        gameglobal.rds.ui.lifeSkill.repairSubtype = int(arg[3][0].GetNumber())
        gameglobal.rds.ui.lifeSkill.repairPart = int(arg[3][1].GetNumber())
        gameglobal.rds.ui.lifeSkill.isSpecialPart = True
        if gameglobal.rds.ui.lifeSkill.repairPart == 0:
            BigWorld.player().showGameMsg(GMDD.data.LIFE_EQUIPMENT_REPAIR_NO_SELECT, ())
            return
        self.showRepairPanel()

    def showRepairPanel(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_LIFE_SKILL_REPAIR, True)

    def onGetRightDetailInfo(self, *arg):
        idx = int(arg[3][0].GetNumber())
        firstIndex = int(arg[3][1].GetNumber())
        secondIndex = int(arg[3][2].GetNumber())
        curLifeSkill = self.lifeSkillFactory.getCurLifeSkillIns(idx)
        curLifeSkill.clickMidSubMenu(firstIndex, secondIndex)
        return curLifeSkill.getDetailInfo()

    def onUpdateSelectNeedItem(self, *arg):
        idx = int(arg[3][0].GetNumber())
        itemId = int(arg[3][1].GetNumber())
        val = int(arg[3][2].GetNumber())
        curLifeSkill = self.lifeSkillFactory.getCurLifeSkillIns(idx)
        curLifeSkill.updateSelectNeedItem(itemId, val)
        self.refreshProp(curLifeSkill)

    def refreshProp(self, curLifeSkill):
        identifiedQuality, identifiedExtraQuality, identifiedProb = curLifeSkill.getIdentified()
        if self.mediator:
            self.mediator.Invoke('refreshIdentifiedDesc', (GfxValue(identifiedProb), GfxValue(identifiedQuality), GfxValue(identifiedExtraQuality)))

    def onMakeAllClick(self, *arg):
        self.showMakeAllPanel()

    def showMakeAllPanel(self):
        p = BigWorld.player()
        if p.curLifeSkillType == gametypes.LIFE_SKILL_TYPE_MANUFACTURE and p.usingLifeSkill:
            p.showGameMsg(GMDD.data.LIFE_SKILL_USING_MANU_SKILL, ())
            return
        dId = self.lifeSkillFactory.getCurLifeSkillIns(uiConst.PANEL_TYPE_MAKE_SKILL).getDetailId()
        if not self.defaultCanDo(dId):
            if not p.getAbilityData(gametypes.ABILITY_LS_MANUFACTURE_SUB_ON, dId):
                p.showGameMsg(GMDD.data.LIFE_SKILL_NOT_LEARN, ())
                return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_LIFE_SKILL_MAKE_ALL, True)

    def closeMakeAllPanel(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_LIFE_SKILL_MAKE_ALL)

    def onMakeClick(self, *arg):
        idx = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        dId = self.lifeSkillFactory.getCurLifeSkillIns(uiConst.PANEL_TYPE_MAKE_SKILL).getDetailId()
        if not self.defaultCanDo(dId):
            if not p.getAbilityData(gametypes.ABILITY_LS_MANUFACTURE_SUB_ON, dId):
                p.showGameMsg(GMDD.data.LIFE_SKILL_NOT_LEARN, ())
                return
        curLifeSkill = self.lifeSkillFactory.getCurLifeSkillIns(idx)
        curLifeSkill.makeClick()

    def onGetManuInfo(self, *arg):
        idx = int(arg[3][0].GetNumber())
        curLifeSkill = self.lifeSkillFactory.getCurLifeSkillIns(idx)
        return curLifeSkill.getManuInfo()

    def onCancelMake(self, *args):
        p = BigWorld.player()
        p.cell.cancelManuLifeSkill()

    def refreshAssistPanel(self):
        if self.mediator:
            self.mediator.Invoke('refreshAssistPanel')

    def showTarget(self, lifeSkillId):
        curLifeSkillId = uiUtils.getCurLifeSkill(lifeSkillId)
        gamelog.debug('@jinjj lifeSkill#refreshPanel:', lifeSkillId, curLifeSkillId)
        if curLifeSkillId[0] is None:
            return
        else:
            lifeSkillData = LSD.data.get(curLifeSkillId, {})
            panelType = uiUtils.lifeSkillType2PanelType(lifeSkillData['type'])
            lifeSkillIns = self.lifeSkillFactory.lifeSkillIns[uiConst.PANEL_TYPE_LIFE_SKILL_OVERVIEW]
            lifeSkillIns.getPanelInfo()
            leftSelectedIndex = lifeSkillIns.leftVal2Index(lifeSkillData['type'], lifeSkillId)
            self.selectMakePos = [leftSelectedIndex, 0, 0]
            if self.mediator:
                self.changeToTab(panelType)
                if self.curLifeTypeIdx == panelType:
                    self.refreshPanel()
            else:
                self.show(panelType)
            return

    def addSkillLevelUpPushMsg(self, lifeSkillId, curExpVal, level):
        lifeSkillData = LSD.data.get((lifeSkillId, level), {})
        maxExpVal = lifeSkillData['lvUpExp']
        if curExpVal >= maxExpVal and level % 10 == 9:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_PUSH_LIFE_SKILL_LV_UP)

    def addFishingPushMsg(self):
        p = BigWorld.player()
        fData = FLD.data.get(p.fishingLv, {})
        curExp = p.fishingExp
        maxExp = fData['exp']
        if curExp >= maxExp and p.fishingLv % 10 == 9:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_PUSH_LIFE_SKILL_LV_UP)

    def toggle(self):
        if self.isShow:
            self.clearWidget()
        else:
            self.show()

    def onGetExtraAbilityInfo(self, *args):
        return uiUtils.dict2GfxDict(self.getExtraAbilityInfo(), True)

    def getExtraAbilityInfo(self):
        if not self.extraAbilityInfo:
            maxPhase = 0
            for key in LSEASD.data:
                phase = LSEASD.data[key]['phase']
                atype = LSEASD.data[key].get('skillType', 0)
                if phase > maxPhase:
                    maxPhase = phase
                elif atype > self.maxAtype:
                    self.maxAtype = atype
                typeName = LSSD.data.get(atype, {}).get('name', '')
                if not self.extraAbilityInfo.get('typeMap'):
                    self.extraAbilityInfo['typeMap'] = {}
                self.extraAbilityInfo['typeMap'][atype] = typeName
                if not self.extraAbilityInfo.get(phase):
                    self.extraAbilityInfo[phase] = {}
                    self.extraAbilityInfo[phase][atype] = []
                elif not self.extraAbilityInfo[phase].get(atype):
                    self.extraAbilityInfo[phase][atype] = []
                info = {}
                info['abilityId'] = key
                info['desc'] = LSEASD.data.get(key, {}).get('desc', '')
                info['name'] = AD.data.get(key, {}).get('name', '')
                info['unripeName'] = AD.data.get(key, {}).get('unripeName', '')
                info['description1'] = AD.data.get(key, {}).get('description1', '')
                self.extraAbilityInfo[phase][atype].append(info)

            tempAtype = 0
            for phase in range(2, maxPhase + 1):
                j = -1
                for atype in range(1, self.maxAtype + 1):
                    for ability in self.extraAbilityInfo[phase].get(atype, []):
                        if atype != tempAtype:
                            j += 1
                        posX = 221 + 60 * j
                        obj = {}
                        obj['abilityId'] = ability.get('abilityId')
                        obj['phase'] = phase
                        obj['posX'] = posX
                        itemName = ability.get('unripeName', '')
                        matchName = ability.get('lifeSkillMatchField', '')
                        tmp1 = {}
                        tmp1['itemName'] = itemName if itemName else ''
                        tmp1['pinyinFirst'] = pinyinConvert.strPinyinFirst(itemName)
                        tmp1['pinyin'] = pinyinConvert.strPinyin(itemName)
                        tmp2 = {}
                        tmp2['itemName'] = matchName if matchName else ''
                        tmp2['pinyinFirst'] = pinyinConvert.strPinyinFirst(matchName)
                        tmp2['pinyin'] = pinyinConvert.strPinyin(matchName)
                        self.extraAbilityPosInfo.append((tmp1, tmp2, obj))
                        tempAtype = atype

        self.refreshAbility()
        return self.extraAbilityInfo

    def onGetMaxAtype(self, *args):
        return GfxValue(self.maxAtype)

    def onClickLvUp(self, *args):
        skillId = int(args[3][0].GetNumber())
        seekIds = SCD.data.get('lifeSkillLevelUpSeekIds', {}).get(skillId, ())
        msg = uiUtils.getTextFromGMD(GMDD.data.LIFE_SKILL_LEVEL_UP_MSG, gameStrings.TEXT_LIFESKILLNEWPROXY_1102)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onTraceRoad, seekIds), gameStrings.TEXT_LIFESKILLNEWPROXY_1103)

    def onBuySmallBtnClick(self, *args):
        itemName = unicode2gbk(args[3][0].GetString())
        BigWorld.player().openAuctionFun(searchItemName=itemName)

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[9:]), int(idItem))

    def onOtherSmallBtnClick(self, *args):
        currentLabel = unicode2gbk(args[3][0].GetString())
        getItemId = int(args[3][1].GetNumber())
        type = uiConst.SMALL_BTN_TYPE_LABEL_REVERT[currentLabel]
        gamelog.debug('@lvc onOtherSmallBtnClick:getItemId,type', getItemId, type)
        if type == 1:
            collectionId = getItemId
            findItemId = LSCD.data.get(collectionId, {}).get('targetId', 0)
            ProductTabId_SubType = {1: 0,
             3: 1,
             4: 2}
            productTabId = LSCD.data.get(collectionId, {}).get('subType', 0)
            self.hideInfo[1] = 0
            self.setSelectProductPos(0, -1, ProductTabId_SubType[productTabId])
            if self.mediator:
                self.mediator.Invoke('setProduceSkillTab', (GfxValue(2), GfxValue(0), GfxValue(findItemId)))
        elif type == 2:
            makeId = getItemId
            self.hideInfo[0] = 0
            subType = LSMD.data.get(makeId, {}).get('subType', '')
            leftId = LSSD.data.get(subType, {}).get('lifeSkillId', 0)
            midId = -1
            for key, value in LSSD.data.items():
                if value['lifeSkillId'] == leftId:
                    midId = midId + 1
                    if subType == key:
                        break

            self.setSelectMakePos(leftId - 6, midId, makeId)
            className = LSMD.data.get(makeId, {}).get('className', '')
            self.openNode[gbk2unicode(className)] = 1
            self.refreshPanel()

    def onTraceRoad(self, seekIds):
        p = BigWorld.player()
        mapName = MCD.data.get(p.mapID, {}).get('name', '')
        msg = SCD.data.get('LIFE_SKILL_LEVEL_UP_SEEK_DESC', gameStrings.TEXT_LIFESKILLNEWPROXY_1151) % mapName
        uiUtils.findPosWithAlert(seekIds, msg)

    def refreshAbility(self):
        for key in self.extraAbilityInfo:
            if key != 'typeMap':
                for key2 in self.extraAbilityInfo[key]:
                    i = 0
                    sizeArray = len(self.extraAbilityInfo[key][key2])
                    for i in xrange(sizeArray):
                        aid = self.extraAbilityInfo[key][key2][i]['abilityId']
                        if aid not in AD.data.keys():
                            continue
                        sid = AD.data.get(aid, {}).get('sid', 0)
                        atype = AD.data.get(aid, {}).get('atype', 0)
                        skey = utils.getAbilityKey(atype, sid)
                        if BigWorld.player().abilityData.get(skey):
                            self.extraAbilityInfo[key][key2][i]['isGet'] = True
                        else:
                            self.extraAbilityInfo[key][key2][i]['isGet'] = False
