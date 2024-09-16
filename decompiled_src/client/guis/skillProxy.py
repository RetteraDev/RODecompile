#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/skillProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import math
import sys
import copy
import gameglobal
import const
import gameconfigCommon
import utils
import gametypes
import skillDataInfo
import logicInfo
import gamelog
import appSetting
import skillInfoManager
from asObject import ASObject
from helpers import cellCmd
from helpers import navigator
from gameclass import SkillInfo
from uiProxy import SlotDataProxy
from ui import gbk2unicode
from guis import uiUtils, uiConst
from guis import ui
from guis import cursor
from gameStrings import gameStrings
from skillEnhanceCommon import CSkillEnhanceVal
from item import Item
from gameclass import PSkillInfo
from callbackHelper import Functor
from data import skill_panel_data as SPD
from data import skill_general_data as SGD
from data import skill_general_template_data as SGTD
from data import general_skill_config_data as GSCD
from data import school_data as SD
from data import qing_gong_skill_data as QGSD
from data import item_data as ID
from cdata import font_config_data as FCD
from data import fishing_lv_data as FLD
from data import ws_skill_config_data as WSCD
from data import explore_lv_data as ELD
from data import special_life_skill_equip_data as SLSED
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from cdata import ws_enhance_data as WED
from cdata import pskill_data as PD
from cdata import pskill_template_data as PSTD
from cdata import ws_skill_lvup_data as WSLD
from cdata import air_skill_lv_data as ASLD
from data import skill_enhance_data as SED
from cdata import skill_enhance_jingjie_data as SEJD
from data import sys_config_data as SCFD
from data import sys_config_data as SCD
from cdata import skill_enhance_cost_data as SECD
from data import state_data as STD
from data import guild_pskill_data as GPD
from data import skill_client_data as SKCD
from data import ws_daoheng_data as WDD
from data import jingjie_data as JJD
from cdata import skill_enhance_lv_data as SELD
from cdata import guanyin_book_data as GBD
from data import intimacy_skill_data as ISD
from cdata import intimacy_skill_lv_data as ISLD
from data import marriage_config_data as MCD
from data import region_server_config_data as RSCD
from cdata import guanyin_data as GD
MAX_NORMAL_SKILL_NUMS = 12
MAX_SPECIAL_SKILL_NUMS = 8
MAX_EQUIP_SKILL_NUMS = 3
DATA_TYPE_SKILL = 1
DATA_TYPE_PSKILL = 2
WU_DAO_MAX_STAR = 5
SKILL_MIN_LV = 1
QINGGONG_FLAG_BASIC = 99
TIANZHAO_WEN_DAO_SKILL_SET_ID = 1915

class SkillProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(SkillProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerCommonSkill': self.onRegisterCommonSkill,
         'unRegisterCommonSkill': self.onUnRegisterCommonSkill,
         'clickClose': self.onClickClose,
         'getNormalSkills': self.onGetNormalSkills,
         'getPSKills': self.onGetPSKills,
         'getSkillPointInfo': self.onGetSkillPointInfo,
         'getXiuLianPoint': self.onGetXiuLianPoint,
         'getXiuLianTips': self.onGetXiuLianTips,
         'getEnhanceLvInfo': self.onGetEnhanceLvInfo,
         'addNormalSkill': self.onAddNormalSkill,
         'checkXiuLianValid': self.onCheckXiuLianValid,
         'registerWuShuangSkillMc': self.onRegisterWuShuangSkillMc,
         'unRegisterWuShuangSkillMc': self.onUnRegisterWuShuangSkillMc,
         'addSkillExpByItem': self.onAddSkillExpByItem,
         'openDaoHengSlot': self.onAddDaoHengSlot,
         'getSpecialSkills': self.onGetSpecialSkills,
         'addSpecialSkill': self.onAddSpecialSkill,
         'registerAirSkillMc': self.onRegisterAirSkillMc,
         'unRegisterAirSkillMc': self.onUnRegisterAirSkillMc,
         'getAirBattleSkills': self.onGetAirBattleSkills,
         'getAirSkillbarInfo': self.onGetAirSkillbarInfo,
         'delAirSkillSlot': self.onDelAirSkillSlot,
         'getAirSkillSwitchOn': self.onGetAirSkillSwitchOn,
         'getSchool': self.onGetSchool,
         'getWsValue': self.onGetWsValue,
         'unEquipSpecialSkill': self.onUnEquipSpecialSkill,
         'getQingGongState': self.onGetQingGongState,
         'getFishingSkillInfo': self.onGetFishingSkillInfo,
         'unEquipFishingItem': self.onUnEquipFishingItem,
         'showIllustration': self.onShowIllustration,
         'addXiuWei': self.onAddXiuWei,
         'addWuShuang': self.onAddWuShuang,
         'getDetailInfo': self.onGetDetailInfo,
         'lvUp': self.onLvUp,
         'rebalanceDaoHang': self.onRebalanceDaoHang,
         'resetDaoHang': self.onResetDaoHang,
         'openItemSelect': self.onOpenItemSelect,
         'WuDao': self.onWuDao,
         'PanelWuDao': self.onPanelWuDao,
         'openDetailpanel': self.onOpenDetailpanel,
         'closeDetailPanel': self.onCloseDetailPanel,
         'getEnhanceType': self.onGetEnhanceType,
         'getWuShuangBarInfo': self.onGetWuShuangBarInfo,
         'getRelieveInfo': self.onGetRelieveInfo,
         'getXiuWeiBarInfo': self.onGetXiuWeiBarInfo,
         'closeEnhancePanel': self.onCloseEnhancePanel,
         'confirmEnhance': self.onConfirmEnhance,
         'relieveDaoHang': self.onRelieveDaoHang,
         'getDaoHangDirectionInfo': self.onGetDaoHangDirectionInfo,
         'realize': self.onRealize,
         'closeDaoHangPanel': self.onCloseDaoHangPanel,
         'getDirectionDesc': self.onGetDirectionDesc,
         'convertPotential': self.onConvertPotential,
         'getBonusTips': self.onGetBonusTips,
         'getTabIdx': self.onGetTabIdx,
         'resetSkills': self.onResetSkills,
         'saveSkills': self.onSaveSkills,
         'addPSkill': self.onAddPSkill,
         'closeLifeSkill': self.onCloseLifeSkill,
         'getExploreSkillInfo': self.onGetExploreSkillInfo,
         'unEquipCompassItem': self.onUnEquipCompassItem,
         'activateSkillEnhancement': self.onActivateSkillEnhancement,
         'getQingGongSkill': self.onGetQingGongSkill,
         'openGuide': self.onOpenGuide,
         'getSkillPracticeInfo': self.onGetSkillPracticeInfo,
         'closeSkillPractice': self.onCloseSkillPractice,
         'confirmPractice': self.onConfirmPractice,
         'cancelPractice': self.onCancelPractice,
         'applyPractice': self.onApplyPractice,
         'equipSkillPracitce': self.onEquipSkillPracitce,
         'unEquipSkillPractice': self.onUnEquipSkillPractice,
         'lvUpQinggong': self.onLvUpQinggong,
         'skillWuDao': self.onSkillWuDao,
         'addSkillEnhancePoint': self.onAddSkillEnhancePoint,
         'reduceSkillEnhancePoint': self.onReduceSkillEnhancePoint,
         'resetSkillEnhancePoint': self.onResetSkillEnhancePoint,
         'showXiuLianAward': self.onShowXiuLianAward,
         'getSkillEnhancePoint': self.onGetSkillEnhancePoint,
         'selectPlan': self.onSelectPlan,
         'minusNormalSkill': self.onMinusNormalSkill,
         'getSkillEnhanceSchemeIndex': self.onGetSkillEnhanceSchemeIndex,
         'getWsEffect': self.onGetWsEffect,
         'setWsEffect': self.onSetWsEffect,
         'minusPSkill': self.onMinusPSkill,
         'getOtherSkill': self.onGetOtherSkill,
         'getGuildSkill': self.onGetGuildSkill,
         'closeGeneralSkill': self.onCloseGeneralSkill,
         'switchScheme': self.onSwitchScheme,
         'convertLingLi': self.onConvertLingLi,
         'onTianZhaoSkillSet': self.OnTianZhaoSkillSet,
         'canAddSkill': self.onCanAddSkill,
         'showSkillGuide': self.onShowSkillGuide,
         'getEnableSkillGuide': self.onGetEnableSkillGuide,
         'isSkillRemoveMode': self.onIsSkillRemoveMode,
         'changeSkillRemoveMode': self.onChangeSkillRemoveMode,
         'removeSkill': self.onRemoveSkill,
         'getSkillEnhanceAllSchool': self.onGetSkillEnhanceAllSchool,
         'changeSchool': self.onChangeSchool,
         'quitEditMode': self.onQuitEditMode,
         'getCurrentSchemeNum': self.getCurrentSchemeNum,
         'gotoWeb': self.onGotoWeb,
         'gameOnOff': self.onGameOnOff,
         'initTabState': self.onInitTabState,
         'getIntimacySkill': self.onGetIntimacySkill,
         'getWudaoTip': self.onGetWudaoTip,
         'openDuanZhangPanel': self.onOpenDuanZhangPanel,
         'getEnableWSSchemes': self.onGetEnableWSSchemes,
         'switchWSScheme': self.onSwitchWSScheme,
         'openSkillMacro': self.onOpenSkillMacro,
         'openSkillAppearance': self.onOpenSkillAppearance,
         'getExcitementDaoheng': self.onGetExcitementDaoheng,
         'shareSkills': self.onShareSkills,
         'resetXiulianSkills': self.onResetXiulianSkills,
         'isGotoXiuLian': self.onIsGotoXiuLian,
         'isUsingTemp': self.onIsUsingTemp,
         'isInPUBG': self.onIsInPUBG,
         'canChangeTemplate': self.onCanChangeTemplate,
         'saveXiuLianTemplate': self.onSaveXiuLianTemplate,
         'saveWuShuangTemplate': self.onSaveWuShuangTemplate,
         'getXiuLianScoreInfo': self.onGetXiuLianScoreInfo,
         'unlockEnhancePoint': self.onUnLockEnhancePoint,
         'isChaos': self.onIsChaos}
        self.binding = {}
        self.bindType = 'skills'
        self.type = 'skillPanel'
        self.mediator = None
        self.lifeMediator = None
        self.generalMediator = None
        self.detailMediator = None
        self.enhanceMediator = None
        self.daoHangDirMediator = None
        self.practiceMediator = None
        self.commonSkillMc = None
        self.isShow = False
        self.airSkillPanelMc = None
        self.wushuangSkillPanelMc = None
        self.normalSkills = []
        self.equipSkills = [[0, 0, 0], [0, 0, 0]]
        self.specialSkills = [[], []]
        self.pskills = []
        self.newSkills = []
        self.cfgedAirSkills = [[], []]
        self.equipedAirSkills = []
        self.activeAirSkillKV = {}
        self.wushuangSkillKV = {}
        self.schoolMap = {1: 3,
         2: 4,
         3: 5,
         4: 7,
         5: 6,
         6: 8}
        self.qingGongMap = {0: (gameStrings.TEXT_SKILLPROXY_249, 24),
         1: (gameStrings.TEXT_SKILLPROXY_249_1, 12),
         2: (gameStrings.TEXT_SKILLPROXY_249_2, 1),
         3: (gameStrings.TEXT_SKILLPROXY_249_3, 21),
         4: (gameStrings.TEXT_SKILLPROXY_249_4, 2),
         5: (gameStrings.TEXT_SKILLPROXY_249_5, 3),
         6: (gameStrings.TEXT_SKILLPROXY_249_6, 13),
         7: (gameStrings.TEXT_SKILLPROXY_249_7, 22)}
        self.RideMap = {0: (gameStrings.TEXT_SKILLPROXY_250, 19),
         1: (gameStrings.TEXT_SKILLPROXY_250_1, 17),
         2: (gameStrings.TEXT_SKILLPROXY_250_2, 18)}
        self.wingMap = {0: (gameStrings.TEXT_SKILLPROXY_251, 20),
         1: (gameStrings.TEXT_SKILLPROXY_251_1, 16),
         2: (gameStrings.TEXT_SKILLPROXY_251_2, 0),
         3: (gameStrings.TEXT_SKILLPROXY_251_3, 15),
         4: (gameStrings.TEXT_SKILLPROXY_251_4, 14),
         5: (gameStrings.TEXT_SKILLPROXY_251_5, 23),
         6: (gameStrings.TEXT_SKILLPROXY_251_6, 0)}
        self.callbackHandler = {}
        self.curType = 0
        self.skillId = 0
        self.enhanceType = None
        self.daoHangItemIds = const.ADD_WSSKILL_SLOT_ITEMS
        self.resetItemIds = const.WS_REST_LOSE_LESS_ITEMS
        self.generalTab = 0
        self.otherSkillData = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_SKILL_BG, self.onClickClose)
        uiAdapter.registerEscFunc(uiConst.WIDGET_SKILL_DETAIL, self.closeDetailpanel)
        uiAdapter.registerEscFunc(uiConst.WIDGET_SKILL_BAR_ENHANCE, self.closeEnhancePanel)
        uiAdapter.registerEscFunc(uiConst.WIDGET_DAOHANG_DIRECTION_V2, self.closeDaohangDirPanel)
        uiAdapter.registerEscFunc(uiConst.WIDGET_LIFE_SKILL_PANEL, self.closeLifeSkill)
        uiAdapter.registerEscFunc(uiConst.WIDGET_GENERAL_SKILL, self.closeGeneralSkill)
        self.fishItems = [None] * 3
        self.tabIdx = 0
        self.lastWsExpDict = {}
        self.bWsSkillPushed = {}
        self.lastWushuang = [0, 0]
        self.matchSkillsLv = {}
        self.skillInfoManager = skillInfoManager.getInstance()
        self.closeMsgBoxId = 0
        self.isSkillRemoveMode = False
        self.selectedSchool = None
        self.canRemoveSkillList = []
        self.reset()
        self.isGotoXiuLian = False

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SKILL_BG:
            self.mediator = mediator
            self._initWsSkillList()
            self.refreshSkillBgBtn()
            return uiUtils.dict2GfxDict({'tabIdx': self.tabIdx}, True)
        if widgetId == uiConst.WIDGET_LIFE_SKILL_PANEL:
            self.lifeMediator = mediator
        else:
            if widgetId == uiConst.WIDGET_GENERAL_SKILL:
                self.generalMediator = mediator
                gameglobal.rds.ui.emote.initHeadGen()
                gameglobal.rds.ui.emote.takePhoto3D()
                return GfxValue(self.generalTab)
            if widgetId == uiConst.WIDGET_SKILL_DETAIL:
                self.detailMediator = mediator
            elif widgetId == uiConst.WIDGET_SKILL_BAR_ENHANCE:
                self.enhanceMediator = mediator
            elif widgetId == uiConst.WIDGET_DAOHANG_DIRECTION_V2:
                self.daoHangDirMediator = mediator
                return self.onGetDaoHangDirectionInfo()

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_DAOHANG_DIRECTION_V2:
            self.closeDaohangDirPanel()
        else:
            SlotDataProxy._asWidgetClose(self, widgetId, multiID)

    def onSwitchScheme(self, *args):
        gameglobal.rds.ui.skillScheme.show()

    def setSchemeName(self):
        if self.commonSkillMc != None:
            idx = BigWorld.player().skillPointSchemeIndex
            name = BigWorld.player().getSkillSchemeName(idx)
            self.commonSkillMc.Invoke('setSchemeName', GfxValue(gbk2unicode(name)))

    def onRegisterCommonSkill(self, *arg):
        self.commonSkillMc = arg[3][0]
        self.selectedSchool = BigWorld.player().realSchool
        self.canRemoveSkillList = []
        self.isSkillRemoveMode = False
        self.setSchemeName()
        BigWorld.player().cell.getCanRemoveSkillEnhances()

    def onUnRegisterCommonSkill(self, *arg):
        self.isSkillRemoveMode = False
        self.commonSkillMc = None
        self.canRemoveSkillList = []
        self.selectedSchool = BigWorld.player().realSchool

    def hasSkillPointChange(self):
        diffVal = self.skillInfoManager.commonSkillIns.getConsumePoint() + self.skillInfoManager.pSkillIns.getConsumePoint()
        return diffVal > 0

    def onClickClose(self, *arg):
        if self.hasSkillPointChange():
            if not self.closeMsgBoxId:
                msg = gameStrings.TEXT_SKILLPROXY_350
                self.closeMsgBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=lambda : self._realClose(), noCallback=self._closeTip)
        else:
            self._realClose()

    def _realClose(self):
        self.closeMsgBoxId = 0
        self.hide(False)

    def _closeTip(self):
        self.closeMsgBoxId = 0

    def onCanAddSkill(self, *arg):
        ret = True
        if gameglobal.rds.configData.get('enableSkillLvAutoUp'):
            autoLv = SCD.data.get('SKILL_AUTO_UP_LV', 40)
            ret = BigWorld.player().lv >= autoLv
        return GfxValue(ret)

    def onShowSkillGuide(self, *arg):
        type = int(arg[3][0].GetNumber())
        gameglobal.rds.ui.skillGuide.show(type=type)

    def onGetNormalSkills(self, *arg):
        return self.skillInfoManager.commonSkillIns.getSkillInfo()

    def onGetPSKills(self, *arg):
        return self.skillInfoManager.pSkillIns.getSkillInfo()

    def onCheckXiuLianValid(self, *arg):
        p = BigWorld.player()
        startJingJie = SCFD.data.get('startJingJie', 3)
        if p.arenaJingJie < startJingJie:
            p.showGameMsg(GMDD.data.SKILL_XIU_LIAN_FAILED_LESS_JING_JIE, (JJD.data.get(startJingJie, {}).get('name', ''),))
            return GfxValue(False)
        diffVal = self.skillInfoManager.commonSkillIns.getConsumePoint() + self.skillInfoManager.pSkillIns.getConsumePoint()
        if diffVal > 0:
            p.showGameMsg(GMDD.data.XIU_LIAN_FAILED_SAVE_SKILL_POINT_FIRST, ())
            return GfxValue(False)
        return GfxValue(True)

    def onAddNormalSkill(self, *arg):
        if not BigWorld.player().stateMachine.checkStatus(const.CT_CHANGE_SKILL_LEVEL):
            return
        idx = int(arg[3][0].GetNumber())
        skillId = self.normalSkills[idx]
        self.skillInfoManager.commonSkillIns.addSkillPoint(skillId)
        self.refreshNormalSkill()
        self.refreshPSkill()

    def onMinusNormalSkill(self, *arg):
        if not BigWorld.player().stateMachine.checkStatus(const.CT_CHANGE_SKILL_LEVEL):
            return
        idx = int(arg[3][0].GetNumber())
        skillId = self.normalSkills[idx]
        self.skillInfoManager.commonSkillIns.reduceSkillPoint(skillId)
        self.refreshNormalSkill()
        self.refreshPSkill()

    def onAddPSkill(self, *arg):
        if not BigWorld.player().stateMachine.checkStatus(const.CT_CHANGE_SKILL_LEVEL):
            return
        idx = int(arg[3][0].GetNumber())
        pskId = self.pskills[idx]
        self.skillInfoManager.pSkillIns.addSkillPoint(pskId)
        self.refreshNormalSkill()
        self.refreshPSkill()

    def onMinusPSkill(self, *arg):
        if not BigWorld.player().stateMachine.checkStatus(const.CT_CHANGE_SKILL_LEVEL):
            return
        idx = int(arg[3][0].GetNumber())
        pskId = self.pskills[idx]
        self.skillInfoManager.pSkillIns.reduceSkillPoint(pskId)
        self.refreshNormalSkill()
        self.refreshPSkill()

    def onRegisterWuShuangSkillMc(self, *arg):
        self.wushuangSkillPanelMc = arg[3][0]

    def onUnRegisterWuShuangSkillMc(self, *arg):
        self.wushuangSkillPanelMc = None

    def onGetSpecialSkills(self, *arg):
        idx = int(arg[3][0].GetNumber())
        self.curType = idx
        ret = self._genSpecialSkillContent(idx)
        return uiUtils.dict2GfxDict(ret, True)

    def onAddSpecialSkill(self, *arg):
        pass

    def onGetSchool(self, *arg):
        return GfxValue(BigWorld.player().school)

    def onGetWsValue(self, *arg):
        idx = int(arg[3][0].GetNumber())
        return GfxValue(BigWorld.player().ws[idx])

    def onUnEquipSpecialSkill(self, *arg):
        if not self.skillEquipCheck():
            return
        skType = int(arg[3][0].GetString())
        idx = int(arg[3][1].GetString())
        skillId = self.equipSkills[skType][idx]
        key = self._getKey(2, skType * MAX_EQUIP_SKILL_NUMS + idx)
        if skillId != 0:
            BigWorld.player().cell.removeWsSkill(skillId)
        self.delSlotItem(key)
        if skType == 0:
            idSlot = 12 + idx
        elif skType == 1:
            idSlot = 15 + idx
        gameglobal.rds.ui.actionbar.removeItem(uiConst.SKILL_ACTION_BAR, idSlot, False)

    def onGetQingGongState(self, *arg):
        ret = self.movie.CreateArray()
        qinggong = self.movie.CreateArray()
        for i in xrange(0, 8):
            arr = self.movie.CreateArray()
            stat = True if i == 0 else BigWorld.player().qinggongMgr._getFlag(self.qingGongMap[i][1])
            arr.SetElement(0, GfxValue(stat))
            arr.SetElement(1, GfxValue(gbk2unicode(self.qingGongMap[i][0])))
            qinggong.SetElement(i, arr)

        ret.SetElement(0, qinggong)
        mount = self.movie.CreateArray()
        for i in xrange(0, 3):
            arr = self.movie.CreateArray()
            stat = BigWorld.player().qinggongMgr._getFlag(self.RideMap[i][1])
            arr.SetElement(0, GfxValue(stat))
            mount.SetElement(i, arr)

        ret.SetElement(1, mount)
        wing = self.movie.CreateArray()
        for i in xrange(0, 6):
            arr = self.movie.CreateArray()
            stat = BigWorld.player().qinggongMgr._getFlag(self.wingMap[i][1])
            arr.SetElement(0, GfxValue(stat))
            wing.SetElement(i, arr)

        ret.SetElement(2, wing)

    def onNotifySlotUse(self, *arg):
        key = arg[3][0].GetString()
        idCon, idx = self.getSlotID(key)
        self.slotUseSkill(idCon, idx)

    def slotUseSkill(self, idCon, idx):
        if idCon == 4:
            p = BigWorld.player()
            if not GSCD.data.has_key(idx):
                gamelog.error('skillProxy: onNotifySlotUse Invalid skill Index: ' + str(idx))
                return
            idItem = GSCD.data.get(idx, {}).get('skillid', 0)
            if idItem == uiConst.HORSE_RIDING:
                if p.tride.inRide() and not BigWorld.player().isOnRideTogetherHorse():
                    self.cancelRideTogether()
                    return
                isInHorse = p.inRiding() and p.bianshen[0] == gametypes.BIANSHEN_RIDING_RB
                if isInHorse:
                    p.leaveRide()
                else:
                    p.enterRide()
            elif idItem == uiConst.WING_FLYING:
                self.enterWingFly()
            elif idItem == uiConst.DAZUOING:
                self.enterDaZuo()
            elif idItem == uiConst.BOOTH:
                self.enterBooth()
            elif idItem == uiConst.RIDE_TOGETHER:
                self.rideTogether()
            elif idItem == uiConst.SHOW_BACK_WEAR:
                p.updateBackWear(True)
                if p.modelServer.backwear.isActionJustSkillWear():
                    p.fashion.stopAllActions()
            elif idItem == uiConst.SHOW_WAIST_WEAR:
                p.updateWaistWear(True)
                if p.modelServer.waistwear.isActionJustSkillWear():
                    p.fashion.stopAllActions()
            elif idItem == uiConst.GEM_ADD_REMOVE:
                if not gameglobal.rds.ui.inventory.mediator:
                    gameglobal.rds.ui.loadWidget(uiConst.WIDGET_INVENTORY)
                if not gameglobal.rds.configData.get('enableEquipChangeGem', False):
                    if not gameglobal.rds.ui.equipGem.mediator:
                        gameglobal.rds.ui.equipGem.show(0)
                else:
                    gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_GEM)
                self.closeGeneralSkill()
            elif idItem == uiConst.EQUIP_LVUP_STAR:
                gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_STAR, 1)
            elif idItem == uiConst.CHUAN_GONG:
                BigWorld.player().useTrainSkill()
            elif idItem == uiConst.FOCUS_SETTING:
                gameglobal.rds.ui.focusTarget.showFocus()
            elif idItem == uiConst.TARGET_SETTING:
                gameglobal.rds.ui.focusTarget.onFocusSelect()
            elif idItem == uiConst.MAKE_EXP_XIUWEI_ITEM:
                gameglobal.rds.ui.bottle.show()
            elif idItem == uiConst.APPLY_SHUANG_XIU:
                BigWorld.player().useShuangxiuSkill()
            elif idItem == uiConst.RENEWAL_ITEM:
                self.setRenewalItem()
            elif idItem == uiConst.YAOPEI_FEED:
                gameglobal.rds.ui.yaoPeiFeed.show()
            elif idItem == uiConst.GENERAL_SKILL_RED_PACKET:
                self.uiAdapter.redPacket.show()
            elif idItem == uiConst.GENERAL_MIX_JEWELRY:
                self.uiAdapter.mixFameJewelry.show()
            elif idItem == uiConst.SWITCH_EQUIP:
                gameglobal.rds.ui.roleInfo.realSwitchEquip()
            elif idItem == uiConst.GO_HOME_ROOM:
                BigWorld.player().useGoHomeRoomSkill()
            elif idItem == uiConst.GO_WING_BORN_ISLAND:
                BigWorld.player().enterToWingBornIslandBySkill(True, GMDD.data.GO_WING_WORLD_BY_SKILL_CONFIRM)
            elif idItem == uiConst.LING_SHI_FLAG_SWITCH:
                BigWorld.player().switchLingShiFlag()
            else:
                gamelog.error('skillProxy: onNotifySlotUse unknown skill id: ' + str(idItem))
            if idItem in uiConst.TUTORIAL_COMMON_SKILL_TRIGGER:
                gameglobal.rds.tutorial.onUseCommonSkillEndCheck(idItem)
        elif idCon == uiConst.SKILL_PANEL_GUILD:
            self.useGuildSkill(idx)
        elif idCon == uiConst.SKILL_PANEL_INTIMACY:
            self.useIntimacySkill(idx)

    def setRenewalItem(self):
        if not gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.show()
        gameglobal.rds.ui.roleInfo.show(uiConst.ROLEINFO_TAB_FASHION)
        if gameglobal.rds.configData.get('enableFashionBagRenew', False):
            gameglobal.rds.ui.fashionBag.show()
        gameglobal.rds.ui.clearState()
        if ui.get_cursor_state() != ui.RENEWAL_STATE2:
            ui.reset_cursor()
            ui.set_cursor_state(ui.RENEWAL_STATE2)
            ui.set_cursor(cursor.repair)
            ui.lock_cursor()
            inv = gameglobal.rds.ui.inventory
            inv.updateCurrentPageSlotState()
            gameglobal.rds.ui.roleInfo.updateSlotState()
            if gameglobal.rds.configData.get('enableFashionBagRenew', False):
                gameglobal.rds.ui.fashionBag.updateCurrentPageSlotState()

    def enterWingFly(self):
        p = BigWorld.player()
        if p.inWingTakeOff:
            return
        if p.inFlyTypeFlyRide():
            return
        if p.inFly:
            if not p.stateMachine.checkCloseWingFly():
                return
            p.leaveWingFly()
        else:
            if not p.stateMachine.checkOpenWingFly():
                return
            if not p.stateMachine.checkStatus(const.CT_OPEN_WINGFLY_CAST):
                return
            p.ap.stopMove()
            p.fashion.stopAllActions()
            p.fashion.stopModelAction(p.modelServer.wingFlyModel.model)
            p.ap.updateVelocity()
            if p.isPathfinding:
                navigator.getNav().stopPathFinding()
            if p.isInCoupleEmote():
                cellCmd.enterWingFly(False)
            else:
                cellCmd.enterWingFly(True)

    def enterFish(self):
        p = BigWorld.player()
        gamelog.debug('enterFish', p.inFishing())
        if p.inFishing():
            p.stopFish()
        else:
            p.startFish()

    def enterDaZuo(self):
        p = BigWorld.player()
        if p.inDaZuo():
            p.cell.leaveDaZuo(True)
        else:
            if not p.stateMachine.checkDaZuo():
                return
            if p.isInPUBG():
                p.showGameMsg(GMDD.data.NO_DAZUO_IN_PUBG, ())
                return
            p.cell.enterDaZuo()

    def enterBooth(self):
        BigWorld.player().checkSetPassword(self.trueEnterBooth)

    def trueEnterBooth(self):
        p = BigWorld.player()
        if p.lv < const.BOOTH_LEVEL:
            p.showGameMsg(GMDD.data.BOOTH_NOT_ALLOWED_LEVEL, (const.BOOTH_LEVEL,))
            return
        if p.boothStat == const.BOOTH_STAT_CLOSE:
            if utils.isAbilityOn() and not p.getAbilityData(gametypes.ABILITY_BOOTH_ON):
                p.showGameMsg(GMDD.data.ABILITY_LACK_MSG, (gameStrings.TEXT_SKILLPROXY_680,))
                return
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_SKILLPROXY_682, Functor(self.showBooth))
        elif p.boothStat == const.BOOTH_STAT_OPEN:
            gameglobal.rds.ui.booth.show()

    def showBooth(self):
        p = BigWorld.player()
        if not p.stateMachine.checkStatus(const.CT_BOOTH):
            return
        if p.inSwim:
            p.showGameMsg(GMDD.data.BOOTH_NOT_ALLOWED_IN_SCENE, ())
            return
        if utils.isAbilityOn() and not p.getAbilityData(gametypes.ABILITY_BOOTH_ON):
            p.showGameMsg(GMDD.data.ABILITY_LACK_MSG, (gameStrings.TEXT_SKILLPROXY_680,))
            return
        p.cell.setUpBooth()

    def rideTogether(self):
        p = BigWorld.player()
        if p.targetLocked is None:
            p.showGameMsg(GMDD.data.NO_COUPLE_EMOTE_TARGET, ())
            return
        elif p.targetLocked.__class__.__name__ != 'Avatar':
            p.showGameMsg(GMDD.data.RIDE_TOGETHER_TARGET, ())
            return
        elif p.isOnRideTogetherHorse():
            p.inviteRideTogether(p.targetLocked.id)
            return
        else:
            if p.targetLocked.tride.inRide():
                p.applyForRideTogether(p.targetLocked.tride.header)
            else:
                p.applyForRideTogether(p.targetLocked.id)
            return

    def cancelRideTogether(self):
        BigWorld.player().cancelRideTogether()

    def useIntimacySkill(self, sid):
        p = BigWorld.player()
        if not p.friend.intimacyTgt:
            p.showGameMsg(GMDD.data.NOT_FIND_INTIMACY_TARGET, ())
            return
        if sid == uiConst.INTIMACY_SKILL_MARRIAGE:
            total, remain = p.getMarriageSkillCd()
            if remain > 0:
                p.showGameMsg(GMDD.data.MARRIAGE_SKILL_IN_CD, ())
                return
            if not p.targetLocked:
                p.showGameMsg(GMDD.data.MARRIAGE_SKILL_NOT_TARGET, ())
                return
            if not p.marriageTgtName:
                p.showGameMsg(GMDD.data.MARRIAGE_SKILL_NOT_MARRIAGE, ())
                return
            if not p._isSoul() and getattr(p.targetLocked, 'roleName', '') != p.marriageTgtName:
                p.showGameMsg(GMDD.data.MARRIAGE_SKILL_NOT_MARRIAGE_TGT, ())
                return
            if p._isSoul():
                targetName = getattr(p.targetLocked, 'roleName', '')
                targetName = targetName[:targetName.rfind('-')]
                if targetName != p.marriageTgtName:
                    p.showGameMsg(GMDD.data.MARRIAGE_SKILL_NOT_MARRIAGE_TGT, ())
                    return
            p.cell.useMarriageSkill(p.targetLocked.id)
            return
        if sid not in p.intimacySkills.keys():
            p.showGameMsg(GMDD.data.INTIMACY_SKILL_NOT_LEARN, ())
            return
        canUse = False
        if p.intimacySkills.has_key(sid):
            remain = p.intimacySkills[sid].nextTime - utils.getNow()
            if remain > 0:
                canUse = False
            else:
                canUse = True
        if sid == uiConst.INTIMACY_SKILL_AXBD:
            if canUse:
                p.cell.useIntimacySkill(sid, ())
            else:
                p.showGameMsg(GMDD.data.INTIMACY_SKILL_TELEPORT_CD, ())
        elif sid == uiConst.INTIMACY_SKILL_SSXS:
            if canUse:
                p.cell.useIntimacySkill(sid, ())
            else:
                p.showGameMsg(GMDD.data.INTIMACY_SKILL_TELEPORT_CD, ())
        elif sid == uiConst.INTIMACY_SKILL_DJTC:
            if canUse:
                p.cell.useIntimacySkill(sid, ())
            else:
                p.showGameMsg(GMDD.data.INTIMACY_SKILL_TELEPORT_CD, ())

    def useGuildSkill(self, sid, params = ()):
        p = BigWorld.player()
        canUse = logicInfo.isUseableGuildMemberSkill(sid)
        if sid == uiConst.GUILD_SKILL_ZHDY:
            if canUse:
                gameglobal.rds.ui.callTeammate.show(sid)
            else:
                p.showGameMsg(GMDD.data.SKILL_NOT_READY, ())
        elif sid in uiConst.GUILD_SIMPLE_PSKILL:
            if canUse:
                if sid == uiConst.GUILD_SKILL_QR or sid == uiConst.GUILD_SKILL_GY:
                    if not p.worldWar.isOpen():
                        p.showGameMsg(GMDD.data.WORLD_WAR_NOT_OPEN, ())
                        return
                    if p.worldWar.isLucky():
                        p.showGameMsg(GMDD.data.WORLD_WAR_ENTER_LUCKY, ())
                        return
                if sid in uiConst.GUILD_SIMPLE_PSKILL_CONFIRM:
                    if len(params) > 0:
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_SKILLPROXY_809 % GPD.data.get((sid, 1), {}).get('name'), Functor(p.cell.useGuildMemberSkillWithParam, sid, params))
                    else:
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_SKILLPROXY_809 % GPD.data.get((sid, 1), {}).get('name'), Functor(p.cell.useGuildMemberSkill, sid))
                elif len(params) > 0:
                    p.cell.useGuildMemberSkillWithParam(sid, params)
                else:
                    p.cell.useGuildMemberSkill(sid)
            elif p.canResetCD(sid):
                msg = GMD.data.get(GMDD.data.CONFIRM_RESET_ENTER_SCENE_CD, {}).get('text', gameStrings.TEXT_SKILLPROXY_819)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.resetGuildSkillCD, sid, ()))
            else:
                p.showGameMsg(GMDD.data.SKILL_NOT_READY, ())
        elif sid == uiConst.GUILD_SKILL_HC:
            if canUse:
                slv = p.guildMemberSkills[sid].level
                destData = GPD.data.get((sid, slv), {}).get('teleportDests', {})
                gameglobal.rds.ui.goHome.show(destData)
            elif p.canResetCD(sid):
                msg = GMD.data.get(GMDD.data.CONFIRM_RESET_TELEPORT_CD, {}).get('text', gameStrings.TEXT_SKILLPROXY_830)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.resetGuildSkillCD, sid, ()))
            else:
                p.showGameMsg(GMDD.data.GUILD_SKILL_TELEPORT_CD, ())

    def __appendSkill(self, skill):
        skillButton = []
        skillInfo = {}
        whichIcon = 1
        isShine = False
        id = skill.get('skillid', 0)
        p = BigWorld.player()
        if id == uiConst.HORSE_RIDING:
            whichIcon = 1 if BigWorld.player().equipment[gametypes.EQU_PART_RIDE] else 2
            isShine = p.inRiding() and p.bianshen[0] == gametypes.BIANSHEN_RIDING_RB
        elif id == uiConst.WING_FLYING:
            whichIcon = 1 if BigWorld.player().equipment[gametypes.EQU_PART_WINGFLY] else 2
            isShine = p.inFlyTypeWing()
        elif id == uiConst.DAZUOING:
            whichIcon = 1
            isShine = p.inDaZuo()
        elif id == uiConst.BOOTH:
            whichIcon = 1
            isShine = p.inBoothing()
        elif id == uiConst.RIDE_TOGETHER:
            condition = p.tride.inRide()
            condition &= not p.isOnRideTogetherHorse()
            whichIcon = 2 if condition else 1
            isShine = p.tride.inRide() or p.isOnRideTogetherHorse()
        else:
            whichIcon = 1
            isShine = False
        icon = 'icon%d' % whichIcon
        skillInfo['iconPath'] = 'generalSkill/%s.dds' % skill.get(icon, '0')
        skillInfo['skillName'] = skill.get('name', '')
        skillInfo['openFlag'] = False if skill.get('levelLimit', 0) > p.lv else True
        skillButton.append(skillInfo)
        skillButton.append(isShine)
        total, passTime = self.getCooldown(skill)
        skillButton.append(total * 1000)
        skillButton.append(passTime * 1000)
        return skillButton

    def getCooldown(self, skill):
        total = 0
        passTime = 0
        id = skill.get('skillid', 0)
        if id == uiConst.GO_HOME_ROOM:
            total, passTime = uiUtils.getBackHomeCoolDown()
            if passTime > total:
                passTime = -1
            if uiUtils.noNeedBackHomeCoolDown():
                passTime = -1
        return (total, passTime)

    def onGetOtherSkill(self, *arg):
        ret = {}
        active = []
        data = GSCD.data
        i = 1
        for k in data:
            skill = data[k]
            skillId = skill.get('skillid', 0)
            if skill.get('hide', 0):
                continue
            if skillId == uiConst.MAKE_EXP_XIUWEI_ITEM:
                if not gameglobal.rds.configData.get('enableExpXiuWeiPool', False):
                    continue
            if skillId == uiConst.APPLY_SHUANG_XIU:
                if not gameglobal.rds.configData.get('enableShuangxiu', False):
                    continue
            if skillId == uiConst.YAOPEI_FEED:
                if not gameglobal.rds.configData.get('enableYaoPei', False):
                    continue
            if skillId == uiConst.SWITCH_EQUIP:
                if not gameglobal.rds.configData.get('enableSubEquipment', False):
                    continue
                achieveId = SCD.data.get('OPEN_SUB_EQUIP_ACHIEVE_ID', 0)
                if achieveId and not gameglobal.rds.ui.achvment.checkAchieveFlag(achieveId):
                    continue
            if skillId == uiConst.GENERAL_SKILL_RED_PACKET:
                if not self.uiAdapter.redPacket.enableRedPacket():
                    continue
            if skillId == uiConst.GO_HOME_ROOM:
                if not gameglobal.rds.configData.get('enableHome', False):
                    continue
            if skillId == uiConst.GO_WING_BORN_ISLAND:
                if not gameglobal.rds.configData.get('enableWingWorld', False):
                    continue
            if skillId == uiConst.LING_SHI_FLAG_SWITCH and (not gameconfigCommon.enableLingShi() or SCD.data.get('lingshiLv', 69) > BigWorld.player().lv):
                continue
            skillButton = self.__appendSkill(skill)
            skillButton[0]['pos'] = k
            active.append(skillButton)
            self.otherSkillData[i] = skill
            i += 1

        ret['active'] = active
        return uiUtils.dict2GfxDict(ret, True)

    def onGetGuildSkill(self, *arg):
        p = BigWorld.player()
        sortData = []
        skill = {}
        for value in GPD.data.itervalues():
            sid = value.get('skillId', 0)
            if sid not in skill:
                sortData.append([sid, value.get('sortId', 0)])
                skill[sid] = True

        sortData.sort(key=lambda x: x[1])
        activeSkill = []
        passiveSkill = []
        for sid, _ in sortData:
            level = 0
            if p.guildMemberSkills.has_key(sid):
                level = p.guildMemberSkills[sid].level
            if level <= 0:
                continue
            skillInfo = {}
            isShine = False
            skillInfo['sid'] = sid
            skillInfo['level'] = level
            if GPD.data.get((sid, 1), {}).get('type', 1) == gametypes.GUILD_PSKILL_TYPE_ACTIVE:
                skillInfo['iconPath'] = 'skill/icon/%d.dds' % SKCD.data.get((sid, 1), {}).get('icon', 0)
            else:
                skillInfo['iconPath'] = 'skill/icon/%d.dds' % PSTD.data.get(sid, {}).get('icon', 0)
            if sid in logicInfo.cooldownGuildMemberSkill:
                end, total = logicInfo.cooldownGuildMemberSkill[sid]
                remain = end - BigWorld.time()
            elif sid in logicInfo.cooldownWWArmySkill:
                end, total = logicInfo.cooldownWWArmySkill[sid]
                remain = end - BigWorld.time()
            elif sid in logicInfo.cooldownClanWarSkill:
                end, total = logicInfo.cooldownClanWarSkill[sid]
                remain = end - BigWorld.time()
            else:
                total = remain = 0
            if remain > 0:
                playCooldown = True
                self.callbackHandler[sid] = BigWorld.callback(remain, Functor(self.afterGuildSkillEndCooldown, sid))
            else:
                playCooldown = False
            if GPD.data.get((sid, 1), {}).get('displayType', 1) == gametypes.GUILD_PSKILL_TYPE_ACTIVE:
                activeSkill.append([skillInfo,
                 isShine,
                 playCooldown,
                 total * 1000,
                 (total - remain) * 1000])
            else:
                passiveSkill.append([skillInfo,
                 isShine,
                 playCooldown,
                 total * 1000,
                 (total - remain) * 1000])

        ret = {}
        ret['activeSkill'] = activeSkill
        ret['passiveSkill'] = passiveSkill
        return uiUtils.dict2GfxDict(ret, True)

    def onGetIntimacySkill(self, *arg):
        if not gameglobal.rds.configData.get('enableIntimacySkill', False):
            return
        p = BigWorld.player()
        intimacySkill = []
        currentLevel = 1
        for key, value in ISD.data.items():
            skillInfo = {}
            sid = key[0]
            level = key[1]
            isShine = False
            playCooldown = True
            currentLevel = self.getIntimacyCurrentLevel(sid)
            if key == (sid, currentLevel):
                if not gameglobal.rds.configData.get('enableMarriageSkill', False) and sid in (uiConst.INTIMACY_SKILL_MARRIAGE,):
                    continue
                if not gameglobal.rds.configData.get('enableIntimacySkillSSXS', True) and sid == uiConst.INTIMACY_SKILL_SSXS:
                    continue
                if sid == uiConst.INTIMACY_SKILL_ZHSF:
                    continue
                skillInfo['sid'] = sid
                skillInfo['sortId'] = value.get('sortId', 0)
                skillInfo['iconPath'] = 'skill/icon64/%d.dds' % value.get('icon', 0)
                skillInfo['tips'] = value.get('tips', '')
                skillInfo['level'] = level
                skillInfo['name'] = value.get('name', 0)
                skillInfo['gary'] = True
                skillInfo['cooldownList'] = [isShine,
                 playCooldown,
                 0,
                 0]

                def _processSkillInfo(total, remain):
                    if remain > 0:
                        playCooldown = True
                        self.callbackHandler[sid] = BigWorld.callback(remain, Functor(self.afterIntimacySkillEndCooldown, sid))
                    else:
                        playCooldown = False
                    skillInfo['cooldownList'] = [isShine,
                     playCooldown,
                     total * 1000,
                     (total - remain) * 1000]
                    skillInfo['gary'] = False

                if sid in (uiConst.INTIMACY_SKILL_MARRIAGE,):
                    total, remain = p.getMarriageSkillCd()
                    _processSkillInfo(total, remain)
                    skillInfo['gary'] = bool(not p.marriageTgtName)
                elif p.intimacySkills.has_key(sid):
                    remain = p.intimacySkills[sid].nextTime - utils.getNow()
                    total = value.get('intimacySkillCD', 0)
                    _processSkillInfo(total, remain)
                intimacySkill.append(skillInfo)

        intimacySkill = sorted(intimacySkill, key=lambda skillInfo: skillInfo['sortId'])
        return uiUtils.array2GfxAarry(intimacySkill, True)

    def afterGuildSkillEndCooldown(self, sid):
        if self.generalMediator:
            self.generalMediator.Invoke('afterGuildSkillEndCooldown', GfxValue(sid))
        logicInfo.cooldownGuildMemberSkill.pop(sid, None)

    def afterIntimacySkillEndCooldown(self, sid):
        if self.generalMediator:
            self.generalMediator.Invoke('afterIntimacySkillEndCooldown', GfxValue(sid))

    def onGetFishingSkillInfo(self, *arg):
        ret = self._genFishingSkillInfo()
        return uiUtils.array2GfxAarry(ret, True)

    def onGetExploreSkillInfo(self, *arg):
        ret = self._genExploreskillInfo()
        return uiUtils.dict2GfxDict(ret, True)

    def onUnEquipFishingItem(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        if slot == 0:
            return
        p = BigWorld.player()
        page, pos = p.inv.searchEmptyInPages()
        if pos != const.CONT_NO_POS:
            if not p.stateMachine.checkStatus(const.CT_TAKE_OFF_FISHING_EQUIP):
                return
            p.cell.exchangeInvFishingEqu(page, pos, slot - 1)
        else:
            p.showGameMsg(GMDD.data.SHOP_BAG_FULL, ())

    def onUnEquipCompassItem(self, *arg):
        p = BigWorld.player()
        page, pos = p.inv.searchEmptyInPages()
        if pos != const.CONT_NO_POS:
            p.cell.exchangeInvExploreEqu(page, pos, gametypes.EXPLORE_EQUIP_COMPASS)
        else:
            p.showGameMsg(GMDD.data.SHOP_BAG_FULL, ())

    def onShowIllustration(self, *arg):
        gameglobal.rds.ui.fishing.showFishingIllustration()

    def onAddXiuWei(self, *arg):
        idx = int(arg[3][0].GetNumber())
        self.curType = idx
        self.enhanceType = uiConst.TYPE_XIUWEI_BAR
        if self.enhanceMediator:
            self.closeEnhancePanel()
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SKILL_BAR_ENHANCE)
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SKILL_BAR_ENHANCE)

    def onAddWuShuang(self, *arg):
        idx = int(arg[3][0].GetNumber())
        self.curType = idx
        self.enhanceType = uiConst.TYPE_WUSHUANG_BAR
        if self.enhanceMediator:
            self.closeEnhancePanel()
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SKILL_BAR_ENHANCE)
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SKILL_BAR_ENHANCE)

    def onGetDetailInfo(self, *arg):
        if self.skillId in BigWorld.player().airSkills:
            ret = self.genAirSkillDetaiInfo()
        else:
            ret = self._genDetailInfo()
        return uiUtils.dict2GfxDict(ret, True)

    def onLvUp(self, *arg):
        msg = self.onGetLvUpConfirmInfo()
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.onConfirmLvUp)

    def onRebalanceDaoHang(self, *arg):
        self.uiAdapter.fengyinShow.show(BigWorld.player().mapID)

    def onResetDaoHang(self, *arg):
        if self.skillId:
            if self.checkUseRebalance():
                msg = uiUtils.getTextFromGMD(GMDD.data.RESET_REBALANCE_WS_DAOHANG, '')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(BigWorld.player().cell.resetRebalanceWudao, self.skillId))
                return
            msg = uiUtils.getTextFromGMD(GMDD.data.RESET_WS_DAOHANG, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._relieveDaoHang, 0))

    def onOpenItemSelect(self, *arg):
        p = BigWorld.player()
        sVal = p.wsSkills.get(self.skillId, None)
        if not sVal:
            return
        else:
            slotNum = len(sVal.slots) if sVal.slots else 0
            daoHengInfo = WDD.data.get((self.skillId, slotNum + 1), {})
            daoHengItems = daoHengInfo.get('daoHengItems', {})
            itemList = []
            for key in daoHengItems:
                curPoint = int(sVal.daoHeng.get('item%s' % key[0], 0))
                itemInfo = (key[0],
                 gameStrings.TEXT_SKILLPROXY_1168 + str(key[1]) + gameStrings.TEXT_SKILLPROXY_1168_1,
                 1,
                 '(%s/%s)' % (curPoint, key[2]))
                itemList.append(itemInfo)

            tips = []
            tipsDescription = daoHengInfo.get('addDhDescription', [])
            tipsData = daoHengInfo.get('addDh', [])
            for i in range(len(tipsDescription)):
                t = {}
                t['description'] = tipsDescription[i]
                t['value'] = getattr(sVal, 'daoHeng', {}).get('%s%s' % (tipsData[i][0], tipsData[i][-1]), 0)
                t['maxValue'] = tipsData[i][3]
                tips.append('%s (%s/%s)' % (t['description'], t['value'], t['maxValue']))

            gameglobal.rds.ui.itemSelect.show(itemList, gameStrings.TEXT_SKILLPROXY_1181, None, Functor(self.onConfirmSelectItem), isModal=False, tips=tips)
            return

    def onConfirmSelectItem(self, itemInfo):
        BigWorld.player().cell.addDaoHengByItem(self.skillId, itemInfo[0])

    def onWuDao(self, *arg):
        self.closeEnhancePanel()
        skType = int(arg[3][0].GetString())
        skIdx = int(arg[3][1].GetString())
        skillId = self.specialSkills[skType][skIdx]
        self.openWuDaoPanel(skillId)

    def onPanelWuDao(self, *arg):
        equipFirst = int(arg[3][0].GetString())
        equipSecond = int(arg[3][1].GetString())
        skillId = self.equipSkills[equipFirst][equipSecond]
        if skillId != 0:
            self.closeEnhancePanel()
            self.openWuDaoPanel(skillId)

    def openWuDaoPanel(self, skillId):
        self.skillId = skillId
        p = BigWorld.player()
        skInfoVal = p.wsSkills.get(self.skillId, None)
        lv = skInfoVal.level if skInfoVal else 1
        if utils.isJingJieOn() and SGD.data.has_key((self.skillId, lv)) and SGD.data[self.skillId, lv].has_key('needJingJie') and p.jingJie < SGD.data[self.skillId, lv]['needJingJie']:
            p.showGameMsg(GMDD.data.JING_JIE_LIMIT, ())
            return
        else:
            if self.daoHangDirMediator:
                self.closeDaohangDirPanel()
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DAOHANG_DIRECTION_V2)
            return

    def onSkillWuDao(self, *arg):
        self.closeEnhancePanel()
        self.skillId = int(arg[3][0].GetString())
        if self.daoHangDirMediator:
            self.closeDaohangDirPanel()
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DAOHANG_DIRECTION_V2)

    def onOpenDetailpanel(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        if bar == uiConst.SKILL_PANEL_AIR_DETAIL:
            skillId = slot
        else:
            skType = slot / MAX_SPECIAL_SKILL_NUMS
            idx = slot % MAX_SPECIAL_SKILL_NUMS
            if idx >= len(self.specialSkills[skType]):
                return
            skillId = self.specialSkills[skType][idx]
        self.openDetailpanel(skillId)

    def onOpenDuanZhangPanel(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        if bar == uiConst.SKILL_PANEL_AIR_DETAIL:
            skillId = slot
        else:
            skType = slot / MAX_SPECIAL_SKILL_NUMS
            idx = slot % MAX_SPECIAL_SKILL_NUMS
            if idx >= len(self.specialSkills[skType]):
                return
            skillId = self.specialSkills[skType][idx]
        sgdData = SGD.data.get((skillId, SKILL_MIN_LV), ())
        openItem = sgdData.get('openItem', ())
        itemNum = sgdData.get('itemNum', ())
        itemList = []
        yesBtnEnable = True
        for i, itemId in enumerate(openItem):
            if i >= len(itemNum):
                continue
            itemData = uiUtils.getGfxItemById(itemId)
            ownNum = BigWorld.player().inv.countItemInPages(itemId, enableParentCheck=True)
            itemData['count'] = '%d/%d' % (ownNum, itemNum[i])
            itemList.append(itemData)
            if ownNum < itemNum[i]:
                yesBtnEnable = False

        msg = SCFD.data.get('duanZhangUseDesc', '')
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.useDuanZhang, skillId), itemData=itemList, yesBtnEnable=yesBtnEnable)

    def useDuanZhang(self, skillId):
        p = BigWorld.player()
        p.cell.learnWsSkillUseMaterial(skillId)

    def onCloseDetailPanel(self, *arg):
        closeOther = False
        if len(arg[3]) > 0 and arg[3][0] is not None:
            closeOther = arg[3][0].GetBool()
        self.closeDetailpanel()
        if closeOther:
            self.closeEnhancePanel()
            self.closeDaohangDirPanel()
            self.closeSkillPractice()

    def onGetEnhanceType(self, *arg):
        return GfxValue(self.enhanceType)

    def onGetWuShuangBarInfo(self, *arg):
        ret = self._genWuShuangBarInfo()
        return uiUtils.dict2GfxDict(ret)

    def onGetXiuWeiBarInfo(self, *arg):
        ret = self._genXiuWeiBarInfo()
        return uiUtils.dict2GfxDict(ret)

    def onGetRelieveInfo(self, *arg):
        ret = self._genRelieveInfo()
        return uiUtils.dict2GfxDict(ret)

    def onCloseEnhancePanel(self, *arg):
        self.closeEnhancePanel()

    def onConfirmEnhance(self, *arg):
        params = arg[3][0].GetString().split(',')
        p = BigWorld.player()
        wsVal = p.wushuang1 if self.curType == 0 else p.wushuang2
        wsData = WED.data.get(wsVal.mwsEnhanceCnt + 1, {})
        items = []
        if self.enhanceType == uiConst.TYPE_WUSHUANG_BAR:
            for idx, param in enumerate(params):
                if int(param):
                    items.append(wsData.get('mwsEnhanceItems', [(0, 0, 0)] * 3)[idx][0])

            p.cell.enhanceMws(self.curType + 1, items)
        elif self.enhanceType == uiConst.TYPE_XIUWEI_BAR:
            for idx, param in enumerate(params):
                if int(param):
                    items.append(wsData.get('xiuweiEnhanceItems', [(0, 0, 0)] * 3)[idx][0])

            p.cell.enhanceXiuwei(self.curType + 1, items)
            if self.mediator != None:
                self.mediator.Invoke('setUsePotentialEffect', GfxValue(self.curType))
        self.closeEnhancePanel()

    def onRelieveDaoHang(self, *arg):
        useItem = arg[3][0].GetBool()
        starVal = self._getWsSkillStar(self.skillId)
        itemId = self.resetItemIds[starVal - 1] if useItem else 0
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_SKILLPROXY_1333, yesCallback=lambda : self._relieveDaoHang(itemId))

    def onConvertLingLi(self, *args):
        if gameglobal.rds.configData.get('enableWSSchemes', False):
            msg = uiUtils.getTextFromGMD(GMDD.data.CONVERT_LING_LI_TO_ITEM_HINT, '')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConvertLingLi, isModal=False)
        else:
            self.trueConvertLingLi()

    def OnTianZhaoSkillSet(self, *args):
        gamelog.info('jbx:OnTianZhaoSkillSet')
        self.uiAdapter.tianZhaoSummonedSpriteSkillSet.show()

    def trueConvertLingLi(self):
        if not self.skillId or not self.daoHangDirMediator:
            return
        costItem = WSCD.data.get(self.skillId, {}).get('convertLingliItem')
        if not costItem:
            return
        costItemId, costItemNum = costItem
        cnt = BigWorld.player().inv.countItemInPages(costItemId, enableParentCheck=True)
        itemData = uiUtils.getGfxItemById(costItemId, uiUtils.convertNumStr(cnt, costItemNum))
        if cnt >= costItemNum:
            itemData['state'] = uiConst.ITEM_NORMAL
        else:
            itemData['state'] = uiConst.COMPLETE_ITEM_LEAKED
        msg = uiUtils.getTextFromGMD(GMDD.data.CONVERT_LING_LI_TO_ITEM_MSG, '%s') % uiUtils.getItemColorName(costItemId)
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.convertLingLiToItem, itemData=itemData, isModal=False)

    def convertLingLiToItem(self):
        if self.skillId:
            BigWorld.player().cell.convertLingliToItem(self.skillId)

    def onGetLvUpConfirmInfo(self, *arg):
        levelAdd = 1
        needMoney = 0
        p = BigWorld.player()
        if p.wsSkills.has_key(self.skillId):
            content = gameStrings.TEXT_SKILLPROXY_1374 % (levelAdd,)
            gameStrings.TEXT_SKILLPROXY_1375
            needMoney = 0
        elif p.airSkills.has_key(self.skillId):
            content = gameStrings.TEXT_SKILLPROXY_1374 % (levelAdd,)
            info = self.genAirSkillContentById(self.skillId)
            needMoney = info.get('extra', {}).get('money', 0)
        else:
            content = ''
            needMoney = 0
        content += gameStrings.TEXT_SKILLPROXY_1385
        if needMoney > p.cash + p.bindCash:
            content += "<font color = \'#FF4B4B\'>%d</font>" % needMoney
            enabled = False
        else:
            content += str(needMoney)
            enabled = True
        content += '</font>'
        return content
        ret = {'content': content,
         'enabled': enabled,
         'skillId': self.skillId}
        return uiUtils.dict2GfxDict(ret, True)

    def onConfirmLvUp(self):
        p = BigWorld.player()
        info = self.genAirSkillContentById(self.skillId)
        needMoney = info.get('extra', {}).get('money', 0)
        if p.bindCash < needMoney and p.cash + p.bindCash >= needMoney:
            msg = GMD.data.get(GMDD.data.ENHANCE_SKILL_CONSUME_COIN_NOTIFY, {}).get('text', gameStrings.TEXT_SKILLPROXY_1402)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.onRealConfirmLvUp, msgType='bindCash', isShowCheckBox=True)
        else:
            self.onRealConfirmLvUp()

    def onRealConfirmLvUp(self):
        p = BigWorld.player()
        if p.airSkills.has_key(self.skillId):
            p.cell.airSkillLvUp(self.skillId)
        else:
            p.cell.upgradeWsSkill(self.skillId)

    def onGetDaoHangDirectionInfo(self, *arg):
        ret = self._genDirectionInfo(self.skillId)
        return uiUtils.dict2GfxDict(ret, True)

    def onRealize(self, *arg):
        if not BigWorld.player().stateMachine.checkStatus(const.CT_WUSHUANG_CHANGE_GEM):
            return False
        else:
            p = BigWorld.player()
            sVal = p.wsSkills.get(self.skillId, None)
            if not sVal:
                return
            gemType = int(arg[3][0].GetNumber())
            _, windCnt, forestCnt, fireCnt, hillCnt = self.getGemsInfo(self.skillId)
            gemNumMap = {gametypes.WUSHUANG_GEM_TYPE_FIRE: fireCnt,
             gametypes.WUSHUANG_GEM_TYPE_MOUNTAIN: hillCnt,
             gametypes.WUSHUANG_GEM_TYPE_WIND: windCnt,
             gametypes.WUSHUANG_GEM_TYPE_WOOD: forestCnt}
            wsData = WSCD.data.get(self.skillId, {})
            curNum = gemNumMap.get(gemType, 0)
            if curNum < WU_DAO_MAX_STAR:
                cost = wsData.get('wudaoLingliCost', [])
                itemId, num = cost[curNum]
                itemName = ID.data.get(itemId, {}).get('name', '')
                curLingliNum = sVal.lingli.get(itemId, 0)
                if self.checkUseRebalance():
                    p.cell.doRebalanceWudao(self.skillId, gemType)
                elif num <= curLingliNum:
                    p.cell.doWudao(self.skillId, gemType)
                else:
                    addLingliItems = wsData.get('addLingliItem', ())
                    lVal = 0
                    for pid, val in addLingliItems:
                        if Item.parentId(itemId) == pid:
                            lVal = val
                            break

                    lingLiName = SCD.data.get('lingLiNames', {}).get(itemId, itemName)
                    msg = uiUtils.getTextFromGMD(GMDD.data.USE_LINGLI_ITEM_ALERT, '%s%s%s%s') % (num,
                     lingLiName,
                     itemName,
                     lVal)
                    needNum = math.ceil((num - curLingliNum) / lVal) if lVal > 0 else 0
                    self.wudaoGemType = gemType
                    self.uiAdapter.itemUse.show(itemId, msg, needNum, self.onUseLingLiItem)
            return

    def onUseLingLiItem(self, itemId, num):
        BigWorld.player().cell.addWsLingliByItem(self.skillId, itemId, num, self.wudaoGemType)

    def onCloseDaoHangPanel(self, *arg):
        self.closeDaohangDirPanel()

    def onGetDirectionDesc(self, *arg):
        type = int(arg[3][0].GetNumber())
        return uiUtils.array2GfxAarry(self.getDirectionDesc(type), True)

    def getDirectionDesc(self, type):
        wsData = WSCD.data.get(self.skillId, {})
        if type == gametypes.WUSHUANG_GEM_TYPE_WIND:
            descs = wsData.get('windPSkill', [])
        elif type == gametypes.WUSHUANG_GEM_TYPE_WOOD:
            descs = wsData.get('woodPSkill', [])
        elif type == gametypes.WUSHUANG_GEM_TYPE_FIRE:
            descs = wsData.get('firePSkill', [])
        elif type == gametypes.WUSHUANG_GEM_TYPE_MOUNTAIN:
            descs = wsData.get('mountainPSkill', [])
        else:
            descs = []
        ret = []
        for item in descs:
            skillId = PD.data.get(item, {}).get('skillId')
            pskillVal = BigWorld.player().pskills.get(item[0], {}).get(skillId, None)
            pData = pskillVal.pData if pskillVal else {}
            desc = gameglobal.rds.ui.runeView.generateDesc(item[0], PSkillInfo(item[0], item[1], pData), item[1])
            ret.append(desc)

        return ret

    def onConvertPotential(self, *arg):
        idx = int(arg[3][0].GetString())
        BigWorld.player().cell.convertPotential(idx + 1)

    def onGetDaohangIconTips(self, type):
        if type == 0:
            ret = gameStrings.TEXT_SKILLPROXY_1499
        elif type == 1:
            ret = gameStrings.TEXT_SKILLPROXY_1501
        elif type == 2:
            ret = gameStrings.TEXT_SKILLPROXY_1503
        elif type == 3:
            ret = gameStrings.TEXT_SKILLPROXY_1505
        elif type == 4:
            ret = gameStrings.TEXT_SKILLPROXY_1507
        elif type == 5:
            ret = gameStrings.TEXT_SKILLPROXY_1509
        return GfxValue(gbk2unicode(ret))

    def onGetBonusTips(self, *arg):
        type = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        sVal = p.wsSkills.get(self.skillId, None)
        ret = ''
        if type == 0:
            if sVal:
                if sVal.level == 1:
                    ret = gameStrings.TEXT_SKILLPROXY_1521
                elif sVal.level == 2:
                    ret = gameStrings.TEXT_SKILLPROXY_1523
        elif type == 1:
            if sVal:
                if sVal.level == 1:
                    ret = gameStrings.TEXT_SKILLPROXY_1527
                elif sVal.level == 2:
                    ret = gameStrings.TEXT_SKILLPROXY_1529
        return GfxValue(gbk2unicode(ret))

    def onGetTabIdx(self, *arg):
        return GfxValue(self.tabIdx)

    def onResetSkills(self, *arg):
        p = BigWorld.player()
        if p.skillPoint == 0:
            p.showGameMsg(GMDD.data.RESET_SKILL_POINT_SCHEME_NEEDLESS, ())
            return
        if p.isUsingTemp():
            self.ResetSkillPoint()
            return
        needItemLv = SCD.data.get('RESET_SP_NEED_ITEM_LV', 58)
        if p.lv > needItemLv:
            page, pos = p.inv.findPassiveUseItemByAttr(self, {'cstype': Item.SUBTYPE_2_RESET_SKILLPOINT}, skipLatchItem=True, lv=p.lv)
            itemFameData = {}
            msg = GMD.data.get(GMDD.data.RESET_SKILL_NOTIFY, {}).get('text', '')
            if (page == const.CONT_NO_PAGE or pos == const.CONT_NO_POS) and gameglobal.rds.configData.get('enableCoinDikou', False):
                if p.lv >= 69:
                    itemId = SCD.data.get('resetSkillPointSchemeItemCoinDikou', ())[1]
                else:
                    itemId = SCD.data.get('resetSkillPointSchemeItemCoinDikou', ())[0]
                itemFameData['itemId'] = itemId
                itemFameData['deltaNum'] = 1
                itemFameData['type'] = 'tianbi'
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.useTianbiResetSkillPoint, itemFameData=itemFameData)
            else:
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.ResetSkillPoint)
        else:
            msg = GMD.data.get(GMDD.data.RESET_SKILL_NO_ITEM_NOTIFY, {}).get('text', gameStrings.TEXT_SKILLPROXY_1563)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.ResetSkillPoint)

    @ui.checkInventoryLock()
    def useTianbiResetSkillPoint(self):
        p = BigWorld.player()
        p.cell.resetSkillPointScheme(True, p.cipherOfPerson)

    def onCanChangeTemplate(self, *args):
        p = BigWorld.player()
        return GfxValue(p.canChangeTemplate())

    def ResetSkillPoint(self):
        BigWorld.player().cell.resetSkillPointScheme(False, ' ')

    def onSaveSkills(self, *arg):
        self.skillInfoManager.saveSkillSchedule()

    def _genFishingSkillInfo(self):
        p = BigWorld.player()
        ret = []
        fData = FLD.data.get(p.fishingLv)
        ret.append(fData['name'] + '(' + str(p.fishingLv) + gameStrings.TEXT_SKILLPROXY_1585)
        if p.fishingLv == 10:
            ret.append(gameStrings.TEXT_SKILLPROXY_1587)
        else:
            ret.append(str(p.fishingExp) + '/' + str(fData['exp']))
        ret.append(gameStrings.TEXT_SKILLPROXY_1590)
        slots = []
        icon = SCFD.data.get('lifeSkillIcons', {}).get(uiConst.LIFE_SKILL_FISHING, 9010)
        slots.append([{'iconPath': 'lifeskill/icon64/%s.dds' % icon}, 'nothing'])
        props = [0,
         0,
         0,
         0]
        for item in p.fishingEquip[0:3]:
            if item:
                iconPath = uiUtils.getItemIconFile40(item.id)
                if hasattr(item, 'quality'):
                    quality = item.quality
                else:
                    quality = ID.data.get(item.id, {}).get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                if item.getMaxRange():
                    props[0] += item.getMaxRange()
                if item.getControllability():
                    props[1] += item.getControllability()
                if item.getHookAbility():
                    props[2] += item.getHookAbility()
                if item.getSensitivity():
                    props[3] += item.getSensitivity()
            else:
                iconPath = 'notFound'
                color = 'nothing'
            slots.append([{'iconPath': iconPath}, color])

        ret.append(slots)
        ret.append(props)
        return ret

    def _genExploreskillInfo(self):
        p = BigWorld.player()
        ret = {}
        slots = []
        icon = SCFD.data.get('lifeSkillIcons', {}).get(uiConst.LIFE_SKILL_EXPLORE, 9020)
        slots.append([{'iconPath': 'lifeskill/icon64/%s.dds' % str(icon)}, 'nothing'])
        item = p.exploreEquip.get(gametypes.EXPLORE_EQUIP_COMPASS)
        if item:
            iconPath = uiUtils.getItemIconFile40(item.id)
            if hasattr(item, 'quality'):
                quality = item.quality
            else:
                quality = ID.data.get(item.id, {}).get('quality', 1)
            color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            equiData = SLSED.data.get(item.id, {})
            ret['pointer'] = equiData.get('pointer', 0)
            ret['senseDist'] = equiData.get('senseDist', 0)
            ret['sensePower'] = equiData.get('sensePower', 0)
        else:
            iconPath = 'notFound'
            color = 'nothing'
            ret['pointer'] = 0
            ret['senseDist'] = 0
            ret['sensePower'] = 0
        slots.append([{'iconPath': iconPath}, color])
        ret['items'] = slots
        eData = ELD.data.get(p.exploreLv, {})
        ret['exploreLv'] = eData.get('name', '') + gameStrings.TEXT_SKILLPROXY_1647 % p.exploreLv
        ret['xiangyaoExp'] = str(p.xiangyaoExp) + '/' + str(eData.get('maxXiangyaoExp', '--'))
        ret['xunbaoExp'] = str(p.xunbaoExp) + '/' + str(eData.get('maxXunbaoExp', '--'))
        ret['zhuizongExp'] = str(p.zhuizongExp) + '/' + str(eData.get('maxZhuizongExp', '--'))
        if p.exploreLv == 10:
            ret['allExp'] = gameStrings.TEXT_SKILLPROXY_1587
        else:
            ret['allExp'] = str(p.xiangyaoExp + p.xunbaoExp + p.zhuizongExp) + '/' + str(eData.get('exp', '--'))
        return ret

    def updateSlotBinding(self, key, data):
        slotKey = self.binding.get(key, None)
        if slotKey is not None:
            slotKey[1].InvokeSelf(data)

    def delSlotItem(self, key, slot = -1):
        idBar, idItem = self.getSlotID(key)
        data = GfxValue(1)
        data.SetNull()
        self.updateSlotBinding(key, data)
        if idBar not in (uiConst.SKILL_PANEL_LIFE, uiConst.SKILL_PANEL_EXPLORE):
            if slot == -1:
                skType = idItem / MAX_EQUIP_SKILL_NUMS
                idItem = idItem % MAX_EQUIP_SKILL_NUMS
                self.equipSkills[skType][idItem] = 0
            else:
                type = 0 if slot <= 14 else 1
                idItem = idItem % MAX_EQUIP_SKILL_NUMS
                self.equipSkills[type][idItem] = 0
            self.refreshSpecialSkillWithoutIcon()
        elif self.binding.get(key, None) is not None:
            if idBar == uiConst.SKILL_PANEL_LIFE:
                self.fishItems[idItem] = None
                self.setFishingSlotColor(idItem, 'nothing')

    def getSlotID(self, key):
        idCon, idItem = key.split('.')
        return (int(idCon[6:]), int(idItem))

    def show(self, tabIdx = 0, isGotoXiuLian = False):
        if not BigWorld.player().checkMapLimitUI(gametypes.MAP_LIMIT_UI_SKILL):
            return
        if BigWorld.player()._isSchoolSwitch():
            BigWorld.player().showGameMsg(GMDD.data.FORBIDEN_SKILL_IN_SCHOOL_SWITCH, ())
            return
        if tabIdx == 0:
            self.isGotoXiuLian = isGotoXiuLian
        if not self.mediator:
            self.tabIdx = tabIdx
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SKILL_BG)
            self.isShow = True
        else:
            self._initWsSkillList()
            self.mediator.Invoke('setTabIndex', GfxValue(tabIdx))

    def refreshWsPanel(self):
        if self.mediator:
            self._initWsSkillList()
            self.mediator.Invoke('refreshWsPanel')

    def showPanelForTuturial(self, tab, type, skillId):
        self.show(tab)
        if type == 0:
            return
        if type == 1:
            self.openWuDaoPanel(skillId)
        elif type == 2:
            self.openDetailpanel(skillId)

    def showLifeSkill(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_LIFE_SKILL_PANEL)

    def closeLifeSkill(self):
        self.lifeMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_LIFE_SKILL_PANEL)

    def showGeneralSkill(self, generalTab = 0):
        if not BigWorld.player().checkMapLimitUI(gametypes.MAP_LIMIT_UI_GENERAL_SKILL):
            return
        self.generalTab = generalTab
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GENERAL_SKILL)

    def closeGeneralSkill(self):
        if gameglobal.rds.configData.get('enableNewCamera', False) and gameglobal.rds.ui.cameraV2.widget:
            gameglobal.rds.ui.cameraV2.widget.bg.content.playBtn.visible = False
            gameglobal.rds.ui.cameraV2.widget.bg.content.stopBtn.visible = False
            BigWorld.setParticleFrameRateMagnitude(1, 0)
            BigWorld.setActionFrameRateMagnitude(1, 0)
        self.generalMediator = None
        self.generalTab = 0
        for handler in self.callbackHandler.values():
            BigWorld.cancelCallback(handler)

        self.callbackHandler = {}
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GENERAL_SKILL)
        gameglobal.rds.ui.emote.resetHeadGen()

    def closeSkillPractice(self):
        self.practiceMediator = None

    def hide(self, destroy = True):
        self.clearWidget()
        if destroy:
            self.reset()

    def clearWidget(self):
        if gameglobal.rds.ui.inDrag:
            BigWorld.player().showTopMsg(gameStrings.TEXT_SKILLPROXY_1776)
            BigWorld.player().chatToEventEx(gameStrings.TEXT_SKILLPROXY_1776, const.CHANNEL_COLOR_RED)
            return
        else:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SKILL_BG)
            self.isShow = False
            self.mediator = None
            self.commonSkillMc = None
            self.airSkillPanelMc = None
            self.wushuangSkillPanelMc = None
            self.closeDetailpanel()
            self.closeEnhancePanel()
            self.closeDaohangDirPanel()
            self.closeSkillPractice()
            self.skillInfoManager.clear()
            self.isEditMode = False
            gameglobal.rds.ui.roleInfo.refreshJingjieInfo()
            gameglobal.rds.ui.roleInfoJingjie.refreshDetailInfo()
            return

    def closeDetailpanel(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SKILL_DETAIL)
        self.detailMediator = None

    def closeEnhancePanel(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SKILL_BAR_ENHANCE)
        self.enhanceMediator = None

    def closeDaohangDirPanel(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DAOHANG_DIRECTION_V2)
        self.daoHangDirMediator = None

    def reset(self):
        self.matchSkillsLv = {}
        self.activeAirSkillKV = {}
        self.wushuangSkillKV = {}
        self.skillsInfo = {}
        self.pskillsInfo = {}
        if self.closeMsgBoxId:
            gameglobal.rds.ui.messageBox.dismiss(self.closeMsgBoxId)
            self.closeMsgBoxId = 0
        self.isEditMode = False
        self.otherSkillData = {}

    def setEditMode(self, value = True):
        if self.isShow:
            self.isEditMode = value
            if self.commonSkillMc:
                self.commonSkillMc.Invoke('setEditMode', GfxValue(value))

    def _initWsSkillList(self):
        temList1 = [0, 0, 0]
        temList2 = [0, 0, 0]
        clientShortCut = gameglobal.rds.ui.actionbar.clientShortCut
        for i in range(3):
            if clientShortCut.has_key((uiConst.SKILL_ACTION_BAR, 12 + i)):
                temList1[i] = clientShortCut[uiConst.SKILL_ACTION_BAR, 12 + i][1]
            if clientShortCut.has_key((uiConst.SKILL_ACTION_BAR, 15 + i)):
                temList2[i] = clientShortCut[uiConst.SKILL_ACTION_BAR, 15 + i][1]

        self.equipSkills[0] = temList1
        self.equipSkills[1] = temList2

    def _getWsSkillStar(self, skillId):
        if skillId == 0:
            return 0
        else:
            skill = BigWorld.player().wsSkills.get(skillId, None)
            if not skill:
                return 0
            return skillDataInfo.getWsStarLv(SkillInfo(skillId, skill.level))

    def refreshNormalSkill(self):
        if self.commonSkillMc != None:
            self.commonSkillMc.Invoke('setNormalSkill')
            self.setSchemeName()

    def refreshPSkill(self):
        if self.commonSkillMc:
            self.commonSkillMc.Invoke('setPSkill')

    def refreshSpecialSkill(self):
        if self.wushuangSkillPanelMc != None:
            self.wushuangSkillPanelMc.Invoke('refreshSpecialSkillPanel')

    def refreshSpecialSkillById(self, skillId, wsType):
        if skillId not in self.specialSkills[wsType - 1]:
            return
        else:
            idx = self.specialSkills[wsType - 1].index(skillId)
            p = BigWorld.player()
            xiuweiNeed = {1: 10,
             2: 15,
             3: 20,
             4: 25}
            wsSkillItem = self.skillInfoManager.commonSkillIns.getSkillItemInfo(skillId)
            skInfoVal = p.wsSkills.get(skillId, None)
            lv = skInfoVal.level if skInfoVal else 1
            isOpen = p.wsSkills.has_key(skillId)
            name = wsSkillItem.get('skillName', '')
            if SGD.data.has_key((skillId, lv)):
                needLv = SGD.data.get((skillId, lv + 1), {}).get('learnLv', 1)
            else:
                needLv = SGD.data.get((skillId, 1), {}).get('learnLv', 1)
            starVal = self._getWsSkillStar(skillId)
            skillSlotState = wsSkillItem.get('skillSlotState', uiConst.SKILL_ICON_STAT_GRAY)
            wsNeed = skillDataInfo.getWsNeed(p.getSkillInfo(skillId, lv))
            wsNeed = wsNeed[0] if wsNeed[0] > 0 else wsNeed[1]
            c = len([ 1 for v in skInfoVal.slots if v[1] == True ]) if skInfoVal else 0
            xwNeed = xiuweiNeed.get(starVal, 0) + 2 * c
            prof = 0
            wsStar = 1
            if skInfoVal:
                for val in skInfoVal.proficiency.values():
                    prof += val

            addXinDeInfo = WSLD.data.get((skillId, lv), {})
            needXinDe = addXinDeInfo.get('maxXd', 0)
            if skInfoVal:
                skLvStr = '%d/%d' % (skInfoVal.level, gametypes.WUSHUANG_LV_MAX)
            else:
                wsStar = SGD.data.get((skillId, 1), {}).get('wsStar', 1)
                if wsStar == 3:
                    skLvStr = gameStrings.TEXT_SKILLPROXY_1900
                else:
                    autoNeedLv = SGD.data.get((skillId, 1), {}).get('learnLv', 1)
                    skLvStr = gameStrings.TEXT_SKILLPROXY_1903 % autoNeedLv
                if p.lv < 49:
                    wsStar = 1
            showAddEff = prof >= needXinDe and p.lv >= needLv
            daoHengInfo = self._genDirectionInfo(skillId)
            showPracticeEff = daoHengInfo['value'] >= daoHengInfo['maxValue']
            wsItemId = SGD.data.get((skillId, 1), ()).get('openItem', 410129)
            maxWsitemNum = SGD.data.get((skillId, 1), ()).get('itemNum', 10)
            wsItemNum = BigWorld.player().inv.countItemInPages(wsItemId, enableParentCheck=True)
            wsStarEff = False
            if wsItemNum > maxWsitemNum:
                wsStarEff = True
            ar = [{'iconPath': self.__getSkillIcon(skillId, lv)},
             name,
             starVal,
             skLvStr,
             [xwNeed, wsNeed],
             showAddEff,
             0,
             isOpen,
             showPracticeEff,
             wsStar,
             wsStarEff,
             skillSlotState]
            if self.wushuangSkillPanelMc:
                self.wushuangSkillPanelMc.Invoke('refreshSpecialSkillByIdx', (GfxValue(idx), uiUtils.array2GfxAarry(ar, True), GfxValue(wsType - 1)))
            return

    def refreshNormalSkillById(self, skillId):
        self.skillInfoManager.commonSkillIns.refreshSkillById(skillId)

    def refreshPSkillById(self, pskId):
        self.skillInfoManager.pSkillIns.refreshSkillById(pskId)

    def getSpecialSkillPointInfo(self):
        if gameglobal.rds.configData.get('enableWingWorldSkillScheme', False) and self.uiAdapter.skillSchemeV2.editorIndex == const.SKILL_SCHEME_WINGWORLD:
            return self.onGetWWSkillPointInfo()
        elif gameglobal.rds.configData.get('enableCrossBFSkillScheme', False) and self.uiAdapter.skillSchemeV2.editorIndex == const.SKILL_SCHEME_CROSS_BF:
            return self.onGetCrossBFSkillPointInfo()
        else:
            return self.onGetArenaSkillPointInfo()

    def onGetCrossBFSkillPointInfo(self, *args):
        p = BigWorld.player()
        crossServerScheme = utils.getCrossBFSkillSchemaData(p.lv)
        curMaxSkillPoints = 0
        activeSkillPoint = 0
        maxSkillPoint = 0
        info = {}
        if crossServerScheme:
            maxSkillPoint = crossServerScheme.get('skillPoint', 0)
            activeSkillPoint = p.crossBFSkillPoint
            curMaxSkillPoints = maxSkillPoint - activeSkillPoint - self.skillInfoManager.commonSkillIns.getConsumePoint() - self.skillInfoManager.pSkillIns.getConsumePoint()
        info['curSkillPoint'] = curMaxSkillPoints
        info['activeSkillPoint'] = activeSkillPoint
        info['maxSkillPoint'] = maxSkillPoint
        info['desc'] = gameStrings.SKILL_SCHEME_TXT % const.BIND_CASH_DESC
        return uiUtils.dict2GfxDict(info, True)

    def onGetSkillPointInfo(self, *arg):
        if self.isEditMode:
            return self.getSpecialSkillPointInfo()
        p = BigWorld.player()
        curMaxSkillPoints = utils.getCurSkillPoint(p.lv)
        info = {}
        info['curSkillPoint'] = curMaxSkillPoints - p.skillPoint - self.skillInfoManager.commonSkillIns.getConsumePoint() - self.skillInfoManager.pSkillIns.getConsumePoint()
        info['activeSkillPoint'] = p.activeSkillPoint
        info['maxSkillPoint'] = utils.getCurSkillPoint(p.lv)
        info['desc'] = gameStrings.SKILL_SCHEME_TXT % const.BIND_CASH_DESC
        return uiUtils.dict2GfxDict(info, True)

    def onGetArenaSkillPointInfo(self):
        p = BigWorld.player()
        arenaSkillScheme = utils.getArenaSkillSchemeData(p.lv)
        curMaxSkillPoints = 0
        activeSkillPoint = 0
        maxSkillPoint = 0
        info = {}
        if arenaSkillScheme:
            maxSkillPoint = arenaSkillScheme.get('arenaSkillPoint', 0)
            activeSkillPoint = p.arenaSkillPoint
            curMaxSkillPoints = maxSkillPoint - activeSkillPoint - self.skillInfoManager.commonSkillIns.getConsumePoint() - self.skillInfoManager.pSkillIns.getConsumePoint()
        info['curSkillPoint'] = curMaxSkillPoints
        info['activeSkillPoint'] = activeSkillPoint
        info['maxSkillPoint'] = maxSkillPoint
        info['desc'] = gameStrings.SKILL_SCHEME_TXT % const.BIND_CASH_DESC
        return uiUtils.dict2GfxDict(info, True)

    def onGetWWSkillPointInfo(self):
        p = BigWorld.player()
        arenaSkillScheme = utils.getWingWorldSkillSchemaData(p.getWingWorldGroupId())
        curMaxSkillPoints = 0
        activeSkillPoint = 0
        maxSkillPoint = 0
        info = {}
        if arenaSkillScheme:
            maxSkillPoint = arenaSkillScheme.get('wingSkillPoint', 0)
            activeSkillPoint = p.wingWorldSkillPoint
            curMaxSkillPoints = maxSkillPoint - activeSkillPoint - self.skillInfoManager.commonSkillIns.getConsumePoint() - self.skillInfoManager.pSkillIns.getConsumePoint()
        info['curSkillPoint'] = curMaxSkillPoints
        info['activeSkillPoint'] = activeSkillPoint
        info['maxSkillPoint'] = maxSkillPoint
        info['desc'] = gameStrings.SKILL_SCHEME_TXT % const.BIND_CASH_DESC
        return uiUtils.dict2GfxDict(info, True)

    def onGetXiuLianTips(self, *arg):
        info = {}
        p = BigWorld.player()
        startJingJie = SCFD.data.get('startJingJie', 3)
        jName = JJD.data.get(startJingJie, {}).get('name', '')
        info['visible'] = not p.skillEnhancePoint > 0
        info['text'] = gameStrings.TEXT_SKILLPROXY_2026 % jName
        needItemLv = SCD.data.get('RESET_SP_NEED_ITEM_LV', 58)
        info['resetTips'] = ''
        info['resetVisible'] = p.lv <= needItemLv
        return uiUtils.dict2GfxDict(info, True)

    def refreshSkillPoint(self):
        if self.commonSkillMc:
            self.commonSkillMc.Invoke('setSkillPoint')

    def onGetXiuLianPoint(self, *arg):
        if self.isEditMode:
            if gameglobal.rds.configData.get('enableWingWorldSkillScheme', False) and self.uiAdapter.skillSchemeV2.editorIndex == const.SKILL_SCHEME_WINGWORLD:
                return self.onGetWWXiuLianPoint()
            elif gameglobal.rds.configData.get('enableCrossBFSkillScheme', False) and self.uiAdapter.skillSchemeV2.editorIndex == const.SKILL_SCHEME_CROSS_BF:
                return self.onGetCrossBFXiuLianPoint()
            else:
                return self.onGetArenaXiuLianPoint()
        p = BigWorld.player()
        totalEnhPoint = SEJD.data.get((p.jingJie, p.lv), {}).get('maxEnhancePoint', 0)
        usedEnhPoint = self._getUsedEnhancePoint()
        curEnhPoint = p.skillEnhancePoint + usedEnhPoint
        enableXiuLianLv = SCD.data.get('enableXiuLianLv', 30)
        info = {'usedEnhPoint': usedEnhPoint,
         'curEnhPoint': curEnhPoint,
         'totalEnhPoint': totalEnhPoint,
         'realLv': p.lv,
         'enableXiuLianLv': enableXiuLianLv}
        return uiUtils.dict2GfxDict(info)

    def onGetArenaXiuLianPoint(self):
        p = BigWorld.player()
        totalEnhPoint = SEJD.data.get((p.arenaJingJie, p.arenaLv), {}).get('maxEnhancePoint', 0)
        usedEnhPoint = self._getUsedArenaEnhancePoint()
        curEnhPoint = utils.getArenaSkillSchemeData(p.lv).get('arenaEnhancePoint', 0)
        enableXiuLianLv = SCD.data.get('enableXiuLianLv', 30)
        info = {'usedEnhPoint': usedEnhPoint,
         'curEnhPoint': curEnhPoint,
         'totalEnhPoint': totalEnhPoint,
         'realLv': p.lv,
         'enableXiuLianLv': enableXiuLianLv}
        gamelog.info('jbx:onGetArenaXiuLianPoint', info)
        return uiUtils.dict2GfxDict(info)

    def onGetWWXiuLianPoint(self):
        p = BigWorld.player()
        skillSchemeData = utils.getWingWorldSkillSchemaData(p.getWingWorldGroupId())
        totalEnhPoint = skillSchemeData.get('wingEnhancePoint', 0)
        usedEnhPoint = self._getUsedArenaEnhancePoint()
        curEnhPoint = skillSchemeData.get('wingEnhancePoint', 0)
        enableXiuLianLv = SCD.data.get('enableXiuLianLv', 30)
        info = {'usedEnhPoint': usedEnhPoint,
         'curEnhPoint': curEnhPoint,
         'totalEnhPoint': totalEnhPoint,
         'realLv': p.lv,
         'enableXiuLianLv': enableXiuLianLv}
        gamelog.info('jbx:onGetWWXiuLianPoint', info)
        return uiUtils.dict2GfxDict(info)

    def onGetCrossBFXiuLianPoint(self):
        p = BigWorld.player()
        skillSchemeData = utils.getCrossBFSkillSchemaData(p.lv)
        totalEnhPoint = skillSchemeData.get('enhancePoint', 0)
        usedEnhPoint = self._getUsedArenaEnhancePoint()
        curEnhPoint = skillSchemeData.get('enhancePoint', 0)
        enableXiuLianLv = SCD.data.get('enableXiuLianLv', 30)
        info = {'usedEnhPoint': usedEnhPoint,
         'curEnhPoint': curEnhPoint,
         'totalEnhPoint': totalEnhPoint,
         'realLv': p.lv,
         'enableXiuLianLv': enableXiuLianLv}
        gamelog.info('jbx:onGetCrossBFXiuLianPoint', info)
        return uiUtils.dict2GfxDict(info)

    def _getUsedArenaEnhancePoint(self):
        p = BigWorld.player()
        ret = 0
        skillPointScheme = p.getSpecialSkillPoint()
        for skVal in skillPointScheme.itervalues():
            if skVal.has_key('enhanceData'):
                for enhData in skVal['enhanceData'].itervalues():
                    ret += enhData.get('enhancePoint', 0)

        return ret

    def refreshXiuLianPoint(self):
        if self.commonSkillMc:
            self.commonSkillMc.Invoke('setXiuLianPoint')

    def getEnhanceInfo(self, school, curEnhanceLv, totalPoint):
        info = []
        enhanceLvList = sorted(SELD.data.keys())
        reachedLength = enhanceLvList.index(curEnhanceLv)
        cnt = 0
        for i in xrange(reachedLength):
            item = {}
            enhanceLv = enhanceLvList[i]
            item['curVal'] = SELD.data[enhanceLv]['maxEnhancePoint']
            item['maxVal'] = SELD.data[enhanceLv]['maxEnhancePoint']
            item['desc'] = SD.data[school]['xiuLianDesc'][i]
            cnt = SELD.data[enhanceLv]['maxEnhancePoint']
            info.append(item)

        item = {}
        if curEnhanceLv == 1:
            item['maxVal'] = SELD.data[curEnhanceLv]['maxEnhancePoint'] - SELD.data[curEnhanceLv]['minEnhancePoint'] + 2
        else:
            item['maxVal'] = SELD.data[curEnhanceLv]['maxEnhancePoint'] - SELD.data[curEnhanceLv]['minEnhancePoint'] + 1
        item['curVal'] = totalPoint - cnt
        item['activeVal'] = SELD.data[curEnhanceLv].get('activeVal', 20)
        item['desc'] = SD.data[school]['xiuLianDesc'][reachedLength]
        info.append(item)
        for i in xrange(reachedLength + 1, 5):
            item = {}
            enhanceLv = enhanceLvList[i]
            item['curVal'] = 0
            item['maxVal'] = SELD.data[enhanceLv]['maxEnhancePoint']
            item['desc'] = SD.data[school]['xiuLianDesc'][i]
            info.append(item)

        return info

    def onGetEnhanceLvInfo(self, *arg):
        ret = {}
        p = BigWorld.player()
        curEnhanceLv = utils.getSkillEnhanceLv(p)
        totalPoint = utils.getTotalSkillEnhancePoint(p)
        ret['curEnhanceLv'] = curEnhanceLv
        ret['totalSkillEnhancePoint'] = p.skillEnhancePoint + self._getUsedEnhancePoint()
        ret['info'] = self.getEnhanceInfo(p.school, curEnhanceLv, totalPoint)
        return uiUtils.dict2GfxDict(ret, True)

    def setSkillPoint(self):
        if self.commonSkillMc:
            self.commonSkillMc.Invoke('setSkillPoint')

    def refreshSpecialSkillLv(self):
        p = BigWorld.player()
        ret = self.movie.CreateObject()
        skills = self.equipSkills[self.curType]
        equ = self.movie.CreateArray()
        for i, item in enumerate(skills):
            if item:
                levelStr = p.wsSkills[item].level
            else:
                levelStr = ''
            equ.SetElement(i, GfxValue(levelStr))

        ret.SetMember('equipedSkills', equ)
        gamelog.debug('wy:curtype', self.curType)
        self.specialSkills[self.curType] = SPD.data.get(p.realSchool, {}).get('wsType%dSpecialSkills' % (self.curType + 1), [])
        idle = self.movie.CreateArray()
        for i, item in enumerate(self.specialSkills[self.curType]):
            arr = self.movie.CreateArray()
            arr.SetElement(0, GfxValue(self.checkWsSkillCanLevelUp(item)))
            isOpen = p.wsSkills.has_key(item)
            wsStar = 1
            if isOpen:
                levelStr = '%d/%d' % (p.wsSkills[item].level, gametypes.WUSHUANG_LV_MAX)
            else:
                wsStar = SGD.data.get((item, 1), {}).get('wsStar', 1)
                if wsStar == 3:
                    levelStr = gameStrings.TEXT_SKILLPROXY_1900
                else:
                    autoNeedLv = SGD.data.get((item, 1), {}).get('learnLv', 1)
                    levelStr = gameStrings.TEXT_SKILLPROXY_1903 % autoNeedLv
                if p.lv < 49:
                    wsStar = 1
            arr.SetElement(1, GfxValue(levelStr))
            arr.SetElement(2, GfxValue(isOpen))
            prof = 0
            if p.wsSkills.get(item, None):
                for val in p.wsSkills[item].proficiency.values():
                    prof += val

            lv = p.wsSkills[item].level
            if SGD.data.has_key((item, lv)):
                needLv = SGD.data.get((item, lv + 1), {}).get('learnLv', 1)
            else:
                needLv = SGD.data.get((item, 1), {}).get('learnLv', 1)
            addXinDeInfo = WSLD.data.get((item, lv), {})
            needXinDe = addXinDeInfo.get('maxXd', 0)
            showAddBtn = prof >= needXinDe and p.lv >= needLv
            arr.SetElement(3, GfxValue(showAddBtn))
            daoHengInfo = self._genDirectionInfo(item)
            showPracticeEff = daoHengInfo['value'] >= daoHengInfo['maxValue']
            arr.SetElement(4, GfxValue(showPracticeEff))
            wsItemId = SGD.data.get((item, 1), ()).get('openItem', 410129)
            maxWsitemNum = SGD.data.get((item, 1), ()).get('itemNum', 10)
            wsItemNum = BigWorld.player().inv.countItemInPages(wsItemId, enableParentCheck=True)
            wsStarEff = False
            if wsItemNum > maxWsitemNum:
                wsStarEff = True
            arr.SetElement(5, GfxValue(wsStar))
            arr.SetElement(6, GfxValue(wsStarEff))
            idle.SetElement(i, arr)

        ret.SetMember('idleSkills', idle)
        ret.SetMember('school', GfxValue(p.school))
        if self.wushuangSkillPanelMc != None:
            self.wushuangSkillPanelMc.Invoke('refreshSpecialSkillLv', ret)

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        type, idx = self.getSlotID(key)
        skillID = 0
        if type == 2:
            skType = idx / MAX_EQUIP_SKILL_NUMS
            idx = idx % MAX_EQUIP_SKILL_NUMS
            skillID = self.equipSkills[skType][idx]
        elif type == 1:
            if idx == -1:
                skillID = self.skillId
            else:
                skType = idx / MAX_SPECIAL_SKILL_NUMS
                idx = idx % MAX_SPECIAL_SKILL_NUMS
                skillID = self.specialSkills[skType][idx]
        elif type == 0:
            if idx < MAX_NORMAL_SKILL_NUMS:
                skillID = self.normalSkills[idx] if not self.isRemoveOldSchoolSkill() else self.getSelectedSchoolSkillList()[idx]
            elif idx >= uiConst.SKILL_SHORT_CUT_BASE:
                offset = idx % uiConst.SKILL_SHORT_CUT_BASE
                parentId = self.normalSkills[idx / uiConst.SKILL_SHORT_CUT_BASE - 1]
                skillID = SGD.data.get((parentId, 1), {}).get('childId', (0, 0, 0))[offset]
            else:
                skillID = self.pskills[idx - MAX_NORMAL_SKILL_NUMS]
                return self.formatPSkillTooltip(skillID, sType=type)
        else:
            if type == 4:
                return self.getOtherSkillTip(idx)
            if type == 5:
                return self.getFishingTip(idx)
            if type == 6:
                skillID = idx
            else:
                if type == 7:
                    wsVal = WED.data.get(BigWorld.player().wushuang[self.curType + 1].mwsEnhanceCnt + 1, {})
                    if self.enhanceType == uiConst.TYPE_WUSHUANG_BAR:
                        itemId = wsVal.get('mwsEnhanceItems', [(0, 0, 0)] * 3)[idx][0]
                    elif self.enhanceType == uiConst.TYPE_XIUWEI_BAR:
                        itemId = wsVal.get('xiuweiEnhanceItems', [(0, 0, 0)] * 3)[idx][0]
                    else:
                        p = BigWorld.player()
                        starVal = self._getWsSkillStar(self.skillId)
                        if idx in (0, 2):
                            itemId = const.GEM_ITEMS[starVal - 1]
                        elif idx in (1, 3):
                            itemId = const.ADD_WSSKILL_SLOT_ITEMS[starVal - 1]
                        else:
                            itemId = self.resetItemIds[starVal - 1]
                    item = Item(itemId)
                    return gameglobal.rds.ui.inventory.GfxToolTip(item)
                if type == 8:
                    starVal = self._getWsSkillStar(self.skillId)
                    itemId = self.daoHangItemIds[starVal - 1]
                    item = Item(itemId)
                    return gameglobal.rds.ui.inventory.GfxToolTip(item)
                if type == uiConst.SKILL_PANEL_EXPLORE:
                    return self._getExploreTip(idx)
                if type == uiConst.SKILL_PANEL_PRACTICE:
                    if idx == -1:
                        skillID = self.skillId
                else:
                    if type == uiConst.SKILL_PANEL_GUILD:
                        p = BigWorld.player()
                        slv = 0 if idx not in p.guildMemberSkills else p.guildMemberSkills[idx].level
                        return self.getGuildSkillTip(idx, slv)
                    if type == uiConst.SKILL_PANEL_SOCIAL:
                        skillID = idx
                    elif type == uiConst.SKILL_PANEL_AIR_ORIG:
                        skillID = self.getAirSkillIdByPanelPos(idx)
                    elif type == uiConst.SKILL_PANEL_AIR_SLOT:
                        skillID = self.equipedAirSkills.get(idx, (0, 0))[1]
                    elif type == uiConst.SKILL_PANEL_AIR_DETAIL:
                        skillID = idx
                    elif type == uiConst.SKILL_PANEL_WUDAO:
                        skillID = self.skillId
                    elif type == uiConst.SKILL_GUIDE_SKILL or type == uiConst.SKILL_GUIDE_WSSKILL:
                        if gameglobal.rds.ui.skillGuide.mediator:
                            if idx < len(gameglobal.rds.ui.skillGuide.skillList):
                                skillID = gameglobal.rds.ui.skillGuide.skillList[idx]
                            else:
                                skillID = idx
                    else:
                        if type == uiConst.SKILL_PANEL_GUANYIN:
                            return self.getGuanYinTip(idx)
                        if type == uiConst.SKILL_PANEL_INTIMACY:
                            return self.getIntimacySkillTip(idx)
                        if type == uiConst.SKILL_PANEL_PUBG:
                            skillID = idx
        if skillID != 0:
            ret = self.formatTooltip(skillID, sType=type)
            return ret

    def onGetNextToolTip(self, *arg):
        key = arg[3][0].GetString()
        type, idx = self.getSlotID(key)
        skillID = 0
        if type == 2:
            skillID = self.equipSkills[self.curType][idx]
        elif type == 1:
            skillID = self.skillId
        elif type == uiConst.SKILL_PANEL_AIR_ORIG:
            skillID = self.getAirSkillIdByPanelPos(idx)
        elif type == uiConst.SKILL_PANEL_AIR_SLOT:
            skillID = self.equipedAirSkills.get(idx, (0, 0))[1]
        elif type == uiConst.SKILL_PANEL_AIR_DETAIL:
            skillID = idx
        elif type == 0:
            if idx < MAX_NORMAL_SKILL_NUMS:
                skillID = self.normalSkills[idx]
            else:
                skillID = self.pskills[idx - MAX_NORMAL_SKILL_NUMS]
                return self.formatNextPSkillTooltip(skillID, type)
        if skillID != 0:
            ret = self.formatNextTooltip(skillID, type)
            return ret

    def _getCastType(self, skillInfo, castType):
        if skillDataInfo.getSkillType(skillInfo) == const.SKILL_TYPE_PASSIVE:
            return ''
        elif skillDataInfo.getSkillCategory(skillInfo) == const.SKILL_CATEGORY_SPRITE_AWAKE:
            return gameStrings.TEXT_SKILLPROXY_2353
        elif castType == uiConst.GUID_SKILL:
            return gameStrings.TEXT_ACTIONBARPROXY_1837
        elif castType == uiConst.ACCUMULATE_SKILL:
            return gameStrings.TEXT_ACTIONBARPROXY_1839
        elif skillDataInfo.getSpellTime(skillInfo) and skillDataInfo.getPreSpell(skillInfo) != 1:
            return gameStrings.TEXT_ACTIONBARPROXY_1841
        else:
            return gameStrings.TEXT_ACTIONBARPROXY_1843

    def _getDamageType(self, damageType):
        if damageType == uiConst.MAGIC_DAMAGE_SKILL:
            return gameStrings.TEXT_ACTIONBARPROXY_1847
        elif damageType == uiConst.PHYSICS_DAMAGE_SKILL:
            return gameStrings.TEXT_ACTIONBARPROXY_1849
        else:
            return gameStrings.TEXT_ACTIONBARPROXY_1851

    def _getSkillType(self, skillType):
        if skillType == 1:
            return gameStrings.TEXT_ACTIONBARPROXY_1855
        elif skillType == 2:
            return gameStrings.TEXT_ACTIONBARPROXY_1857
        elif skillType == 3:
            return gameStrings.TEXT_ACTIONBARPROXY_1859
        elif skillType == 4:
            return gameStrings.TEXT_ACTIONBARPROXY_1861
        elif skillType == 5:
            return gameStrings.TEXT_SKILLPROXY_2381
        elif skillType == 6:
            return gameStrings.TEXT_SKILLPROXY_2383
        else:
            return ''

    def _getWSType(self, ws1, ws2, school):
        if not school:
            school = BigWorld.player().realSchool
        try:
            if ws1 > 0:
                return SPD.data.get(school, {}).get('wsType1', '')
            if ws2 > 0:
                return SPD.data.get(school, {}).get('wsType2', '')
            return ''
        except:
            (gameStrings.TEXT_ACTIONBARPROXY_1550, ws1, ws2)

    def _getSkillCurLv(self, skillID):
        curLv = 1
        sVal = BigWorld.player().getSkills().get(skillID, None)
        if sVal:
            curLv = sVal.level
        return curLv

    SKILL_STATE_UNSTUDIED = 1
    SKILL_STATE_TOP_LEVEL = 2
    SKILL_STATE_CAN_NOT_STUDY_LV = 3
    SKILL_STATE_CAN_NOT_STUDY_MONEY = 4
    SKILL_STATE_CAN_STUDY = 5
    SKILL_STATE_CAN_NOT_STUDY_SKILL_POINT = 6

    def checkWsSkillCanLevelUp(self, skillId):
        import const
        p = BigWorld.player()
        if not p.skills.has_key(skillId):
            return False
        sVal = p.skills[skillId]
        if sVal == const.MAX_SKILL_LEVEL:
            return False
        nextLv = sVal.level + 1
        skillInfo = p.getSkillInfo(skillId, min(const.MAX_SKILL_LEVEL, nextLv))
        if skillInfo.hasSkillData('learnLv'):
            learnLv = skillInfo.getSkillData('learnLv')
            if p.lv < learnLv:
                return False
        if skillInfo.hasSkillData('learnGold'):
            learnGold = skillInfo.getSkillData('learnGold')
            if p.cash + p.bindCash < learnGold:
                return False
        return True

    def getGraphVal(self, graph):
        ret = self.movie.CreateArray()
        gamelog.debug('getGraphVal', graph)
        ret.SetElement(0, GfxValue(gbk2unicode(graph[0])))
        ret.SetElement(1, GfxValue('f' + str(graph[1])))
        ret.SetElement(2, GfxValue(gbk2unicode(graph[2])))
        return ret

    def formatTooltip(self, skillId, sType = -1, isNext = False, isLearn = False, option = 0, sLv = 0, extraInfo = {}):
        p = BigWorld.player()
        fixLv = 0
        if sLv != 0:
            fixLv = p.getSkillInfo(skillId, sLv).hijackData.get('skillCalcLvAdd', 0)
            skillInfo = SkillInfo(skillId, min(sLv + fixLv, const.MAX_SKILL_LEVEL))
            skillTipsInfo = p.getSkillTipsInfo(skillId, min(sLv + fixLv, const.MAX_SKILL_LEVEL))
        else:
            sVal = p.getSkills().get(skillId, None)
            rLv = self._getCommonSkillLv(sType, skillId, sVal)
            fixLv = p.getSkillInfo(skillId, rLv).hijackData.get('skillCalcLvAdd', 0) if sVal else 0
            skillInfo = SkillInfo(skillId, min(rLv + fixLv, const.MAX_SKILL_LEVEL))
            skillTipsInfo = p.getSkillTipsInfo(skillId, min(rLv + fixLv, const.MAX_SKILL_LEVEL))
        skillName = skillDataInfo.getSkillName(skillInfo)
        wsAdd1, wsAdd2 = skillDataInfo.getWuShuang(skillInfo)
        mwsAdd = int(skillDataInfo.getWuShuangMwsAdd(skillInfo) / 100)
        wsNeed1, wsNeed2 = skillDataInfo.getWsNeed(skillInfo)
        wsNeed = '-' + str(int(math.floor(wsNeed1 / 100.0)) if wsNeed1 > 0 else int(math.floor(wsNeed2 / 100.0)))
        wsType = self._getWSType(wsNeed1, wsNeed2, skillInfo.getSkillData('school', None))
        if wsType == '':
            wsType = self._getWSType(wsAdd1, wsAdd2, skillInfo.getSkillData('school', None))
            if wsType != '':
                wsNeed = '+' + str(wsAdd1 / 100.0 if wsAdd1 > 0 else wsAdd2 / 100.0)
            else:
                wsNeed = ''
        wsType = wsType
        skillLv = skillDataInfo.getSkillLv(skillInfo)
        sd = skillDataInfo.ClientSkillInfo(skillId, sLv if sLv else 1)
        if option:
            shortCutWithParamIcon = SGTD.data.get(skillId, {}).get('shortCutWithParamIcon', ())
            offset = option % uiConst.SKILL_SHORT_CUT_BASE
            if offset < len(shortCutWithParamIcon):
                icon = shortCutWithParamIcon[offset]
            else:
                icon = 0
        else:
            icon = sd.getSkillData('icon', None)
        iconPath = 'skill/icon64/' + str(icon) + '.dds'
        skillType = self._getSkillType(skillDataInfo.getSkillType(skillInfo))
        skillCastType = self._getCastType(skillInfo, skillDataInfo.getCastType(skillInfo))
        mpNeed = skillDataInfo.getSkillMpNeed(skillInfo)
        hpNeed = skillDataInfo.getSkillHpNeed(skillInfo)
        learnLv = skillDataInfo.getLearnLv(skillInfo)
        if mpNeed > 0:
            castNeed = mpNeed
        elif hpNeed > 0:
            castNeed = hpNeed
        else:
            castNeed = 0
        if castNeed == 0:
            castNeed = ''
        guideMpNeed = skillDataInfo.getGuideMpNeed(skillInfo)
        guideHpNeed = skillDataInfo.getGuideHpNeed(skillInfo)
        guideNeed = 0
        if guideMpNeed > 0:
            guideNeed = guideMpNeed
        elif hpNeed > 0:
            guideNeed = guideHpNeed
        if guideNeed == 0:
            guideNeed = ''
        if option:
            offset = option % uiConst.SKILL_SHORT_CUT_BASE
            mainEff = skillTipsInfo.getSkillData('shortMainEff', '')
            detailEff1 = skillTipsInfo.getSkillData('shortDetailEff1', '')
            detailEff2 = skillTipsInfo.getSkillData('shortDetailEff2', '')
            detailEff3 = skillTipsInfo.getSkillData('shortDetailEff2', '')
        else:
            mainEff = skillTipsInfo.getSkillData('mainEff', '')
            detailEff1 = skillTipsInfo.getSkillData('detailEff1', '')
            detailEff2 = skillTipsInfo.getSkillData('detailEff2', '')
            detailEff3 = skillTipsInfo.getSkillData('detailEff3', '')
        detailArr = []
        if detailEff1:
            detailArr.append(uiUtils.calSkillTipValue(detailEff1, skillLv))
        if detailEff2:
            detailArr.append(uiUtils.calSkillTipValue(detailEff2, skillLv))
        if detailEff3:
            detailArr.append(uiUtils.calSkillTipValue(detailEff3, skillLv))
        graph1 = skillDataInfo.getGraph1(skillInfo)
        graph2 = skillDataInfo.getGraph2(skillInfo)
        graph3 = skillDataInfo.getGraph3(skillInfo)
        graph4 = skillDataInfo.getGraph4(skillInfo)
        graphArr = []
        if graph1:
            graphArr.append(self.getGraphVal(graph1))
        if graph2:
            graphArr.append(self.getGraphVal(graph2))
        if graph3:
            graphArr.append(self.getGraphVal(graph3))
        if graph4:
            graphArr.append(self.getGraphVal(graph4))
        daoHang = []
        gems, windCnt, forestCnt, fireCnt, hillCnt = self.getGemsInfo(skillId)
        if extraInfo:
            if extraInfo.windCnt != None:
                windCnt = extraInfo.windCnt
            if extraInfo.forestCnt != None:
                forestCnt = extraInfo.forestCnt
            if extraInfo.fireCnt != None:
                fireCnt = extraInfo.fireCnt
            if extraInfo.hillCnt != None:
                hillCnt = extraInfo.hillCnt
        if extraInfo:
            if extraInfo.windCnt != None:
                gems = []
                for i in xrange(0, extraInfo.windCnt):
                    daoHangType = uiConst.DAOHENG_WIND
                    gems.append((daoHangType, self.onGetDaohangIconTips(daoHangType)))

                for i in xrange(0, extraInfo.forestCnt):
                    daoHangType = uiConst.DAOHENG_WOOD
                    gems.append((daoHangType, self.onGetDaohangIconTips(daoHangType)))

                for i in xrange(0, extraInfo.fireCnt):
                    daoHangType = uiConst.DAOHENG_FIRE
                    gems.append((daoHangType, self.onGetDaohangIconTips(daoHangType)))

                for i in xrange(0, extraInfo.hillCnt):
                    daoHangType = uiConst.DAOHENG_HILL
                    gems.append((daoHangType, self.onGetDaohangIconTips(daoHangType)))

        for idx, item in enumerate(gems):
            daoHang.append(item[0])

        wsData = WSCD.data.get(skillId, {})
        daoHangDesc = []
        if windCnt != 0:
            id = wsData.get('windPSkill', [(0, 0)] * 5)[windCnt - 1]
            skillId = PD.data.get(id, {}).get('skillId')
            pskillVal = BigWorld.player().pskills.get(id[0], {}).get(skillId, None)
            pData = pskillVal.pData if pskillVal else {}
            desc = gameglobal.rds.ui.runeView.generateDesc(id[0], PSkillInfo(id[0], id[1], pData), id[1])
            daoHangDesc.append('wind:%s' % desc)
        if forestCnt != 0:
            id = wsData.get('woodPSkill', [(0, 0)] * 5)[forestCnt - 1]
            skillId = PD.data.get(id, {}).get('skillId')
            pskillVal = BigWorld.player().pskills.get(id[0], {}).get(skillId, None)
            pData = pskillVal.pData if pskillVal else {}
            desc = gameglobal.rds.ui.runeView.generateDesc(id[0], PSkillInfo(id[0], id[1], pData), id[1])
            daoHangDesc.append('wood:%s' % desc)
        if fireCnt != 0:
            id = wsData.get('firePSkill', [(0, 0)] * 5)[fireCnt - 1]
            skillId = PD.data.get(id, {}).get('skillId')
            pskillVal = BigWorld.player().pskills.get(id[0], {}).get(skillId, None)
            pData = pskillVal.pData if pskillVal else {}
            desc = gameglobal.rds.ui.runeView.generateDesc(id[0], PSkillInfo(id[0], id[1], pData), id[1])
            daoHangDesc.append('fire:%s' % desc)
        if hillCnt != 0:
            id = wsData.get('mountainPSkill', [(0, 0)] * 5)[hillCnt - 1]
            skillId = PD.data.get(id, {}).get('skillId')
            pskillVal = BigWorld.player().pskills.get(id[0], {}).get(skillId, None)
            pData = pskillVal.pData if pskillVal else {}
            desc = gameglobal.rds.ui.runeView.generateDesc(id[0], PSkillInfo(id[0], id[1], pData), id[1])
            daoHangDesc.append('hill:%s' % desc)
        shortMainEff = skillTipsInfo.getSkillData('shortMainEff', mainEff)
        shortDetailEff1 = skillTipsInfo.getSkillData('shortDetailEff1', '')
        shortDetailEff2 = skillTipsInfo.getSkillData('shortDetailEff2', '')
        shortDetailEff3 = skillTipsInfo.getSkillData('shortDetailEff3', '')
        shortDetailArr = []
        if shortDetailEff1:
            shortDetailArr.append(uiUtils.calSkillTipValue(shortDetailEff1, skillLv))
        if shortDetailEff2:
            shortDetailArr.append(uiUtils.calSkillTipValue(shortDetailEff2, skillLv))
        if shortDetailEff3:
            shortDetailArr.append(uiUtils.calSkillTipValue(shortDetailEff3, skillLv))
        stateIcon1 = skillInfo.getSkillData('stateIcon1', '')
        stateType1 = STD.data.get(stateIcon1, {}).get('iconShowType', 1)
        stateIcon2 = skillInfo.getSkillData('stateIcon2', '')
        stateType2 = STD.data.get(stateIcon2, {}).get('iconShowType', 1)
        stateIcon3 = skillInfo.getSkillData('stateIcon3', '')
        stateType3 = STD.data.get(stateIcon3, {}).get('iconShowType', 1)
        stateIconArr = []
        if stateIcon1:
            stateIconArr.append(['state/40/%s.dds' % STD.data.get(stateIcon1, {}).get('iconId', 0), stateType1])
        if stateIcon2:
            stateIconArr.append(['state/40/%s.dds' % STD.data.get(stateIcon2, {}).get('iconId', 0), stateType2])
        if stateIcon3:
            stateIconArr.append(['state/40/%s.dds' % STD.data.get(stateIcon3, {}).get('iconId', 0), stateType3])
        stateDesc1 = skillTipsInfo.getSkillData('stateDesc1', '')
        stateDesc2 = skillTipsInfo.getSkillData('stateDesc2', '')
        stateDesc3 = skillTipsInfo.getSkillData('stateDesc3', '')
        stateDescArr = []
        if stateDesc1:
            stateDescArr.append(uiUtils.calSkillTipValue(stateDesc1, skillLv))
        if stateDesc2:
            stateDescArr.append(uiUtils.calSkillTipValue(stateDesc2, skillLv))
        if stateDesc3:
            stateDescArr.append(uiUtils.calSkillTipValue(stateDesc3, skillLv))
        shortStateDesc1 = skillTipsInfo.getSkillData('shortStateDesc1', '')
        shortStateDesc2 = skillTipsInfo.getSkillData('shortStateDesc2', '')
        shortStateDesc3 = skillTipsInfo.getSkillData('shortStateDesc3', '')
        shortStateDescArr = []
        if shortStateDesc1:
            shortStateDescArr.append(uiUtils.calSkillTipValue(shortStateDesc1, skillLv))
        if shortStateDesc2:
            shortStateDescArr.append(uiUtils.calSkillTipValue(shortStateDesc2, skillLv))
        if shortStateDesc3:
            shortStateDescArr.append(uiUtils.calSkillTipValue(shortStateDesc3, skillLv))
        if fixLv:
            if sLv != 0:
                if sLv + fixLv > const.MAX_SKILL_LEVEL:
                    skillLvDesc = str(sLv) + "<font color=\'#7FFF95\'>+" + str(const.MAX_SKILL_LEVEL - sLv) + '</font>'
                else:
                    skillLvDesc = str(sLv) + "<font color=\'#7FFF95\'>+" + str(fixLv) + '</font>'
            else:
                sVal = p.getSkills().get(skillId, None)
                sklLv = sVal.level if sVal and sVal.level != 0 else 1
                if sklLv + fixLv > const.MAX_SKILL_LEVEL:
                    skillLvDesc = str(sklLv) + "<font color=\'#7FFF95\'>+" + str(const.MAX_SKILL_LEVEL - sklLv) + '</font>'
                else:
                    skillLvDesc = str(sklLv) + "<font color=\'#7FFF95\'>+" + str(fixLv) + '</font>'
        else:
            skillLvDesc = skillLv
        showLv = False
        if skillId in p.getSkills().keys():
            showLv = True
        if skillId in p.guildMemberSkills.keys():
            showLv = True
        levelUpCondition = gameglobal.rds.ui.roleInfo.getLevelUpCondition(skillId)
        worldViewDesc = SGTD.data.get(skillId, {}).get('worldViewDesc', '')
        isOnlyDetail = False
        if extraInfo and extraInfo.isOnlyDetail != None:
            isOnlyDetail = extraInfo.isOnlyDetail
        ret = [skillName,
         wsType,
         wsNeed,
         skillLvDesc,
         iconPath,
         skillType,
         skillCastType,
         castNeed,
         guideNeed,
         mainEff,
         detailArr,
         graphArr,
         daoHang,
         daoHangDesc,
         learnLv,
         showLv,
         shortMainEff,
         shortDetailArr,
         stateIconArr,
         stateDescArr,
         shortStateDescArr,
         mwsAdd,
         levelUpCondition,
         worldViewDesc,
         isOnlyDetail]
        return uiUtils.array2GfxAarry(ret, True)

    def formatPSkillTooltip(self, skillId, sType = -1, sLv = 0, mainEffExtra = ''):
        p = BigWorld.player()
        learn = p.learnedPSkills.get(skillId)
        if sLv != 0:
            skillInfo = PSkillInfo(skillId, sLv, {})
        elif learn:
            sLv = self._getPSkillLv(sType, skillId, learn)
            skillInfo = PSkillInfo(skillId, sLv, {})
        else:
            skillInfo = PSkillInfo(skillId, 1, {})
        skillName = skillInfo.getSkillData('sname', '')
        wsNeed = ''
        wsType = ''
        skillLv = skillDataInfo.getSkillLv(skillInfo)
        icon = skillInfo.getSkillData('icon', 'notFound')
        iconPath = 'skill/icon64/' + str(icon) + '.dds'
        skillType = self._getSkillType(5)
        skillCastType = ''
        castNeed = ''
        guideNeed = ''
        mainEff = skillInfo.getSkillData('mainEff', '') + mainEffExtra
        detailEff1 = skillInfo.getSkillData('detailEff1', '')
        detailEff2 = skillInfo.getSkillData('detailEff2', '')
        detailEff3 = skillInfo.getSkillData('detailEff3', '')
        detailArr = []
        if detailEff1:
            detailArr.append(uiUtils.calSkillTipValue(detailEff1, skillLv))
        if detailEff2:
            detailArr.append(uiUtils.calSkillTipValue(detailEff2, skillLv))
        if detailEff3:
            detailArr.append(uiUtils.calSkillTipValue(detailEff3, skillLv))
        graphArr = []
        daoHang = []
        daoHangDesc = []
        learnLv = skillDataInfo.getLearnLv(skillInfo)
        shortMainEff = skillInfo.getSkillData('shortMainEff', mainEff)
        shortDetailEff1 = skillInfo.getSkillData('shortDetailEff1', detailEff1)
        shortDetailEff2 = skillInfo.getSkillData('shortDetailEff2', detailEff2)
        shortDetailEff3 = skillInfo.getSkillData('shortDetailEff3', detailEff3)
        shortDetailArr = []
        if shortDetailEff1:
            shortDetailArr.append(uiUtils.calSkillTipValue(shortDetailEff1, skillLv))
        if shortDetailEff2:
            shortDetailArr.append(uiUtils.calSkillTipValue(shortDetailEff2, skillLv))
        if shortDetailEff3:
            shortDetailArr.append(uiUtils.calSkillTipValue(shortDetailEff3, skillLv))
        stateIcon1 = skillInfo.getSkillData('stateIcon1', '')
        stateType1 = STD.data.get(stateIcon1, {}).get('iconShowType', 1)
        stateIcon2 = skillInfo.getSkillData('stateIcon2', '')
        stateType2 = STD.data.get(stateIcon2, {}).get('iconShowType', 1)
        stateIcon3 = skillInfo.getSkillData('stateIcon3', '')
        stateType3 = STD.data.get(stateIcon3, {}).get('iconShowType', 1)
        stateIconArr = []
        if stateIcon1:
            stateIconArr.append(['state/icon/%s.dds' % STD.data.get(stateIcon1, {}).get('iconId', 0), stateType1])
        if stateIcon2:
            stateIconArr.append(['state/icon/%s.dds' % STD.data.get(stateIcon2, {}).get('iconId', 0), stateType2])
        if stateIcon3:
            stateIconArr.append(['state/icon/%s.dds' % STD.data.get(stateIcon3, {}).get('iconId', 0), stateType3])
        stateDesc1 = skillInfo.getSkillData('stateDesc1', '')
        stateDesc2 = skillInfo.getSkillData('stateDesc2', '')
        stateDesc3 = skillInfo.getSkillData('stateDesc3', '')
        stateDescArr = []
        if stateDesc1:
            stateDescArr.append(uiUtils.calSkillTipValue(stateDesc1, skillLv))
        if stateDesc2:
            stateDescArr.append(uiUtils.calSkillTipValue(stateDesc2, skillLv))
        if stateDesc3:
            stateDescArr.append(uiUtils.calSkillTipValue(stateDesc3, skillLv))
        shortStateDesc1 = skillInfo.getSkillData('shortStateDesc1', '')
        shortStateDesc2 = skillInfo.getSkillData('shortStateDesc2', '')
        shortStateDesc3 = skillInfo.getSkillData('shortStateDesc3', '')
        shortStateDescArr = []
        if shortStateDesc1:
            shortStateDescArr.append(uiUtils.calSkillTipValue(shortStateDesc1, skillLv))
        if shortStateDesc2:
            shortStateDescArr.append(uiUtils.calSkillTipValue(shortStateDesc2, skillLv))
        if shortStateDesc3:
            shortStateDescArr.append(uiUtils.calSkillTipValue(shortStateDesc3, skillLv))
        mwsAdd = 0
        levelUpCondition = ''
        ret = [skillName,
         wsType,
         wsNeed,
         skillLv,
         iconPath,
         skillType,
         skillCastType,
         castNeed,
         guideNeed,
         mainEff,
         detailArr,
         graphArr,
         daoHang,
         daoHangDesc,
         learnLv,
         skillId in p.learnedPSkills.keys(),
         shortMainEff,
         shortDetailArr,
         stateIconArr,
         stateDescArr,
         shortStateDescArr,
         mwsAdd,
         levelUpCondition]
        return uiUtils.array2GfxAarry(ret, True)

    def _getCommonSkillLv(self, sType, skillId, skillInfo):
        if sType == 0:
            lv = self.skillInfoManager.commonSkillIns.getSkillLv(skillId)
            if lv == 0:
                lv = 1
        elif skillInfo:
            lv = skillInfo.level
        elif utils.isMonsterSkill(skillId):
            lv = const.MONSTER_SKILL_LV
        else:
            lv = 1
        return lv

    def formatNextTooltip(self, skillId, sType, isNext = False, isLearn = False, option = ''):
        p = BigWorld.player()
        learn = p.getSkills().get(skillId)
        curMaxSkillPoints = utils.getCurSkillPoint(p.lv)
        fixLv = 0
        if learn:
            curSkillLv = self._getCommonSkillLv(sType, skillId, learn)
            skillInfoNext = SkillInfo(skillId, min(curSkillLv + 1, const.MAX_SKILL_LEVEL))
            fixLv = p.getSkillInfo(skillId, curSkillLv + 1).hijackData.get('skillCalcLvAdd', 0)
            skillTipsInfo = p.getSkillTipsInfo(skillId, min(curSkillLv + 1 + fixLv, const.MAX_SKILL_LEVEL))
        else:
            fixLv = p.getSkillInfo(skillId, 1).hijackData.get('skillCalcLvAdd', 0)
            skillInfoNext = SkillInfo(skillId, 1 + fixLv)
            skillTipsInfo = p.getSkillTipsInfo(skillId, 1 + fixLv)
        ret = self.movie.CreateArray()
        skillName = gbk2unicode(skillDataInfo.getSkillName(skillInfoNext))
        skillLv = skillDataInfo.getSkillLv(skillInfoNext)
        if skillId not in p.getSkills().keys():
            skillLv = 1
        if fixLv:
            if skillLv != 0:
                if skillLv + fixLv > const.MAX_SKILL_LEVEL:
                    skillLvDesc = str(skillLv) + "<font color=\'#7FFF95\'>+" + str(const.MAX_SKILL_LEVEL - skillLv) + '</font>'
                else:
                    skillLvDesc = str(skillLv) + "<font color=\'#7FFF95\'>+" + str(fixLv) + '</font>'
        else:
            skillLvDesc = skillLv
        sd = skillDataInfo.ClientSkillInfo(skillId)
        icon = sd.getSkillData('icon', None)
        iconPath = 'skill/icon64/' + str(icon) + '.dds'
        needLvLabel = gbk2unicode(gameStrings.TEXT_SKILLPROXY_2847)
        needGoldLabel = gbk2unicode(gameStrings.TEXT_SKILLPROXY_2848)
        needSkillPointLabel = gbk2unicode(gameStrings.TEXT_SKILLPROXY_2849)
        leanLv = skillDataInfo.getLearnLv(skillInfoNext)
        leanGold = skillDataInfo.getLearnGold(skillInfoNext)
        learnPoint = skillDataInfo.getLearnPoint(skillInfoNext)
        if skillInfoNext.hasSkillData('learnLv'):
            learnLv = skillInfoNext.getSkillData('learnLv')
            if p.lv < learnLv:
                needLvLabel = gbk2unicode(gameStrings.TEXT_SKILLPROXY_2858)
                leanLv = "<font color= \'#FF4C4C\'>" + str(leanLv) + '</font>'
        if skillInfoNext.hasSkillData('learnGold'):
            learnGold = skillInfoNext.getSkillData('learnGold')
            if p.cash + p.bindCash < learnGold:
                needGoldLabel = gbk2unicode(gameStrings.TEXT_SKILLPROXY_2864)
                leanGold = "<font color= \'#FF4C4C\'>" + str(leanGold) + '</font>'
        if skillInfoNext.hasSkillData('learnPoint'):
            learnPoint = skillInfoNext.getSkillData('learnPoint')
            if curMaxSkillPoints - p.skillPoint < learnPoint:
                needSkillPointLabel = gbk2unicode(gameStrings.TEXT_SKILLPROXY_2870)
                learnPoint = "<font color= \'#FF4C4C\'>" + str(learnPoint) + '</font>'
        mainEff = gbk2unicode(uiUtils.calSkillTipValue(skillTipsInfo.getSkillData('mainEnhEff', ''), skillLv))
        detailEff1 = gbk2unicode(uiUtils.calSkillTipValue(skillTipsInfo.getSkillData('enhEff1', ''), skillLv))
        detailEff2 = gbk2unicode(uiUtils.calSkillTipValue(skillTipsInfo.getSkillData('enhEff2', ''), skillLv))
        detailEff3 = gbk2unicode(uiUtils.calSkillTipValue(skillTipsInfo.getSkillData('enhEff3', ''), skillLv))
        ret.SetElement(0, GfxValue(skillName))
        ret.SetElement(1, GfxValue(skillLvDesc))
        ret.SetElement(2, GfxValue(str(iconPath)))
        ret.SetElement(3, GfxValue(needLvLabel))
        ret.SetElement(4, GfxValue(needGoldLabel))
        ret.SetElement(5, GfxValue(str(leanLv)))
        ret.SetElement(6, GfxValue(str(leanGold)))
        ret.SetElement(7, GfxValue(str(mainEff)))
        detailArr = self.movie.CreateArray()
        i = 0
        if detailEff1:
            detailArr.SetElement(0, GfxValue(detailEff1))
            i = i + 1
        if detailEff2:
            detailArr.SetElement(i, GfxValue(detailEff2))
            i = i + 1
        if detailEff3:
            detailArr.SetElement(i, GfxValue(detailEff3))
        ret.SetElement(8, detailArr)
        ret.SetElement(9, GfxValue(needSkillPointLabel))
        ret.SetElement(10, GfxValue(str(learnPoint)))
        if hasattr(p, 'carrerGuideData') and self.getGuideData(skillId):
            ret.SetElement(11, GfxValue(self.getGuideData(skillId)))
        return ret

    def _getPSkillLv(self, sType, skillId, skillInfo):
        if sType == 0:
            lv = self.skillInfoManager.pSkillIns.getSkillLv(skillId)
            if lv == 0:
                lv = 1
        elif skillInfo:
            lv = skillInfo.lv
        else:
            lv = 1
        return lv

    def formatNextPSkillTooltip(self, skillId, sType):
        p = BigWorld.player()
        learn = p.learnedPSkills.get(skillId)
        curMaxSkillPoints = utils.getCurSkillPoint(p.lv)
        if learn:
            skillInfo = p.getPSkillInfo(learn)
            skillInfoNext = PSkillInfo(skillId, min(self._getPSkillLv(sType, skillId, skillInfo) + 1, const.MAX_SKILL_LEVEL), skillInfo.pData)
        else:
            skillInfo = PSkillInfo(skillId, 1, {})
            skillInfoNext = PSkillInfo(skillId, 2, {})
        ret = self.movie.CreateArray()
        skillName = gbk2unicode(skillInfoNext.getSkillData('sname', ''))
        skillLv = skillDataInfo.getSkillLv(skillInfoNext)
        if skillId not in p.learnedPSkills.keys():
            skillLv = 0
        icon = skillInfoNext.getSkillData('icon', 'notFound')
        iconPath = 'skill/icon64/' + str(icon) + '.dds'
        needLvLabel = gbk2unicode(gameStrings.TEXT_SKILLPROXY_2847)
        needGoldLabel = gbk2unicode(gameStrings.TEXT_SKILLPROXY_2848)
        needSkillPointLabel = gbk2unicode(gameStrings.TEXT_SKILLPROXY_2849)
        leanLv = skillDataInfo.getLearnLv(skillInfoNext)
        leanGold = skillDataInfo.getLearnGold(skillInfoNext)
        learnPoint = skillDataInfo.getLearnPoint(skillInfoNext)
        if skillInfoNext.hasSkillData('learnLv'):
            learnLv = skillInfoNext.getSkillData('learnLv')
            if p.lv < learnLv:
                needLvLabel = gbk2unicode(gameStrings.TEXT_SKILLPROXY_2858)
                leanLv = "<font color= \'#FF4C4C\'>" + str(leanLv) + '</font>'
        if skillInfoNext.hasSkillData('learnGold'):
            learnGold = skillInfoNext.getSkillData('learnGold')
            if p.cash + p.bindCash < learnGold:
                needGoldLabel = gbk2unicode(gameStrings.TEXT_SKILLPROXY_2864)
                leanGold = "<font color= \'#FF4C4C\'>" + str(leanGold) + '</font>'
        if skillInfoNext.hasSkillData('learnPoint'):
            learnPoint = skillInfoNext.getSkillData('learnPoint')
            if curMaxSkillPoints - p.skillPoint < learnPoint:
                needSkillPointLabel = gbk2unicode(gameStrings.TEXT_SKILLPROXY_2870)
                learnPoint = "<font color= \'#FF4C4C\'>" + str(learnPoint) + '</font>'
        mainEff = gbk2unicode(skillInfoNext.getSkillData('mainEnhEff', ''))
        detailEff1 = gbk2unicode(skillInfoNext.getSkillData('enhEff1', ''))
        detailEff2 = gbk2unicode(skillInfoNext.getSkillData('enhEff2', ''))
        detailEff3 = gbk2unicode(skillInfoNext.getSkillData('enhEff3', ''))
        ret.SetElement(0, GfxValue(skillName))
        ret.SetElement(1, GfxValue(str(skillLv)))
        ret.SetElement(2, GfxValue(str(iconPath)))
        ret.SetElement(3, GfxValue(needLvLabel))
        ret.SetElement(4, GfxValue(needGoldLabel))
        ret.SetElement(5, GfxValue(str(leanLv)))
        ret.SetElement(6, GfxValue(str(leanGold)))
        ret.SetElement(7, GfxValue(str(mainEff)))
        detailArr = self.movie.CreateArray()
        i = 0
        if detailEff1:
            detailArr.SetElement(0, GfxValue(detailEff1))
            i = i + 1
        if detailEff2:
            detailArr.SetElement(i, GfxValue(detailEff2))
            i = i + 1
        if detailEff3:
            detailArr.SetElement(i, GfxValue(detailEff3))
        ret.SetElement(8, detailArr)
        ret.SetElement(9, GfxValue(needSkillPointLabel))
        ret.SetElement(10, GfxValue(str(learnPoint)))
        if hasattr(p, 'carrerGuideData') and self.getGuideData(skillId):
            ret.SetElement(11, GfxValue(self.getGuideData(skillId)))
        return ret

    def getGuideData(self, skillId):
        if not gameglobal.rds.configData.get('enableCareerGuilde', False):
            return ''
        p = BigWorld.player()
        if p.lv <= gametypes.GUIDE_SKILL_LV_REQUIRE:
            return ''
        skillInfo = p.carrerGuideData.get('skillInfo', {})
        lvKey, lvTxt = uiUtils.getGuideLv()
        if not skillInfo or not skillInfo.get(lvKey, 0):
            return ''
        lv = p.lv
        schoolName = const.SCHOOL_DICT[p.school]
        skillNum = skillInfo.get(lvKey, 0).get(skillId, -1)
        if skillNum < 0:
            return ''
        return gbk2unicode(gameStrings.SKILL_GUIDE_TIP % (lvTxt, schoolName, skillNum))

    def formatReqStr(self, lvReq, schReq, desc, price):
        p = BigWorld.player()
        school = ''
        for item in schReq:
            school += SD.data.get(item, {}).get('name', gameStrings.TEXT_GAME_1747) + gameStrings.TEXT_ACTIVITYFACTORY_280

        school = school[:-2]
        if p.school in schReq:
            ret = gameStrings.TEXT_SKILLPROXY_3021 + school + '</font><br>'
        else:
            ret = gameStrings.TEXT_SKILLPROXY_3023 + school + '</font><br>'
        if p.lv < lvReq:
            ret += gameStrings.TEXT_SKILLPROXY_3025 + str(lvReq) + '</font><br>'
        else:
            ret += gameStrings.TEXT_SKILLPROXY_3027 + str(lvReq) + '</font><br>'
        ret += "<font size = \'12\'>" + desc + '</font><br>'
        ret += gameStrings.TEXT_SKILLPROXY_3029 + str(price) + '</font><br>'
        return ret

    def formatConStr(self, skillInfo, isLearn = False, id = -1):
        ret = ''
        weapon = skillDataInfo.getWeaponTips(skillInfo)
        for item in weapon:
            if item[1]:
                ret += gameStrings.TEXT_SKILLPROXY_3037 + item[0] + '</font><br>'
            else:
                ret += gameStrings.TEXT_SKILLPROXY_3039 + item[0] + '</font><br>'

        selfBuffer = skillDataInfo.getSelfBufferName(skillInfo)
        for item in selfBuffer:
            if item[1]:
                ret += gameStrings.TEXT_SKILLPROXY_3037 + item[0] + '</font><br>'
            else:
                ret += gameStrings.TEXT_SKILLPROXY_3039 + item[0] + '</font><br>'

        if isLearn and not BigWorld.isPublishedVersion():
            ret += gameStrings.TEXT_SKILLPROXY_3048 + str(id) + '</font>'
        return ret

    def formatActiveToPSkillTooltip(self, skillId, sLv = 0):
        p = BigWorld.player()
        if sLv != 0:
            skillInfo = SkillInfo(skillId, sLv)
            skillTipsInfo = p.getSkillTipsInfo(skillId, sLv)
        else:
            sVal = p.getSkills().get(skillId, None)
            skillInfo = SkillInfo(skillId, sVal.level if sVal and sVal.level != 0 else 1)
            skillTipsInfo = p.getSkillTipsInfo(skillId, sVal.level if sVal and sVal.level != 0 else 1)
        skillName = skillDataInfo.getSkillName(skillInfo)
        wsNeed = ''
        wsType = ''
        skillLv = skillDataInfo.getSkillLv(skillInfo)
        sd = skillDataInfo.ClientSkillInfo(skillId)
        icon = sd.getSkillData('icon', None)
        iconPath = 'skill/icon64/' + str(icon) + '.dds'
        skillType = self._getSkillType(5)
        skillCastType = ''
        castNeed = ''
        guideNeed = ''
        mainEff = skillTipsInfo.getSkillData('mainEff', '')
        detailArr = []
        graphArr = []
        daoHang = []
        daoHangDesc = []
        learnLv = skillDataInfo.getLearnLv(skillInfo)
        shortMainEff = skillTipsInfo.getSkillData('shortMainEff', mainEff)
        shortDetailArr = []
        stateIconArr = []
        stateDescArr = []
        shortStateDescArr = []
        mwsAdd = 0
        if sLv != 0:
            skillLvDesc = sLv
        else:
            skillLvDesc = skillLv
        levelUpCondition = ''
        ret = [skillName,
         wsType,
         wsNeed,
         skillLvDesc,
         iconPath,
         skillType,
         skillCastType,
         castNeed,
         guideNeed,
         mainEff,
         detailArr,
         graphArr,
         daoHang,
         daoHangDesc,
         learnLv,
         skillId in p.guildMemberSkills.keys(),
         shortMainEff,
         shortDetailArr,
         stateIconArr,
         stateDescArr,
         shortStateDescArr,
         mwsAdd,
         levelUpCondition]
        return uiUtils.array2GfxAarry(ret, True)

    def isWsType(self, skillInfo):
        self.WsNeed = skillDataInfo.getWsNeed(skillInfo)
        return self.WsNeed[0] or self.WsNeed[1]

    def getActionIDByPos(self, nBar, nSlot):
        if nBar == 0:
            if nSlot < len(self.normalSkills):
                return self.normalSkills[nSlot]
            elif nSlot >= uiConst.SKILL_SHORT_CUT_BASE:
                offset = nSlot % uiConst.SKILL_SHORT_CUT_BASE
                parentId = self.normalSkills[nSlot / uiConst.SKILL_SHORT_CUT_BASE - 1]
                return SGD.data.get((parentId, 1), {}).get('childId', (0, 0, 0))[offset]
            else:
                return 0
        else:
            if nBar == 1:
                skType = nSlot / MAX_SPECIAL_SKILL_NUMS
                nSlot = nSlot % MAX_SPECIAL_SKILL_NUMS
                return self.specialSkills[skType][nSlot]
            if nBar == 2:
                skType = nSlot / MAX_EQUIP_SKILL_NUMS
                nSlot = nSlot % MAX_EQUIP_SKILL_NUMS
                return self.equipSkills[skType][nSlot]
            if nBar == uiConst.SKILL_PANEL_GUILD:
                return nSlot
            if nBar == uiConst.SKILL_PANEL_SOCIAL:
                return nSlot
            if nBar == uiConst.SKILL_PANEL_INTIMACY:
                return nSlot
            if nBar == uiConst.SKILL_PANEL_PUBG:
                return nSlot
            return 0

    def setItem(self, idAction, idBar, idSlot, barSlot = -1):
        if idBar == 2:
            p = BigWorld.player()
            skillId = idAction
            skType = idSlot / MAX_EQUIP_SKILL_NUMS
            if not self.skillEquipCheck():
                return False
            if skillId == 0:
                key = self._getKey(idBar, idSlot)
                self.delSlotItem(key, barSlot)
                idSlot = idSlot % MAX_EQUIP_SKILL_NUMS
                if barSlot == -1:
                    if skType == 0:
                        idx = 12 + idSlot
                    elif skType == 1:
                        idx = 15 + idSlot
                else:
                    idx = barSlot
                gameglobal.rds.ui.actionbar.removeItem(uiConst.SKILL_ACTION_BAR, idx, False)
                return True
            if not self._checkWsSkillValue(skillId, idSlot):
                return False
            iconPath = self.__getSkillIcon(idAction)
            name = self.__getSkillIcon(idAction)
            data = self.uiAdapter.movie.CreateObject()
            data.SetMember('name', GfxValue(name))
            data.SetMember('iconPath', GfxValue(iconPath))
            key = self._getKey(idBar, idSlot)
            type = p.wsSkills[skillId].wsType
            idSlot = idSlot % MAX_EQUIP_SKILL_NUMS
            if skType + 1 == type:
                self.updateSlotBinding(key, data)
                self.equipSkills[skType][idSlot] = idAction
            for pos, id in enumerate(self.equipSkills[skType]):
                if id == idAction and pos != idSlot:
                    key = self._getKey(2, pos + skType * MAX_EQUIP_SKILL_NUMS)
                    self.delSlotItem(key)
                    if skType == 0:
                        slot = 12 + pos
                    elif skType == 1:
                        slot = 15 + pos
                    gameglobal.rds.ui.actionbar.removeItem(uiConst.SKILL_ACTION_BAR, slot, False)

            slot = 12
            if type == 1:
                slot = 12 + idSlot
            elif type == 2:
                slot = 15 + idSlot
            gameglobal.rds.ui.actionbar.setItem(idAction, uiConst.SKILL_ACTION_BAR, slot, False, False, uiConst.SHORTCUT_TYPE_SKILL)
            self.refreshSpecialSkillWithoutIcon()
        elif idBar == 1 or idBar == 0:
            iconPath = self.__getSkillIcon(idAction)
            name = self.__getSkillIcon(idAction)
            data = self.uiAdapter.movie.CreateObject()
            data.SetMember('name', GfxValue(name))
            data.SetMember('iconPath', GfxValue(iconPath))
            key = self._getKey(idBar, idSlot)
            self.updateSlotBinding(key, data)
        elif idBar == 5:
            if idSlot > 0:
                self.fishItems[idSlot] = idAction
                iconPath = uiUtils.getItemIconFile40(idAction.id)
                data = self.uiAdapter.movie.CreateObject()
                data.SetMember('iconPath', GfxValue(iconPath))
                key = self._getKey(idBar, idSlot)
                self.updateSlotBinding(key, data)
                if hasattr(idAction, 'quality'):
                    quality = idAction.quality
                else:
                    quality = ID.data.get(idAction.id, {}).get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                self.setFishingSlotColor(idSlot, color)
                self.refreshFishingSkillPanel()
        elif idBar == uiConst.SKILL_PANEL_PRACTICE:
            key = self._getKey(idBar, idSlot)
            iconPath = 'skillEnhance/%s.dds' % idAction
            self.updateSlotBinding(key, uiUtils.dict2GfxDict({'iconPath': iconPath}))
        elif idBar == uiConst.SKILL_PANEL_AIR_SLOT:
            self.setAirSkillItem(idAction, idSlot)
        return True

    def _checkWsSkillValue(self, skillId, idSlot):
        p = BigWorld.player()
        if not p.wsSkills.has_key(skillId):
            return False
        return True

    def __getSkillIcon(self, skillId, level = 1):
        sd = skillDataInfo.ClientSkillInfo(skillId, level)
        icon = sd.getSkillData('icon', None)
        if icon != None:
            return 'skill/icon64/' + str(icon) + '.dds'
        else:
            raise Exception('can not find icon of skill %d' % skillId)
            return

    def _getKey(self, nBar, nSlot):
        return 'skills%d.%d' % (nBar, nSlot)

    def _getKeyByNormalSkillId(self, skillId):
        skillList = self.getSelectedSchoolSkillList() if self.isRemoveOldSchoolSkill() else self.normalSkills
        if skillId in skillList:
            return self._getKey(0, skillList.index(skillId))
        return 'skills0.0'

    def unEquipSpecialSkill(self, idBar, idSlot):
        if not self.skillEquipCheck():
            return
        idx = idSlot - 12
        key = self._getKey(2, idx)
        skType = 0 if idSlot <= 14 else 1
        if skType == 1:
            idx -= 3
        skillId = self.equipSkills[skType][idx]
        if isinstance(skillId, int) and skillId > 0:
            BigWorld.player().cell.removeWsSkill(skillId)
        self.delSlotItem(key, idSlot)
        gameglobal.rds.ui.actionbar.removeItem(uiConst.SKILL_ACTION_BAR, idSlot, False)

    def dragMatch(self, src, dest):
        skType = src / MAX_SPECIAL_SKILL_NUMS
        if skType == 0 and dest >= 12 and dest <= 14:
            return True
        if skType == 1 and dest >= 15 and dest <= 17:
            return True
        return False

    def setSpecialSlotsShine(self, enabled):
        if self.mediator != None:
            self.mediator.Invoke('setSpecialSlotsShine', GfxValue(enabled))

    def isQingGong(self, name):
        for item in self.qingGongMap.values():
            if item[0] == name:
                return True

        return False

    def getQingGongIdxByName(self, name):
        for k, v in self.qingGongMap.items():
            if v[0] == name:
                return k

        return 0

    def refreshOtherSkillPanel(self):
        if self.generalMediator:
            self.generalMediator.Invoke('refreshOtherSkillPanel', GfxValue(True))

    def refreshGuildSkillPanel(self):
        if self.generalMediator:
            self.generalMediator.Invoke('refreshGuildSkillPanel', GfxValue(True))

    def refreshIntimacyPanel(self):
        if self.generalMediator:
            self.generalMediator.Invoke('refreshIntimacyPanel', GfxValue(True))

    def refreshEmotePanel(self):
        if self.generalMediator:
            self.generalMediator.Invoke('refreshEmotePanel', GfxValue(True))

    def setRideShine(self, slot, isShow):
        key = 'skills4.' + str(slot)
        if not self.binding.has_key(key):
            return
        self.binding[key][0].Invoke('showToggleShine', GfxValue(isShow))

    def getOtherSkillTip(self, idx):
        skill = GSCD.data.get(idx, {})
        if not skill:
            gamelog.error('skillProxy: getOtherSkillTip Invalid skill Index: ' + str(idx))
            return None
        else:
            ret = "<font size = \'14\' color = \'#f2ab0d\'>" + skill['name'] + '</font><br>'
            ret += "<font size = \'12\'>" + skill['tips'] + '</font>'
            return GfxValue(gbk2unicode(ret))

    def getGuildSkillTip(self, sid, sLv):
        if GPD.data.get((sid, 1), {}).get('type', 1) == gametypes.GUILD_PSKILL_TYPE_ACTIVE:
            if GPD.data.get((sid, 1), {}).get('displayType', 1) == gametypes.GUILD_PSKILL_TYPE_ACTIVE:
                skillTips = gameglobal.rds.ui.skill.formatTooltip(sid, sLv=sLv)
            else:
                skillTips = gameglobal.rds.ui.skill.formatActiveToPSkillTooltip(sid, sLv=sLv)
        else:
            skillTips = gameglobal.rds.ui.skill.formatPSkillTooltip(sid, sLv=sLv)
        return skillTips

    def getIntimacyCurrentLevel(self, skillId):
        currentLevel = 1
        p = BigWorld.player()
        intimacyTgt = getattr(p.friend, 'intimacyTgt', None)
        if intimacyTgt:
            if p.friend.get(intimacyTgt, None):
                intimacyLv = p.friend[intimacyTgt].intimacyLv
                if skillId == uiConst.INTIMACY_SKILL_MARRIAGE:
                    marriageCombatBuffLvDict = MCD.data.get('marriageCombatBuffLvDict', {})
                    currentLevel = marriageCombatBuffLvDict.get(intimacyLv, 1)
                elif intimacyLv <= ISLD.data.get(uiConst.INTIMACY_SKILL_MIN_LV, {}).get('intimacyTgtLv', 5):
                    currentLevel = uiConst.INTIMACY_SKILL_MIN_LV
                elif intimacyLv >= ISLD.data.get(uiConst.INTIMACY_SKILL_MAX_LV, {}).get('intimacyTgtLv', 8):
                    currentLevel = uiConst.INTIMACY_SKILL_MAX_LV
                else:
                    for key, value in ISLD.data.items():
                        if value.get('intimacyTgtLv', 1) == intimacyLv:
                            currentLevel = key

        return currentLevel

    def getIntimacySkillTip(self, sid):
        ret = None
        tips = ''
        currentLevel = self.getIntimacyCurrentLevel(sid)
        for key, value in ISD.data.items():
            if key == (sid, currentLevel):
                tips = value.get('tips', '')

        ret = "<font size = \'12\'>" + tips + '</font>'
        return GfxValue(gbk2unicode(ret))

    def getGuildSkillCd(self, sid, sLv):
        if GPD.data.get((sid, 1), {}).get('type', 1) == gametypes.GUILD_PSKILL_TYPE_ACTIVE:
            skillcd = SGD.data.get((sid, sLv), {}).get('cd', 0.0)
        else:
            skillcd = PD.data.get((sid, sLv), {}).get('cd', 0.0)
        return skillcd

    def getGuanYinTip(self, bookId):
        gpd = GBD.data.get(bookId, {})
        pskillId = gpd.get('pskillId', [])
        if len(pskillId) > 0:
            pskillId = pskillId[0]
        else:
            pskillId = 0
        mainEffExtra = ''
        equip = BigWorld.player().equipment[gametypes.EQU_PART_CAPE]
        guanYin = getattr(BigWorld.player(), 'guanYin', None)
        now = utils.getNow()
        isPreEquip = False
        slotIdx = -1
        if gameconfigCommon.enableGuanYinThirdPhase():
            for idx, guanYinSlotVal in guanYin.iteritems():
                if guanYinSlotVal.guanYinInfo[0] == bookId:
                    slotIdx = idx
                    break

            isPreEquip = slotIdx >= GD.data.get(equip.id if equip else 0, {}).get('pskillNum', -1)
        item = Item(bookId)
        if item.isGuanYinSuperSkillBook():
            ttl = gpd.get('ttl')
            if gameconfigCommon.enableGuanYinThirdPhase():
                guanYinBookVal = None
                for bookVal in guanYin.books.itervalues():
                    if bookVal.guanYinSuperBookId == bookId:
                        guanYinBookVal = bookVal
                        break

                guanYinSuperPskillExpire = guanYinBookVal.guanYinSuperPskillExpire if guanYinBookVal else 0
            else:
                guanYinSuperPskillExpire = equip.guanYinSuperPskillExpire
            if ttl:
                if now > guanYinSuperPskillExpire:
                    mainEffExtra = '<br>%s' % uiUtils.toHtml(gameStrings.TEXT_REDPACKETPROXY_623, '#F43804')
                else:
                    timeStr = gameStrings.TEXT_SKILLPROXY_3418 % utils.formatTimeStr(guanYinSuperPskillExpire - now, gameStrings.TEXT_SKILLPROXY_3418_1)
                    mainEffExtra = '<br>%s' % uiUtils.toHtml(timeStr, '#66CD00')
        elif not gameconfigCommon.enableGuanYinThirdPhase():
            for slot, info in enumerate(equip.guanYinInfo):
                if equip.guanYinStat[slot] == None:
                    continue
                part = equip.guanYinStat[slot]
                if info[part] == bookId:
                    extra = equip.guanYinExtraInfo[slot][part]
                    if extra.has_key('expireTime'):
                        if now > extra['expireTime']:
                            mainEffExtra = '<br>%s' % uiUtils.toHtml(gameStrings.TEXT_REDPACKETPROXY_623, '#F43804')
                        else:
                            timeStr = gameStrings.TEXT_SKILLPROXY_3433 % utils.formatTimeStr(extra['expireTime'] - now, gameStrings.TEXT_SKILLPROXY_3418_1)
                            mainEffExtra = '<br>%s' % uiUtils.toHtml(timeStr, '#66CD00')
                        break
                    if extra.has_key('commonExpireTime'):
                        if now > extra['commonExpireTime']:
                            pass
                    break

        if isPreEquip:
            lv = uiConst.GUAN_YIN_VALID_LV.get(slotIdx, 6)
            mainEffExtra += "<br><font color=\'#FF471C\'>%s</font>" % (gameStrings.GUAN_YIN_V3_VALID_LV % lv)
        return self.formatPSkillTooltip(pskillId, sLv=gpd.get('lv', 0), mainEffExtra=mainEffExtra)

    def getFishingTip(self, idx):
        if idx == 0:
            ret = gameStrings.TEXT_SKILLPROXY_3450
            ret += gameStrings.TEXT_SKILLPROXY_3451
            return GfxValue(gbk2unicode(ret))
        else:
            i = BigWorld.player().fishingEquip[idx - 1]
            if i == None:
                return GfxValue(gbk2unicode((gameStrings.TEXT_SKILLPROXY_3456, gameStrings.TEXT_SKILLPROXY_3456_1, gameStrings.TEXT_SKILLPROXY_3456_2)[idx - 1]))
            return gameglobal.rds.ui.inventory.GfxToolTip(i)

    def _getExploreTip(self, idx):
        if idx == 0:
            ret = gameStrings.TEXT_SKILLPROXY_3462
            ret += gameStrings.TEXT_SKILLPROXY_3463
            return GfxValue(gbk2unicode(ret))
        else:
            i = BigWorld.player().exploreEquip.get(gametypes.EXPLORE_EQUIP_COMPASS)
            if i:
                return gameglobal.rds.ui.inventory.GfxToolTip(i)
            return GfxValue(gbk2unicode(gameStrings.TEXT_SKILLPROXY_3470))

    def setFishingSlotColor(self, slot, color):
        if self.lifeMediator != None:
            self.lifeMediator.Invoke('setFishingSlotColor', (GfxValue(slot), GfxValue(color)))

    def refreshFishingSkillPanel(self):
        ret = self._genFishingSkillInfo()
        if self.lifeMediator != None:
            self.lifeMediator.Invoke('refreshFishingSkill', uiUtils.array2GfxAarry(ret, True))

    def setProgressBarWarning(self, nPageSrc, nItemSrc, isShow):
        skill = self.getActionIDByPos(nPageSrc, nItemSrc)
        if not skill:
            return
        else:
            cnt = 0
            xiuweiCnt = 0
            xiuweiNeed = {1: 10,
             2: 15,
             3: 20,
             4: 25}
            for skillId in self.equipSkills[self.curType]:
                if skillId != 0:
                    cnt += 1
                    sVal = BigWorld.player().wsSkills.get(skillId, None)
                    if sVal:
                        c = len([ 1 for v in sVal.slots if v[1] == True ])
                        xiuweiCnt += xiuweiNeed.get(self._getWsSkillStar(skillId), 0) + 2 * c

            if cnt > 2:
                return
            xiuwei = 0
            dragSVal = BigWorld.player().wsSkills.get(skill, None)
            if dragSVal:
                c = len([ 1 for v in dragSVal.slots if v[1] == True ])
                xiuwei = xiuweiNeed.get(self._getWsSkillStar(skill), 0) + 2 * c
            wsVal = BigWorld.player().wushuang1 if self.curType == 0 else BigWorld.player().wushuang2
            if xiuwei + xiuweiCnt <= wsVal.getXiuwei(BigWorld.player()):
                return
            pos = 0
            for skillId in self.equipSkills[self.curType]:
                if skillId != 0:
                    sVal = BigWorld.player().wsSkills.get(skillId, None)
                    if sVal:
                        c = len([ 1 for v in sVal.slots if v[1] == True ])
                        if xiuweiCnt - (xiuweiNeed.get(self._getWsSkillStar(skillId), 0) + 2 * c) + xiuwei <= wsVal.getXiuwei(BigWorld.player()):
                            cnt = pos
                            break
                    pos += 1

            if self.mediator:
                self.mediator.Invoke('setProgressBarWarning', (GfxValue(cnt), GfxValue(xiuwei), GfxValue(isShow)))
            return

    def onAddSkillExpByItem(self, *arg):
        p = BigWorld.player()
        itemId = int(arg[3][0].GetNumber())
        if p.airSkills.has_key(self.skillId):
            p.cell.addAirCombatExpByUseItem(self.skillId, itemId)
        else:
            p.cell.addProficiencyByItem(self.skillId, itemId)

    def onAddDaoHengSlot(self, *arg):
        BigWorld.player().cell.addDaoHengSlot(self.skillId)

    def _genDetailInfo(self):
        ret = {}
        p = BigWorld.player()
        sVal = p.wsSkills[self.skillId]
        sd = skillDataInfo.ClientSkillInfo(self.skillId)
        icon = sd.getSkillData('icon', None)
        name = SGTD.data.get(self.skillId, {}).get('name', '')
        if SGD.data.has_key((self.skillId, sVal.level)):
            needLv = SGD.data.get((self.skillId, sVal.level + 1), {}).get('learnLv', 1)
        else:
            needLv = SGD.data.get((self.skillId, 1), {}).get('learnLv', 1)
        starVal = self._getWsSkillStar(self.skillId)
        addXinDeInfo = WSLD.data.get((self.skillId, sVal.level), {})
        tips = []
        gameStrings.TEXT_SKILLPROXY_3554
        if addXinDeInfo.get('useAddXd', 0) > 0:
            tip = {}
            tip['hint'] = gameStrings.TEXT_SKILLPROXY_3557
            tip['add'] = addXinDeInfo.get('useAddXd', 0)
            tip['value'] = sVal.proficiency.get(gametypes.WUSHUANG_PROF_COND_USED, 0)
            tip['max'] = addXinDeInfo.get('useAddXdMax', 0)
            tips.append(tip)
        gameStrings.TEXT_SKILLPROXY_3563
        itemAddxd = []
        addXdItem = addXinDeInfo.get('itemAddXd', [])
        for item in addXdItem:
            addXd = {}
            itemId = item[0]
            addXd['hint'] = gameStrings.TEXT_SKILLPROXY_3570
            addXd['add'] = item[1]
            addXd['value'] = sVal.proficiency.get(gametypes.WUSHUANG_PROF_COND_ITEM + str(itemId), 0)
            addXd['max'] = item[2]
            addXd['itemId'] = itemId
            addXd['itemCount'] = p.inv.countItemInPages(itemId, enableParentCheck=True)
            addXd['iconPath'] = uiUtils.getItemIconFile64(itemId)
            itemAddxd.append(addXd)

        prof = 0
        for val in sVal.proficiency.values():
            prof += val

        levelStr = sVal.level
        ret['skillId'] = self.skillId
        ret['school'] = p.realSchool
        ret['wsType'] = sVal.wsType - 1
        ret['skillName'] = name
        ret['slotData'] = {'iconPath': 'skill/icon64/' + str(icon) + '.dds'}
        ret['starVal'] = starVal
        ret['skillLv'] = levelStr
        ret['skillExp'] = prof
        ret['needExp'] = addXinDeInfo.get('maxXd', 0)
        ret['tips'] = tips
        ret['itemAddExp'] = itemAddxd
        ret['roleLv'] = p.lv
        ret['needLv'] = needLv
        return ret

    def refreshDetailInfo(self):
        if self.detailMediator is None:
            return
        else:
            if self.skillId in BigWorld.player().airSkills:
                info = self.genAirSkillDetaiInfo()
            else:
                info = self._genDetailInfo()
            self.detailMediator.Invoke('setDetailInfo', uiUtils.dict2GfxDict(info, True))
            return

    def _getItemQualityColor(self, id):
        quality = ID.data.get(id, {}).get('quality', 1)
        color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
        return color

    def _genWuShuangBarInfo(self):
        p = BigWorld.player()
        wsVal = p.wushuang1 if self.curType == 0 else p.wushuang2
        wsData = WED.data.get(wsVal.mwsEnhanceCnt + 1, {})
        curWsVal = 0
        selectedWs = self.getSelectedWS(wsVal)
        for skillId in selectedWs:
            if skillId != 0:
                wsNeed = skillDataInfo.getWsNeed(p.getSkillInfo(skillId, p.wsSkills[skillId].level))
                wsNeed = wsNeed[0] if wsNeed[0] > 0 else wsNeed[1]
                curWsVal += wsNeed

        ret = {'school': p.realSchool,
         'type': self.curType,
         'currentVal': curWsVal,
         'maxVal': int(math.floor(wsVal.getMws(p) / 100.0)),
         'addVal': int(math.floor(wsData.get('mwsAdd', 0) / 100.0)),
         'curXlVal': wsVal.potential,
         'needXlVal': wsData.get('mwsPotentialCost', 0),
         'item': []}
        items = wsData.get('mwsEnhanceItems', [])
        for item in items:
            if item[0] != -1:
                iconPath = uiUtils.getItemIconFile40(item[0])
                count = p.inv.countItemInPages(item[0], enableParentCheck=True)
            else:
                iconPath = 'notFound'
                count = -1
            ret['item'].append([{'iconPath': iconPath},
             count,
             item[1],
             int(math.floor(item[2] / 100.0))])

        return ret

    def getSelectedWS(self, wsVal):
        selectedWs = []
        currSchemeNo = gameglobal.rds.ui.actionbar.currSchemeNo
        if currSchemeNo == uiConst.SHORT_CUT_CASE_1:
            selectedWs = wsVal.selectedWs
        elif currSchemeNo == uiConst.SHORT_CUT_CASE_2:
            selectedWs = wsVal.selectedWs1
        elif currSchemeNo == uiConst.SHORT_CUT_CASE_3:
            selectedWs = wsVal.selectedWs2
        return selectedWs

    def refreshWuShuangBarInfo(self):
        if self.enhanceMediator:
            self.enhanceMediator.Invoke('setWuShuangPanel')

    def _genXiuWeiBarInfo(self):
        p = BigWorld.player()
        wsVal = p.wushuang1 if self.curType == 0 else p.wushuang2
        wsData = WED.data.get(wsVal.mwsEnhanceCnt + 1, {})
        ret = {'school': p.realSchool,
         'type': self.curType,
         'currentVal': [],
         'addVal': wsData.get('xiuweiAdd', 0),
         'maxVal': wsVal.getXiuwei(BigWorld.player()),
         'curXlVal': wsVal.potential,
         'needXlVal': wsData.get('xiuweiPotentialCost', 0),
         'item': []}
        selectedWs = self.getSelectedWS(wsVal)
        xiuweiNeed = {1: 10,
         2: 15,
         3: 20,
         4: 25}
        for skillId in selectedWs:
            if skillId == 0:
                ret['currentVal'].append(0)
            else:
                ret['currentVal'].append(xiuweiNeed.get(self._getWsSkillStar(skillId), 0))

        items = wsData.get('xiuweiEnhanceItems', [])
        for item in items:
            if item[0] != -1:
                iconPath = uiUtils.getItemIconFile40(item[0])
                count = p.inv.countItemInPages(item[0], enableParentCheck=True)
            else:
                iconPath = 'notFound'
                count = -1
            ret['item'].append([{'iconPath': iconPath},
             count,
             item[1],
             item[2]])

        return ret

    def refreshXiuWeiBarInfo(self):
        if self.enhanceMediator:
            self.enhanceMediator.Invoke('setXiuWeiPanel')

    def _genRelieveInfo(self):
        p = BigWorld.player()
        sVal = p.wsSkills.get(self.skillId, None)
        starVal = self._getWsSkillStar(self.skillId)
        ret = {'normal': [],
         'extra': [],
         'item': []}
        itemIds = [const.GEM_ITEMS[starVal - 1], const.ADD_WSSKILL_SLOT_ITEMS[starVal - 1]]
        itemsGain = {}
        itemsGain[const.GEM_ITEMS[starVal - 1]] = 0
        for gemTp in gametypes.WUSHUANG_ALL_GEM_TYPES:
            gemUsed = self._calcGemUsed(sVal, gemTp)
            itemsGain[const.GEM_ITEMS[starVal - 1]] += gemUsed

        itemsGain[const.ADD_WSSKILL_SLOT_ITEMS[starVal - 1]] = 0
        for itemId in itemIds:
            itemCnt = int(round(itemsGain[itemId] * 0.7))
            ret['normal'].append({'iconPath': uiUtils.getItemIconFile40(itemId),
             'count': itemCnt})
            ret['extra'].append({'iconPath': uiUtils.getItemIconFile40(itemId),
             'count': itemsGain[itemId] - itemCnt})

        it = Item(self.resetItemIds[starVal - 1])
        count = p.inv.countItemInPages(self.resetItemIds[starVal - 1], enableParentCheck=True)
        ret['item'] = [{'iconPath': uiUtils.getItemIconFile40(self.resetItemIds[starVal - 1])},
         gbk2unicode(it.name),
         count,
         1]
        return ret

    def _calcGemUsed(self, sVal, gemType):
        gemUsed = 0
        c = sum([ True for v in sVal.slots if v[1] and v[2] == gemType ])
        for i in range(c):
            gemUsed += 2 ** i

        return gemUsed

    def _calcSlotItemUsed(self, sVal, source):
        c = len([ 1 for v in sVal.slots if v[0] == source ])
        return sum(range(c)) + c

    def refreshRelieveInfo(self):
        if self.enhanceMediator:
            self.enhanceMediator.Invoke('setRelievePanel')

    def getGemsInfo(self, skillId):
        p = BigWorld.player()
        sVal = p.wsSkills.get(skillId, None)
        if sVal is None:
            return ([],
             0,
             0,
             0,
             0)
        else:
            gemTypeMap = {gametypes.WUSHUANG_GEM_TYPE_WIND: uiConst.DAOHENG_WIND,
             gametypes.WUSHUANG_GEM_TYPE_WOOD: uiConst.DAOHENG_WOOD,
             gametypes.WUSHUANG_GEM_TYPE_FIRE: uiConst.DAOHENG_FIRE,
             gametypes.WUSHUANG_GEM_TYPE_MOUNTAIN: uiConst.DAOHENG_HILL}
            gems = []
            daoHengCnt = [0] * 6
            for slot in sVal.slots:
                if slot[1] == True:
                    type = gemTypeMap[slot[2]]
                    gems.append((type, self.onGetDaohangIconTips(type)))
                    daoHengCnt[type] += 1
                else:
                    gems.append((uiConst.DAOHENG_IDLE, self.onGetDaohangIconTips(uiConst.DAOHENG_IDLE)))

            wddd = WDD.data
            jjdd = JJD.data
            maxGemsData = SCD.data.get('daoHengSlotMaxNum', 10)
            for i in range(len(gems), maxGemsData):
                needJingjie = wddd.get((skillId, i + 1), {}).get('needJingJie', 0)
                if p.arenaJingJie >= needJingjie:
                    gems.append((uiConst.DAOHENG_PLUS, self.onGetDaohangIconTips(uiConst.DAOHENG_PLUS)))
                else:
                    tip = gameStrings.TEXT_SKILLPROXY_3768 + jjdd.get(needJingjie, {}).get('name', gameStrings.TEXT_SKILLPROXY_3768_1)
                    gems.append((uiConst.DAOHENG_LOCK, tip))

            return (gems,
             daoHengCnt[uiConst.DAOHENG_WIND],
             daoHengCnt[uiConst.DAOHENG_WOOD],
             daoHengCnt[uiConst.DAOHENG_FIRE],
             daoHengCnt[uiConst.DAOHENG_HILL])

    def _genDirectionInfo(self, skillId):
        p = BigWorld.player()
        sVal = p.wsSkills.get(skillId, None)
        wsData = WSCD.data.get(skillId, {})
        if sVal is None:
            return {'value': 0,
             'maxValue': 1000}
        else:
            gems, windCnt, forestCnt, fireCnt, hillCnt = self.getGemsInfo(skillId)
            ret = {}
            tips = []
            slotNum = len(sVal.slots) if sVal.slots else 0
            daoHengInfo = WDD.data.get((skillId, slotNum + 1), {})
            tipsDescription = daoHengInfo.get('addDhDescription', [])
            tipsData = daoHengInfo.get('addDh', [])
            for i in range(len(tipsDescription)):
                t = {}
                t['description'] = tipsDescription[i]
                t['value'] = getattr(sVal, 'daoHeng', {}).get('%s%s' % (tipsData[i][0], tipsData[i][-1]), 0)
                t['maxValue'] = tipsData[i][3]
                tips.append(t)

            daoHengValue = sum(getattr(sVal, 'daoHeng', {}).values())
            useRebalance = self.checkUseRebalance()
            ret['daoHangNum'] = {gametypes.WUSHUANG_GEM_TYPE_FIRE: fireCnt,
             gametypes.WUSHUANG_GEM_TYPE_MOUNTAIN: hillCnt,
             gametypes.WUSHUANG_GEM_TYPE_WIND: windCnt,
             gametypes.WUSHUANG_GEM_TYPE_WOOD: forestCnt}
            lockNum = 0
            hasNum = 0
            for i, val in enumerate(gems):
                state = val[0]
                if state == uiConst.DAOHENG_LOCK:
                    lockNum += 1
                elif state in [uiConst.DAOHENG_WIND,
                 uiConst.DAOHENG_FIRE,
                 uiConst.DAOHENG_WOOD,
                 uiConst.DAOHENG_HILL]:
                    hasNum += 1

            if hasNum + lockNum == len(gems):
                wuDaoBtnVisible = False
            else:
                wuDaoBtnVisible = True
            ret['slots'] = slotNum
            ret['fire'] = fireCnt
            ret['wind'] = windCnt
            ret['hill'] = hillCnt
            ret['forest'] = forestCnt
            ret['daohang'] = gems
            ret['skillId'] = skillId
            ret['value'] = daoHengValue
            ret['tips'] = tips
            ret['maxValue'] = daoHengInfo.get('addSlotDh', 1000)
            itemIds, itemNums = self._getWSWudaoItmes(skillId)
            ret['itemNums'] = itemNums
            ret['curNums'] = [ p.inv.countItemInPages(wuDaoItemId, enableParentCheck=True) for wuDaoItemId in itemIds ]
            ret['slotDatas'] = [ uiUtils.getGfxItemById(wuDaoItemId) for wuDaoItemId in itemIds ]
            ret['wuDaoBtnVisible'] = wuDaoBtnVisible
            lingliNum = 0
            lingliTxt = ''
            for itemId in const.ALL_LINGLI_ITEM:
                num = sVal.lingli.get(itemId, 0)
                lingLiName = SCD.data.get('lingLiNames', {}).get(itemId, ID.data.get(itemId, {}).get('name', ''))
                if not useRebalance:
                    lingliTxt += '%s %s    ' % (lingLiName, num)
                lingliNum += num

            ret['lingliNum'] = lingliNum
            ret['lingliTxt'] = lingliTxt
            ret['skillName'] = SGTD.data.get(skillId, {}).get('name', '')
            daoHangDes = {}
            for type in gametypes.WUSHUANG_ALL_GEM_TYPES:
                tmpData = {'desc': self.getDirectionDesc(type)}
                cost = wsData.get('wudaoLingliCost', [])
                cnt = ret['daoHangNum'].get(type, 0)
                if cost and cnt < WU_DAO_MAX_STAR:
                    itemId, num = cost[cnt]
                    lingLiName = SCD.data.get('lingLiNames', {}).get(itemId, ID.data.get(itemId, {}).get('name', ''))
                    costTxt = '%s%s' % (lingLiName, num)
                    tmpData['cost'] = num
                    if lingLiName == gameStrings.TEXT_SKILLPROXY_3863:
                        tmpData['type'] = 'lan'
                    elif lingLiName == gameStrings.TEXT_SKILLPROXY_3865:
                        tmpData['type'] = 'lv'
                    elif lingLiName == gameStrings.TEXT_SKILLPROXY_3867:
                        tmpData['type'] = 'hong'
                else:
                    costTxt = 'MAX'
                    tmpData['cost'] = -1
                    tmpData['type'] = None
                tmpData['costTxt'] = costTxt
                tmpData['lvlTxt'] = '' if useRebalance else gameStrings.SKILL_WS_WUDAO_DAOHANG_UP_TITLE
                daoHangDes['daoHang%s' % type] = tmpData

            ret['daoHangDes'] = daoHangDes
            if self.skillId:
                ret['skillInfo'] = {'iconPath': self.__getSkillIcon(self.skillId)}
            ret['useRebalance'] = useRebalance
            ret['rebalanceBtnTips'] = SCD.data.get('rebalanceHelpTips', '')
            ret['enableTianZhaoSkillSet'] = skillId == TIANZHAO_WEN_DAO_SKILL_SET_ID
            return ret

    def checkUseRebalance(self):
        if not gameglobal.rds.configData.get('enableRebalance', False):
            return False
        p = BigWorld.player()
        if p.rebalancing and utils.needRebalanceDataWSWD(p.rebalanceMode):
            return True
        return False

    @ui.callInCD(0.5)
    def refreshHaoHangDirectionPanel(self):
        if self.daoHangDirMediator != None:
            ret = self._genDirectionInfo(self.skillId)
            self.daoHangDirMediator.Invoke('setDaohangPanel', uiUtils.dict2GfxDict(ret, True))
            if gameglobal.rds.ui.itemSelect.mediator:
                self.onOpenItemSelect()
                gameglobal.rds.ui.itemSelect.refreshItemList()

    def _genSpecialSkillContent(self, idx):
        p = BigWorld.player()
        equipSkills = self.equipSkills[idx]
        ret = {'equipedSkills': [],
         'idleSkills': []}
        xiuweiNeed = {1: 10,
         2: 15,
         3: 20,
         4: 25}
        usedXiuwei = 0
        for equipSkillIdx, skillId in enumerate(equipSkills):
            if skillId and p.wsSkills.has_key(skillId):
                starVal = self._getWsSkillStar(skillId)
                wsSkillInfoVal = p.wsSkills.get(skillId, None)
                lv = wsSkillInfoVal.level if wsSkillInfoVal else 1
                wsSkillInfo = p.getSkillInfo(skillId, lv)
                wsSkillItem = self.skillInfoManager.commonSkillIns.getSkillItemInfo(skillId)
                name = wsSkillItem.get('skillName', '')
                skillSlotState = wsSkillItem.get('skillSlotState', uiConst.SKILL_ICON_STAT_GRAY)
                icon = self.__getSkillIcon(skillId)
                levelStr = str(lv)
                wsNeed = skillDataInfo.getWsNeed(wsSkillInfo)
                wsNeed = wsNeed[0] if wsNeed[0] > 0 else wsNeed[1]
                c = len([ 1 for v in wsSkillInfoVal.slots if v[1] == True ])
                xwNeed = xiuweiNeed.get(starVal, 0) + 2 * c
                usedXiuwei += xwNeed
                fireCnt = 0
                windCnt = 0
                hillCnt = 0
                forestCnt = 0
                for slot in wsSkillInfoVal.slots:
                    if slot[1] == True:
                        if slot[2] == gametypes.WUSHUANG_GEM_TYPE_WIND:
                            windCnt += 1
                        elif slot[2] == gametypes.WUSHUANG_GEM_TYPE_WOOD:
                            forestCnt += 1
                        elif slot[2] == gametypes.WUSHUANG_GEM_TYPE_FIRE:
                            fireCnt += 1
                        elif slot[2] == gametypes.WUSHUANG_GEM_TYPE_MOUNTAIN:
                            hillCnt += 1

                daoHangCnt = [windCnt,
                 forestCnt,
                 hillCnt,
                 fireCnt]
            else:
                icon = ''
                name = ''
                levelStr = ''
                wsNeed = 0
                xwNeed = 0
                starVal = 0
                daoHangCnt = [0] * 4
                skillSlotState = uiConst.SKILL_ICON_STAT_GRAY
            if idx == 0:
                keyStr = gameglobal.rds.ui.actionbar.slotKey[uiConst.WUSHUANG_SKILL_START_POS_LEFT + equipSkillIdx]
            else:
                keyStr = gameglobal.rds.ui.actionbar.slotKey[uiConst.WUSHUANG_SKILL_START_POS_RIGHT + equipSkillIdx]
            ar = [{'iconPath': icon},
             name,
             starVal,
             levelStr,
             keyStr,
             xwNeed,
             wsNeed,
             skillId,
             daoHangCnt,
             skillSlotState]
            ret['equipedSkills'].append(ar)

        self.specialSkills[idx] = SPD.data.get(p.realSchool, {}).get('wsType%dSpecialSkills' % (idx + 1), [])
        for equipSkillIdx, skillId in enumerate(self.specialSkills[idx]):
            wsSkillInfoVal = p.wsSkills.get(skillId, None)
            lv = wsSkillInfoVal.level if wsSkillInfoVal else 1
            isOpen = True if wsSkillInfoVal else False
            wsSkillInfo = p.getSkillInfo(skillId, lv)
            wsSkillItem = self.skillInfoManager.commonSkillIns.getSkillItemInfo(skillId)
            name = wsSkillItem.get('skillName', '')
            needLv = wsSkillItem.get('learnLv', 99)
            skillSlotState = wsSkillItem.get('skillSlotState', uiConst.SKILL_ICON_STAT_GRAY)
            starVal = self._getWsSkillStar(skillId)
            wsNeed = skillDataInfo.getWsNeed(wsSkillInfo)
            wsNeed = wsNeed[0] if wsNeed[0] > 0 else wsNeed[1]
            c = len([ 1 for v in wsSkillInfoVal.slots if v[1] == True ]) if wsSkillInfoVal else 0
            xwNeed = xiuweiNeed.get(starVal, 0) + 2 * c
            prof = 0
            if wsSkillInfoVal:
                for val in wsSkillInfoVal.proficiency.values():
                    prof += val

            addXinDeInfo = WSLD.data.get((skillId, lv), {})
            needXinDe = addXinDeInfo.get('maxXd', 100)
            wsStar = 1
            if wsSkillInfoVal:
                skLvStr = '%d/%d' % (wsSkillInfoVal.level, gametypes.WUSHUANG_LV_MAX)
            else:
                wsStar = SGD.data.get((skillId, 1), {}).get('wsStar', 1)
                if wsStar == 3:
                    skLvStr = gameStrings.TEXT_SKILLPROXY_1900
                else:
                    autoNeedLv = SGD.data.get((skillId, 1), {}).get('learnLv', 1)
                    skLvStr = gameStrings.TEXT_SKILLPROXY_1903 % autoNeedLv
                if p.lv < 49:
                    wsStar = 1
            showAddEff = prof >= needXinDe and p.lv >= needLv
            daoHengInfo = self._genDirectionInfo(skillId)
            showPracticeEff = daoHengInfo['value'] >= daoHengInfo['maxValue']
            wsItemId = SGD.data.get((skillId, 1), ()).get('openItem', 410129)
            maxWsitemNum = SGD.data.get((skillId, 1), ()).get('itemNum', 10)
            wsItemNum = BigWorld.player().inv.countItemInPages(wsItemId, enableParentCheck=True)
            wsStarEff = False
            if wsItemNum > maxWsitemNum:
                wsStarEff = True
            ar = [{'iconPath': self.__getSkillIcon(skillId, lv)},
             name,
             starVal,
             skLvStr,
             [xwNeed, wsNeed],
             showAddEff,
             0,
             isOpen,
             showPracticeEff,
             wsStar,
             wsStarEff,
             skillSlotState]
            ret['idleSkills'].append(ar)

        wsVal = p.wushuang1 if idx == 0 else p.wushuang2
        ret['school'] = p.school
        ret['xlPoint'] = wsVal.potential
        ret['wsExp'] = wsVal.exp
        ret['wsMaxExp'] = WED.data.get(wsVal.mwsEnhanceCnt + 1, {}).get('mwsExpCost', 0)
        ret['xiuwei'] = wsVal.getXiuwei(p)
        ret['wsValue'] = int(math.floor(wsVal.getMws(p) / 100.0))
        ret['convertEnabled'] = wsVal.exp >= ret['wsMaxExp']
        ret['usedXiuwei'] = usedXiuwei
        ret['wsAdd'] = int(math.floor(WED.data.get(wsVal.mwsEnhanceCnt + 1, {}).get('mwsAdd', 200) / 100.0))
        ret['showBgAnimation'] = True if ret['wsValue'] > self.lastWushuang[idx] else False
        ret['wsCeil'] = int(p.mws[idx] / 100)
        ret['maxCeil'] = int(SCD.data.get('wsMaxLimit' + str(idx), 10000) / 100)
        self.lastWushuang[idx] = ret['wsValue']
        return ret

    def refreshSpecialSkillWithoutIcon(self):
        if self.wushuangSkillPanelMc != None:
            info = [self._genSpecialSkillContent(0), self._genSpecialSkillContent(1)]
            self.wushuangSkillPanelMc.Invoke('refreshSpecialSkillWithoutIcon', uiUtils.array2GfxAarry(info, True))

    def checkWsExp(self, wsType):
        ws = BigWorld.player().wushuang1 if wsType == gametypes.WS_TYPE_1 else BigWorld.player().wushuang2
        oldWsExp = self.lastWsExpDict.get(wsType)
        self.lastWsExpDict[wsType] = ws.exp
        fullVal = WED.data.get(ws.mwsEnhanceCnt + 1, {}).get('mwsExpCost', 100)
        maxVal = SCD.data.get('wushuangMax', 100)
        wsVal = int(math.floor(ws.getMws(BigWorld.player()) / 100.0))
        if oldWsExp == None or wsVal >= maxVal:
            return
        else:
            if oldWsExp < fullVal and ws.exp >= fullVal:
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WS_LVL_UP, {'data': wsType})
            elif ws.exp < fullVal:
                gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_WS_LVL_UP, {'data': wsType})
            return

    def checkWsProficiency(self, skillId, proficiency):
        totalProficiency = 0
        for item in proficiency.values():
            totalProficiency += item

        lv = BigWorld.player().wsSkills[skillId].level
        addXinDeInfo = WSLD.data.get((skillId, lv), {})
        needXinDe = addXinDeInfo.get('maxXd', 100)
        if totalProficiency >= needXinDe:
            skillLv = BigWorld.player().wsSkills[skillId].level
            nextSkill = SkillInfo(skillId, skillLv + 1)
            if nextSkill and nextSkill.hasSkillData('learnLv'):
                learnLv = nextSkill.getSkillData('learnLv')
                if BigWorld.player().lv < learnLv:
                    return
        bPushed = self.bWsSkillPushed.get(skillId, False)
        if not bPushed and totalProficiency >= needXinDe:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WS_SKILL_LVL_UP_100, {'data': skillId})
            self.bWsSkillPushed[skillId] = True
        elif bPushed and totalProficiency < needXinDe:
            gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_WS_SKILL_LVL_UP_100, {'data': skillId})
            self.bWsSkillPushed[skillId] = False

    def wsExpPushClick(self):
        lastData = gameglobal.rds.ui.pushMessage.getLastData(uiConst.MESSAGE_TYPE_WS_LVL_UP)
        tab = None
        if lastData:
            tab = lastData.get('data')
        self.show(tab)

    def wsProficiencyPushClick(self, pushType):
        lastData = gameglobal.rds.ui.pushMessage.getLastData(pushType)
        if lastData:
            skillId = lastData.get('data')
            skillId and skillId in BigWorld.player().wsSkills.keys() and self.openDetailpanel(skillId)

    def openDetailpanel(self, skillId):
        self.skillId = skillId
        if self.detailMediator:
            self.closeDetailpanel()
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SKILL_DETAIL)
            self.closeDaohangDirPanel()
            if self.enhanceType == uiConst.TYPE_RELIEVE:
                self.closeEnhancePanel()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SKILL_DETAIL)

    def _relieveDaoHang(self, itemId):
        if not BigWorld.player().stateMachine.checkStatus(const.CT_WUSHUANG_CHANGE_GEM):
            return False
        BigWorld.player().cell.resetWudao(self.skillId, itemId)

    def _createPSkillTip(self, skillId):
        p = BigWorld.player()
        lv = 1
        if p.learnedPSkills.has_key(skillId):
            lv = p.learnedPSkills[skillId].level
        desc = PD.data.get((skillId, lv), {}).get('desc', '')
        return GfxValue(gbk2unicode(desc))

    def onCloseLifeSkill(self, *arg):
        self.closeLifeSkill()

    def onCloseGeneralSkill(self, *arg):
        self.closeGeneralSkill()

    def refreshExploreSkill(self, *arg):
        if self.lifeMediator:
            self.lifeMediator.Invoke('updateExploreView', uiUtils.dict2GfxDict(self._genExploreskillInfo(), True))

    def onActivateSkillEnhancement(self, *arg):
        state = arg[3][0].GetBool()
        pos = int(arg[3][1].GetString())
        skillIdx = int(arg[3][2].GetString())
        skillId = self.normalSkills[skillIdx]
        p = BigWorld.player()
        if state:
            p.cell.inactivateSkillEnhancement(skillId, pos)
        else:
            p.cell.activateSkillEnhancement(skillId, pos)

    def _getMaxActiveSkillEnhancement(self, sLv):
        num = 0
        lvArray = const.SKILL_ENHANCE_DICT.items()
        lvArray.sort(key=lambda k: k[0], reverse=True)
        for key, value in lvArray:
            if sLv >= value:
                num = key
                return num

        return num

    def _getPrePart(self, part):
        row, col = part / 10, part % 10
        prePart = row - 1
        if prePart > 0:
            return prePart * 10 + col
        return 0

    def getSkillEnhanceTip(self, part, extraInfo = {}):
        if extraInfo and extraInfo.skillId != None:
            return self.getSkillEnhanceTipBySkillId(extraInfo.skillId, part, extraInfo)
        else:
            return self.getSkillEnhanceTipBySkillId(self.skillId, part, extraInfo)

    def getRequireText(self, requireInfo):
        rareInfo = SCD.data.get('skillEnhScoreTypeInfo', {})
        return gameStrings.SKILL_ENHANCE_REQUIRE_TEXT % (str(requireInfo[1]), rareInfo.get(requireInfo[0], ('', 0))[0])

    def getRareType(self, requireInfo):
        if len(requireInfo) != 2:
            return 0
        rareInfo = SCD.data.get('skillEnhScoreTypeInfo', {})
        return rareInfo.get(requireInfo[0], ('', 0))[1]

    def isRequireScoreEnough(self, skillId, part):
        data = SED.data.get((skillId, part), {})
        requireScore = data.get('requireScore', ())
        if requireScore:
            p = BigWorld.player()
            requireType = requireScore[0]
            requireNum = requireScore[1]
            if p.learnSkillEnhanceScore.get(requireType, 0) < requireNum:
                return False
        return True

    def getSkillEnhanceTipBySkillId(self, skillId, part, extraInfo = {}):
        p = BigWorld.player()
        data = SED.data.get((skillId, part), {})
        if extraInfo and extraInfo.state:
            state = int(extraInfo.state)
            enhancePoint = int(extraInfo.enhancePoint)
            enhanceData = {}
            enhanceData[part] = CSkillEnhanceVal(state, enhancePoint)
        else:
            sVal = p.arenaSkill.get(skillId, None)
            enhanceData = getattr(sVal, 'enhanceData', {})
        pskills = data.get('pskills', ())
        maxLv = len(pskills)
        enhanceName = ''
        otherReuiqreText = ''
        xiuLianRequire = ''
        pskillId, pskillLv = (0, 0)
        itemName = ''
        requireScoreEnough = False
        if pskills:
            pskillId, pskillLv = pskills[0]
            enhanceName = PSTD.data.get(pskillId, {}).get('sname', '')
        if enhanceData.has_key(part):
            lv = enhanceData[part].enhancePoint
            state = enhanceData[part].state
            itemName = ''
            xiuLianRequire = ''
        else:
            lv = 0
            state = const.SKILL_ENHANCE_STATE_UNUSABLE
            if gameglobal.rds.configData.get('enableSkillXiuLianScore', False):
                if data.get('initLearn', 0):
                    xiuLianRequire = gameStrings.SKILL_ENHANCE_NO_REQUIRE_TEXT
                    requireScoreEnough = True
                else:
                    xiuLianRequire = self.getRequireText(data.get('requireScore', (0, 0)))
                    requireScoreEnough = self.isRequireScoreEnough(skillId, part)
                requireJunJieLevel = data.get('requireJunJieLevel', 0)
                requireQuMoLevel = data.get('requireQuMoLevel', 0)
                if requireJunJieLevel:
                    otherReuiqreText = gameStrings.SKILL_ENHANCE_REQUIRE_JUNJIE_TEXT % str(requireJunJieLevel)
                    if p.junJieLv >= requireJunJieLevel:
                        otherReuiqreText = uiUtils.toHtml(otherReuiqreText, '0xF43804')
                    else:
                        otherReuiqreText = uiUtils.toHtml(otherReuiqreText, '0x6DE539')
                elif requireQuMoLevel:
                    otherReuiqreText = gameStrings.SKILL_ENHANCE_REQUIRE_QUMO_TEXT % str(requireQuMoLevel)
                    if p.qumoLv >= requireQuMoLevel:
                        otherReuiqreText = uiUtils.toHtml(otherReuiqreText, '0xF43804')
                    else:
                        otherReuiqreText = uiUtils.toHtml(otherReuiqreText, '0x6DE539')
            else:
                itemId = PD.data.get((pskillId, pskillLv), {}).get('learnItemId', 0)
                if itemId:
                    itemName = ID.data.get(itemId, {}).get('name', ' ')
                else:
                    itemName = ''
        enhanceEffect = []
        needSkilllv = data.get('needSkillLv', ())
        for i in xrange(maxLv):
            needLv = needSkilllv[i]
            pskillId, pskillLv = pskills[i]
            pskillVal = p.pskills.get(pskillId, {}).get(skillId, None)
            pData = pskillVal.pData if pskillVal else {}
            try:
                desc = gameglobal.rds.ui.runeView.generateDesc(pskillId, PSkillInfo(pskillId, pskillLv, pData), pskillLv)
            except:
                desc = ''

            enhanceEffect.append({'lv': needLv,
             'desc': desc})

        prevNeed = data.get('prePoint', 0)
        totalNeed = data.get('totalPoint', 0)
        if extraInfo and extraInfo.canActivate != None:
            canActivate = extraInfo.canActivate
        else:
            canActivate = sVal and sVal.canAddEnhancePoint(p, part, jingJie=p.arenaJingJie)
        needJingJieLv = data.get('needJingjie', 0)
        jingJieState = False
        if p.arenaJingJie >= needJingJieLv:
            jingJieState = True
        else:
            jingJieState = False
        needJineJieDesc = ''
        if needJingJieLv:
            needJineJieDesc = gameStrings.TEXT_SKILLPROXY_4312 + JJD.data.get(needJingJieLv, {}).get('name', gameStrings.TEXT_SKILLPROXY_4312_1)
        if extraInfo and extraInfo.skillLv != None:
            skillLv = extraInfo.skillLv
        else:
            skillLv = sVal.level if sVal else 0
        skillEnhanceInfo = self.getEnhanceGuideData(skillId, part)
        ret = {'enhanceName': enhanceName,
         'lv': lv,
         'maxLv': maxLv,
         'enhanceEffect': enhanceEffect,
         'prevNeed': prevNeed,
         'totalNeed': totalNeed,
         'state': state,
         'itemName': itemName,
         'tipType': 'skillEnhance',
         'canActivate': canActivate,
         'skillLv': skillLv,
         'needJineJieDesc': needJineJieDesc,
         'jingJieState': jingJieState,
         'skillEnhanceInfo': skillEnhanceInfo,
         'otherRequireDesc': otherReuiqreText,
         'xiuLianRequire': xiuLianRequire,
         'requireScoreEnough': requireScoreEnough}
        return ret

    def getEnhanceGuideData(self, skillId, part):
        if not gameglobal.rds.configData.get('enableCareerGuilde', False):
            return ''
        p = BigWorld.player()
        if p.lv <= gametypes.GUIDE_SKILL_LV_REQUIRE:
            return ''
        if hasattr(p, 'carrerGuideData'):
            lvKey, lvTxt = uiUtils.getGuideLv()
            if not p.carrerGuideData.get('skillEnhanceInfo', {}).get(lvKey, {}):
                return ''
            skillEnhanceInfo = p.carrerGuideData.get('skillEnhanceInfo', {}).get(lvKey, {})
            if not skillEnhanceInfo.get(skillId, {}).get(part, []):
                return ''
            enhanceNum = skillEnhanceInfo.get(skillId, {}).get(part, [])[0]
            enhancePercent = int(skillEnhanceInfo.get(skillId, {}).get(part, -1)[1] * 100)
            schoolName = const.SCHOOL_DICT[p.school]
            if enhanceNum < 0:
                return ''
            else:
                return gameStrings.SKILL_ENHANCE_GUIDE_TIP % (lvTxt,
                 schoolName,
                 enhancePercent,
                 enhanceNum)
        else:
            return ''

    def onGetQingGongSkill(self, *arg):
        ret = self._createQingGongSkill()
        return uiUtils.dict2GfxDict(ret, True)

    def _createQingGongSkill(self):
        p = BigWorld.player()
        ret = {'ride': [],
         'qinggong': [],
         'wing': []}
        for key, value in QGSD.data.items():
            order = value.get('order', (-1, -1))
            if value['skillId'] == uiConst.QINGGONG_FLAG_BASIC:
                learned = True
                lv = 1
                icon = value.get('icon', 0)
            else:
                learned = p.qingGongSkills.has_key(key[0])
                if learned:
                    lv = p.qingGongSkills[key[0]].level
                    icon = QGSD.data.get((key[0], lv), {}).get('icon', 0)
                else:
                    lv = ''
                    icon = value.get('icon', 0)
            if icon:
                iconPath = 'misc/%d.dds' % icon
            else:
                iconPath = 'misc/notFound.dds'
            btnEnabled = QGSD.data.get((key[0], lv), {}).has_key('detailChangeDesc')
            if order[0] == uiConst.QINGGONG_TYPE_RIDE and value['lv'] == 1:
                ret['ride'].append({'iconPath': iconPath,
                 'learned': learned,
                 'order': order[1],
                 'lv': lv,
                 'skillId': value['skillId'],
                 'btnEnabled': btnEnabled})
            elif order[0] == uiConst.QINGGONG_TYPE_QINGGONG and value['lv'] == 1:
                ret['qinggong'].append({'iconPath': iconPath,
                 'learned': learned,
                 'order': order[1],
                 'lv': lv,
                 'skillId': value['skillId'],
                 'btnEnabled': btnEnabled})
            elif order[0] == uiConst.QINGGONG_TYPE_WING and value['lv'] == 1:
                ret['wing'].append({'iconPath': iconPath,
                 'learned': learned,
                 'order': order[1],
                 'lv': lv,
                 'skillId': value['skillId'],
                 'btnEnabled': btnEnabled})

        for value in ret.values():
            value.sort(key=lambda k: k['order'])

        return ret

    def onOpenGuide(self, *arg):
        guideType = int(arg[3][0].GetNumber())
        gameglobal.rds.ui.lifeSkillGuide.show(guideType)

    def createSkillPracticeInfo(self, key):
        ret = {}
        if not key or not isinstance(key, str) or key.find('.') < 0:
            return uiUtils.dict2GfxDict(ret, True)
        else:
            _, slot = self.getSlotID(key)
            p = BigWorld.player()
            if self.isSkillRemoveMode and p.school != self.selectedSchool:
                skillId = self.getSelectedSchoolSkillList()[slot]
            else:
                skillId = self.normalSkills[slot]
            self.skillId = skillId
            skInfoVal = p.arenaSkill.get(skillId, None)
            skillEnhData = getattr(skInfoVal, 'enhanceData', {})
            enhanceData = []
            for i in xrange(const.MAX_XIULIAN_ROW):
                rowData = []
                for j in xrange(const.MAX_XIULIAN_COLUMN):
                    index = int('%d%d' % (i + 1, j + 1))
                    data = SED.data.get((skillId, index), {})
                    prePoint = data.get('prePoint', 0)
                    requireInfo = data.get('requireScore', [])
                    rareType = self.getRareType(requireInfo)
                    if self.isRemoveOldSchoolSkill():
                        canActivate = False
                        isJingjie = True
                        curPoint = 0
                        maxPoint = len(data.get('pskills', ()))
                        activated = index in p.canRemoveSkillEnhances.get(self.selectedSchool, {}).get(skillId, [])
                        canRemove = activated and SED.data.get((skillId, index), {}).get('itemIdsOnRemove', None)
                        state = const.SKILL_ENHANCE_STATE_INACTIVE if activated or data.get('initLearn', 0) else const.SKILL_ENHANCE_STATE_UNUSABLE
                        visible = data != {}
                    else:
                        canActivate = skInfoVal and skInfoVal.canAddEnhancePoint(p, index, jingJie=p.arenaJingJie)
                        isJingjie = True
                        if data.get('needJingjie', 1) > 1 and p.arenaJingJie < data.get('needJingjie', 1):
                            isJingjie = False
                        if skillEnhData.has_key(index):
                            visible = True
                            state = skillEnhData[index].state
                            curPoint = skillEnhData[index].enhancePoint
                            maxPoint = len(data.get('pskills', ()))
                        elif data.get('initLearn', 0):
                            visible = True
                            state = const.SKILL_ENHANCE_STATE_INACTIVE
                            curPoint = 0
                            maxPoint = len(data.get('pskills', ()))
                        else:
                            visible = data != {}
                            state = const.SKILL_ENHANCE_STATE_UNUSABLE
                            curPoint = 0
                            maxPoint = 0
                        canRemove = self.isSkillRemoveMode and index in p.canRemoveSkillEnhances.get(self.selectedSchool, {}).get(self.skillId, []) and SED.data.get((skillId, index), {}).get('itemIdsOnRemove', None)
                    rowData.append({'visible': visible,
                     'state': state,
                     'curPoint': curPoint,
                     'maxPoint': maxPoint,
                     'prePoint': prePoint,
                     'canActivate': canActivate,
                     'isJingjie': isJingjie,
                     'canRemove': canRemove,
                     'rareType': rareType})

                enhanceData.append(rowData)

            ret = {'enhanceData': enhanceData,
             'school': p.school}
            return uiUtils.dict2GfxDict(ret, True)

    def isRemoveOldSchoolSkill(self):
        return self.isSkillRemoveMode and BigWorld.player().school != self.selectedSchool

    def _getUsedEnhancePoint(self):
        ret = 0
        for skVal in BigWorld.player().skills.values():
            if hasattr(skVal, 'enhanceData'):
                for enhData in skVal.enhanceData.values():
                    ret += enhData.enhancePoint

        return ret

    def _getEnhanceState(self, skillVal, index, type = 0):
        for i in xrange(index * uiConst.SKILL_ENHANCE_NUM_PER_DIR, (index + 1) * uiConst.SKILL_ENHANCE_NUM_PER_DIR):
            if skillVal.enhanceData.get(i, None):
                if not type:
                    return (skillVal.enhanceData[i], i)
                if type == skillVal.enhanceData[i]:
                    return (skillVal.enhanceData[i], i)

        return (const.SKILL_ENHANCE_STATE_UNUSABLE, -1)

    def isEnhanceActivate(self, skillVal, index):
        for i in xrange(index * uiConst.SKILL_ENHANCE_NUM_PER_DIR, (index + 1) * uiConst.SKILL_ENHANCE_NUM_PER_DIR):
            if skillVal.enhanceData.has_key(i) and skillVal.enhanceData[i] == const.SKILL_ENHANCE_STATE_ACTIVE:
                return True

        return False

    def isEnhanceUnactivate(self, skillVal, index):
        for i in xrange(index * uiConst.SKILL_ENHANCE_NUM_PER_DIR, (index + 1) * uiConst.SKILL_ENHANCE_NUM_PER_DIR):
            if skillVal.enhanceData.has_key(i) and skillVal.enhanceData[i] == const.SKILL_ENHANCE_STATE_INACTIVE:
                return True

        return False

    def refreshSkillPracticeInfo(self, skillId):
        self.skillId = skillId
        key = self._getKeyByNormalSkillId(skillId)
        if self.commonSkillMc:
            self.commonSkillMc.Invoke('setSkillPracticeInfo', GfxValue(key))

    def refreshSkillEnhanceLv(self):
        if self.commonSkillMc:
            self.commonSkillMc.Invoke('setEnhanceLvInfo')

    def refreshSkillList(self):
        if self.commonSkillMc:
            self.commonSkillMc.Invoke('setSkillList')

    def onGetSkillPracticeInfo(self, *arg):
        key = arg[3][0].GetString()
        ret = self.createSkillPracticeInfo(key)
        return ret

    def onCloseSkillPractice(self, *arg):
        self.closeSkillPractice()

    def applyPractice(self):
        p = BigWorld.player()
        for i in xrange(uiConst.SKILL_ENHANCE_DIR_NUM):
            for j in xrange(uiConst.SKILL_ENHANCE_NUM_PER_DIR):
                pos = i * uiConst.SKILL_ENHANCE_NUM_PER_DIR + j
                p.cell.inactivateSkillEnhancement(self.skillId, pos)

    def onConfirmPractice(self, *arg):
        self.applyPractice()
        self.closeSkillPractice()

    def onCancelPractice(self, *arg):
        self.closeSkillPractice()

    def onApplyPractice(self, *arg):
        self.applyPractice()

    def onEquipSkillPracitce(self, *arg):
        dstKey = arg[3][0].GetString()
        srcKey = arg[3][1].GetString()
        idBar, idSlot = self.getSlotID(dstKey)
        _, srcSlot = self.getSlotID(srcKey)
        srcSlot = (srcSlot - uiConst.SKILL_ENHANCE_DIR_NUM) % uiConst.SKILL_ENHANCE_NUM_PER_DIR
        self.setItem('%d_%d' % (idSlot, srcSlot), idBar, idSlot)

    def onUnEquipSkillPractice(self, *arg):
        key = arg[3][0].GetString()
        self.delSlotItem(key)

    def refreshQingGongPanel(self):
        if self.mediator:
            self.mediator.Invoke('setQinggongContent', uiUtils.dict2GfxDict(self._createQingGongSkill(), True))

    def onLvUpQinggong(self, *arg):
        idx = int(arg[3][0].GetNumber())
        BigWorld.player().cell.qingGongSkillLevelUp(idx)

    def checkJinejieValid(self, part):
        p = BigWorld.player()
        data = SED.data.get((self.skillId, part), {})
        if not self.isRemoveOldSchoolSkill() and data.get('needJingjie', 1) > 1 and p.arenaJingJie < data.get('needJingjie', 1):
            return False
        return True

    def onAddSkillEnhancePoint(self, *arg):
        part = int(arg[3][0].GetString())
        if not self.isEditMode:
            if not self.checkJinejieValid(part):
                BigWorld.player().showGameMsg(GMDD.data.ENHANCE_SKILL_FORBIDDEN_NEED_JINGJIE, ())
            else:
                BigWorld.player().cell.addSkillEnhancePoint(self.skillId, part)
        else:
            self.updateSkillEnhanceScheme(self.skillId, part, 1)

    def onIsChaos(self, *args):
        p = BigWorld.player()
        return GfxValue(p.isInBfChaos())

    def onUnLockEnhancePoint(self, *arg):
        if not gameglobal.rds.configData.get('enableSkillXiuLianScore', False):
            return
        part = int(arg[3][0].GetString())
        data = SED.data.get((self.skillId, part), {})
        if not self.isRequireScoreEnough(self.skillId, part):
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.SKILL_ENHANCE_SCORE_NOT_ENOUGH,))
            return
        requireInfo = data.get('requireScore', ())
        if requireInfo:
            msg = gameStrings.SKILL_ENHANCE_UNLOCK_CONFIRM % self.getRequireText(requireInfo)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.conrfirmUnlockEnhancePoint, self.skillId, part))

    def conrfirmUnlockEnhancePoint(self, skillId, part):
        p = BigWorld.player()
        p.cell.learnSkillEnhancementByScore(skillId, part)

    def onReduceSkillEnhancePoint(self, *arg):
        if not BigWorld.player().stateMachine.checkStatus(const.CT_CHANGE_SKILL_ENHANCE):
            return
        part = int(arg[3][0].GetString())
        if not self.isEditMode:
            BigWorld.player().cell.reduceSkillEnhancePoint(self.skillId, part)
        else:
            self.updateSkillEnhanceScheme(self.skillId, part, -1)

    def onRemoveSkill(self, *args):
        part = int(args[3][0].GetString())
        text = GMD.data.get(GMDD.data.REMOVE_ENHANCE_SKILL_CONFIRM, {}).get('text', '%s')
        text = text % self.getRemoveEnhanceSkillRewardStr(self.skillId, part)
        func = Functor(BigWorld.player().cell.removeSkillEnhance, self.selectedSchool, self.skillId, part)
        self.uiAdapter.messageBox.showYesNoMsgBox(text, func)

    def onGetSkillEnhanceAllSchool(self, *arsg):
        dataList = []
        schoolList = BigWorld.player().canRemoveSkillEnhances.keys()
        schoolList.sort()
        schoolIndex = schoolList.index(self.selectedSchool)
        schoolIndex = max(0, schoolIndex)
        for id in schoolList:
            dataList.append(SD.data.get(id, {}).get('name', ''))

        dataList.append(schoolIndex)
        return uiUtils.array2GfxAarry(dataList, True)

    def onChangeSchool(self, *args):
        index = int(args[3][0].GetNumber())
        self.canRemoveSkillList = []
        schoolList = BigWorld.player().canRemoveSkillEnhances.keys()
        schoolList.sort()
        if index < len(schoolList):
            self.selectedSchool = schoolList[index]
            self.commonSkillMc.Invoke('initXiuLian')

    def getRemoveEnhanceSkillRewardStr(self, skillId, part):
        itemIdsOnRemove = SED.data.get((skillId, part), {}).get('itemIdsOnRemove', {})
        rewardStr = ''
        for itemId, cnt in itemIdsOnRemove.iteritems():
            itemName = uiUtils.getItemColorNameWithClickTips(itemId, cnt)
            if rewardStr:
                rewardStr += ','
            rewardStr += itemName

        skillName = SED.data.get((skillId, part), {}).get('name', {})
        return (skillName, rewardStr)

    def getSelectedSchoolSkillList(self):
        if not self.canRemoveSkillList:
            self.canRemoveSkillList = BigWorld.player().canRemoveSkillEnhances.get(self.selectedSchool, {}).keys()
            self.canRemoveSkillList.sort()
        return self.canRemoveSkillList

    def updateSkillEnhanceScheme(self, skillId, part, offset):
        p = BigWorld.player()
        skillPointScheme = p.getSpecialSkillPoint()
        value = skillPointScheme.get(skillId, {}).get('enhanceData', {}).get(part, {}).get('enhancePoint', 0)
        if value + offset >= 0:
            if self.uiAdapter.skillSchemeV2.editorIndex == const.SKILL_SCHEME_WINGWORLD:
                p.base.updateSkillEnhanceSchemeEx(const.SKILL_SCHEME_WINGWORLD, skillId, [part], [value + offset])
            elif self.uiAdapter.skillSchemeV2.editorIndex == const.SKILL_SCHEME_CROSS_BF:
                p.base.updateSkillEnhanceSchemeEx(const.SKILL_SCHEME_CROSS_BF, skillId, [part], [value + offset])
            else:
                p.base.updateSkillEnhanceSchemeEx(const.SKILL_SCHEME_ARENA, skillId, [part], [value + offset])

    def onResetSkillEnhancePoint(self, *arg):
        if not BigWorld.player().stateMachine.checkStatus(const.CT_CHANGE_SKILL_ENHANCE):
            return
        BigWorld.player().cell.resetSkillEnhancePoint(self.skillId)

    def onShowXiuLianAward(self, *arg):
        if not BigWorld.player().stateMachine.checkStatus(const.CT_CHANGE_SKILL_ENHANCE):
            return
        gameglobal.rds.ui.xiuLianAward.show()

    def onGetSkillEnhancePoint(self, *arg):
        if gameglobal.rds.configData.get('enableSkillDiKou', False):
            gameglobal.rds.ui.getSkillPoint.show()
        else:
            p = BigWorld.player()
            nextEnhPoint = self._getUsedEnhancePoint() + p.skillEnhancePoint + 1
            nextInfo = SECD.data.get(nextEnhPoint, None)
            if nextInfo:
                msg = GMD.data.get(GMDD.data.ENHANCE_SKILL_CONSUME_CASH_LINGSHI_NOTIFY, {}).get('text', gameStrings.TEXT_SKILLPROXY_4682)
                msg = msg % (nextInfo.get('exp', 0), nextInfo.get('cash', 0))
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.gotoGetSkillEnhancePoint, nextInfo.get('exp', 0), nextInfo.get('cash', 0), self.runServerSkillEnhancePoint))

    def gotoGetSkillEnhancePoint(self, expl, cost, callFunction):
        p = BigWorld.player()
        if p.expXiuWei < expl and p.bindCash < cost:
            msg = GMD.data.get(GMDD.data.ENHANCE_SKILL_CONSUME_EXP_COIN_NOTIFY, {}).get('text', gameStrings.TEXT_SKILLPROXY_4691)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=callFunction, msgType='expXiuWeiBindCash', isShowCheckBox=True)
        elif p.expXiuWei < expl:
            msg = GMD.data.get(GMDD.data.ENHANCE_SKILL_CONSUME_EXP_NOTIFY, {}).get('text', gameStrings.TEXT_SKILLPROXY_4694)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=callFunction, msgType='expXiuWei', isShowCheckBox=True)
        elif p.bindCash < cost:
            msg = GMD.data.get(GMDD.data.ENHANCE_SKILL_CONSUME_COIN_NOTIFY, {}).get('text', gameStrings.TEXT_SKILLPROXY_1402)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=callFunction, msgType='bindCash', isShowCheckBox=True)
        else:
            callFunction()

    def runServerSkillEnhancePoint(self):
        p = BigWorld.player()
        p.cell.getSkillEnhancePoint(0)

    def onSelectPlan(self, *arg):
        index = int(arg[3][0].GetNumber())
        if index != BigWorld.player().skillPointSchemeIndex:
            gamelog.info('jjh@switchSkillPointScheme ', index)
            BigWorld.player().base.switchSkillPointScheme(index)

    def onGetSkillEnhanceSchemeIndex(self, *arg):
        return GfxValue(BigWorld.player().skillPointSchemeIndex)

    def onGetWsEffect(self, *arg):
        return GfxValue(gameglobal.showWsEffect)

    def onSetWsEffect(self, *arg):
        gameglobal.showWsEffect = int(arg[3][0].GetBool())
        appSetting.VideoQualitySettingObj.setWsEffect(gameglobal.showWsEffect)

    gameStrings.TEXT_SKILLPROXY_4724

    def wushuangSkillDragFromOrig2Slot(self, srcPage, srcPos, desPage, desPos):
        p = BigWorld.player()
        srcType = int(srcPos / MAX_SPECIAL_SKILL_NUMS)
        desType = int(desPos / MAX_EQUIP_SKILL_NUMS)
        if srcType != desType:
            return
        srcSkillId = self.getActionIDByPos(srcPage, srcPos)
        desSkillId = self.getActionIDByPos(desPage, desPos)
        if not self._checkWsSkillValue(srcSkillId, desPage):
            return
        if not self.skillEquipCheck():
            return
        if desSkillId != 0 and desSkillId != srcSkillId:
            p.cell.removeWsSkill(desSkillId)
        if self.wushuangSkillSelected(srcSkillId):
            self.setItem(srcSkillId, desPage, desPos)
            return
        self.wushuangSkillKV[srcSkillId] = desPos
        p.cell.addWsSkill(srcSkillId)

    def wushuangSkillDragFromSlot2Slot(self, srcPage, srcPos, desPage, desPos):
        srcType = int(srcPos / MAX_EQUIP_SKILL_NUMS)
        desType = int(desPos / MAX_EQUIP_SKILL_NUMS)
        if srcType != desType:
            return
        if not self.skillEquipCheck():
            return
        srcSkillId = self.getActionIDByPos(srcPage, srcPos)
        desSkillId = self.getActionIDByPos(desPage, desPos)
        self.setItem(desSkillId, srcPage, srcPos)
        self.setItem(srcSkillId, desPage, desPos)

    def wsSkillChangeFromShortCut(self, newShortCut):
        if not self.skillEquipCheck():
            return
        p = BigWorld.player()
        oldShortCut = uiUtils.getWSSkillShortCut(gameglobal.rds.ui.actionbar.clientShortCut)
        oldSkillList = []
        newSkillList = []
        newSkillDict = {}
        for i in xrange(uiConst.WUSHUANG_SKILL_START_POS_LEFT, uiConst.WUSHUANG_SKILL_END_POS):
            key = (uiConst.SKILL_ACTION_BAR, i)
            oldSkillId = oldShortCut.get(key, (0, 0))[1]
            oldSkillList.append(oldSkillId)
            newSkillId = newShortCut.get(key, (0, 0))[1]
            newSkillList.append(newSkillId)
            newSkillDict[newSkillId] = (uiConst.SKILL_PANEL_SPECIAL_RIGHT, i - uiConst.WUSHUANG_SKILL_START_POS_LEFT)

        for skillId in oldSkillList:
            if skillId == 0:
                continue
            if skillId in newSkillDict:
                page, pos = newSkillDict.pop(skillId)
                self.setItem(skillId, page, pos)
            else:
                p.cell.removeWsSkill(skillId)

        for skillId in newSkillList:
            if skillId == 0:
                continue
            if skillId in newSkillDict:
                page, pos = newSkillDict.pop(skillId)
                self.wushuangSkillKV[skillId] = pos
                p.cell.addWsSkill(skillId)

    def wushuangSkillSelectDone(self, skillId, select):
        if not skillId:
            return
        if select:
            self.addWushuangShortCut(skillId)
        else:
            self.removeWushuangShortCut(skillId)

    def addWushuangShortCut(self, skillId):
        if skillId not in self.wushuangSkillKV:
            return
        self.setItem(skillId, uiConst.SKILL_PANEL_SPECIAL_RIGHT, self.wushuangSkillKV[skillId])
        self.wushuangSkillKV.pop(skillId)

    def removeWushuangShortCut(self, skillId):
        actionbar = gameglobal.rds.ui.actionbar
        keys = actionbar._getPosByActionID(skillId)
        for item in keys:
            bar, slot = actionbar.getSlotID(item)
            idSlot = slot - uiConst.WUSHUANG_SKILL_START_POS_LEFT
            self.setItem(0, uiConst.SKILL_PANEL_SPECIAL_RIGHT, idSlot)

    def wushuangSkillSelected(self, skillId):
        p = BigWorld.player()
        currSchemeNo = gameglobal.rds.ui.actionbar.currSchemeNo
        selWsList = []
        if currSchemeNo == uiConst.SHORT_CUT_CASE_1:
            selWsList = p.wushuang1.selectedWs + p.wushuang2.selectedWs
        elif currSchemeNo == uiConst.SHORT_CUT_CASE_2:
            selWsList = p.wushuang1.selectedWs1 + p.wushuang2.selectedWs1
        elif currSchemeNo == uiConst.SHORT_CUT_CASE_3:
            selWsList = p.wushuang1.selectedWs2 + p.wushuang2.selectedWs2
        return skillId in selWsList

    def skillEquipCheck(self):
        p = BigWorld.player()
        if not p.stateMachine.checkStatus(const.CT_EQUIP_WS_SKILL):
            p.showTopMsg(gameStrings.TEXT_SKILLPROXY_4848)
            return False
        if p.inCombat:
            p.showTopMsg(gameStrings.TEXT_SKILLPROXY_4852)
            p.chatToEventEx(gameStrings.TEXT_SKILLPROXY_4852, const.CHANNEL_COLOR_RED)
            return False
        return True

    def initAirSkillData(self):
        p = BigWorld.player()
        self.cfgedAirSkills[0] = SPD.data.get(p.school, {}).get('airSkills', [])
        self.cfgedAirSkills[1] = SPD.data.get(p.school, {}).get('airPsSkills', [])
        gameStrings.TEXT_SKILLPROXY_4866
        self.equipedAirSkills = gameglobal.rds.ui.airbar.airShortCut

    def onRegisterAirSkillMc(self, *arg):
        self.airSkillPanelMc = arg[3][0]

    def onUnRegisterAirSkillMc(self, *arg):
        self.airSkillPanelMc = None

    def onGetAirBattleSkills(self, *arg):
        ret = self.genAllAirSkillContent()
        return uiUtils.dict2GfxDict(ret, True)

    def onGetAirSkillbarInfo(self, *arg):
        ret = self.genAirSkillbarInfo()
        return uiUtils.dict2GfxDict(ret, True)

    def onDelAirSkillSlot(self, *arg):
        if arg[3][0] is None:
            return
        else:
            type, idx = self.getSlotID(arg[3][0].GetString())
            if type != uiConst.SKILL_PANEL_AIR_SLOT:
                return
            skillId = self.equipedAirSkills[idx][1]
            if skillId != 0:
                BigWorld.player().cell.disableAirSkill(skillId)
            self.setAirSkillItem(0, idx)
            return

    def onGetAirSkillSwitchOn(self, *arg):
        enableAirSkill = gameglobal.rds.configData.get('enableAirSkill', False)
        return GfxValue(enableAirSkill)

    def inAirBattleState(self):
        enableAirSkill = gameglobal.rds.configData.get('enableAirSkill', False)
        if not enableAirSkill:
            return False
        return BigWorld.player().inFly == 1

    def genAirSkillbarInfo(self):
        ret = {}
        p = BigWorld.player()
        shortCutInfo = {}
        for i in range(len(self.equipedAirSkills)):
            skillId = self.equipedAirSkills[i][1]
            if skillId > 0:
                shortCutInfo[i] = self.genAirSkillContentById(skillId)
            else:
                shortCutInfo[i] = None

        jingjieNames = {}
        jjdd = JJD.data
        for j in jjdd:
            jingjieNames[j] = jjdd[j].get('name', gameStrings.TEXT_SKILLPROXY_3768_1)

        ret['xiuwei'] = p.airXiuwei
        ret['openSlotNum'] = self.getOpenSlotNum(p.airXiuwei, p.jingJie)
        ret['airXiuweiNeed'] = SCD.data.get('airXiuweiNeed', {1: 0})
        ret['airJingjieNeed'] = SCD.data.get('airJingJieNeed', {1: 0})
        ret['jingjieData'] = jingjieNames
        ret['airShortCut'] = shortCutInfo
        ret['slotKey'] = gameglobal.rds.ui.airbar.airbarSlotKey()
        ret['operationMode'] = p.getOperationMode()
        return ret

    def genAirSkillContentById(self, skillId):
        ret = {}
        pSkill = False
        p = BigWorld.player()
        cInfo = skillDataInfo.ClientSkillInfo(skillId)
        pInfo = p.airSkills.get(skillId, None)
        pSkill = skillId in self.cfgedAirSkills[1]
        icon = cInfo.getSkillData('icon', 'notFound')
        lv = pInfo.level if pInfo else 0
        name = SGTD.data.get(skillId, {}).get('name', '')
        si = None
        if pSkill:
            si = PSkillInfo(skillId, min(lv + 1, const.MAX_SKILL_LEVEL))
        else:
            si = SkillInfo(skillId, min(lv + 1, const.MAX_SKILL_LEVEL))
        state, extra = self.checkAirSkillState(si)
        self.appendAirSkillLvUpNeed(ret, si)
        ret['iconPath'] = 'skill/icon64/%s.dds' % icon
        ret['lv'] = lv
        ret['maxLv'] = const.MAX_SKILL_LEVEL
        ret['name'] = name
        ret['skillId'] = skillId
        ret['state'] = state
        ret['extra'] = extra
        ret['roleLv'] = p.lv
        ret['needLv'] = si.getSkillData('learnLv')
        return ret

    def getOpenSlotNum(self, xiuwei, jingjie):
        airXiuweiNeed = SCD.data.get('airXiuweiNeed', {1: 0})
        airJingjieNeed = SCD.data.get('airJingJieNeed', {1: 0})
        openNum = 0
        for i in range(1, 9):
            xiuweiNeed = airXiuweiNeed.get(i, sys.maxint)
            jingjieNeed = airJingjieNeed.get(i, sys.maxint)
            if xiuwei >= xiuweiNeed and jingjie >= jingjieNeed:
                openNum = i
            else:
                break

        return openNum

    def genAllAirSkillContent(self):
        ret = {}
        airSkills = []
        psSkills = []
        for i in range(0, len(self.cfgedAirSkills[0])):
            skillInfo = self.genAirSkillContentById(self.cfgedAirSkills[0][i])
            airSkills.append(skillInfo)

        for i in range(0, len(self.cfgedAirSkills[1])):
            skillInfo = self.genAirSkillContentById(self.cfgedAirSkills[1][i])
            psSkills.append(skillInfo)

        airSkills.append(len(airSkills))
        psSkills.append(len(psSkills))
        ret['airSkills'] = airSkills
        ret['psSkills'] = psSkills
        return ret

    def onLearnNewAirSkill(self, skillId):
        if self.airSkillPanelMc is None:
            if self.mediator:
                self.hide()
            self.show(4)
        if skillId not in self.cfgedAirSkills[0]:
            return
        else:
            srcPos = self.cfgedAirSkills[0].index(skillId)
            desPos = -1
            p = BigWorld.player()
            openSlogNum = self.getOpenSlotNum(p.airXiuwei, p.jingJie)
            for i in range(openSlogNum):
                if self.equipedAirSkills[i][1] == 0:
                    desPos = i
                    break

            if desPos < 0:
                return
            self.airSkillDragFromOrig2Slot(srcPos, desPos)
            return

    def refreshAirSkillById(self, id):
        if self.airSkillPanelMc is None:
            return
        else:
            isAirPsSkill = False
            if id in self.cfgedAirSkills[0]:
                isAirPsSkill = False
                idx = self.cfgedAirSkills[0].index(id)
            elif id in self.cfgedAirSkills[1]:
                isAirPsSkill = True
                idx = self.cfgedAirSkills[1].index(id)
            else:
                return
            skillData = self.genAirSkillContentById(id)
            self.airSkillPanelMc.Invoke('updateAirSkill', (uiUtils.dict2GfxDict(skillData, True), GfxValue(idx), GfxValue(isAirPsSkill)))
            return

    def refreshAirSkillPanel(self):
        if self.airSkillPanelMc is None:
            return
        else:
            info = self.genAllAirSkillContent()
            self.airSkillPanelMc.Invoke('refreshAirSkills', (uiUtils.array2GfxAarry(info['airSkills'], True), GfxValue(False)))
            self.airSkillPanelMc.Invoke('refreshAirSkills', (uiUtils.array2GfxAarry(info['psSkills'], True), GfxValue(True)))
            return

    def refreshAirSkillbar(self):
        if self.airSkillPanelMc is None:
            return
        else:
            info = self.genAirSkillbarInfo()
            self.airSkillPanelMc.Invoke('refreshAirSkillbarInfo', uiUtils.dict2GfxDict(info, True))
            return

    def checkAirSkillState(self, skillInfo):
        extra = {}
        p = BigWorld.player()
        if not p.airSkills.has_key(skillInfo.num):
            return (self.SKILL_STATE_UNSTUDIED, extra)
        pInfo = p.airSkills[skillInfo.num]
        if pInfo.level != const.MAX_SKILL_LEVEL:
            pass
        else:
            return (self.SKILL_STATE_TOP_LEVEL, extra)
        if skillInfo.hasSkillData('learnLv'):
            learnLv = skillInfo.getSkillData('learnLv')
            extra['learnLv'] = learnLv
            if p.lv < learnLv:
                return (self.SKILL_STATE_CAN_NOT_STUDY_LV, extra)
        else:
            extra['learnLv'] = 0
        if skillInfo.hasSkillData('learnGold'):
            learnGold = skillInfo.getSkillData('learnGold')
            extra['money'] = learnGold
            if p.cash + p.bindCash < learnGold:
                return (self.SKILL_STATE_CAN_NOT_STUDY_MONEY, extra)
        else:
            extra['money'] = 0
        return (self.SKILL_STATE_CAN_STUDY, extra)

    def appendAirSkillLvUpNeed(self, ret, skillNextInfo):
        p = BigWorld.player()
        if not p.airSkills.has_key(skillNextInfo.num):
            ret['expValue'] = 0
            ret['expNeed'] = 100
            return
        else:
            tips = []
            addExpInfo = ASLD.data.get((skillNextInfo.num, skillNextInfo.lv - 1), {})
            sVal = p.airSkills[skillNextInfo.num]
            gameStrings.TEXT_SKILLPROXY_3554
            if addExpInfo.get('useAddExp', 0) > 0:
                tip = {}
                tip['hint'] = gameStrings.TEXT_SKILLPROXY_5118
                tip['add'] = addExpInfo.get('useAddExp', 0)
                tip['value'] = sVal.exp.get('skill', 0)
                tip['max'] = addExpInfo.get('useAddExpMax', 0)
                tips.append(tip)
            gameStrings.TEXT_SKILLPROXY_3563
            addExps = []
            itemAddExp = addExpInfo.get('itemAddExp', [])
            for item in itemAddExp:
                addExp = {}
                itemId = item[0]
                addExp['hint'] = gameStrings.TEXT_SKILLPROXY_3570
                addExp['add'] = item[1]
                addExp['value'] = sVal.exp.get('item' + str(itemId), 0)
                addExp['max'] = item[2]
                addExp['itemId'] = itemId
                addExp['itemCount'] = p.inv.countItemInPages(itemId, enableParentCheck=True)
                addExp['iconPath'] = uiUtils.getItemIconFile64(itemId)
                addExps.append(addExp)

            exp = 0
            for val in sVal.exp.values():
                if val is not None:
                    exp += val

            ret['tips'] = tips
            ret['itemAddExp'] = addExps
            ret['needExp'] = addExpInfo.get('maxExp', 100)
            ret['skillExp'] = min(exp, ret['needExp'])
            return

    def genAirSkillDetaiInfo(self):
        """basic info """
        ret = self.genAirSkillContentById(self.skillId)
        ret['airSkill'] = True
        ret['school'] = BigWorld.player().realSchool
        return ret

    def getAirSkillIdByPanelPos(self, pos):
        if pos < uiConst.MAX_AIRBAR_SLOT_NUM:
            return self.cfgedAirSkills[0][pos]
        else:
            pos -= uiConst.MAX_AIRBAR_SLOT_NUM
            return self.cfgedAirSkills[1][pos]

    def airSkillDragFromOrig2Slot(self, srcPos, desPos):
        p = BigWorld.player()
        if desPos >= self.getOpenSlotNum(p.airXiuwei, p.jingJie):
            return
        gameStrings.TEXT_SKILLPROXY_5172
        srcSkillId = self.getAirSkillIdByPanelPos(srcPos)
        desSkillId = self.equipedAirSkills[desPos][1]
        if desSkillId != 0 and srcSkillId != desSkillId:
            p.cell.disableAirSkill(desSkillId)
        if p.airSkills[srcSkillId].enable:
            self.setItem(srcSkillId, uiConst.SKILL_PANEL_AIR_SLOT, desPos)
        else:
            self.activeAirSkillKV[srcSkillId] = desPos
            p.cell.enableAirSkill(srcSkillId)

    def airSkillActiveDone(self, skillId, enable):
        if skillId not in self.activeAirSkillKV:
            return
        if enable:
            self.setItem(skillId, uiConst.SKILL_PANEL_AIR_SLOT, self.activeAirSkillKV[skillId])
            self.activeAirSkillKV.pop(skillId)

    def airSkillDragFromSlot2Slot(self, srcPos, desPos):
        p = BigWorld.player()
        slotNum = self.getOpenSlotNum(p.airXiuwei, p.jingJie)
        if srcPos >= slotNum or desPos >= slotNum:
            return
        srcSkillId = self.equipedAirSkills[srcPos][1]
        desSkillId = self.equipedAirSkills[desPos][1]
        self.setItem(srcSkillId, uiConst.SKILL_PANEL_AIR_SLOT, desPos)
        self.setItem(desSkillId, uiConst.SKILL_PANEL_AIR_SLOT, srcPos)

    def setAirSkillItem(self, skillId, slotPos):
        p = BigWorld.player()
        gameStrings.TEXT_SKILLPROXY_5209
        if skillId != 0 and not p.airSkills.has_key(skillId):
            return
        if not p.stateMachine.checkStatus(const.CT_EQUIP_AIR_SKILL):
            p.showTopMsg(gameStrings.TEXT_SKILLPROXY_4848)
            return
        if p.inCombat:
            p.showTopMsg(gameStrings.TEXT_SKILLPROXY_5218)
            return
        self.equipedAirSkills[slotPos] = (0, skillId)
        self.checkAirSkillEquipDuplicate(skillId, slotPos)
        self.refreshAirSkillbar()
        gameglobal.rds.ui.airbar.setAirSkillItem(skillId, slotPos)

    def checkAirSkillEquipDuplicate(self, skillId, slotPos):
        if uiConst.AIR_BAR_SLOT_DUPLICABLE:
            return
        for i in range(len(self.equipedAirSkills)):
            if self.equipedAirSkills[i][1] == skillId and slotPos != i and skillId != 0:
                self.setItem(0, uiConst.SKILL_PANEL_AIR_SLOT, i)

    def _getWSWudaoItmes(self, skillId):
        data = WSCD.data.get(skillId, {})
        if data:
            return (data.get('wudaoItem', ()), data.get('wudaoItemNum', ()))

    def onIsSkillRemoveMode(self, *args):
        return GfxValue(self.isSkillRemoveMode)

    @ui.checkInventoryLock()
    def onChangeSkillRemoveMode(self, *args):
        self.isSkillRemoveMode = not self.isSkillRemoveMode
        self.commonSkillMc.Invoke('refreshSkillRemoveMode', GfxValue(True))

    def onGetEnableSkillGuide(self, *args):
        return GfxValue(True)

    def onQuitEditMode(self, *args):
        if self.hasSkillPointChange():
            if not self.closeMsgBoxId:
                msg = gameStrings.TEXT_SKILLPROXY_350
                self.closeMsgBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=lambda : self.realQuitEditMode(), noCallback=self._closeTip)
        else:
            self.realQuitEditMode()

    def realQuitEditMode(self):
        self.skillInfoManager.clear()
        self._closeTip()
        self.setEditMode(False)
        self.skillInfoManager.setEditMode(False)
        self.refreshNormalSkill()
        self.refreshSkillPoint()

    def enterEditMode(self):
        self.skillInfoManager.clear()
        self.setEditMode(True)
        self.skillInfoManager.setEditMode(True)
        self.refreshNormalSkill()
        self.refreshSkillPoint()

    def updateArenaSkillInfo(self):
        if not self.isEditMode:
            return
        self.refreshXiuLianPoint()
        self.refreshXiuLianScore()
        self.refreshSkillPracticeInfo(self.skillId)

    def getCurrentSchemeNum(self, *args):
        return GfxValue(BigWorld.player().skillPointSchemeIndex)

    def onGotoWeb(self, *args):
        skillId = args[3][0].GetNumber()
        self.gotoWeb(skillId)

    def gotoWeb(self, skillId):
        url = ''
        if skillId:
            url = SCD.data.get('WEB_SKILL_SEARCH', uiConst.WEB_SKILL_SEARCH)
            url = url % skillId
        else:
            url = SCD.data.get('WEB_INDEX_SEARCH', uiConst.WEB_INDEX_SEARCH)
        BigWorld.openUrl(url)

    def onGameOnOff(self, *args):
        ret = False
        if gameglobal.rds.configData.get('enableEquipGotoWeb', False) and self.mediator:
            ret = True
        return GfxValue(ret)

    def onInitTabState(self, *args):
        if BigWorld.player()._isSoul():
            if self.generalMediator:
                self.generalMediator.Invoke('setSoulOutTabState')
        if not gameglobal.rds.configData.get('enableIntimacySkill', False):
            self.generalMediator.Invoke('hideIntimacyView')

    def onGetWudaoTip(self, *args):
        tips = uiUtils.getTextFromGMD(GMDD.data.WU_DAO_TIP, '')
        return GfxValue(gbk2unicode(tips))

    def onGetEnableWSSchemes(self, *args):
        enableWSSchemes = gameglobal.rds.configData.get('enableWSSchemes', False)
        if enableWSSchemes:
            self.refreshWSSchemeInfo()
        return GfxValue(enableWSSchemes)

    def refreshWSSchemeInfo(self):
        if self.wushuangSkillPanelMc:
            info = {'schemeName': gameStrings.CURRENT_SCHEME_TITLE % BigWorld.player().getCurWSSchemeName()}
            self.wushuangSkillPanelMc.Invoke('refreshWSSchemeInfo', uiUtils.dict2GfxDict(info, True))

    def onSwitchWSScheme(self, *args):
        gameglobal.rds.ui.schemeSwitch.show(uiConst.SCHEME_SWITCH_WUSHUANG)

    def onOpenSkillMacro(self, *args):
        if not gameglobal.rds.configData.get('enableSkillMacro', False) and BigWorld.isPublishedVersion():
            return
        gameglobal.rds.ui.skillMacroOverview.showOverviewPanel()

    def onOpenSkillAppearance(self, *args):
        gameglobal.rds.ui.skillAppearance.show()

    def onGetExcitementDaoheng(self, *args):
        p = BigWorld.player()
        result = p.checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_DAOHENG)
        return GfxValue(bool(result))

    def refreshSkillBgBtn(self):
        if self.mediator:
            skillBgWidget = ASObject(self.mediator.Invoke('getWidget'))
            if skillBgWidget:
                p = BigWorld.player()
                skillBgWidget.hit.wsSkillTab.enabled = p.checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_WUSHUANG)

    def onShareSkills(self, *args):
        p = BigWorld.player()
        if p._isSoul():
            p.showGameMsg(GMDD.data.SKILL_SHARE_NOT_AVALIABLE_CROSS, ())
            return
        roleName = p.roleName
        msg = gameStrings.SKILL_SHARE_TXT % (roleName, utils.getHostId(), roleName)
        gameglobal.rds.ui.sendLink(msg)

    def onResetXiulianSkills(self, *args):
        p = BigWorld.player()
        msg = GMD.data.get(GMDD.data.RESET_XIULIAN_SKILL_NOTIFY, {}).get('text', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=lambda : p.cell.resetAllSkillEnhancePoint())

    def onIsGotoXiuLian(self, *args):
        isGotoXiuLian = self.isGotoXiuLian
        self.isGotoXiuLian = False
        return GfxValue(isGotoXiuLian)

    def onIsUsingTemp(self, *args):
        p = BigWorld.player()
        isTemp = p.isUsingTemp()
        return GfxValue(isTemp)

    def onSaveXiuLianTemplate(self, *args):
        p = BigWorld.player()
        p.cell.saveCharTempSkillPointScheme(p.charTempType, True)

    def onSaveWuShuangTemplate(self, *args):
        p = BigWorld.player()
        p.cell.saveCharTempWSSkillScheme(p.charTempType, True)

    def refreshXiuLianScore(self):
        if self.commonSkillMc:
            self.commonSkillMc.Invoke('setXiuLianScoreInfo')

    def onGetXiuLianScoreInfo(self, *args):
        scores = []
        p = BigWorld.player()
        rareInfo = SCD.data.get('skillEnhScoreTypeInfo', {})
        for requireType in rareInfo:
            score = p.learnSkillEnhanceScore.get(requireType, 0)
            totalScore = p.totalLearnSkillEnhanceScore.get(requireType, 0)
            scoreText = str(score)
            totalScoreText = '/ %d' % totalScore
            scores.append((gbk2unicode(rareInfo.get(requireType)[0]), scoreText, totalScoreText))

        return uiUtils.array2GfxAarry(scores)

    def onIsInPUBG(self, *args):
        p = BigWorld.player()
        isInPUBG = p.isInPUBG()
        return GfxValue(isInPUBG)
