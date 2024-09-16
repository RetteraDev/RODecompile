#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/lifeSkillProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gamelog
import gameglobal
import gametypes
import uiUtils
import utils
from uiProxy import SlotDataProxy
from guis import uiConst
from guis import lifeSkillFactory
from data import life_skill_data as LSD
from data import life_skill_config_data as LSCD
from cdata import game_msg_def_data as GMDD
TA = None
MAKE_SKILL_ID = 3

class LifeSkillProxy(SlotDataProxy):
    SPECIAL_PANEL = 4

    def __init__(self, uiAdapter):
        super(LifeSkillProxy, self).__init__(uiAdapter)
        self.bindType = 'lifeSkill'
        self.type = 'lifeSkill'
        self.modelMap = {'getPanelInfo': self.onGetPanelInfo,
         'getLeftListMenuInfo': self.onGetLeftListMenuInfo,
         'getMidListInfo': self.onGetMidListInfo,
         'getDetailInfo': self.onGetDetailInfo,
         'getRightDetailInfo': self.onGetRightDetailInfo,
         'getExpertiseInfo': self.onGetExpertiseInfo,
         'getLabourInfo': self.onGetLabourInfo,
         'abilityTreeClick': self.onAbilityTreeClick,
         'setCurPanelType': self.onSetCurPanelType,
         'getCurPanelType': self.onGetCurPanelType,
         'clickCloseBtn': self.onClickCloseBtn,
         'clickHelpBtn': self.onClickHelpBtn,
         'getStepperInfo': self.onGetStepperInfo,
         'makeAllClick': self.onMakeAllClick,
         'getKuiLingBtnEnabled': self.onGetKuiLingBtnEnabled,
         'makeClick': self.onMakeClick,
         'cancelMake': self.onCancelMake,
         'getManuInfo': self.onGetManuInfo,
         'usingManuLifeSkillInfo': self.onUsingManuLifeSkillInfo,
         'getLeftSelectedIndex': self.onGetLeftSelectedIndex,
         'getJoinFlag': self.onGetJoinFlag,
         'getOverviewInfo': self.onGetOverviewInfo,
         'joinBtnClick': self.onJoinBtnClick,
         'getKuiLingInfo': self.onGetKuiLingInfo,
         'getLeftList': self.onGetLeftList,
         'getKuiLingDetailInfo': self.onGetKuiLingDetailInfo,
         'getLabourBack': self.onGetLabourBack,
         'marketClick': self.onMarketClick,
         'backClick': self.onBackClick,
         'refreshClick': self.onRefreshClick,
         'acceptQuestClick': self.onAcceptQuestClick,
         'getRefreshTime': self.onGetRefreshTime,
         'registerMakePanel': self.onRegisterMakePanel,
         'unRegisterMakePanel': self.onUnRegisterMakePanel,
         'makeAllPanelConfirmClick': self.onMakeAllPanelConfirmClick,
         'makeAllPanelCloseClick': self.onMakeAllPanelCloseClick,
         'makeAllPanelCancelClick': self.onMakeAllPanelCancelClick,
         'getMakeAllPanelInfo': self.onGetMakeAllPanelInfo,
         'updateSelectNeedItem': self.onUpdateSelectNeedItem,
         'getAssistInfo': self.onGetAssistInfo,
         'repairClick': self.onRepairClick,
         'cancelRepair': self.onCancelRepair,
         'confirmRepair': self.onConfirmRepair,
         'getRepairInfo': self.onGetRepairInfo,
         'getNowCanMakeNum': self.onGetNowCanMakeNum,
         'clickToPanel': self.onClickToPanel,
         'clickToSpecial': self.onClickToSpecial}
        self.lifeSkillFactory = lifeSkillFactory.getInstance()
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_LIFE_SKILL_PANEL, self.hide)
        uiAdapter.registerEscFunc(uiConst.WIDGET_LIFE_SKILL_MAKE_ALL, self.onMakeAllPanelCancelClick)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_LIFE_SKILL_PANEL:
            self.mediator = mediator
            p = BigWorld.player()
            enableKuilingLv = LSCD.data.get('enableKuilingLv', 20)
            self.mediator.Invoke('setBtnEnable', GfxValue(p.lv >= enableKuilingLv))
            return uiUtils.dict2GfxDict({'tabIdx': self.panelType})

    def reset(self):
        self.isShow = False
        self.curLifeSkill = None
        self.mediator = None
        self.makePanelMc = None
        self.manuStage = gametypes.MANUFACTURE_STAGE_BEGIN
        self.leftSelectedIndex = 0
        self.panelType = uiConst.PANEL_TYPE_LIFE_SKILL_OVERVIEW
        self.repairSubtype = 0
        self.repairPart = 0
        self.isSpecialPart = False
        self.lifeSkillFactory.reset()

    def onRegisterMakePanel(self, *arg):
        self.makePanelMc = arg[3][0]

    def onUnRegisterMakePanel(self, *arg):
        self.makePanelMc = None

    def getSlotID(self, key):
        idCon, idItem = key.split('.')
        return (int(idCon[9:]), int(idItem))

    def show(self):
        if not BigWorld.player().checkMapLimitUI(gametypes.MAP_LIMIT_UI_LIFE_SKILL):
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_LIFE_SKILL_PANEL)
        self.isShow = True

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_LIFE_SKILL_PANEL)

    def onClickCloseBtn(self, *arg):
        self.hide(True)

    def onClickHelpBtn(self, *arg):
        skillType = int(arg[3][0].GetNumber())
        self.curLifeSkill.clickHelp(skillType)

    def onAbilityTreeClick(self, *arg):
        if gameglobal.rds.ui.abilityTree.mediator:
            gameglobal.rds.ui.abilityTree.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ABILITY_TREE)

    def onSetCurPanelType(self, *arg):
        curPanelType = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if curPanelType == uiConst.PANEL_TYPE_KUI_LING and p.kuilingOrg > 0:
            gameglobal.rds.ui.lifeSkill.lifeSkillFactory.createKuiLingIns(p.kuilingOrg)
        self.setCurLifeSkill(curPanelType)

    def setCurLifeSkill(self, curPanelType):
        if self.curLifeSkill:
            self.curLifeSkill.reset()
        self.curLifeSkill = self.lifeSkillFactory.getCurLifeSkillIns(curPanelType)

    def onGetCurPanelType(self, *arg):
        return GfxValue(self.panelType)

    def onGetPanelInfo(self, *arg):
        gamelog.debug('@hjx lifeSkill#onGetPanelInfo:', self.curLifeSkill)
        return self.curLifeSkill.getPanelInfo()

    def refreshAssistPanel(self):
        if self.mediator:
            self.mediator.Invoke('refreshAssistPanel')

    def onGetLeftListMenuInfo(self, *arg):
        return self.curLifeSkill.getLeftListMenuInfo()

    def onGetMidListInfo(self, *arg):
        firstIndex = int(arg[3][0].GetNumber())
        secondIndex = int(arg[3][1].GetNumber())
        self.curLifeSkill.clickSubMenu(firstIndex, secondIndex)
        gamelog.debug('@hjx lifeSkill#onGetMidListInfo:', firstIndex, secondIndex)
        return uiUtils.array2GfxAarry(self.curLifeSkill.getMidListInfo(), True)

    def onGetDetailInfo(self, *arg):
        firstIndex = int(arg[3][0].GetNumber())
        secondIndex = int(arg[3][1].GetNumber())
        self.curLifeSkill.clickSubMenu(firstIndex, secondIndex)
        gamelog.debug('@hjx lifeSkill#onGetDetailInfo:', firstIndex, secondIndex)
        return self.curLifeSkill.getDetailInfo()

    def onGetRightDetailInfo(self, *arg):
        firstIndex = int(arg[3][0].GetNumber())
        secondIndex = int(arg[3][1].GetNumber())
        self.curLifeSkill.clickMidSubMenu(firstIndex, secondIndex)
        gamelog.debug('@hjx lifeSkill#onGetRightDetailInfo:', firstIndex, secondIndex)
        return self.curLifeSkill.getDetailInfo()

    def onGetExpertiseInfo(self, *arg):
        return self.curLifeSkill.getExpertiseInfo()

    def onGetLabourInfo(self, *arg):
        return self.curLifeSkill.getLabourInfo()

    def onGetStepperInfo(self, *arg):
        direc = int(arg[3][0].GetNumber())
        return self.curLifeSkill.getStepperInfo(direc)

    def onGetKuiLingBtnEnabled(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableKuilingOrg', False))

    def onMakeAllClick(self, *arg):
        self.showMakeAllPanel()

    def showMakeAllPanel(self):
        p = BigWorld.player()
        if p.curLifeSkillType == gametypes.LIFE_SKILL_TYPE_MANUFACTURE and p.usingLifeSkill:
            p.showGameMsg(GMDD.data.LIFE_SKILL_USING_MANU_SKILL, ())
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_LIFE_SKILL_MAKE_ALL, True)

    def closeMakeAllPanel(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_LIFE_SKILL_MAKE_ALL)

    def onMakeAllPanelConfirmClick(self, *arg):
        num = arg[3][0].GetString()
        p = BigWorld.player()
        if num == '':
            p.showGameMsg(GMDD.data.MANU_SKILL_FAILED_NULL_NUM, ())
            return
        num = int(num)
        if num == 0:
            p.showGameMsg(GMDD.data.MANU_SKILL_FAILED_NULL_0, ())
            return
        makeSkill = self.lifeSkillFactory.getCurLifeSkillIns(MAKE_SKILL_ID)
        if not makeSkill:
            return
        makeSkill.makeAllClick(num)
        self.closeMakeAllPanel()

    def onMakeAllPanelCloseClick(self, *arg):
        self.closeMakeAllPanel()

    def onMakeAllPanelCancelClick(self, *arg):
        p = BigWorld.player()
        p.cell.cancelManuLifeSkill()
        self.closeMakeAllPanel()

    def onGetMakeAllPanelInfo(self, *arg):
        makeSkill = self.lifeSkillFactory.getCurLifeSkillIns(MAKE_SKILL_ID)
        return makeSkill.getMakeAllInfo()

    def onUpdateSelectNeedItem(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        val = int(arg[3][1].GetNumber())
        self.curLifeSkill.updateSelectNeedItem(itemId, val)

    def onGetAssistInfo(self, *arg):
        subType = int(arg[3][0].GetNumber())
        gamelog.debug('@hjx lifeSkill#onGetAssistInfo:', subType)
        return self.curLifeSkill.getAssistInfo(subType)

    def onRepairClick(self, *arg):
        self.repairSubtype = int(arg[3][0].GetNumber())
        self.repairPart = int(arg[3][1].GetNumber())
        gamelog.debug('@hjx lifeSkill#onRepairClick:', self.repairSubtype, self.repairPart)
        if self.repairPart == 0:
            BigWorld.player().showGameMsg(GMDD.data.LIFE_EQUIPMENT_REPAIR_NO_SELECT, ())
            return
        self.showRepairPanel()

    def onCancelRepair(self, *arg):
        self.closeRepairPanel()

    def onConfirmRepair(self, *arg):
        mType = gametypes.LIFE_EQUIPMENT_NORMAL_REPAIR
        p = BigWorld.player()
        if self.isSpecialPart == False:
            p.cell.repairLifeEquipDurability(self.repairSubtype, self.repairPart, mType)
        else:
            sendType = gametypes.LIFE_SKILL_TYPE_FISHING
            if self.repairSubtype == 2:
                sendType = gametypes.LIFE_SKILL_TYPE_EXPLORE
            p.cell.repairSpecialLifeEquipDurability(sendType, self.repairPart - 1, mType)
        self.closeRepairPanel()

    def onGetRepairInfo(self, *arg):
        p = BigWorld.player()
        if self.isSpecialPart == False:
            eItem = p.lifeEquipment.get(self.repairSubtype, self.repairPart)
        else:
            if self.repairSubtype == 1:
                container = p.fishingEquip
            elif self.repairSubtype == 2:
                container = p.exploreEquip
            eItem = container[self.repairPart - 1]
        if eItem is None:
            return uiUtils.array2GfxAarry([])
        else:
            rData = utils.getLifeRepairData(eItem.itemLv)
            if rData is None:
                return uiUtils.array2GfxAarry([])
            info = []
            if self.isSpecialPart == False:
                amount = utils.getLifeRepairItemAmount(p, self.repairSubtype, eItem)
            else:
                amount = utils.getSpecialLifeRepairItemAmount(eItem)
            itemInfo = {}
            itemId = rData['normalFixItem']
            iconPath = uiUtils.getItemIconFile64(itemId)
            itemInfo['itemId'] = itemId
            itemInfo['icon'] = {'iconPath': iconPath,
             'itemId': itemId,
             'count': str(p.inv.countItemInPages(itemId)) + '/' + str(amount)}
            info.append(itemInfo)
            itemInfo = {}
            itemId = rData['fineFixItem']
            iconPath = uiUtils.getItemIconFile64(itemId)
            itemInfo['itemId'] = itemId
            itemInfo['icon'] = {'iconPath': iconPath,
             'itemId': itemId,
             'count': str(p.inv.countItemInPages(itemId)) + '/' + str(amount)}
            info.append(itemInfo)
            return uiUtils.array2GfxAarry(info, True)

    def showRepairPanel(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_LIFE_SKILL_REPAIR, True)

    def closeRepairPanel(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_LIFE_SKILL_REPAIR)

    def onMakeClick(self, *arg):
        self.curLifeSkill.makeClick()

    def refreshMakingPanel(self, stage):
        gamelog.debug('@hjx lifeSkill#refreshMakingPanel:', stage, self.makePanelMc)
        self.manuStage = stage
        if self.makePanelMc:
            self.makePanelMc.Invoke('refreshMakingPanel', GfxValue(stage))

    def refreshLifeSkillPanel(self):
        if self.mediator:
            self.mediator.Invoke('refreshLifeSkillPanel')

    def onLifeSkillLevelUp(self):
        if self.mediator:
            self.mediator.Invoke('onLifeSkillLevelUp')

    def onCancelMake(self, *arg):
        p = BigWorld.player()
        p.cell.cancelManuLifeSkill()

    def onGetManuInfo(self, *arg):
        return self.curLifeSkill.getManuInfo()

    def onUsingManuLifeSkillInfo(self, *arg):
        return self.curLifeSkill.usingManuLifeSkillInfo()

    def onGetLeftSelectedIndex(self, *arg):
        return GfxValue(self.leftSelectedIndex)

    def onClickToPanel(self, *args):
        lifeSkillId = int(args[3][0].GetNumber())
        self.refreshPanel(lifeSkillId)

    def onClickToSpecial(self, *args):
        typeName = args[3][0].GetString()
        self.goToFishOrExplore(typeName)

    def goToFishOrExplore(self, type):
        self.panelType = self.SPECIAL_PANEL
        if type == 'fish':
            self.leftSelectedIndex = 0
        else:
            self.leftSelectedIndex = 1
        if self.mediator:
            self.mediator.Invoke('refreshPanel', GfxValue(self.panelType))
        else:
            self.show()

    def refreshPanel(self, lifeSkillId):
        curLifeSkillId = uiUtils.getCurLifeSkill(lifeSkillId)
        gamelog.debug('@hjx lifeSkill#refreshPanel:', lifeSkillId, curLifeSkillId)
        if curLifeSkillId[0] is None:
            return
        else:
            lifeSkillData = LSD.data.get(curLifeSkillId, {})
            self.panelType = uiUtils.lifeSkillType2PanelType(lifeSkillData['type'])
            lifeSkillIns = self.lifeSkillFactory.lifeSkillIns[uiConst.PANEL_TYPE_LIFE_SKILL_OVERVIEW]
            self.leftSelectedIndex = lifeSkillIns.leftVal2Index(lifeSkillData['type'], lifeSkillId)
            gamelog.debug('@hjx lifeSkill#refreshPanel1:', lifeSkillData['type'], self.panelType, self.curLifeSkill, self.leftSelectedIndex)
            if self.mediator:
                self.mediator.Invoke('refreshPanel', GfxValue(self.panelType))
            else:
                self.show()
            return

    def onGetJoinFlag(self, *arg):
        p = BigWorld.player()
        return GfxValue(p.kuilingOrg > 0)

    def onGetOverviewInfo(self, *arg):
        return self.lifeSkillFactory.getKuiLingOverview()

    def onJoinBtnClick(self, *arg):
        index = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        p.cell.addToKuilingOrg(index)

    def onGetKuiLingInfo(self, *arg):
        return self.curLifeSkill.getKuiLingInfo()

    def onGetLeftList(self, *arg):
        return self.curLifeSkill.getLeftList()

    def onGetKuiLingDetailInfo(self, *arg):
        index = int(arg[3][0].GetNumber())
        return self.curLifeSkill.getDetailInfo(index)

    def onGetLabourBack(self, *arg):
        p = BigWorld.player()
        p.cell.chargeLabourByKuiling()

    def onMarketClick(self, *arg):
        gameglobal.rds.ui.resourceMarket.show()

    def onBackClick(self, *arg):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_LIFESKILLPROXY_431, self._quitFromKuiling)

    def _quitFromKuiling(self):
        p = BigWorld.player()
        p.cell.quitFromKuilingOrg()

    def onRefreshClick(self, *arg):
        p = BigWorld.player()
        p.cell.refreshKuilingQuests()

    def onAcceptQuestClick(self, *arg):
        index = int(arg[3][0].GetNumber())
        if self.curLifeSkill:
            self.curLifeSkill.acceptQuest(index)

    def onGetRefreshTime(self, *arg):
        return GfxValue(self.curLifeSkill.getRefreshTime())

    def onGetNowCanMakeNum(self, *args):
        num = 0
        makeSkill = self.lifeSkillFactory.getCurLifeSkillIns(MAKE_SKILL_ID)
        if makeSkill and hasattr(makeSkill, 'getCanBuildNum'):
            detailId = makeSkill.getDetailId()
            num = makeSkill.getCanBuildNum(detailId)
        return GfxValue(num)
