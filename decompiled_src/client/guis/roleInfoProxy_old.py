#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/roleInfoProxy_old.o
from gamestrings import gameStrings
import time
import sys
import math
from guis.asObject import ASObject
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import ui
import gamelog
import const
import gametypes
import commcalc
import formula
import utils
import clientUtils
import keys
import socialSkillCommon
import itemToolTipUtils
from gameclass import PSkillInfo, StateInfo
from gamescript import FormularEvalEnv
from guis import cursor
from item import Item
from uiProxy import SlotDataProxy
from ui import gbk2unicode
from ui import unicode2gbk
import uiUtils
from helpers import cellCmd
from helpers import capturePhoto
from callbackHelper import Functor
from sMath import distance2D
from guis import tipUtils
from guis import events
import gameconfigCommon
from guis.asObject import ASObject
from gamestrings import gameStrings
from appSetting import Obj as AppSettings
from data import avatar_lv_data as ALD
from data import fame_data as FD
from data import fb_data as FBD
from data import school_data as SD
from data import tree_structure_data as TSD
from data import item_data as ID
from cdata import font_config_data as FCD
from data import formula_client_data as FCCD
from data import equip_data as ED
from data import title_data as TD
from data import rune_effect_data as RED
from cdata import rune_equip_exp_data as REED
from data import rune_equip_xilian_effect_data as REXED
from data import prop_ref_data as PRD
from data import role_panel_attr_data as RPAD
from data import primary_property_point_consume_data as PPPCD
from data import message_desc_data as MSGDD
from data import prop_data as PD
from data import recommend_point_data as RPD
from cdata import prop_def_data as PDD
from data import rune_equip_data as REQD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from data import radar_chart_dimension_data as RCDD
from data import vp_level_data as VLD
from data import rune_data as RD
from data import map_config_data as MCD
from data import life_skill_subtype_reverse_data as LSSRD
from data import social_lv_data as SLD
from data import social_school_data as SSD
from data import social_school_skill_data as SSSD
from data import life_skill_prop_tips_data as LSPTD
from data import life_skill_config_data as LSCD
from data import vp_tips_data as VTD
from data import skill_client_data as SKCD
from data import social_school_config_data as SSCD
from data import skill_general_template_data as SGTD
from data import zhanxun_rank_data as ZRD
from data import junjie_config_data as JCD
from data import seeker_data as SEEKD
from data import mall_item_data as MID
from data import qumo_lv_data as QLD
from data import quest_loop_data as QLOOPD
from data import activity_basic_data as ABD
from data import quest_data as QD
from cdata import vp_stage_data
from data import jingjie_data as JD
from data import npc_data as ND
from data import game_msg_data as GMD
from data import bonus_data as BD
from data import effect_title_data as ETD
from data import life_skill_config_data as LSCFD
from data import activity_state_config_data as ASCD
from data import mingpai_data as MPD
from data import novice_boost_score_type_data as NBSTD
from cdata import item_parentId_data as IPD
from cdata import item_coin_dikou_cost_data as ICDCD
LEFT_FLAG = '['
MIDDLE_FLAG = '.'
RIGHT_FLAG = ']'
potentialMap = {uiConst.POTENTIAL_POW: 'pow',
 uiConst.POTENTIAL_INT: 'int',
 uiConst.POTENTIAL_PHY: 'phy',
 uiConst.POTENTIAL_SPR: 'spr',
 uiConst.POTENTIAL_AGI: 'agi'}
potentialIdMap = {uiConst.POTENTIAL_POW: PDD.data.PROPERTY_ATTR_PW,
 uiConst.POTENTIAL_INT: PDD.data.PROPERTY_ATTR_INT,
 uiConst.POTENTIAL_PHY: PDD.data.PROPERTY_ATTR_PHY,
 uiConst.POTENTIAL_SPR: PDD.data.PROPERTY_ATTR_SPR,
 uiConst.POTENTIAL_AGI: PDD.data.PROPERTY_ATTR_AGI}
SOCIAL_SCHOOL_BIG_ICON = 'socialSchool/icon64/'
SOCIAL_SCHOOL_SMALL_ICON = 'socialSchool/icon40/'
FASHION_SLOT_BINDING_MAP = {gametypes.EQU_PART_FASHION_HEAD: 0,
 gametypes.EQU_PART_FASHION_BODY: 1,
 gametypes.EQU_PART_FASHION_SHOE: 2,
 gametypes.EQU_PART_FASHION_HAND: 3,
 gametypes.EQU_PART_FASHION_LEG: 4,
 gametypes.EQU_PART_HEADWEAR: 5,
 gametypes.EQU_PART_HEADWEAR_RIGHT: 6,
 gametypes.EQU_PART_HEADWEAR_LFET: 7,
 gametypes.EQU_PART_FACEWEAR: 8,
 gametypes.EQU_PART_WAISTWEAR: 9,
 gametypes.EQU_PART_BACKWEAR: 10,
 gametypes.EQU_PART_TAILWEAR: 11,
 gametypes.EQU_PART_CHESTWEAR: 12,
 gametypes.EQU_PART_EARWEAR: 13,
 gametypes.EQU_PART_FASHION_WEAPON_ZHUSHOU: 14,
 gametypes.EQU_PART_FASHION_WEAPON_FUSHOU: 15,
 gametypes.EQU_PART_FASHION_NEIYI: 16,
 gametypes.EQU_PART_FASHION_NEIKU: 17,
 gametypes.EQU_PART_FOOT_DUST: 18,
 gametypes.EQU_PART_YUANLING: 19,
 gametypes.EQU_PART_FASHION_CAPE: 20}
LIFE_SKILL_PROP_MAP = {1: 'sense',
 2: 'study',
 3: 'lucky',
 4: 'charm',
 5: 'str',
 6: 'dex',
 7: 'know'}
ATTR_GUIDE_KEY_DICT = {(1, 7): 0,
 (1, 4): 1,
 (1, 5): 2,
 (1, 3): 3,
 (1, 6): 4}
BENYUAN_RUNE_POS = 30
LV_UP_DOUBLE_CHECK_NORMAL = 1
LV_UP_DOUBLE_CHECK_SKIP_BREAK = 2

class RoleInfoProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        self.common = self.getPropsArray(uiConst.COMMON_PROPS)
        self.attack = self.getPropsArray(uiConst.ATTACK_PROPS)
        self.defense = self.getPropsArray(uiConst.DEFENSE_PROPS)
        self.advance = self.getPropsArray(uiConst.ADVANCE_PROPS)
        self.fashionPart = {'head': 0,
         'head2': 0,
         'head1': 0,
         'body': 1,
         'shoe': 2,
         'hand': 3,
         'leg': 4,
         'headdress': 5,
         'headdressRight': 6,
         'headdressLeft': 7,
         'facewear': 8,
         'waistwear': 9,
         'backwear': 10,
         'tailwear': 11,
         'chestwear': 12,
         'earwear': 13,
         'neiyi': 16,
         'neiku': 17,
         'footdust': 18,
         'cape': 20}
        super(RoleInfoProxy, self).__init__(uiAdapter)
        self.modelMap = {'initPanel': self.onInitPanel,
         'unRegisterPanel': self.onUnRegisterPanel,
         'getRoleEquipPartInfo': self.onGetRoleEquipPartInfo,
         'getRoleInfo': self.onGetRoleInfo,
         'getInitInfo': self.onGetInitInfo,
         'clickLvUp': self.onClickLvUp,
         'clickClose': self.onClickClose,
         'processSlot': self.onProcessSlot,
         'sendSet': self.onSendSet,
         'getFashionInfo': self.onGetFashionInfo,
         'showFashion': self.onShowFashion,
         'unEquipFashion': self.onUnEquipFashion,
         'setTabIndex': self.onSetTabIndex,
         'setSubEquipFlag': self.onSetSubEquipFlag,
         'getFashionSuit': self.onGetFashionSuit,
         'getPropsTooltip': self.onGetPropsTooltip,
         'potChange': self.onPotChange,
         'potConfirm': self.onPotConfirm,
         'potRecommend': self.onPotRecommend,
         'getPotTooltip': self.onGetPotTooltip,
         'getPotData': self.onGetPotData,
         'getRuneData': self.onGetRuneData,
         'getSocialInfo': self.onGetSocialInfo,
         'getSocialJobInfo': self.onGetSocialJobInfo,
         'getSocialSkillInfo': self.onGetSocialSkillInfo,
         'getSocialExp': self.onGetSocialExp,
         'getSocialLv': self.onGetSocialLv,
         'getJobTip': self.onGetJobTip,
         'levelUpClick': self.onLevelUpClick,
         'resignClick': self.onResignClick,
         'abilityTreeClick': self.onAbilityTreeClick,
         'skillLevelUpClick': self.onSkillLevelUpClick,
         'gotoSocClick': self.onGotoSocClick,
         'clickExpUp': self.onClickExpUp,
         'clickChongXi': self.onClickChongXi,
         'clickRuneItem': self.onClickRuneItem,
         'slotChongXi': self.onsSlotChongXi,
         'runeView': self.onRuneView,
         'getTabIndex': self.onGetTabIndex,
         'resetPoint': self.onResetPoint,
         'getHpMp': self.onGetHpMp,
         'getRadarData': self.onGetRadarData,
         'getRadarTip': self.onGetRadarTip,
         'getTitleData': self.onGetTitleData,
         'getEffectTitleEnableFlag': self.onGetEffectTitleEnableFlag,
         'getEffectTitleData': self.onGetEffectTitleData,
         'applyAllEffectTitle': self.onApplyAllEffectTitle,
         'applySimpleEffectTitle': self.onApplySimpleEffectTitle,
         'cancelApplyEffectTitle': self.onCancelApplyEffectTitle,
         'getXiulianBtnState': self.onGetXiulianBtnState,
         'selectTitle': self.onSelectTitle,
         'selectTitleProp': self.onSelectTitleProp,
         'deSelectTitleProp': self.onDeSelectTitleProp,
         'previewTitle': self.onPreviewTitle,
         'getTitleTooltip': self.onGetTitleTooltip,
         'checkEnablePropTitle': self.onCheckEnablePropTitle,
         'checkProp': self.onCheckProp,
         'openScheme': self.onOpenScheme,
         'getVpTransformValue': self.onGetVpTransformValue,
         'confirmVpTransform': self.onConfirmVpTransform,
         'confirmVpTransformDirect': self.onConfirmVpTransformDirect,
         'getVpTransformInfo': self.onGetVpTransformInfo,
         'sendVpValue': self.onSendVpValue,
         'closeVpTransformTip': self.onCloseVpTransformTip,
         'getVpTransformDesc': self.onGetVpTransformDesc,
         'rotateFigure': self.onRotateFigure,
         'getInitEquipData': self.onGetInitEquipData,
         'loadComplete': self.onLoadComplete,
         'unEquipSocialItem': self.onUnEquipSocialItem,
         'unEquipFishItem': self.onUnEquipFishItem,
         'unEquipExploreItem': self.onUnEquipExploreItem,
         'showEarType': self.onShowEarType,
         'showBack': self.onShowBack,
         'isInTrainingFuben': self.onIsInTrainingFuben,
         'getHonorData': self.onGetHonorData,
         'clickFashionBag': self.onClickFashionBag,
         'playSound': self.onPlaySound,
         'saveSetting': self.onSaveSetting,
         'gotoFameShop': self.onGoToFameShop,
         'getAllPotPointTips': self.onGetAllPotPointTips,
         'openGrowth': self.onOpenGrowth,
         'getJunjieInfo': self.onGetJunjieInfo,
         'getAward': self.onGetAward,
         'getJunziBonus': self.onGetJunziBonus,
         'refreshRenewalInfo': self.onRefreshRenewalInfo,
         'commitMallItem': self.onCommitMallItem,
         'getQumoInfo': self.onGetQumoInfo,
         'refreshVpPanel': self.onRefreshVpPanel,
         'getQumoPoints': self.onGetQumoPoints,
         'genMaxVpTip': self.onGenMaxVpTip,
         'genVpTip': self.onGenVpTip,
         'genBottleVipTip': self.onGenBottleVipTip,
         'genVpExpireTimeTip': self.onGenVpExpireTimeTip,
         'getJingJieNotifyInfo': self.onGetJingJieNotifyInfo,
         'openWingAndMount': self.onOpenWingAndMount,
         'openZhanXunList': self.onOpenZhanXunList,
         'canOpenTab': self.onCanOpenTab,
         'getQumoActBonus': self.onGetQumoActBonus,
         'getNeiYiConfig': self.onGetNeiYiConfig,
         'traceRoad': self.onTraceRoad,
         'getTraceRoadBtnDesc': self.onGetTraceRoadBtnDesc,
         'getMingPaiInfo': self.onGetMingPaiInfo,
         'applyMingPai': self.onApplyMingPai,
         'getRoleNameWithMingPai': self.onGetRoleNameWithMingPai,
         'openGuanYin': self.onOpenGuanYin,
         'openYaoPei': self.onOpenYaoPei,
         'openEquipChange': self.onOpenEquipChange,
         'openGuiBaoge': self.onOpenGuiBaoge,
         'openSkillAppearance': self.onOpenSkillAppearance,
         'openActEffectAppearance': self.onActEffectAppearance,
         'isSkillAppearanceVisible': self.onIsSkillAppearanceVisible,
         'showFashionWeapon': self.onShowFashionWeapon,
         'getZhuangshiTips': self.onGetZhuangshiTips,
         'switchEquip': self.onSwitchEquip,
         'potReset': self.onPotReset,
         'enableHideFashionHead': self.onEnableHideFashionHead,
         'enableYuanLing': self.onEnableYuanLing,
         'hideFashionHead': self.onHideFashionHead,
         'getHieroHasAvailablePos': self.onGetHieroHasAvailablePos,
         'getRuneTransInfo': self.onGetRuneTransInfo,
         'resetRuneFunc': self.onResetRuneFunc,
         'getEnableGuiBaoGe': self.onGetEnableGuiBaoGe,
         'checkHideFashionHead': self.onCheckHideFashionHead,
         'isHadNewFame': self.onIsHadNewFame,
         'getApplyTips': self.onGetApplyTips,
         'getDisableTips': self.onGetDisableTips,
         'getTemplateName': self.onGetTemplateName,
         'canChangeTemplate': self.onCanChangeTemplate,
         'isUsingTemp': self.onIsUsingTemp}
        self.isShow = False
        self.mediator = None
        self.vpTransformMediator = None
        self.vpTransformTipMediator = None
        self.vpTransform = None
        self.bindType = 'fashion'
        self.type = 'fashion'
        self.tabIdx = uiConst.ROLEINFO_TAB_ROLE
        self.subPanel = None
        self.isRuneChongXiState = False
        self.pointMinus = 0
        self.powAdd = 0
        self.intAdd = 0
        self.phyAdd = 0
        self.sprAdd = 0
        self.agiAdd = 0
        self.headGen = None
        self.titleNewTime = 0
        self.oldLv = 0
        self.selectedJob = 0
        self.preSkillPoint = 0
        self.socialSkillDict = {}
        self.junziWeekVal = 0
        self.weeklyQumoScore = 0
        self.weeklyMaxQumoScore = 0
        self.qumoScoreExtraLimit = 0
        self.qumoXichenRefId = 0
        self.subEquipFlag = False
        self.widget = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_ROLE_INFO, self.hide)

    def onCommitMallItem(self, *args):
        mallID = int(args[3][0].GetNumber())
        gameglobal.rds.ui.tianyuMall.show(mallID)

    def onRefreshRenewalInfo(self, *args):
        commonType = SCD.data.get('FashionCommon_RenewalType', 0)
        mallIDList = []
        mallIDList.append(SCD.data.get('FashionCommon_RenewalItem', 0))
        articlesType = SCD.data.get('Articles_RenewalType', 0)
        mallIDList.append(SCD.data.get('Articles_RenewalItem', 0))
        info = {}
        p = BigWorld.player()
        timeList = []
        commonTTLTime = p.renewalTypeExpireTimeDict.get(commonType, 0)
        articlesTTLTime = p.renewalTypeExpireTimeDict.get(articlesType, 0)
        timeList.append(commonTTLTime)
        timeList.append(articlesTTLTime)
        now = p.getServerTime()
        timeTextList = []
        mallItemlist = []
        for i in xrange(0, 2):
            leftTime = timeList[i] - now
            timeText = ''
            if leftTime <= 0:
                timeText = gameStrings.TEXT_ROLEINFOPROXY_393
            else:
                txt = utils.formatDurationShortVersion(leftTime)
                if leftTime < 86400:
                    timeText = "<font color = \'#FFCC32\'>" + txt + '</font>'
                else:
                    timeText = "<font color = \'#73E539\'>" + txt + '</font>'
            timeTextList.append(timeText)
            mallId = mallIDList[i]
            if mallId:
                info = MID.data.get(mallId, {})
                itemId = int(info.get('itemId', 0))
                iconPath = uiUtils.getItemIconFile64(itemId)
                itemInfo = {'itemId': itemId,
                 'iconPath': iconPath,
                 'mallID': mallId}
                mallItemlist.append(itemInfo)
            else:
                mallItemlist.append(None)

        closeRenewal = gameglobal.rds.configData.get('enableCommonResumeHide', False)
        ret = {'timeTextList': timeTextList,
         'mallItemIdList': mallItemlist,
         'isCloseRenewal': closeRenewal}
        trueRet = uiUtils.dict2GfxDict(ret, True)
        if self.mediator:
            self.mediator.Invoke('setRenewalInfo', trueRet)

    def refreshRenewal(self):
        self.onRefreshRenewalInfo(None)

    def getVpRatio(self):
        p = BigWorld.player()
        maxVp = p.maxVp if p.maxVp > 0 else 1
        return max(0.0001, float(p.baseVp + p.savedVp) / maxVp)

    def onGetInitInfo(self, *arg):
        p = BigWorld.player()
        ret = list()
        for tabIdx in uiConst.ROLEINFO_TAB_ALL:
            canOpen, tips = self.checkRoleInfoTabCanOpen(tabIdx)
            ret.append([tabIdx, canOpen, tips])

        return uiUtils.array2GfxAarry(ret, True)

    def checkRoleInfoTabCanOpen(self, tabIdx):
        p = BigWorld.player()
        lv = p.lv
        if tabIdx == uiConst.ROLEINFO_TAB_ROLE:
            pass
        elif tabIdx == uiConst.ROLEINFO_TAB_FAME:
            if p.isUsingTemp():
                return (False, None)
        elif tabIdx == uiConst.ROLEINFO_TAB_FASHION:
            pass
        elif tabIdx == uiConst.ROLEINFO_TAB_RUNE:
            if p.isInPUBG():
                return (False, None)
            canOpenRune = p.checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_HIEROGRAM)
            openRuneLv = SCD.data.get('OPENRUNELV', 30)
            if openRuneLv > lv:
                return (False, gameStrings.ROLE_INFO_TAB_IDX_LV_LIMIT_TIPS % openRuneLv)
            if not canOpenRune:
                return (False, gameStrings.EXCITEMENT_FORBIDDEN_TIPS)
        elif tabIdx == uiConst.ROLEINFO_TAB_SOCIAL:
            if p.isInPUBG():
                return (False, None)
            if p.isUsingTemp():
                return (False, None)
            openSocialLv = SCD.data.get('OpenSocialLv', 15)
            if openSocialLv > lv:
                return (False, gameStrings.ROLE_INFO_TAB_IDX_LV_LIMIT_TIPS % openSocialLv)
        elif tabIdx == uiConst.ROLEINFO_TAB_HONOR:
            if p.isInPUBG():
                return (False, None)
            if p.isUsingTemp():
                return (False, None)
        elif tabIdx == uiConst.ROLEINFO_TAB_JUNJIE:
            openJunjieLv = SCD.data.get('OpenJunjieLv', 40)
            if openJunjieLv > lv:
                return (False, gameStrings.ROLE_INFO_TAB_IDX_LV_LIMIT_TIPS % openJunjieLv)
        elif tabIdx == uiConst.ROLEINFO_TAB_QUMO:
            if p.isInPUBG():
                return (False, None)
            if p.isUsingTemp():
                return (False, None)
            openQumoLv = SCD.data.get('OpenQumoLv', 30)
            if openQumoLv > lv:
                return (False, gameStrings.ROLE_INFO_TAB_IDX_LV_LIMIT_TIPS % openQumoLv)
        elif tabIdx == uiConst.ROLEINFO_TAB_JINGJIE:
            if p.isInPUBG():
                return (False, None)
            canOpenJingjie = p.checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_JINGJIE)
            if not canOpenJingjie:
                return (False, gameStrings.EXCITEMENT_FORBIDDEN_TIPS)
        return (True, None)

    def onGetRoleEquipPartInfo(self, *arg):
        equipPartMainList = list(gametypes.EQU_PART_MAIN)
        equipPartSubList = list(gametypes.EQU_PART_SUB)
        ret = [equipPartMainList, equipPartSubList]
        return uiUtils.array2GfxAarry(ret)

    def onGetRoleInfo(self, *arg):
        p = BigWorld.player()
        if not p or not p.inWorld:
            return
        lv = p.realLv
        exp = '%d/%d' % (p.exp, ALD.data.get(p.realLv, {}).get('upExp', 1))
        if p.inFuben() and p.fbGuideEffect == const.GUIDE_MASTER_MODE:
            lv = p.lv
            exp = '%d/%d' % (p.exp, ALD.data.get(p.lv, {}).get('upExp', 1))
        exp = (exp, p.getLvBreakStep())
        name = uiUtils.getNameWithMingPain(p.realRoleName, p.selectedMPId)
        school = p.school
        attrList = self.createInfo()
        score = p.equipment.calcAllEquipScore(p.suitsCache)
        if gameconfigCommon.enableSplitWenYinFromEquip():
            score += p.combatScoreList[const.WEN_YIN_SCORE]
        equipChangeTip = gameStrings.TEXT_ROLEINFOPROXY_511
        if SD.data[p.school].has_key('leftConsumEqu'):
            leftConsumEquObj = {'isShow': True,
             'type': SD.data[p.school]['leftConsumEqu']}
        else:
            leftConsumEquObj = {'isShow': False}
        if SD.data[p.school].has_key('leftConsumEqu'):
            rightConsumEquObj = {'isShow': True,
             'type': SD.data[p.school]['rightConsumEqu']}
        else:
            rightConsumEquObj = {'isShow': False}
        pointInfo = {}
        extraPotPoint = p.primaryProp.gpoint - min(ALD.data.get(p.realLv, {}).get('maxGPoint', 0), p.primaryProp.gpoint)
        if extraPotPoint > 0:
            pointInfo['extraPotPoint'] = '(+%d)' % extraPotPoint
            pointInfo['extraPotPointTips'] = gameStrings.TEXT_ROLEINFOPROXY_526 % extraPotPoint
        else:
            pointInfo['extraPotPoint'] = ''
            pointInfo['extraPotPointTips'] = ''
        pointInfo['potPoint'] = gameStrings.TEXT_ROLEINFOPROXY_530 % (p.primaryProp.point - self.pointMinus - extraPotPoint)
        titleName, titleStyle = self._getShowTitleStyle()
        titleObj = {'name': titleName,
         'style': titleStyle}
        vpRatio = self.getVpRatio()
        lvDesc = 'Lv.%d' % p.realLv
        if p.inFuben() and p.fbGuideEffect == const.GUIDE_MASTER_MODE:
            lvDesc = gameStrings.TEXT_ROLEINFOPROXY_537 % (p.lv, p.realLv)
        showLvUpBtn, canManualLvUp, enhTips, lvLabel = self.getLvUpBtnInfo()
        savingKey = keys.SET_UI_INFO + '/' + 'roleInfo' + '/open/raid'
        isOpenRole = AppSettings.get(savingKey, 1)
        jingjie = JD.data.get(p.jingJie, {}).get('name', '')
        expXiuWeiInfo = {}
        expXiuWeiInfo['expXiuWei'] = gameStrings.TEXT_ROLEINFOPROXY_546 % (format(p.expXiuWei, ','), format(ALD.data.get(p.realLv, {}).get('maxExpXiuWei', 0), ','))
        expXiuWeiInfo['expXiuWeiTips'] = SCD.data.get('expXiuWeiTips', '')
        expXiuWeiInfo['enableExpXiuWei'] = gameglobal.rds.configData.get('enableExpXiuWei', False)
        enableMingPai = gameglobal.rds.configData.get('enableMingpai', False)
        equip = p.equipment[gametypes.EQU_PART_CAPE]
        guanYinBtnVisible = equip and gameglobal.rds.configData.get('enableGuanYinSecondPhase', False) or gameconfigCommon.enableGuanYinThirdPhase() and p.guanYinFirstEquip
        equip = p.equipment[gametypes.EQU_PART_YAOPEI]
        yaoPeiBtnVisible = equip and gameglobal.rds.configData.get('enableYaoPei', False)
        openSubEquipLv = SCD.data.get('OPEN_SUB_EQUIP_LV', 79)
        changeToSubBtnVisible = gameglobal.rds.configData.get('enableSubEquipment', False) and openSubEquipLv <= p.realLv
        changeToSubBtnInfo = {'visible': changeToSubBtnVisible}
        if changeToSubBtnVisible:
            achieveId = SCD.data.get('OPEN_SUB_EQUIP_ACHIEVE_ID', 0)
            if achieveId:
                changeToSubBtnInfo['enabled'] = gameglobal.rds.ui.achvment.checkAchieveFlag(achieveId)
                changeToSubBtnInfo['tips'] = uiUtils.getTextFromGMD(GMDD.data.OPEN_SUB_EQUIP_TIPS, '')
            else:
                changeToSubBtnInfo['enabled'] = True
        initialPotInfo = SD.data[p.school]['point']
        xiuweiLvInfo = {'visible': True,
         'value': p.xiuweiLevel}
        isUsingTemp = p.isUsingTemp()
        ret = [lv,
         name,
         school,
         attrList[0],
         attrList[1],
         attrList[2],
         attrList[3],
         exp,
         score,
         leftConsumEquObj,
         rightConsumEquObj,
         pointInfo,
         titleObj,
         vpRatio,
         lvDesc,
         p.getVpStage(),
         canManualLvUp,
         showLvUpBtn,
         showLvUpBtn and canManualLvUp,
         isOpenRole,
         jingjie,
         enhTips,
         expXiuWeiInfo,
         enableMingPai,
         guanYinBtnVisible,
         yaoPeiBtnVisible,
         changeToSubBtnInfo,
         initialPotInfo,
         equipChangeTip,
         lvLabel,
         xiuweiLvInfo,
         isUsingTemp]
        self.setSchemeName()
        return uiUtils.array2GfxAarry(ret, True)

    def updateTitle(self):
        if self.mediator:
            titleName, titleStyle = self._getShowTitleStyle()
            self.mediator.Invoke('updateTitle', (GfxValue(gbk2unicode(titleName)), GfxValue(str(titleStyle))))

    def updateEffectTitle(self):
        p = BigWorld.player()
        if not p.inWorld:
            return
        if self.mediator:
            self.mediator.Invoke('updateCurEffectTitle', GfxValue(p.curEffectTitleId))

    def openJingjie(self):
        if self.mediator:
            self.mediator.Invoke('openJingjie')

    def openRune(self):
        if self.mediator:
            self.mediator.Invoke('openRune')

    def openQumo(self):
        if self.mediator:
            self.mediator.Invoke('openQumo')

    def openJunjie(self):
        if self.mediator:
            self.mediator.Invoke('openJunjie')

    def openSocial(self):
        if self.mediator:
            self.mediator.Invoke('openSocial')

    def onGetHpMp(self, *arg):
        p = BigWorld.player()
        ret = [p.hp,
         p.mhp,
         p.mp,
         p.mmp]
        return uiUtils.array2GfxAarry(ret)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ROLE_INFO:
            self.mediator = mediator
            BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)
            BigWorld.player().registerEvent(const.EVENT_UPDATE_PROP_SCHEME, self.onPropSchemeChange)
            if self.subPanel:
                return GfxValue(self.subPanel)
        elif widgetId == uiConst.WIDGET_VP_TRANSFORM_TIP:
            self.vpTransformTipMediator = mediator

    def setSchemeName(self):
        curSchemeNo = BigWorld.player().curPropScheme
        curScheme = BigWorld.player().getPropSchemeById(curSchemeNo)
        if not curScheme:
            return
        if curScheme.has_key('schemeName'):
            name = curScheme['schemeName']
        else:
            name = ''
        myName = gameStrings.TEXT_ROLEINFOPROXY_650 + name
        p = BigWorld.player()
        now = p.getServerTime()
        if curScheme['expireTime'] < now and curScheme['expireTime'] != 0:
            myName += gameStrings.TEXT_ROLEINFOPROXY_655
        if self.mediator:
            self.mediator.Invoke('setCurrentScheme', GfxValue(gbk2unicode(myName)))

    def onPropSchemeChange(self, params):
        self.setSchemeName()

    def onItemChange(self, params):
        if params[0] != const.RES_KIND_EQUIP:
            return
        page = params[1]
        pos = params[2]
        key = self._getFashionKey(page, pos)
        if not self.binding.has_key(key):
            return
        self.binding[key][0].Invoke('refreshTip')

    def checkAllEquipStarLvUp(self):
        equipment = BigWorld.player().equipment
        for pos in xrange(len(equipment)):
            if not equipment[pos]:
                continue
            self.onCheckEquipStarLvUp(pos)

    def onCheckEquipStarLvUp(self, pos):
        p = BigWorld.player()
        it = p.equipment[pos]
        canLvUp = it and it.starExp >= it._getEquipStarUpExp() and it.starLv < it.maxStarLv
        if it and (it.isYaoPei() or it.isGuanYin()):
            canLvUp = False
        canPush = canLvUp and it.starExp >= it._getEquipStarExpCeil()
        hasPushed = False
        dataList = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_EQUIP_STAR_LV_UP)
        for item in dataList:
            if item.get('data', -1) == pos:
                hasPushed = True
                break

        if canPush and not hasPushed:
            self.equipStarLvUpPush(pos)
        elif not canLvUp and hasPushed:
            gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_EQUIP_STAR_LV_UP, {'data': pos})

    def equipStarLvUpPush(self, pos):
        callBackDict = {'click': gameglobal.rds.ui.equipChangeStarLvUp.showStarLvUpByAutoPush}
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_EQUIP_STAR_LV_UP, {'data': pos})
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_EQUIP_STAR_LV_UP, callBackDict)

    def onSendSet(self, *arg):
        key = arg[3][0].GetString()
        _, idItem = key.split('.')
        idItem = int(idItem[4:])
        p = BigWorld.player()
        if idItem >= const.SUB_EQUIP_PART_OFFSET:
            equIt = commcalc.getAlternativeEquip(p, idItem - const.SUB_EQUIP_PART_OFFSET)
            isSubEquip = True
            realPos = gametypes.equipTosubEquipPartMap.get(idItem - const.SUB_EQUIP_PART_OFFSET, -1)
            if realPos < 0:
                return
        else:
            equIt = p.equipment.get(idItem)
            isSubEquip = False
            realPos = idItem
        if equIt == const.CONT_EMPTY_VAL:
            return
        if isSubEquip:
            p.constructItemInfo(const.RES_KIND_SUB_EQUIP_BAG, const.DEFAULT_SUB_EQU_PAGE_NO, realPos)
        else:
            p.constructItemInfo(const.RES_KIND_EQUIP, 0, realPos)

    def onGetHonorData(self, *args):
        data = {}
        for key, value in FD.data.items():
            if value.get('display', 0) == gametypes.FAME_SHOW_IN_HONORPANEL:
                itemData = {'name': value.get('name', ''),
                 'fameId': key}
                itemData['icon'] = 'fame/fame156/%s.dds' % value.get('icon', '')
                fame = BigWorld.player().getFame(key)
                itemData['fame'] = fame
                itemData['tip'] = value.get('desc', '')
                if value.get('weekGainLimit', ''):
                    fameW, maxW = BigWorld.player().fameWeek.get(key, (0, 0))
                    if not maxW:
                        maxW = FormularEvalEnv.evaluate(value.get('weekGainLimit', ''), {'lv': BigWorld.player().lv})
                    itemData['honorWeekDesc'] = gameStrings.TEXT_ROLEINFOPROXY_755 % (fameW, maxW)
                else:
                    itemData['honorWeekDesc'] = ''
                data.setdefault((value.get('treeName', ''), value.get('tree', 0)), []).append(itemData)

        keys = data.keys()
        keys.sort(cmp=lambda x, y: cmp(x[1], y[1]))
        result = []
        for key in keys:
            value = data.get(key)
            result.append({'label': key[0],
             'children': [value],
             'expand': True})

        return uiUtils.array2GfxAarry(result, True)

    def onClickLvUp(self, *arg):
        p = BigWorld.player()
        if p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            p.showGameMsg(GMDD.data.MANU_LV_UP_FAILED_IN_DUEL, ())
            return
        if gameglobal.rds.loginManager.serverMode() == gametypes.SERVER_MODE_NOVICE and p.lv >= gameglobal.rds.configData.get('noviceServerMaxPlayerLv'):
            BigWorld.player().showGameMsg(GMDD.data.SERVER_NOVICE_MAX_LEVEL_HINT, ())
            return
        if not self.needNewBieGuideExamHint():
            self._doLvUp()

    def needNewBieGuideExamHint(self):
        p = BigWorld.player()
        newBieGuideExamDict = SCD.data.get('newBieGuideExamDict', {})
        if p.lv not in newBieGuideExamDict:
            return False
        typeId = newBieGuideExamDict[p.lv]
        examInfo = gameglobal.rds.ui.newbieGuideExam.getResInfo().get(typeId, {})
        if not examInfo:
            return False
        elif gameglobal.rds.configData.get('enableNoviceBoost', False) and examInfo.get('graduateState', 0) == gametypes.NOVICE_TYPE_GRADUATE_NONE:
            topic = NBSTD.data.get(typeId, {}).get('topic', '')
            msg = uiUtils.getTextFromGMD(GMDD.data.NEWBIE_GUIDE_EXAM_LVUP_HINT, '%s%d') % (topic, p.lv + 1)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self._doLvUp)
            return True
        else:
            return False

    def _doLvUp(self):
        p = BigWorld.player()
        lvNotice = SCD.data.get('LV_UP_LOCK_NOTICE', [49, 59, 69])
        if p.lv in lvNotice:
            self._doLvUpByCheckLock()
        else:
            self._doLvUpNotCheckLock()

    @ui.checkInventoryLock()
    def _doLvUpByCheckLock(self):
        self._performLvUp()

    def _doLvUpNotCheckLock(self):
        self._performLvUp()

    def _performLvUp(self):
        p = BigWorld.player()
        needDoubleCheck = ALD.data.get(p.lv + 1, {}).get('needDoubleCheck', 0)
        if p.canLvBreak():
            msg = uiUtils.getTextFromGMD(getattr(GMDD.data, 'BREAK_LV_UP_DOUBLE_CHECK_NOTIFY_%d' % p.getBreakEndLv()), '')
            gameglobal.rds.ui.doubleCheckWithInput.show3ButtonCheck(msg, 'YES', gameStrings.TEXT_QUESTPROXY_495, (gameStrings.TEXT_ROLEINFOPROXY_821, gameStrings.TEXT_ROLEINFOPROXY_821_1, gameStrings.TEXT_PLAYRECOMMPROXY_494_1), self._breakLvUp, self._doManulaLvUp, canEnter=False)
        elif needDoubleCheck == LV_UP_DOUBLE_CHECK_NORMAL:
            msg = uiUtils.getTextFromGMD(GMDD.data.MANUAL_LV_UP_DOUBLE_CHECK_NOTIFY, '')
            gameglobal.rds.ui.doubleCheckWithInput.show(msg, 'YES', confirmCallback=self._doManulaLvUp)
        elif needDoubleCheck == LV_UP_DOUBLE_CHECK_SKIP_BREAK:
            msg = uiUtils.getTextFromGMD(getattr(GMDD.data, 'MANUAL_LV_UP_DOUBLE_CHECK_NOTIFY_SKIP_BREAK_%d' % p.getBreakEndLv()), '')
            gameglobal.rds.ui.doubleCheckWithInput.show(msg, 'YES', confirmCallback=self._doManulaLvUp)
        else:
            self._doManulaLvUp()

    def _breakLvUp(self):
        p = BigWorld.player()
        p.breakLvUp()

    def _doManulaLvUp(self):
        p = BigWorld.player()
        curLvKey = utils.lv2ArenaPlayoffsTeamkey(p.lv)
        nextLvKey = utils.lv2ArenaPlayoffsTeamkey(p.lv + 1)
        if p.getArenaPlayoffsTeamNUID() > 0 and curLvKey != nextLvKey:
            msg = MSGDD.data.get('ARENA_PLAYOFFS_LV_UP_DOUBLE_CHECK_NOTIFY', gameStrings.TEXT_ROLEINFOPROXY_841)
            gameglobal.rds.ui.doubleCheckWithInput.show(msg, 'YES', confirmCallback=p.cell.manualLvUp)
        else:
            p.cell.manualLvUp()

    def onClickFashionBag(self, *arg):
        if gameglobal.rds.configData.get('enableWardrobe', False):
            self.hide()
            BigWorld.player().openWardrobe()
        else:
            gameglobal.rds.ui.fashionBag.askForShow()

    def onClickClose(self, *arg):
        self.hide()

    def onProcessSlot(self, *arg):
        key = arg[3][0].GetString()
        _, idItem = key.split('.')
        idItem = int(idItem[4:])
        p = BigWorld.player()
        if idItem >= const.SUB_EQUIP_PART_OFFSET:
            equIt = commcalc.getAlternativeEquip(p, idItem - const.SUB_EQUIP_PART_OFFSET)
        else:
            equIt = p.equipment.get(idItem)
        if equIt == const.CONT_EMPTY_VAL:
            return
        isReal = False
        if gameglobal.rds.ui.shop.inRepair:
            isReal = True
        elif gameglobal.rds.ui.inventory.isDyeState:
            isReal = True
        elif ui.get_cursor_state() == ui.ADD_STAR_EXP_STATE:
            isReal = True
        elif ui.get_cursor_state() == ui.RENEWAL_STATE:
            isReal = True
        elif ui.get_cursor_state() == ui.RENEWAL_STATE2:
            isReal = True
        elif gameglobal.rds.ui.inventory.isUnlatchState:
            isReal = True
        elif gameglobal.rds.ui.inventory.isLatchTimeState:
            isReal = True
        elif gameglobal.rds.ui.inventory.isLatchCipherState:
            isReal = True
        if isReal:
            self.realProcessSlot(key)

    @ui.callFilter(1, True)
    def realProcessSlot(self, key):
        _, idItem = key.split('.')
        idItem = int(idItem[4:])
        p = BigWorld.player()
        if idItem >= const.SUB_EQUIP_PART_OFFSET:
            equIt = commcalc.getAlternativeEquip(p, idItem - const.SUB_EQUIP_PART_OFFSET)
            isSubEquip = True
            realPos = gametypes.equipTosubEquipPartMap.get(idItem - const.SUB_EQUIP_PART_OFFSET, -1)
            if realPos < 0:
                return
        else:
            equIt = p.equipment.get(idItem)
            isSubEquip = False
            realPos = idItem
        if equIt == const.CONT_EMPTY_VAL:
            return
        if gameglobal.rds.ui.shop.inRepair:
            if isSubEquip:
                gameglobal.rds.ui.shop.doRepair(const.INV_PAGE_SUBEQUIP, realPos)
            else:
                gameglobal.rds.ui.shop.doRepair(const.INV_PAGE_EQUIP, realPos)
        elif gameglobal.rds.ui.inventory.isDyeState:
            if isSubEquip:
                return
            i = p.inv.getQuickVal(self.uiAdapter.inventory.dyeItemPage, self.uiAdapter.inventory.dyeItemPos)
            if i.isDye():
                self.uiAdapter.inventory._onDyeDesItem(const.INV_PAGE_EQUIP, realPos)
            elif i.isRongGuang():
                self.uiAdapter.inventory._onRongGuangDesItem(const.INV_PAGE_EQUIP, realPos)
            elif getattr(i, 'cstype', 0) == Item.SUBTYPE_2_RUBBING_CLEAN:
                self.uiAdapter.inventory._onRubbingCleanItem(const.INV_PAGE_EQUIP, realPos)
        elif ui.get_cursor_state() == ui.ADD_STAR_EXP_STATE:
            if isSubEquip:
                return
            self.uiAdapter.inventory.doAddStarExp(const.RES_KIND_EQUIP, 0, realPos)
        elif ui.get_cursor_state() == ui.RENEWAL_STATE:
            if isSubEquip:
                return
            self.uiAdapter.inventory.doRenewerItem(const.INV_PAGE_EQUIP, realPos)
        elif ui.get_cursor_state() == ui.RENEWAL_STATE2:
            if isSubEquip:
                return
            sItem = p.equipment.get(realPos)
            if sItem.isMallFashionRenewable():
                self.uiAdapter.itemResume.show(sItem, 0, realPos, const.RES_KIND_EQUIP)
        elif gameglobal.rds.ui.inventory.isUnlatchState:
            if not equIt.hasLatch():
                gameglobal.rds.ui.inventory.clearUnlatchState()
                return
            if equIt.isLatchOfTime():
                if isSubEquip:
                    p.cell.unLatchTime(const.LATCH_ITEM_SUB_EQUIP, const.DEFAULT_SUB_EQU_PAGE_NO, realPos)
                else:
                    p.cell.unLatchTime(const.LATCH_ITEM_EQUIP, 0, realPos)
            elif isSubEquip:
                gameglobal.rds.ui.inventoryPassword.show(const.LATCH_ITEM_SUB_EQUIP, const.DEFAULT_SUB_EQU_PAGE_NO, realPos)
            else:
                gameglobal.rds.ui.inventoryPassword.show(const.LATCH_ITEM_EQUIP, 0, realPos)
            gameglobal.rds.ui.inventory.clearUnlatchState()
        elif gameglobal.rds.ui.inventory.isLatchTimeState:
            if not equIt.canLatch():
                BigWorld.player().showGameMsg(GMDD.data.LATCH_FORBIDDEN_NO_LATCH, ())
                return
            if isSubEquip:
                gameglobal.rds.ui.inventoryLatchTime.show(const.LATCH_ITEM_SUB_EQUIP, const.DEFAULT_SUB_EQU_PAGE_NO, realPos)
            else:
                gameglobal.rds.ui.inventoryLatchTime.show(const.LATCH_ITEM_EQUIP, 0, realPos)
            gameglobal.rds.ui.inventory.clearLatchTimeState()
        elif gameglobal.rds.ui.inventory.isLatchCipherState:
            if not equIt.hasLatch():
                if isSubEquip:
                    p.cell.latchCipher(const.LATCH_ITEM_SUB_EQUIP, const.DEFAULT_SUB_EQU_PAGE_NO, realPos)
                else:
                    p.cell.latchCipher(const.LATCH_ITEM_EQUIP, 0, realPos)
            elif isSubEquip:
                uiUtils.unLatchItem(equIt, const.LATCH_ITEM_SUB_EQUIP, const.DEFAULT_SUB_EQU_PAGE_NO, realPos)
            else:
                uiUtils.unLatchItem(equIt, const.LATCH_ITEM_EQUIP, 0, realPos)

    def updateSocialPanel(self):
        if self.mediator:
            self.mediator.Invoke('updateSocialPanel')

    def updateSocialJob(self):
        if self.mediator:
            self.mediator.Invoke('updateSocialJob')

    @ui.uiEvent(uiConst.WIDGET_ROLE_INFO, events.EVENT_FAME_UPDATE)
    def updateHonor(self, event = None):
        if self.mediator:
            self.mediator.Invoke('refreshHonorNotify')

    @ui.callAfterTime()
    def updateSocialSkill(self):
        if self.mediator:
            self.mediator.Invoke('updateSocialSkill')

    def show(self, tabIdx = uiConst.ROLEINFO_TAB_ROLE, subPanel = None, subItem = None):
        if not BigWorld.player().checkMapLimitUI(gametypes.MAP_LIMIT_UI_ROLE_INFO):
            return
        else:
            self.isShow = True
            self.tabIdx = tabIdx
            self.subPanel = subPanel
            if tabIdx == uiConst.ROLEINFO_TAB_HONOR and subItem is not None:
                self.uiAdapter.roleInfoHonor.selectedItemByFameId(subItem)
            if self.mediator:
                if self.subPanel == None:
                    self.subPanel = ''
                self.mediator.Invoke('setTabId', (GfxValue(self.tabIdx), GfxValue(self.subPanel)))
            else:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ROLE_INFO)
            return

    def hide(self, destroy = True):
        self.clearWidget()
        if destroy:
            self.reset()

    def reset(self):
        self.isShow = False
        self.tabIdx = uiConst.ROLEINFO_TAB_ROLE
        self.resetAddPoint()
        self.subPanel = None

    def resetAddPoint(self):
        self.pointMinus = 0
        self.powAdd = 0
        self.intAdd = 0
        self.phyAdd = 0
        self.sprAdd = 0
        self.agiAdd = 0

    def clearWidget(self):
        self.isShow = False
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ROLE_INFO)
        self.mediator = None
        self.resetHeadGen()
        self.clearState()
        if BigWorld.player():
            if BigWorld.player().__class__.__name__ == 'PlayerAvatar':
                BigWorld.player().unRegisterEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)
                BigWorld.player().unRegisterEvent(const.EVENT_UPDATE_PROP_SCHEME, self.onPropSchemeChange)
        if gameglobal.rds.ui.equipFeed.mediator:
            gameglobal.rds.ui.equipFeed.hide()

    def onGetTabIndex(self, *arg):
        return GfxValue(self.tabIdx)

    def createInfo(self):
        common = self.createArr(self.common, False)
        attack = self.createArr(self.attack, True)
        defense = self.createArr(self.defense, True)
        advance = self.createArr(self.advance, True)
        return (common,
         attack,
         defense,
         advance)

    @ui.callInCD(1)
    def refreshInfo(self):
        if self.isShow and self.mediator:
            self.mediator.Invoke('refreshInfo')
        self.onRefreshVpPanel(None)
        self.refreshRefineSuitsBtn()

    def refreshExpXiuWei(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            info['expXiuWei'] = gameStrings.TEXT_ROLEINFOPROXY_546 % (format(p.expXiuWei, ','), format(ALD.data.get(p.realLv, {}).get('maxExpXiuWei', 0), ','))
            info['expXiuWeiTips'] = SCD.data.get('expXiuWeiTips', '')
            info['xiuweiLv'] = p.xiuweiLevel
            self.mediator.Invoke('refreshExpXiuWei', uiUtils.dict2GfxDict(info, True))

    def refreshHpMp(self):
        if self.isShow and self.mediator:
            p = BigWorld.player()
            info = [p.hp,
             p.mhp,
             p.mp,
             p.mmp]
            self.mediator.Invoke('setHpMp', uiUtils.array2GfxAarry(info))

    def createArr(self, info, isExtra, toGfxValue = True):
        ret = []
        for idx, item in enumerate(info):
            attrStr = ''
            try:
                attrStr = self.calcAttr(item.get('showType', ''), item.get('idParam', []))
            except:
                raise Exception('role_panel_attr_data err ' + gbk2unicode(item.get('name', '')) + ' , to: wangjun')

            key = str(item['type']) + ',' + str(item['displayOrder'])
            if isExtra:
                ret.append([gbk2unicode(item['name'] + '  ' + attrStr), key])
            else:
                ret.append([gbk2unicode(item['name']), attrStr, key])

        if toGfxValue:
            ret = uiUtils.array2GfxAarry(ret)
        return ret

    def calcAttr(self, showType, idParam):
        p = BigWorld.player()
        primaryAttrStr = "<font color = \'#FFFFFF\'>%d</font><font color = \'#E5BE67\'> + %d</font>"
        for i, propInfo in enumerate(idParam):
            params, formulaVal = propInfo
            for idx in xrange(len(params)):
                prop = params[idx]
                if prop in PDD.data.PRIMARY_PROPERTIES:
                    if prop == PDD.data.PROPERTY_ATTR_PW:
                        bVal = p.getPrimaryPropBaseValue(PDD.data.PROPERTY_ATTR_PW)
                        showType = primaryAttrStr % (bVal, p.primaryProp.pow - bVal)
                    elif prop == PDD.data.PROPERTY_ATTR_INT:
                        bVal = p.getPrimaryPropBaseValue(PDD.data.PROPERTY_ATTR_INT)
                        showType = primaryAttrStr % (bVal, p.primaryProp.int - bVal)
                    elif prop == PDD.data.PROPERTY_ATTR_PHY:
                        bVal = p.getPrimaryPropBaseValue(PDD.data.PROPERTY_ATTR_PHY)
                        showType = primaryAttrStr % (bVal, p.primaryProp.phy - bVal)
                    elif prop == PDD.data.PROPERTY_ATTR_SPR:
                        bVal = p.getPrimaryPropBaseValue(PDD.data.PROPERTY_ATTR_SPR)
                        showType = primaryAttrStr % (bVal, p.primaryProp.spr - bVal)
                    elif prop == PDD.data.PROPERTY_ATTR_AGI:
                        bVal = p.getPrimaryPropBaseValue(PDD.data.PROPERTY_ATTR_AGI)
                        showType = primaryAttrStr % (bVal, p.primaryProp.agi - bVal)
                    continue
                pVal = self.getPropValueById(p, prop)
                if prop in (uiConst.PROPERTY_MIN_PHY_ATK,
                 uiConst.PROPERTY_MAX_PHY_ATK,
                 uiConst.PROPERTY_MIN_MAG_ATK,
                 uiConst.PROPERTY_MAX_MAG_ATK):
                    pVal = min(99999, pVal)
                formulaVal = formulaVal.replace('p' + str(idx + 1), str(pVal))

            if showType.find('p' + str(i + 1)) < 0:
                continue
            val = eval(formulaVal)
            placeHolder = '[1.p' + str(i + 1) + ']'
            showType = showType.replace(placeHolder, str(int(val)))
            placeHolder = '[2.p' + str(i + 1) + ']'
            showType = showType.replace(placeHolder, str(round(val * 100, 1)) + '%')
            placeHolder = '[3.p' + str(i + 1) + ']'
            showType = showType.replace(placeHolder, str(round(val, 1)))

        return showType

    def setSlotState(self, idSlot, state):
        if self.mediator:
            self.mediator.Invoke('setSlotState', (GfxValue(idSlot), GfxValue(state)))

    def setItemSlotData(self, idSlot, itemInfo):
        if self.mediator:
            info = {'idSlot': idSlot,
             'itemInfo': itemInfo}
            self.mediator.Invoke('setItemSlotData', uiUtils.dict2GfxDict(info))

    def onGetTitleData(self, *arg):
        p = BigWorld.player()
        groupTitleMap = {}
        titleMap = {}
        prefixArr = []
        colorArr = []
        basicArr = []
        worldArr = []
        titleList = p.title.getTitle()
        if p.activeTitleType == const.ACTIVE_TITLE_TYPE_COMMON:
            currTitle = [const.ACTIVE_TITLE_TYPE_COMMON,
             p.currTitle[const.TITLE_TYPE_PREFIX],
             p.currTitle[const.TITLE_TYPE_COLOR],
             p.currTitle[const.TITLE_TYPE_BASIC]]
        elif p.activeTitleType == const.ACTIVE_TITLE_TYPE_WORLD:
            currTitle = [const.ACTIVE_TITLE_TYPE_WORLD, p.currTitle[const.TITLE_TYPE_WORLD]]
        if p.activePropTitleTypeEx == const.ACTIVE_TITLE_TYPE_COMMON:
            currPropTitleEx = [const.ACTIVE_TITLE_TYPE_COMMON,
             p.currPropTitleEx[const.TITLE_TYPE_PREFIX],
             p.currPropTitleEx[const.TITLE_TYPE_COLOR],
             p.currPropTitleEx[const.TITLE_TYPE_BASIC]]
        elif p.activePropTitleTypeEx == const.ACTIVE_TITLE_TYPE_WORLD:
            currPropTitleEx = [const.ACTIVE_TITLE_TYPE_WORLD, p.currPropTitleEx[const.TITLE_TYPE_WORLD]]
        for item in titleList:
            data = TD.data.get(item)
            if data is not None:
                groupId = data.get('gId')
                if groupId == gametypes.TITLE_GROUP_PARTNER and p._isSoul():
                    continue
                groupLv = data.get('gLv')
                if groupId != None:
                    glv = groupTitleMap.get(groupId)
                    if data.get('groupByTitleId', 0):
                        titleMap[item] = [groupLv, item]
                    elif glv is None:
                        groupTitleMap[groupId] = [groupLv, item]
                    elif groupLv > glv[0]:
                        groupTitleMap[groupId] = [groupLv, item]
                        if self.titleNewTime < p.title[item].tGain:
                            currTitle = [const.ACTIVE_TITLE_TYPE_WORLD, 0]
                else:
                    titleMap[item] = [groupLv, item]

        for title in titleMap.values() + groupTitleMap.values():
            data = TD.data.get(title[1])
            name = gbk2unicode(p.getTitleName(title[1]))
            style = data.get('style', 1)
            titleType = data.get('titleType', 3)
            if titleType == const.TITLE_TYPE_WORLD:
                worldArr.append([title[1],
                 name,
                 style,
                 p.title[title[1]].tGain,
                 self.titleNewTime < p.title[title[1]].tGain])
            elif titleType == const.TITLE_TYPE_PREFIX:
                prefixArr.append([title[1],
                 name,
                 style,
                 p.title[title[1]].tGain,
                 self.titleNewTime < p.title[title[1]].tGain])
            elif titleType == const.TITLE_TYPE_COLOR:
                colorArr.append([title[1],
                 name,
                 style,
                 p.title[title[1]].tGain,
                 self.titleNewTime < p.title[title[1]].tGain])
            elif titleType == const.TITLE_TYPE_BASIC:
                basicArr.append([title[1],
                 name,
                 style,
                 p.title[title[1]].tGain,
                 self.titleNewTime < p.title[title[1]].tGain])

        sorted(worldArr, reverse=True)
        worldArr.sort(key=lambda x: x[3], reverse=True)
        prefixArr.sort(key=lambda x: x[3], reverse=True)
        colorArr.sort(key=lambda x: x[3], reverse=True)
        basicArr.sort(key=lambda x: x[3], reverse=True)
        newList = [len([ i for i in worldArr if i[4] ]), len([ i for i in prefixArr + colorArr + basicArr if i[4] ]), len([ eId for eId in p.effectTitle.iterkeys() if not p.effectTitle.isTitleExpired(eId) and gameglobal.rds.configData.get('enableEffectTitle', False) and self.titleNewTime < p.effectTitle[eId].tGain ])]
        titleArr = [uiUtils.array2GfxAarry(worldArr),
         uiUtils.array2GfxAarry(prefixArr),
         uiUtils.array2GfxAarry(colorArr),
         uiUtils.array2GfxAarry(basicArr),
         uiUtils.array2GfxAarry(currTitle),
         uiUtils.array2GfxAarry(newList),
         uiUtils.array2GfxAarry(currPropTitleEx)]
        self.titleNewTime = p.getServerTime()
        return uiUtils.array2GfxAarry(titleArr)

    def onGetEffectTitleEnableFlag(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableEffectTitle', False))

    def genEffectTitleDesc(self, eId, eVal):
        if not ETD.data.has_key(eId):
            return ''
        else:
            eData = ETD.data[eId]
            if eData.get('manuDesc') != None:
                return eData['manuDesc']
            return gameStrings.TEXT_ROLEINFOPROXY_1247 + (gameStrings.TEXT_ROLEINFOPROXY_1247_1 if eVal.tExpired == const.EFFECT_TITLE_VALID_TIME_INFINITE else formula.toYearDesc(eVal.tExpired, 1))

    def getEffectTitleAttrDesc(self, eData, eValFromServer):
        if eData.get('props', []):
            return gameStrings.ROLE_INFO_TITLE_EXPIRETIME + (gameStrings.ROLE_INFO_TITLE_NEVEREXPIRE if eValFromServer.tAttr == const.EFFECT_TITLE_VALID_TIME_INFINITE else formula.toYearDesc(eValFromServer.tAttr, 1))
        else:
            return ''

    def getAttrValueByShowType(self, showType, prop):
        attrValue = ''
        if showType == 1 or prop[1] == 1:
            attrValue += str(round(prop[2] * 100, 1)) + '%'
        elif showType == 0:
            attrValue += str(int(prop[2]))
        elif showType == 2:
            attrValue += str(round(prop[2], 1))
        return attrValue

    def getEffectTitleAttrTextByETD(self, eData):
        allAttribute = ''
        for prop in eData.get('props', []):
            prdData = PRD.data.get(prop[0], {})
            attrName = prdData.get('name', '')
            showType = prdData.get('showType', 0)
            attrValue = self.getAttrValueByShowType(showType, prop)
            attrDesc = attrName + '  +' + attrValue
            allAttribute += attrDesc + '\n'

        return allAttribute

    def onGetEffectTitleData(self, *args):
        info = []
        p = BigWorld.player()
        for eId, eVal in p.effectTitle.iteritems():
            if not ETD.data.has_key(eId):
                continue
            eData = ETD.data[eId]
            info.append({'effectTitleId': eId,
             'icon': 'effectTitle/' + str(eData['icon']) + '.dds',
             'isCurEffectTitle': p.curEffectTitleId == eId,
             'tExpired': self.genEffectTitleDesc(eId, eVal),
             'preShowSwfName': 'widgets/dynamicTitle/' + eData['preShowSwfName'] + '.swf',
             'showAndActiveText': gameStrings.ROLE_INFO_TITLE_SHOWING,
             'allAttribute': self.getEffectTitleAttrTextByETD(eData),
             'titleTime': self.getEffectTitleAttrDesc(eData, eVal)})

        return uiUtils.array2GfxAarry(info, True)

    def onApplyAllEffectTitle(self, *args):
        effectTitleId = int(args[3][0].GetNumber())
        BigWorld.player().cell.alterEffectTitle(effectTitleId, gametypes.EFFECT_TITLE_LV_HIGH)

    def onApplySimpleEffectTitle(self, *args):
        effectTitleId = int(args[3][0].GetNumber())
        BigWorld.player().cell.alterEffectTitle(effectTitleId, gametypes.EFFECT_TITLE_LV_LOW)

    def onCancelApplyEffectTitle(self, *args):
        pass

    def onGetXiulianBtnState(self, *arg):
        ret = gameglobal.rds.ui.guildGrowth.checkLearnGrowthBaseBtnState()
        return uiUtils.array2GfxAarry(ret, True)

    def onSelectTitle(self, *arg):
        p = BigWorld.player()
        if int(arg[3][0].GetNumber()):
            p.cell.alterActiveTitleType(const.ACTIVE_TITLE_TYPE_COMMON)
            if p.currTitle[const.TITLE_TYPE_PREFIX] != int(arg[3][2].GetNumber()):
                p.cell.alterTitle(int(arg[3][2].GetNumber()), const.TITLE_TYPE_PREFIX)
            if p.currTitle[const.TITLE_TYPE_COLOR] != int(arg[3][3].GetNumber()):
                p.cell.alterTitle(int(arg[3][3].GetNumber()), const.TITLE_TYPE_COLOR)
            if p.currTitle[const.TITLE_TYPE_BASIC] != int(arg[3][4].GetNumber()):
                p.cell.alterTitle(int(arg[3][4].GetNumber()), const.TITLE_TYPE_BASIC)
            prefixName = p.getTitleName(int(arg[3][2].GetNumber()))
            colorName = p.getTitleName(int(arg[3][3].GetNumber()))
            basicName = p.getTitleName(int(arg[3][4].GetNumber()))
            sytle = 1
            if colorName:
                sytle = TD.data.get(int(arg[3][3].GetNumber()), {}).get('style', 1)
            elif basicName:
                sytle = TD.data.get(int(arg[3][4].GetNumber()), {}).get('style', 1)
            elif prefixName:
                sytle = TD.data.get(int(arg[3][2].GetNumber()), {}).get('style', 1)
            if self.mediator != None:
                self.mediator.Invoke('setPreviewTitle', (GfxValue(str(sytle)),
                 GfxValue(gbk2unicode(prefixName)),
                 GfxValue(gbk2unicode(colorName)),
                 GfxValue(gbk2unicode(basicName))))
        else:
            p.cell.alterActiveTitleType(const.ACTIVE_TITLE_TYPE_WORLD)
            if p.currTitle[const.TITLE_TYPE_WORLD] != int(arg[3][1].GetNumber()):
                p.cell.alterTitle(int(arg[3][1].GetNumber()), const.TITLE_TYPE_WORLD)

    def onSelectTitleProp(self, *arg):
        p = BigWorld.player()
        if int(arg[3][0].GetNumber()):
            p.cell.alterActivePropTitleType(const.ACTIVE_TITLE_TYPE_COMMON)
            if p.currPropTitleEx[const.TITLE_TYPE_PREFIX] != int(arg[3][2].GetNumber()):
                p.cell.alterPropTitle(int(arg[3][2].GetNumber()), const.TITLE_TYPE_PREFIX)
            if p.currPropTitleEx[const.TITLE_TYPE_COLOR] != int(arg[3][3].GetNumber()):
                p.cell.alterPropTitle(int(arg[3][3].GetNumber()), const.TITLE_TYPE_COLOR)
            if p.currPropTitleEx[const.TITLE_TYPE_BASIC] != int(arg[3][4].GetNumber()):
                p.cell.alterPropTitle(int(arg[3][4].GetNumber()), const.TITLE_TYPE_BASIC)
        else:
            p.cell.alterActivePropTitleType(const.ACTIVE_TITLE_TYPE_WORLD)
            if p.currPropTitleEx[const.TITLE_TYPE_WORLD] != int(arg[3][1].GetNumber()):
                p.cell.alterPropTitle(int(arg[3][1].GetNumber()), const.TITLE_TYPE_WORLD)

    def onDeSelectTitleProp(self, *arg):
        p = BigWorld.player()
        if int(arg[3][0].GetNumber()):
            p.cell.deActivePropTitleType(const.ACTIVE_TITLE_TYPE_COMMON)
        else:
            p.cell.deActivePropTitleType(const.ACTIVE_TITLE_TYPE_WORLD)

    def onPreviewTitle(self, *arg):
        p = BigWorld.player()
        prefixName = p.getTitleName(int(arg[3][0].GetNumber()))
        colorName = p.getTitleName(int(arg[3][1].GetNumber()))
        basicName = p.getTitleName(int(arg[3][2].GetNumber()))
        sytle = 1
        if colorName:
            sytle = TD.data.get(int(arg[3][1].GetNumber()), {}).get('style', 1)
        elif basicName:
            sytle = TD.data.get(int(arg[3][2].GetNumber()), {}).get('style', 1)
        elif prefixName:
            sytle = TD.data.get(int(arg[3][0].GetNumber()), {}).get('style', 1)
        if self.mediator != None:
            self.mediator.Invoke('setPreviewTitle', (GfxValue(str(sytle)),
             GfxValue(gbk2unicode(prefixName)),
             GfxValue(gbk2unicode(colorName)),
             GfxValue(gbk2unicode(basicName))))

    def onCheckProp(self, *arg):
        titleId = int(arg[3][0].GetNumber())
        cfgData = TD.data.get(titleId, {})
        if cfgData.get('props', []) or cfgData.get('canApplyProp', 0):
            return GfxValue(False)
        else:
            return GfxValue(True)

    def onCheckEnablePropTitle(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enablePropTitle', False))

    def onGetTitleTooltip(self, *arg):
        p = BigWorld.player()
        titleTypeMap = {const.TITLE_TYPE_PREFIX: gameStrings.TEXT_ROLEINFOPROXY_1398,
         const.TITLE_TYPE_COLOR: gameStrings.TEXT_ROLEINFOPROXY_1399,
         const.TITLE_TYPE_BASIC: gameStrings.TEXT_ROLEINFOPROXY_1400,
         const.TITLE_TYPE_WORLD: gameStrings.TEXT_ROLEINFOPROXY_1401}
        titleId = int(arg[3][0].GetNumber())
        data = TD.data.get(titleId)
        if data is not None:
            name = p.getTitleName(titleId)
            style = data.get('style', 1)
            titleType = titleTypeMap[data.get('titleType', 3)]
            showAndActive = ''
            if arg[3][1].GetBool():
                showAndActive += gameStrings.TEXT_ROLEINFOPROXY_1412
                if arg[3][2].GetBool():
                    showAndActive += gameStrings.TEXT_CHATPROXY_403
            if arg[3][2].GetBool():
                showAndActive += gameStrings.TEXT_ROLEINFOPROXY_1417
            desc = data.get('desc', '')
            props = data.get('props', [])
            titleProp = ''
            for prop in props:
                attr = ''
                prdData = PRD.data.get(prop[0], {})
                attrName = prdData.get('name', '')
                showType = prdData.get('showType', 0)
                if showType == 1 or prop[1] == 1:
                    attr += str(round(prop[2] * 100, 1)) + '%'
                elif showType == 0:
                    attr += str(int(prop[2]))
                elif showType == 2:
                    attr += str(round(prop[2], 1))
                attrDesc = attrName + '  +' + attr
                titleProp += attrDesc + '\n'

            titleTime = ''
            if not BigWorld.player().title.isTitleOut(titleId):
                time1 = BigWorld.player().title[titleId].tAttr
                time2 = BigWorld.player().title[titleId].tOutdate
                if time2 != 0:
                    titleTime = gameStrings.TEXT_ROLEINFOPROXY_1442 + str(time.strftime('%Y-%m-%d %H:%M', time.localtime(time2)))
                if time1 != 0 and time1 != time2:
                    if titleTime:
                        titleTime += gameStrings.TEXT_ROLEINFOPROXY_1445 + str(time.strftime('%Y-%m-%d %H:%M', time.localtime(time1)))
                    else:
                        titleTime = gameStrings.TEXT_ROLEINFOPROXY_1447 + str(time.strftime('%Y-%m-%d %H:%M', time.localtime(time1)))
            else:
                titleTime = gameStrings.TEXT_ROLEINFOPROXY_1450
            tipsData = ','.join((name,
             str(style),
             str(titleType),
             showAndActive,
             desc,
             titleProp,
             titleTime))
            return GfxValue(gbk2unicode(tipsData))
        else:
            return

    def onGetApplyTips(self, *arg):
        msg = SCD.data.get('titleNoProp', '')
        return GfxValue(gbk2unicode(msg))

    def onGetDisableTips(self, *arg):
        msg = SCD.data.get('titleDisableTips', '')
        return GfxValue(gbk2unicode(msg))

    def isFashionCanDye(self):
        fashions = BigWorld.player().equipment[gametypes.EQU_PART_FASHION_HEAD:gametypes.EQU_PART_FASHION_LEG + 1] + BigWorld.player().equipment[gametypes.EQU_PART_HEADWEAR:gametypes.EQU_PART_EARWEAR + 1]
        for item in fashions:
            if item and item.isCanDye():
                return True

        return False

    def getFashionEquipment(self):
        p = BigWorld.player()
        return p.equipment[gametypes.EQU_PART_FASHION_HEAD:gametypes.EQU_PART_FASHION_LEG + 1] + p.equipment[gametypes.EQU_PART_HEADWEAR:gametypes.EQU_PART_EARWEAR + 1] + p.equipment[gametypes.EQU_PART_FASHION_WEAPON_ZHUSHOU:gametypes.EQU_PART_FASHION_WEAPON_FUSHOU + 1] + p.equipment[gametypes.EQU_PART_FASHION_NEIYI:gametypes.EQU_PART_FASHION_NEIKU + 1] + p.equipment[gametypes.EQU_PART_FOOT_DUST:gametypes.EQU_PART_FOOT_DUST + 1] + [p.equipment[gametypes.EQU_PART_YUANLING], p.equipment[gametypes.EQU_PART_FASHION_CAPE]]

    def onGetFashionInfo(self, *arg):
        p = BigWorld.player()
        showFashion = p.isShowFashion()
        if not self.isEquipedFashion():
            showFashion = False
        showEarType = 2
        showBack = commcalc.getSingleBit(p.signal, gametypes.SIGNAL_SHOW_BACK)
        showFashionWeapon = p.isShowFashionWeapon()
        hideFashionHead = p.isHideFashionHead()
        score = p.equipment.calcAllEquipScore(p.suitsCache)
        options = [showFashion,
         showEarType,
         showBack,
         showFashionWeapon,
         hideFashionHead,
         score]
        ret = []
        ret.append(options)
        if self.mediator:
            self.mediator.Invoke('enableShowFashion', GfxValue(self.isEquipedFashion()))
            self.mediator.Invoke('enableShowFashionWeapon', GfxValue(p.equipment.isEquipedFashionWeapon()))
            self.mediator.Invoke('enableHideFashionHead', GfxValue(p.realAspect.fashionHead != 0))
        fashions = self.getFashionEquipment()
        for item in fashions:
            if item:
                iconPath = uiUtils.getItemIconFile64(item.id)
                itemInfo = {'iconPath': iconPath,
                 'overIconPath': iconPath,
                 'color': uiUtils.getItemColorByItem(item),
                 'state': self.calcSlotState(item, True),
                 'cornerMark': itemToolTipUtils.getCornerMark(item)}
            else:
                itemInfo = None
            ret.append(itemInfo)

        return uiUtils.array2GfxAarry(ret, True)

    def onShowFashion(self, *arg):
        show = int(arg[3][0].GetNumber())
        BigWorld.player().cell.setSignal(gametypes.SIGNAL_SHOW_FASHION, show)

    def onShowFashionWeapon(self, *arg):
        show = arg[3][0].GetBool()
        p = BigWorld.player()
        if show != p.isShowFashionWeapon():
            p.cell.setSignal(gametypes.SIGNAL_SHOW_FASHION_WEAPON, show)

    def onGetZhuangshiTips(self, *arg):
        p = BigWorld.player()
        zhuangshiTTL = getattr(p, 'zhuangshiTTL', 0)
        tips = gameStrings.TEXT_ROLEINFOPROXY_1528
        hasTips = 0
        if zhuangshiTTL > utils.getNow():
            tips = gameStrings.TEXT_ROLEINFOPROXY_1531 % uiUtils.formatTime(zhuangshiTTL - utils.getNow())
            hasTips = 1
        return uiUtils.array2GfxAarry((hasTips, tips), True)

    def getSlotID(self, key):
        _, idSlot = key.split('.')
        return (0, int(idSlot[4:]))

    def _getFashionKey(self, bar, slot):
        return 'fashion.slot%d' % slot

    def setFashionItem(self, item, bar, slot):
        if not item:
            return
        if not self.mediator:
            return
        p = BigWorld.player()
        if self.isEquipedFashion() and slot in p.equipment.ALL_FASHION_PARTS:
            self.mediator.Invoke('enableShowFashion', GfxValue(True))
            self.mediator.Invoke('selectShowFashion', GfxValue(True))
        if p.equipment.isEquipedFashionWeapon() and slot in p.equipment.FASHION_WEAPON_PARTS:
            self.mediator.Invoke('enableShowFashionWeapon', GfxValue(True))
            self.mediator.Invoke('selectShowFashionWeapon', GfxValue(True))
        self.mediator.Invoke('enableHideFashionHead', GfxValue(p.realAspect.fashionHead != 0))
        self.mediator.Invoke('selectShowBack', GfxValue(bool(p.showBackWaist)))
        self.mediator.Invoke('setFashionSuit', self._genFashionSuit())
        key = self._getFashionKey(bar, slot)
        if not self.binding.has_key(key):
            return
        if slot not in FASHION_SLOT_BINDING_MAP:
            return
        slotIndex = FASHION_SLOT_BINDING_MAP.get(slot)
        iconPath = uiUtils.getItemIconFile64(item.id)
        itemInfo = {'iconPath': iconPath,
         'overIconPath': iconPath,
         'color': uiUtils.getItemColorByItem(item),
         'state': self.calcSlotState(item, True),
         'cornerMark': itemToolTipUtils.getCornerMark(item)}
        self.setItemSlotData(slotIndex, itemInfo)

    def removeFashionItem(self, bar, slot):
        if not self.mediator:
            return
        else:
            p = BigWorld.player()
            if not self.isEquipedFashion() and slot in p.equipment.ALL_FASHION_PARTS:
                self.mediator.Invoke('enableShowFashion', GfxValue(False))
                self.mediator.Invoke('selectShowFashion', GfxValue(False))
            if not p.equipment.isEquipedFashionWeapon() and slot in p.equipment.FASHION_WEAPON_PARTS:
                self.mediator.Invoke('enableShowFashionWeapon', GfxValue(False))
                self.mediator.Invoke('selectShowFashionWeapon', GfxValue(False))
            if p.realAspect.fashionHead == 0:
                self.mediator.Invoke('enableHideFashionHead', GfxValue(False))
                self.mediator.Invoke('selectHideFashionHead', GfxValue(False))
            self.mediator.Invoke('selectShowBack', GfxValue(bool(p.showBackWaist)))
            self.mediator.Invoke('setFashionSuit', self._genFashionSuit())
            key = self._getFashionKey(bar, slot)
            if not self.binding.has_key(key):
                return
            if slot not in FASHION_SLOT_BINDING_MAP:
                return
            slotIndex = FASHION_SLOT_BINDING_MAP.get(slot)
            self.setItemSlotData(slotIndex, None)
            return

    def onUnEquipFashion(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        p = BigWorld.player()
        unEquipItem = p.equipment[slot]
        if unEquipItem and unEquipItem.isStorageByWardrobe():
            p.cell.exchangeWardrobeEquip([''], [slot], False, '')
        else:
            page, pos = p.inv.searchEmptyInPages()
            if pos != const.CONT_NO_POS:
                cellCmd.exchangeInvEqu(page, pos, slot)
            else:
                p.showGameMsg(GMDD.data.SHOP_BAG_FULL, ())

    def onSetTabIndex(self, *arg):
        idx = int(arg[3][0].GetNumber())
        self.tabIdx = idx
        if idx != uiConst.ROLEINFO_TAB_RUNE:
            self.clearRuneChongXiState()
        if idx == uiConst.ROLEINFO_TAB_ROLE:
            if gameglobal.rds.ui.equipFeed.posMap.has_key((0, 0)):
                page, pos = gameglobal.rds.ui.equipFeed.posMap[0, 0]
                gameglobal.rds.ui.actionbar._setItemSlotState(page, pos, uiConst.ITEM_DISABLE)
        else:
            self.subEquipFlag = False

    def onSetSubEquipFlag(self, *arg):
        self.subEquipFlag = arg[3][0].GetBool()

    def getSubEquipFlag(self):
        if self.mediator:
            return self.subEquipFlag
        return False

    def onGetRuneSlotXiLianToolTip(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = key.split('.')
        runeSlotsType = int(bar[14:])
        part = int(slot[4:])
        return self.formatRuneChongXiTooltip(runeSlotsType, part)

    def formatRuneChongXiTooltip(self, runeSlotsType, part):
        p = BigWorld.player()
        if p.runeBoard.runeEquip:
            ret = []
            for key, value in p.runeBoard.runeEquip.runeEquipXiLianData.iteritems():
                runeSlotsType, part = key
                xiLianId, pskData = value
                if runeSlotsType == runeSlotsType and part == part:
                    iconPath = 'item/icon64/' + str(REXED.data[xiLianId].get('tipsIcon', 'notFound')) + '.dds'
                    bindType = gameStrings.TEXT_EQUIPSOULPROXY_1042
                    itemName = REXED.data[xiLianId]['name']
                    desc = gameStrings.TEXT_ROLEINFOPROXY_1669
                    for rTypeNeed, rLvNeed in REXED.data[xiLianId].get('activateCondition', []):
                        desc += gameStrings.TEXT_ROLEINFOPROXY_1671 + str(rLvNeed) + gameStrings.TEXT_ROLEINFOPROXY_1671_1 + const.RUNE_NAME_DESC[rTypeNeed] + '\n'

                    desc += gameStrings.TEXT_ROLEINFOPROXY_1672
                    for skillId in pskData:
                        skillLv = pskData[skillId]
                        desc += gameglobal.rds.ui.runeView.generateDesc(skillId, PSkillInfo(skillId, skillLv, {}), skillLv) + '\n'

                    for effect in REXED.data[xiLianId].get('effects', []):
                        if effect[0] == gametypes.RUNE_EQUIP_XILIAN_EFFECT_TYPE_SHENLI:
                            desc += const.RUNE_POWER_DESC[effect[1]] + '*' + str(effect[2]) + '\n'

                    isActivate = False
                    for runeDataVal in p.runeBoard.runeEquip.runeData:
                        if runeDataVal.runeSlotsType == runeSlotsType and runeDataVal.part == part:
                            for rTypeNeed, rLvNeed in REXED.data[xiLianId].get('activateCondition', []):
                                if runeDataVal.item.runeLv >= rLvNeed and RD.data[runeDataVal.item.id]['runeEffects'][rTypeNeed] > 0:
                                    isActivate = True
                                    break

                    if isActivate:
                        bindType = gameStrings.TEXT_EQUIPSOULPROXY_1042
                    else:
                        bindType = gameStrings.TEXT_EQUIPSOULPROXY_1045
                    ret.append({'itemName': itemName,
                     'bindType': bindType,
                     'isCurrentEquip': False,
                     'price': '',
                     'priceLabel': '',
                     'iconPath': iconPath,
                     'desc': desc,
                     'runeDesc': '',
                     'enhLv': '',
                     'qualityColor': 'gray',
                     'score': '',
                     'useTime': '',
                     'isRand': '',
                     'dura': '',
                     'schReq': '',
                     'equPart': '',
                     'starLv': 0,
                     'maxStarLv': 0,
                     'lv': 1,
                     'starExp': 0,
                     'maxStarExp': 0,
                     'rank': '',
                     'basicProp': '',
                     'aptitude': '',
                     'randProp': '',
                     'prefixProp': '',
                     'enhProp': '',
                     'fixedProp': '',
                     'extraProp': '',
                     'extraSkill': '',
                     'limits': [],
                     'lvReq': {'satisfy': True,
                               'desc': ''},
                     'compositeShopData': '',
                     'boothLabel': '',
                     'boothPrice': '',
                     'initStarLv': 0,
                     'maker': '',
                     'tianlunSlotNum': '',
                     'dilunSlotNum': '',
                     'allRuneEffects': (),
                     'runeEquipData': [],
                     'ownerShip': True,
                     'returnTime': '',
                     'famePrice': [],
                     'learnDesc': '',
                     'isEquip': False})
                    return uiUtils.array2GfxAarry(ret, True)

        return GfxValue('')

    def clearState(self):
        self.clearRuneChongXiState()

    def setRuneChongXiState(self):
        self.uiAdapter.clearState()
        self.isRuneChongXiState = True
        self.updateRuneChongXiState()
        if ui.get_cursor_state() != ui.RUNE_CHONGXI_STATE:
            ui.reset_cursor()
            ui.set_cursor_state(ui.RUNE_CHONGXI_STATE)
            ui.set_cursor(cursor.pickup)
            ui.lock_cursor()

    def clearRuneChongXiState(self):
        if self.isRuneChongXiState:
            self.isRuneChongXiState = False
            self.updateRuneChongXiState()
            if ui.get_cursor_state() == ui.RUNE_CHONGXI_STATE:
                ui.reset_cursor()

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        i = BigWorld.player().equipment.get(slot)
        return self.uiAdapter.inventory.GfxToolTip(i, const.ITEM_IN_EQUIPMENT)

    def onGetFashionSuit(self, *arg):
        ret = self._genFashionSuit()
        return ret

    def _genFashionSuit(self):
        fashions = self.getFashionEquipment()
        arr = [0] * len(fashions)
        for i, item in enumerate(fashions):
            if not item:
                continue
            eData = ED.data.get(item.id, {})
            parts = eData.get('slotParts', [])
            if parts:
                arr[i] = 1
                for part in parts:
                    arr[self.fashionPart[part]] = 1

        return uiUtils.array2GfxAarry(arr)

    def isEquipedFashion(self):
        p = BigWorld.player()
        return p.equipment.isEquipedFashion()

    def getPropsArray(self, type):
        ret = []
        for key, val in RPAD.data.items():
            if val['type'] == type:
                ret.append(val)

        ret.sort(key=lambda k: k['displayOrder'])
        return ret

    def getPropValueById(self, owner, propId):
        if not PD.data.has_key(propId):
            if propId == 20001:
                return owner.atk[0]
            elif propId == 20002:
                return max(owner.atk[0], owner.atk[1])
            elif propId == 20003:
                return owner.atk[2]
            elif propId == 20004:
                return max(owner.atk[2], owner.atk[3])
            elif propId == 20005:
                return owner.defence[0]
            elif propId == 20006:
                return owner.defence[1]
            elif propId == 20007:
                return max(0, int((0.4 * owner.equipAtk[2] + owner.healAdd) * (1 + owner.atkDefRatio[9])))
            elif propId == 20008:
                return max(0, int((0.4 * max(owner.equipAtk[2], owner.equipAtk[3]) + owner.healAdd) * (1 + owner.atkDefRatio[9])))
            else:
                raise Exception('@zs, getPropValueById, propId wrong:%d' % propId)
                return
        return commcalc.getAvatarPropValueById(owner, propId)

    def onGetPropsTooltip(self, *arg):
        params = arg[3][0].GetString().split(',')
        key = (int(params[0]), int(params[1]))
        ret = self.getPropsTipContent(key)
        return uiUtils.dict2GfxDict(ret, True)

    def getPropsTipContent(self, key):
        p = BigWorld.player()
        ret = {}
        data = RPAD.data.get(key, {})
        if data:
            detail = data.get('detail' + str(BigWorld.player().school - 2), '')
            i = 1
            formulaDate = data.get('formula' + str(i), '')
            while formulaDate:
                for idx, item in enumerate(data.get('formual' + str(i) + 'Params', [])):
                    formulaDate = formulaDate.replace('p' + str(idx + 1), str(self.getPropValueById(p, item)))

                try:
                    val = eval(formulaDate)
                except:
                    val = 0

                detail = detail.replace('[1.p' + str(i) + ']', str(int(val)))
                detail = detail.replace('[2.p' + str(i) + ']', str(round(val * 100, 1)) + '%')
                detail = detail.replace('[3.p' + str(i) + ']', str(round(val, 1)))
                i += 1
                formulaDate = data.get('formula' + str(i), '')

            if detail.find('$d1') and detail.find('$d2'):
                bVal = 0
                val = 0
                if PDD.data.PROPERTY_ATTR_PW in data['idGroup']:
                    bVal = p.getPrimaryPropBaseValue(PDD.data.PROPERTY_ATTR_PW)
                    val = p.primaryProp.pow - bVal
                elif PDD.data.PROPERTY_ATTR_INT in data['idGroup']:
                    bVal = p.getPrimaryPropBaseValue(PDD.data.PROPERTY_ATTR_INT)
                    val = p.primaryProp.int - bVal
                elif PDD.data.PROPERTY_ATTR_PHY in data['idGroup']:
                    bVal = p.getPrimaryPropBaseValue(PDD.data.PROPERTY_ATTR_PHY)
                    val = p.primaryProp.phy - bVal
                elif PDD.data.PROPERTY_ATTR_SPR in data['idGroup']:
                    bVal = p.getPrimaryPropBaseValue(PDD.data.PROPERTY_ATTR_SPR)
                    val = p.primaryProp.spr - bVal
                elif PDD.data.PROPERTY_ATTR_AGI in data['idGroup']:
                    bVal = p.getPrimaryPropBaseValue(PDD.data.PROPERTY_ATTR_AGI)
                    val = p.primaryProp.agi - bVal
                detail = detail.replace('$d1', str(bVal))
                detail = detail.replace('$d2', str(val))
            ret['tipContent'] = detail
            ret['guideData'] = self.getGuideData(key)
        return ret

    def getGuideData(self, key):
        if not gameglobal.rds.configData.get('enableCareerGuilde', False):
            return ''
        p = BigWorld.player()
        if not hasattr(p, 'carrerGuideData'):
            return ''
        if p.lv <= gametypes.GUIDE_ATTR_LV_REQUIRE:
            return ''
        primaryInfo = p.carrerGuideData.get('primaryInfo', {})
        lvKey, lvTxt = uiUtils.getGuideLv()
        if not primaryInfo or not primaryInfo.get(lvKey, []):
            return ''
        attrIdx = ATTR_GUIDE_KEY_DICT.get(key, -1)
        if attrIdx < 0:
            return ''
        lv = p.lv
        schoolName = const.SCHOOL_DICT[p.school]
        attrNum = primaryInfo.get(lvKey, [])[attrIdx]
        data = RPAD.data.get(key, {})
        attrName = data.get('name', '')
        return gameStrings.ATTR_GUIDE_TIP % (lvTxt,
         schoolName,
         attrNum,
         attrName)

    def updateAllPotential(self):
        p = BigWorld.player()
        for type in potentialMap:
            prop = getattr(p.primaryProp, potentialMap[type], 0)
            bProp = p.getPrimaryPropBaseValue(potentialIdMap[type])
            if getattr(self, potentialMap[type] + 'Add'):
                val = "%d<font color = \'#E5BE67\'> + %d</font>" % (getattr(self, potentialMap[type] + 'Add') + bProp, prop - bProp)
                self.updatePotential(type, val)
            else:
                val = "<font color = \'#FFFFFF\'>%d</font><font color = \'#E5BE67\'> + %d</font>" % (bProp, prop - bProp)
                self.updatePotential(type, val, False)

        self.updatePotential(uiConst.POTENTIAL_ALL, self.getCanUsePoint())
        self.calAttrPreview()
        if self.powAdd + self.intAdd + self.phyAdd + self.sprAdd + self.agiAdd == 0:
            self.clearPreivew()

    def updatePotential(self, type, value, isAdd = True):
        if self.mediator:
            if type == uiConst.POTENTIAL_ALL:
                pointInfo = {}
                p = BigWorld.player()
                extraPotPoint = p.primaryProp.gpoint - min(ALD.data.get(p.realLv, {}).get('maxGPoint', 0), p.primaryProp.gpoint)
                if extraPotPoint > 0:
                    pointInfo['extraPotPoint'] = '(+%d)' % extraPotPoint
                    pointInfo['extraPotPointTips'] = gameStrings.TEXT_ROLEINFOPROXY_526 % extraPotPoint
                else:
                    pointInfo['extraPotPoint'] = ''
                    pointInfo['extraPotPointTips'] = ''
                pointInfo['potPoint'] = gameStrings.TEXT_ROLEINFOPROXY_530 % (p.primaryProp.point - self.pointMinus - extraPotPoint)
                self.mediator.Invoke('updatePotPoint', uiUtils.dict2GfxDict(pointInfo, True))
            else:
                self.mediator.Invoke('updatePotential', (GfxValue(type), GfxValue(value), GfxValue(isAdd)))

    def potBtnVisible(self, visibleList):
        if self.mediator:
            self.mediator.Invoke('potBtnVisible', uiUtils.array2GfxAarry(visibleList))

    def schoolSwitchPotential(self):
        p = BigWorld.player()
        self.potBtnVisible([])
        self.updatePotential(uiConst.POTENTIAL_ALL, 0)
        for type in potentialMap:
            prop = getattr(p.primaryProp, potentialMap[type], 0)
            bProp = commcalc.getPrimaryPropBaseValueInSchoolSwitch(p, potentialIdMap[type])
            op = '+' if prop >= bProp else '-'
            val = "<font color = \'#FFFFFF\'>%d</font><font color = \'#E5BE67\'> %s %d</font>" % (bProp, op, abs(prop - bProp))
            self.updatePotential(type, val, False)

    def onPotChange(self, *arg):
        p = BigWorld.player()
        type = int(arg[3][0].GetString())
        if type in potentialMap:
            lv = getattr(p.primaryProp, 'b' + potentialMap[type]) + getattr(self, potentialMap[type] + 'Add')
            pointReduce = self.calcPoint(potentialMap[type], lv)
            if pointReduce + self.pointMinus <= self.getCanUsePoint():
                self.pointMinus += pointReduce
                value = getattr(self, potentialMap[type] + 'Add') + 1
                setattr(self, potentialMap[type] + 'Add', value)
                prop = getattr(p.primaryProp, potentialMap[type], 0)
                bProp = p.getPrimaryPropBaseValue(potentialIdMap[type])
                val = "%d<font color = \'#E5BE67\'> + %d</font>" % (getattr(self, potentialMap[type] + 'Add') + bProp, prop - bProp)
                self.updatePotential(type, val)
                self.updatePotBtnVisible()
        else:
            type -= uiConst.POTENTIAL_DIF
            if getattr(self, potentialMap[type] + 'Add') <= 0:
                return
            lv = getattr(p.primaryProp, 'b' + potentialMap[type]) + getattr(self, potentialMap[type] + 'Add') - 1
            pointReduce = self.calcPoint(potentialMap[type], lv)
            if pointReduce <= self.pointMinus:
                self.pointMinus -= pointReduce
                value = getattr(self, potentialMap[type] + 'Add') - 1
                setattr(self, potentialMap[type] + 'Add', value)
                prop = getattr(p.primaryProp, potentialMap[type], 0)
                bProp = p.getPrimaryPropBaseValue(potentialIdMap[type])
                if getattr(self, potentialMap[type] + 'Add'):
                    val = "%d<font color = \'#E5BE67\'> + %d</font>" % (getattr(self, potentialMap[type] + 'Add') + bProp, prop - bProp)
                else:
                    val = "<font color = \'#FFFFFF\'>%d</font><font color = \'#E5BE67\'> + %d</font>" % (getattr(self, potentialMap[type] + 'Add') + bProp, prop - bProp)
                self.updatePotential(type, val, getattr(self, potentialMap[type] + 'Add'))
                self.updatePotBtnVisible()
        self.updatePotential(uiConst.POTENTIAL_ALL, self.getCanUsePoint() - self.pointMinus)
        self.calAttrPreview()
        if self.powAdd + self.intAdd + self.phyAdd + self.sprAdd + self.agiAdd == 0:
            self.clearPreivew()
        savingKey = keys.SET_UI_INFO + '/' + 'roleInfo' + '/open/raid'
        if AppSettings.get(savingKey, 1) != 1:
            AppSettings[savingKey] = 1
            AppSettings.save()

    def calcPoint(self, type, lv):
        p = BigWorld.player()
        pppcd = PPPCD.data.get(p.school, {})
        if pppcd:
            if type in ('pow', 'int', 'phy', 'spr', 'agi'):
                pd = pppcd[type]
                fId = pd[0]
                vars = {'lv': lv}
                params = pd[1:]
                for i in range(len(params)):
                    param = params[i]
                    vars['p%d' % (i + 1,)] = param

                return formula.calcFormulaById(fId, vars)
        return 0

    def onPotConfirm(self, *arg):
        if not BigWorld.player().stateMachine.checkStatus(const.CT_ASSIGN_PROPPOINT):
            return
        BigWorld.player().cell.assignPrimaryPropPonit(self.powAdd, self.intAdd, self.phyAdd, self.sprAdd, self.agiAdd)
        self.pointMinus = 0
        self.powAdd = 0
        self.intAdd = 0
        self.phyAdd = 0
        self.sprAdd = 0
        self.agiAdd = 0
        self.clearPreivew()

    def onPotReset(self, *args):
        p = BigWorld.player()
        if p.isUsingTemp():
            msg = gameStrings.TEXT_ROLEINFOPROXY_1991
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.resetPotential)
            return
        curplayer = BigWorld.player()
        if curplayer.lv >= SCD.data.get('resetPropPointFreeLv', 59):
            page, pos = curplayer.inv.findPassiveUseItemByAttr(curplayer, {'cstype': Item.SUBTYPE_2_REWARD_POINT_RESET,
             'clearPoint': 1}, skipLatchItem=True, lv=curplayer.lv)
            itemFameData = {}
            if page == const.CONT_NO_PAGE or pos == const.CONT_NO_POS:
                if gameglobal.rds.configData.get('enableCoinDikou', False):
                    if curplayer.lv >= 69:
                        itemId = SCD.data.get('resetPropPointSchemeItemCoinDikou', ())[1]
                    else:
                        itemId = SCD.data.get('resetPropPointSchemeItemCoinDikou', ())[0]
                    itemFameData['itemId'] = itemId
                    itemFameData['deltaNum'] = 1
                    itemFameData['type'] = 'tianbi'
                    msg = uiUtils.getTextFromGMD(GMDD.data.POT_RESET_INVENT_NEED, '')
                    itemIds = IPD.data.get(itemId, [])
                    itemIds.append(itemId)
                    itemCost = 0
                    for id in itemIds:
                        if ICDCD.data.has_key(id):
                            itemCoinData = ICDCD.data.get(id, [])
                            itemCost = itemCoinData[1]

                    totalCost = 1 * itemCost
                    tianBi = curplayer.unbindCoin + curplayer.bindCoin + curplayer.freeCoin
                    if totalCost <= tianBi:
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.useTianbiResetPot, True), itemFameData=itemFameData)
                    else:
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.useTianbiResetPot, False), itemFameData=itemFameData)
                else:
                    msg = uiUtils.getTextFromGMD(GMDD.data.POT_RESET_INVENT_NEED, '')
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg)
            else:
                msg = uiUtils.getTextFromGMD(GMDD.data.POT_RESET_INVENT_COST, '')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.resetPotential)
        else:
            msg = uiUtils.getTextFromGMD(GMDD.data.POT_RESET_INVENT_FREE, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.resetPotential)

    @ui.checkInventoryLock()
    def useTianbiResetPot(self, isCoinEnough = False):
        p = BigWorld.player()
        p.cell.resetPropPointScheme(True, p.cipherOfPerson)
        if isCoinEnough:
            self.mediator.Invoke('resetPotSuccess')

    def resetPotential(self):
        if not self.mediator:
            return
        BigWorld.player().cell.resetPropPointScheme(False, BigWorld.player().cipherOfPerson)
        self.mediator.Invoke('resetPotSuccess')

    def calcRecommendPoint(self, type, planId = -1):
        p = BigWorld.player()
        sdData = SD.data.get(p.realSchool)
        if not sdData:
            return 0
        _, bpow, bint, bphy, bspr, bagi = sdData.get('point', (0, 0, 0, 0, 0, 0))
        consumePoint = self._calcPrimaryPropPointConsume(bpow, bint, bphy, bspr, bagi, p.primaryProp.bpow, p.primaryProp.bint, p.primaryProp.bphy, p.primaryProp.bspr, p.primaryProp.bagi)
        if planId == -1:
            btnNum = int(self.mediator.Invoke('getSelectedPotBtn', ()).GetNumber())
            prcdDate = RPD.data.get((p.realSchool, btnNum + 1), {})
        else:
            prcdDate = RPD.data.get((p.realSchool, planId), {})
        if not prcdDate:
            prcdDate = RPD.data.get(p.realSchool, {})
        if prcdDate:
            if type in ('pow', 'int', 'phy', 'spr', 'agi'):
                pd = prcdDate[type]
                fId = pd[0]
                vars = {'point': p.primaryProp.point + consumePoint}
                params = pd[1:]
                for i in range(len(params)):
                    param = params[i]
                    vars['p%d' % (i + 1,)] = param

                return formula.calcFormulaById(fId, vars)
        return 0

    def _calcPrimaryPropPointConsume(self, bPow, bInt, bPhy, bSpr, bAgi, destPow, destInt, destPhy, destSpr, destAgi):
        p = BigWorld.player()
        pppcd = PPPCD.data.get(p.realSchool, {})
        if not pppcd:
            return 0
        tmpDict = {'pow': [bPow, destPow],
         'int': [bInt, destInt],
         'phy': [bPhy, destPhy],
         'spr': [bSpr, destSpr],
         'agi': [bAgi, destAgi]}
        res = 0
        for propName, val in tmpDict.items():
            pd = pppcd[propName]
            fId = pd[0]
            params = pd[1:]
            baseVal, destVal = val
            vars = {}
            for i in range(len(params)):
                param = params[i]
                vars['p%d' % (i + 1,)] = param

            for value in range(baseVal, destVal):
                vars['lv'] = value
                res += formula.calcFormulaById(fId, vars)

        return res

    def getCanUsePoint(self):
        p = BigWorld.player()
        leftPoint = p.primaryProp.point
        sdData = SD.data.get(p.realSchool)
        _, bpow, bint, bphy, bspr, bagi = sdData.get('point', (0, 0, 0, 0, 0, 0))
        consumePoint = self._calcPrimaryPropPointConsume(bpow, bint, bphy, bspr, bagi, p.primaryProp.bpow, p.primaryProp.bint, p.primaryProp.bphy, p.primaryProp.bspr, p.primaryProp.bagi)
        allPoint = leftPoint + consumePoint
        ad = ALD.data.get(p.lv)
        maxGPoint = ad.get('maxGPoint', 0)
        lvp = allPoint - p.primaryProp.gpoint
        canUse = min(p.primaryProp.gpoint, maxGPoint)
        canUseNow = lvp + canUse - consumePoint
        return canUseNow

    def onPotRecommend(self, *arg):
        p = BigWorld.player()
        self.powAdd = 0
        self.intAdd = 0
        self.phyAdd = 0
        self.sprAdd = 0
        self.agiAdd = 0
        self.pointMinus = 0
        recommendMap = {}
        recommendMap['pow'] = self.calcRecommendPoint('pow') - p.primaryProp.bpow
        recommendMap['int'] = self.calcRecommendPoint('int') - p.primaryProp.bint
        recommendMap['phy'] = self.calcRecommendPoint('phy') - p.primaryProp.bphy
        recommendMap['spr'] = self.calcRecommendPoint('spr') - p.primaryProp.bspr
        recommendMap['agi'] = self.calcRecommendPoint('agi') - p.primaryProp.bagi
        canUseNow = self.getCanUsePoint()
        recommendList = sorted(recommendMap.items(), key=lambda d: d[1], reverse=True)
        for type, typeValue in recommendList:
            if typeValue <= 0:
                self.updatePotBtnVisible()
                self.updateAllPotential()
                self.calAttrPreview()
                if self.powAdd + self.intAdd + self.phyAdd + self.sprAdd + self.agiAdd == 0:
                    self.clearPreivew()
                self.updatePotential(uiConst.POTENTIAL_ALL, self.getCanUsePoint() - self.pointMinus)
                return
            for value in range(0, typeValue):
                lv = getattr(p.primaryProp, 'b' + type) + value
                pointReduce = self.calcPoint(type, lv)
                if self.pointMinus + pointReduce > canUseNow:
                    setattr(self, type + 'Add', value)
                    self.updatePotBtnVisible()
                    self.updateAllPotential()
                    self.calAttrPreview()
                    if self.powAdd + self.intAdd + self.phyAdd + self.sprAdd + self.agiAdd == 0:
                        self.clearPreivew()
                    self.updatePotential(uiConst.POTENTIAL_ALL, self.getCanUsePoint() - self.pointMinus)
                    return
                self.pointMinus += pointReduce

            setattr(self, type + 'Add', typeValue)

        self.updatePotBtnVisible()
        self.updateAllPotential()
        self.calAttrPreview()
        if self.powAdd + self.intAdd + self.phyAdd + self.sprAdd + self.agiAdd == 0:
            self.clearPreivew()
        self.updatePotential(uiConst.POTENTIAL_ALL, self.getCanUsePoint() - self.pointMinus)

    def updatePotBtnVisible(self):
        valueDict = {}
        p = BigWorld.player()
        canUseNow = self.getCanUsePoint()
        point = canUseNow - self.pointMinus
        for type in ('pow', 'int', 'phy', 'spr', 'agi'):
            lv = getattr(p.primaryProp, 'b' + type) + getattr(self, type + 'Add')
            valueDict[type] = point >= self.calcPoint(type, lv)

        canRecom = False
        for i in xrange(3):
            recommendMap = {}
            planId = i + 1
            recommendMap['pow'] = self.calcRecommendPoint('pow', planId) - p.primaryProp.bpow
            recommendMap['int'] = self.calcRecommendPoint('int', planId) - p.primaryProp.bint
            recommendMap['phy'] = self.calcRecommendPoint('phy', planId) - p.primaryProp.bphy
            recommendMap['spr'] = self.calcRecommendPoint('spr', planId) - p.primaryProp.bspr
            recommendMap['agi'] = self.calcRecommendPoint('agi', planId) - p.primaryProp.bagi
            recommendList = sorted(recommendMap.items(), key=lambda d: d[1], reverse=True)
            for type, typeValue in recommendList:
                if typeValue > 0:
                    lv = getattr(p.primaryProp, 'b' + type) + 1
                    pointReduce = self.calcPoint(type, lv)
                    if pointReduce <= canUseNow:
                        canRecom = True
                if canRecom:
                    break

            if canRecom:
                break

        arrForPlan = [None, None, None]
        hasPlan = False
        for i in xrange(3):
            planId = i + 1
            planData = RPD.data.get((p.school, planId))
            if planData:
                arrForPlan[i] = gbk2unicode(planData.get('planName'))
                hasPlan = True

        if hasPlan == False:
            txt = gameStrings.TEXT_ROLEINFOPROXY_2218
            arrForPlan[0] = gbk2unicode(txt)
        self.potBtnVisible([valueDict['pow'],
         valueDict['int'],
         valueDict['phy'],
         valueDict['spr'],
         valueDict['agi'],
         self.powAdd,
         self.intAdd,
         self.phyAdd,
         self.sprAdd,
         self.agiAdd,
         canRecom,
         arrForPlan[0],
         arrForPlan[1],
         arrForPlan[2]])

    def onGetAllPotPointTips(self, *arg):
        str = ''
        p = BigWorld.player()
        leftPoint = p.primaryProp.point
        sdData = SD.data.get(p.realSchool)
        if not sdData:
            return GfxValue(gbk2unicode(str))
        _, bpow, bint, bphy, bspr, bagi = sdData.get('point', (0, 0, 0, 0, 0, 0))
        consumePoint = self._calcPrimaryPropPointConsume(bpow, bint, bphy, bspr, bagi, p.primaryProp.bpow, p.primaryProp.bint, p.primaryProp.bphy, p.primaryProp.bspr, p.primaryProp.bagi)
        allPoint = leftPoint + consumePoint
        ad = ALD.data.get(p.lv)
        maxGPoint = ad.get('maxGPoint', 0)
        showGPoint = min(maxGPoint, p.primaryProp.gpoint)
        lvp = allPoint - p.primaryProp.gpoint
        canUse = min(p.primaryProp.gpoint, maxGPoint)
        canUseNow = lvp + canUse - consumePoint
        str = gameStrings.TEXT_ROLEINFOPROXY_2243 % (allPoint, canUseNow)
        str += gameStrings.TEXT_ROLEINFOPROXY_2244 % lvp
        str += gameStrings.TEXT_ROLEINFOPROXY_2245 % p.primaryProp.gpoint
        str += gameStrings.TEXT_ROLEINFOPROXY_2246 % showGPoint
        return GfxValue(gbk2unicode(str))

    def onGetPotTooltip(self, *arg):
        p = BigWorld.player()
        PotToolTipMap = {uiConst.POTENTIAL_POW: gameStrings.TEXT_ROLEINFOPROXY_2252,
         uiConst.POTENTIAL_INT: gameStrings.TEXT_ROLEINFOPROXY_2253,
         uiConst.POTENTIAL_PHY: gameStrings.TEXT_ROLEINFOPROXY_2254,
         uiConst.POTENTIAL_SPR: gameStrings.TEXT_ROLEINFOPROXY_2255,
         uiConst.POTENTIAL_AGI: gameStrings.TEXT_ROLEINFOPROXY_2256}
        type = int(arg[3][0].GetString())
        lv = getattr(p.primaryProp, 'b' + potentialMap[type]) + getattr(self, potentialMap[type] + 'Add')
        pointReduce = self.calcPoint(potentialMap[type], lv)
        return GfxValue(gbk2unicode(PotToolTipMap[type] % pointReduce))

    def onGetPotData(self, *arg):
        if BigWorld.player()._isSchoolSwitch():
            self.schoolSwitchPotential()
        else:
            self.updatePotBtnVisible()
            self.updateAllPotential()

    def onGetRuneData(self, *arg):
        p = BigWorld.player()
        dataObj = self.movie.CreateObject()
        pskillArray = self.movie.CreateArray()
        itemArr = self.movie.CreateArray()
        tianLunEffectArray = self.movie.CreateArray()
        diLunEffectArray = self.movie.CreateArray()
        dataObj.SetMember('school', GfxValue(p.school))
        if p.runeBoard.runeEquip:
            xiLianSlotArr = self.movie.CreateArray()
            xiLianIconArr = self.movie.CreateArray()
            xiLianSlotNum = 0
            for key, value in p.runeBoard.runeEquip.runeEquipXiLianData.iteritems():
                runeSlotsType, part = key
                xiLianId, pskData = value
                xiLianSlotArr.SetElement(xiLianSlotNum, GfxValue(runeSlotsType * 10 + part))
                xiLianIconArr.SetElement(xiLianSlotNum, GfxValue(REXED.data[xiLianId]['icon']))
                xiLianSlotNum += 1
                runeSlotsType * 10 + part

            dataObj.SetMember('xiLianSlotArr', xiLianSlotArr)
            dataObj.SetMember('xiLianIconArr', xiLianIconArr)
            i = 0
            arr = self.initItemArr(p.runeBoard.runeEquip, 0)
            itemArr.SetElement(i, arr)
            i += 1
            for runeDataVal in p.runeBoard.runeEquip.runeData:
                if runeDataVal.item:
                    arr = self.initItemArr(runeDataVal.item, runeDataVal.runeSlotsType * 10 + runeDataVal.part)
                    itemArr.SetElement(i, arr)
                    i += 1

        dataObj.SetMember('itemArr', itemArr)
        if p.runeBoard.runeEquip:
            dataObj.SetMember('tianLunSlotsNum', GfxValue(p.runeBoard.runeEquip.getRuneEquipSlotNum(const.RUNE_TYPE_TIANLUN)))
            dataObj.SetMember('diLunSlotsNum', GfxValue(p.runeBoard.runeEquip.getRuneEquipSlotNum(const.RUNE_TYPE_DILUN)))
            dataObj.SetMember('benYuanSlotsNum', GfxValue(p.runeBoard.runeEquip.getRuneEquipSlotNum(const.RUNE_TYPE_BENYUAN)))
            juexingValid = bool(REQD.data.get(p.runeBoard.runeEquip.id, {}).get('juexingValid', 1))
            dataObj.SetMember('juexingValid', GfxValue(juexingValid))
            dataObj.SetMember('tianlunAwake', GfxValue(p.runeBoard.awakeDict[const.RUNE_TYPE_TIANLUN] and juexingValid))
            dataObj.SetMember('dilunAwake', GfxValue(p.runeBoard.awakeDict[const.RUNE_TYPE_DILUN] and juexingValid))
        else:
            dataObj.SetMember('tianlunAwake', GfxValue(False))
            dataObj.SetMember('dilunAwake', GfxValue(False))
        i = 0
        for effectId in p.runeBoard.pskillSet:
            pskillId, pskillLv = p.runeBoard.pskillSet[effectId]
            pskillObj = self.movie.CreateObject()
            desc = gameglobal.rds.ui.runeView.generateDesc(pskillId, PSkillInfo(pskillId, pskillLv, {}), pskillLv)
            pskillObj.SetMember('name', GfxValue(gbk2unicode(RED.data.get(effectId, [])[pskillLv - 1].get('name', ''))))
            pskillObj.SetMember('desc', GfxValue(gbk2unicode(desc)))
            pskillArray.SetElement(i, pskillObj)
            i += 1

        dataObj.SetMember('pskillArray', pskillArray)
        i = 0
        j = 0
        if p.runeBoard.runeEquip:
            tianLunEffectData = REQD.data[p.runeBoard.runeEquip.id]['tianLunAwakeNeed']
            diLunEffectData = REQD.data[p.runeBoard.runeEquip.id]['diLunAwakeNeed']
            for id in xrange(const.RUNE_EFFECT_TYPE_NUM):
                if tianLunEffectData[id]:
                    tianLunEffectObj = self.movie.CreateObject()
                    tianLunEffectObj.SetMember('type', GfxValue(uiConst.RUNE_TUPLE[id]))
                    tianLunEffectObj.SetMember('needValue', GfxValue(tianLunEffectData[id]))
                    tianLunEffectObj.SetMember('value', GfxValue(p.runeBoard.runeEffectsDict[const.RUNE_TYPE_TIANLUN][id]))
                    tianLunEffectArray.SetElement(i, tianLunEffectObj)
                    i += 1
                if diLunEffectData[id]:
                    diLunEffectObj = self.movie.CreateObject()
                    diLunEffectObj.SetMember('type', GfxValue(uiConst.RUNE_TUPLE[id]))
                    diLunEffectObj.SetMember('needValue', GfxValue(diLunEffectData[id]))
                    diLunEffectObj.SetMember('value', GfxValue(p.runeBoard.runeEffectsDict[const.RUNE_TYPE_DILUN][id]))
                    diLunEffectArray.SetElement(j, diLunEffectObj)
                    j += 1

            tianLunPSkillList = REQD.data.get(p.runeBoard.runeEquip.id, {}).get('tianLunPSkillList', ())
            diLunPSkillList = REQD.data.get(p.runeBoard.runeEquip.id, {}).get('diLunPSkillList', ())
            if tianLunPSkillList:
                pskId = tianLunPSkillList[0]
                tianLunPskillDesc = gameglobal.rds.ui.runeView.generateDesc(pskId, PSkillInfo(pskId, p.runeBoard.runeEquip.runeEquipLv, {}), p.runeBoard.runeEquip.runeEquipLv)
                dataObj.SetMember('tianLunPskill', GfxValue(gbk2unicode(tianLunPskillDesc)))
            if diLunPSkillList:
                pskId = diLunPSkillList[0]
                diLunPskillDesc = gameglobal.rds.ui.runeView.generateDesc(pskId, PSkillInfo(pskId, p.runeBoard.runeEquip.runeEquipLv, {}), p.runeBoard.runeEquip.runeEquipLv)
                dataObj.SetMember('diLunPskill', GfxValue(gbk2unicode(diLunPskillDesc)))
            dataObj.SetMember('tianLunEffectArray', tianLunEffectArray)
            dataObj.SetMember('diLunEffectArray', diLunEffectArray)
            dataObj.SetMember('runeEquipLv', GfxValue(p.runeBoard.runeEquip.runeEquipLv))
            if const.RUNE_EQUIP_MAX_LV <= p.runeBoard.runeEquip.runeEquipLv:
                eData = REED.data.get((const.RUNE_EQUIP_MAX_LV - 1, p.runeBoard.runeEquip.runeEquipOrder))
                dataObj.SetMember('runeEquipExp', GfxValue(eData['upExp']))
                dataObj.SetMember('runeEquipUpExp', GfxValue(eData['upExp']))
            else:
                eData = REED.data.get((p.runeBoard.runeEquip.runeEquipLv, p.runeBoard.runeEquip.runeEquipOrder))
                dataObj.SetMember('runeEquipUpExp', GfxValue(eData['upExp']))
                dataObj.SetMember('runeEquipExp', GfxValue(p.runeBoard.runeEquip.runeEquipExp))
            dataObj.SetMember('runeEquipOrder', GfxValue(p.runeBoard.runeEquip.runeEquipOrder))
            dataObj.SetMember('runeEquipAptitude', GfxValue(p.runeBoard.runeEquip.runeEquipAptitude))
            dataObj.SetMember('canOrderUp', GfxValue(REQD.data[p.runeBoard.runeEquip.id]['orderUpLvLimit'] <= p.runeBoard.runeEquip.runeEquipLv))
            dataObj.SetMember('runeEquipUuid', GfxValue(str(p.runeBoard.runeEquip.uuid)))
        else:
            dataObj.SetMember('runeEquipUuid', GfxValue('0'))
        return dataObj

    def _getSocialPropItem(self, desc, num, tips):
        ret = self.movie.CreateObject()
        ret.SetMember('desc', GfxValue(gbk2unicode(desc)))
        ret.SetMember('num', GfxValue(num))
        ret.SetMember('tips', GfxValue(gbk2unicode(tips)))
        return ret

    def genLifeSkillEquipSkillLvList(self, skillName):
        reqSkillLvTips = []
        num = 1
        toolPartsCount = LSCD.data.get('toolPartsCount', {})
        for key, val in sorted(toolPartsCount.iteritems(), key=lambda d: d[0]):
            if val == num:
                reqSkillLvTips.append(gameStrings.TEXT_ROLEINFOPROXY_2394 % skillName + str(key[0]) + gameStrings.TEXT_MANUALEQUIPPROXY_171)
                num += 1

        return reqSkillLvTips

    def _getEquipByLifeSkillType(self, lifeSkillType):
        produeceData = LSSRD.data[lifeSkillType]
        p = BigWorld.player()
        produceEquipItems = []
        for key in sorted(produeceData.iterkeys()):
            for subVal in produeceData[key]:
                if not subVal['open']:
                    continue
                skillId = utils.getLifeSkillIdBySubType(subVal['id'])
                limitCnt = utils.getLifeCanEquipCnt(p, skillId)
                skillLevel = p.lifeSkill.get(skillId, {}).get('level', 0)
                itemInfo = {'limitCnt': limitCnt,
                 'equipData': [],
                 'reqSkillLvTips': self.genLifeSkillEquipSkillLvList(subVal['name']),
                 'itemName': subVal['name'],
                 'itemLv': 'lv.' + str(skillLevel)}
                for part in gametypes.LIFE_EQUIPMENT_PART:
                    if p.lifeEquipment.has_key((subVal['id'], part)) and p.lifeEquipment[subVal['id'], part]:
                        itemId = p.lifeEquipment[subVal['id'], part].id
                        iconPath = uiUtils.getItemIconFile64(itemId)
                        cdura = p.lifeEquipment[subVal['id'], part].cdura
                        if hasattr(p.lifeEquipment[subVal['id'], part], 'quality'):
                            quality = p.lifeEquipment[subVal['id'], part].quality
                        else:
                            quality = ID.data.get(p.lifeEquipment[subVal['id'], part].id, {}).get('quality', 1)
                        color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                        itemInfo['equipData'].append({'isEquip': True,
                         'itemId': itemId,
                         'icon': {'iconPath': iconPath,
                                  'itemId': itemId,
                                  'srcType': 'roleInfoLifeSkill'},
                         'subType': subVal['id'],
                         'part': part,
                         'color': color,
                         'cdura': cdura,
                         'equipName': p.lifeEquipment[subVal['id'], part].name})
                    else:
                        itemInfo['equipData'].append({'isEquip': False,
                         'equipName': ''})

                produceEquipItems.append(itemInfo)

        return uiUtils.array2GfxAarry(produceEquipItems, True)

    def _getSpecailEquip(self):
        p = BigWorld.player()
        equipDict = {}
        itemInfo = {'equipData': [],
         'itemName': gameStrings.TEXT_ACTIONBARPROXY_1899,
         'itemLv': 'Lv.' + str(p.fishingLv)}
        for index, item in enumerate(p.fishingEquip[0:3]):
            if item:
                iconPath = uiUtils.getItemIconFile64(item.id)
                if hasattr(item, 'quality'):
                    quality = item.quality
                else:
                    quality = ID.data.get(item.id, {}).get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                itemInfo['equipData'].append({'itemId': item.id,
                 'icon': {'iconPath': iconPath,
                          'itemId': item.id,
                          'srcType': 'roleInfoLifeSkillFish',
                          'color': color},
                 'color': color,
                 'equipName': uiConst.FISH_EQUIP_DESC[index]})
            else:
                itemInfo['equipData'].append({'equipName': uiConst.FISH_EQUIP_DESC[index]})

        equipDict['fishEquip'] = itemInfo
        itemInfo = {'equipData': [],
         'itemName': gameStrings.TEXT_ACTIONBARPROXY_1901,
         'itemLv': 'Lv.' + str(p.exploreLv)}
        item = p.exploreEquip.get(gametypes.EXPLORE_EQUIP_COMPASS)
        if item:
            iconPath = uiUtils.getItemIconFile64(item.id)
            if hasattr(item, 'quality'):
                quality = item.quality
            else:
                quality = ID.data.get(item.id, {}).get('quality', 1)
            color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            itemInfo['equipData'].append({'itemId': item.id,
             'icon': {'iconPath': iconPath,
                      'itemId': item.id,
                      'srcType': 'roleInfoLifeSkillExplore',
                      'color': color},
             'color': color,
             'equipName': uiConst.EXPLORE_EQUIP_DESC[0]})
        else:
            itemInfo['equipData'].append({'equipName': uiConst.EXPLORE_EQUIP_DESC[0]})
        equipDict['exploreEquip'] = itemInfo
        return uiUtils.dict2GfxDict(equipDict, True)

    def onLevelUpClick(self, *arg):
        BigWorld.player().cell.socLvUp()

    def onResignClick(self, *arg):
        p = BigWorld.player()
        enterTime = p.socSchools.get(p.socialSchool, 0)
        if enterTime:
            joinReviewTime = SSCD.data.get('joinReviewDays', 3) * 24 * 3600
            leftTime = enterTime + joinReviewTime - int(p.getServerTime())
            if leftTime <= 0:
                msg = gameStrings.TEXT_ROLEINFOPROXY_2492
            else:
                msg = gameStrings.TEXT_ROLEINFOPROXY_2494
        else:
            msg = gameStrings.TEXT_ROLEINFOPROXY_2492
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, p.cell.quitFromSocSchool, yesBtnText=gameStrings.TEXT_IMPPLAYERTEAM_644, noBtnText=gameStrings.TEXT_AVATAR_2876_1)

    def onAbilityTreeClick(self, *arg):
        gameglobal.rds.ui.lifeSkillNew.show(1)

    def onSkillLevelUpClick(self, *arg):
        sid = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        enableSocialSkill = MCD.data.get(formula.getMapId(p.spaceNo), {}).get('enableSocialSkill', 1)
        if not enableSocialSkill:
            p.showGameMsg(GMDD.data.SOCIAL_SKILL_CAST_FAILED_IN_DUEL, ())
            return
        else:
            schoolSkillsData = SSSD.data.get(self.socialSkillDict[sid], {})
            skillInfo = schoolSkillsData.get(sid, {})
            sVal = p.skills.get(sid, None)
            if sVal:
                nextLevel = sVal.level
            else:
                nextLevel = 0
            cashReduce = skillInfo.get('cashReduce', ())
            socMoney = cashReduce[nextLevel]
            if uiUtils.checkBindCashEnough(socMoney, p.bindCash, p.cash, Functor(p.cell.socialSkillLevelUp, sid)):
                p.cell.socialSkillLevelUp(sid)
            return

    def onGotoSocClick(self, *arg):
        seekId = SSD.data.get(self.selectedJob, {}).get('npcTk', 0)
        if seekId:
            uiUtils.findPosById(str(seekId))

    def _calRadius(self):
        p = BigWorld.player()
        maxPropVal = 0
        for prop in LIFE_SKILL_PROP_MAP.itervalues():
            scoPropVal = getattr(p.socProp, prop)
            if scoPropVal > maxPropVal:
                maxPropVal = scoPropVal

        socialPropRadius = list(LSCD.data.get('socialPropRadius', (255,)))
        socialPropRadius.sort()
        for radius in socialPropRadius:
            if maxPropVal <= radius:
                return radius

        if len(socialPropRadius) > 0:
            return socialPropRadius[-1]
        else:
            return 255

    def onGetSocialInfo(self, *arg):
        ret = self.movie.CreateObject()
        p = BigWorld.player()
        socialLvData = SLD.data[p.socLv]
        jobIdx = p.socialSchool
        ret.SetMember('jobIdx', GfxValue(jobIdx))
        ret.SetMember('roleName', GfxValue(gbk2unicode(p.realRoleName)))
        ret.SetMember('socialLevel', GfxValue(p.socLv))
        jobInfo = SSD.data.get(jobIdx, {})
        ret.SetMember('socialSchool', GfxValue(gbk2unicode(jobInfo.get('job', gameStrings.TEXT_ROLEINFOPROXY_2565))))
        if jobIdx == 0:
            ret.SetMember('socialSchoolBigIcon', GfxValue(SOCIAL_SCHOOL_BIG_ICON + '0' + uiUtils.ICON_FILE_EXT))
        else:
            ret.SetMember('socialSchoolBigIcon', GfxValue(SOCIAL_SCHOOL_BIG_ICON + str(jobInfo.get('icon', 'notFound')) + uiUtils.ICON_FILE_EXT))
        enterTime = p.socSchools.get(jobIdx, 0)
        if enterTime:
            joinReviewTime = SSCD.data.get('joinReviewDays', 3) * 24 * 3600
            leftTime = enterTime + joinReviewTime - int(p.getServerTime())
            if leftTime <= 0:
                observation = ''
            elif leftTime < 3600:
                observation = gameStrings.TEXT_ROLEINFOPROXY_2578
            else:
                observation = gameStrings.TEXT_ROLEINFOPROXY_2580
                if leftTime > 86400:
                    observation += gameStrings.TEXT_FASHIONPROPTRANSFERPROXY_229 % (leftTime / 86400)
                    leftTime %= 86400
                observation += gameStrings.TEXT_GUILDWWTOURNAMENTRESULTPROXY_116 % (leftTime / 3600)
        else:
            observation = ''
        ret.SetMember('observation', GfxValue(gbk2unicode(observation)))
        if uiUtils.hasVipBasic():
            mLabour = 2 * p.mLabour / 10
            mMental = 2 * p.mMental / 10
        else:
            mLabour = p.mLabour / 10
            mMental = p.mMental / 10
        ret.SetMember('labour', GfxValue(p.labour / 10))
        ret.SetMember('mLabour', GfxValue(mLabour))
        labour = p.labour / 10
        labourValue = float(labour) * 100 / mLabour if mLabour != 0 else 100
        ret.SetMember('labourValue', GfxValue(labourValue))
        labourTips = LSPTD.data.get(uiConst.LABOUR_TIPS_INDEX, {}).get('tips', gameStrings.TEXT_LIFESKILLFACTORY_247)
        strLabourBackRate = LSCFD.data.get('strLabourBackRate', 0)
        value = (LSCFD.data.get('labourRegenVal', 1) + int(strLabourBackRate * int(BigWorld.player().socProp.str / 10))) / 10.0
        useTime = max(30, LSCFD.data.get('labourRegenInterval', 300) - BigWorld.player().getAbilityData(gametypes.ABILITY_LS_LABOUR_REGEN_INTERVAL))
        labourTips = labourTips % (useTime, value)
        ret.SetMember('labourTips', GfxValue(gbk2unicode(labourTips)))
        labourText = '%d/%d' % (labour, mLabour)
        ret.SetMember('labourText', GfxValue(labourText))
        mental = p.mental / 10
        mentalValue = float(mental) * 100 / mMental if mMental != 0 else 100
        ret.SetMember('mentalValue', GfxValue(mentalValue))
        mentalText = '%d/%d' % (mental, mMental)
        ret.SetMember('mentalText', GfxValue(mentalText))
        mentalTips = LSPTD.data.get(uiConst.MENTAL_TIPS_INDEX, {}).get('tips', gameStrings.TEXT_LIFESKILLFACTORY_247)
        strMentalBackRate = LSCFD.data.get('strMentalBackRate', 0)
        value = (LSCFD.data.get('mentalRegenVal', 1) + int(strMentalBackRate * int(BigWorld.player().socProp.know / 10))) / 10.0
        useTime = max(30, LSCFD.data.get('mentalRegenInterval', 300) - BigWorld.player().getAbilityData(gametypes.ABILITY_LS_LABOUR_REGEN_INTERVAL))
        mentalTips = mentalTips % (useTime, value)
        ret.SetMember('mentalTips', GfxValue(gbk2unicode(mentalTips)))
        ret.SetMember('curSocExp', GfxValue(p.socExp))
        ret.SetMember('maxSocExp', GfxValue(socialLvData.get('upExp', 0)))
        ret.SetMember('radius', GfxValue(self._calRadius()))
        for key in sorted(LIFE_SKILL_PROP_MAP.iterkeys()):
            val = LIFE_SKILL_PROP_MAP[key]
            propData = LSPTD.data[key]
            scoPropVal = getattr(p.socProp, val)
            ret.SetMember(val, self._getSocialPropItem(propData['name'], scoPropVal, propData['tips']))

        ret.SetMember('produceEquip', self._getEquipByLifeSkillType(gametypes.LIFE_SKILL_TYPE_COLLECTION))
        ret.SetMember('produceEquipDesc', GfxValue(gbk2unicode(gameStrings.TEXT_ROLEINFOPROXY_2642)))
        ret.SetMember('makeEquip', self._getEquipByLifeSkillType(gametypes.LIFE_SKILL_TYPE_MANUFACTURE))
        ret.SetMember('makeEquipDesc', GfxValue(gbk2unicode(gameStrings.TEXT_ROLEINFOPROXY_2644)))
        ret.SetMember('specailEquip', self._getSpecailEquip())
        ret.SetMember('specailEquipDesc', GfxValue(gbk2unicode(gameStrings.TEXT_ROLEINFOPROXY_2646)))
        return ret

    def onGetSocialJobInfo(self, *arg):
        p = BigWorld.player()
        ret = []
        for jobIdx, jobInfo in SSD.data.iteritems():
            isOpen = jobInfo.get('isOpen', 0)
            if isOpen == 0:
                continue
            jobName = jobInfo.get('job', '')
            if p.socialSchool == jobIdx:
                ret.append([jobIdx, jobName, False])
                continue
            unFit = False
            needLv = jobInfo.get('needLv', 0)
            if p.realLv < needLv:
                unFit = True
            needSex = jobInfo.get('needSex', 0)
            if needSex > 0:
                if p.physique.sex != needSex:
                    unFit = True
            socLv = jobInfo.get('socLv', 0)
            if p.socLv < socLv:
                unFit = True
            socProps = jobInfo.get('socProps', ((),))
            if unFit == False and socProps != ((),):
                for key, value in socProps:
                    scoPropVal = getattr(p.socProp, LIFE_SKILL_PROP_MAP[key])
                    if scoPropVal < value:
                        unFit = True
                        break

            socMoney = jobInfo.get('socMoney', 0)
            if p.cash + p.bindCash < socMoney:
                unFit = True
            socItems = jobInfo.get('socItems', ((),))
            if unFit == False and socItems != ((),):
                for itemId, needNum in socItems:
                    num = p.inv.countItemInPages(itemId)
                    if num < needNum:
                        unFit = True
                        break

            if unFit:
                jobName = "<font color = \'#F43804\'>" + jobName + '</font>'
            ret.append([jobIdx, jobName, True])

        return uiUtils.array2GfxAarry(ret, True)

    def onGetJobTip(self, *arg):
        jobIdx = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        ret = {}
        jobInfo = SSD.data.get(jobIdx, {})
        ret['jobName'] = jobInfo.get('job', '')
        ret['jobDescription'] = jobInfo.get('jobDescription', '')
        ret['jobCondition'] = ''
        ret['itemList'] = []
        if p.socialSchool == jobIdx:
            return uiUtils.dict2GfxDict(ret, True)
        jobCondition = gameStrings.TEXT_ROLEINFOPROXY_2718
        needLv = jobInfo.get('needLv', 0)
        if p.realLv >= needLv:
            jobCondition += gameStrings.TEXT_ROLEINFOPROXY_2722 % needLv
        else:
            jobCondition += gameStrings.TEXT_ROLEINFOPROXY_2724 % needLv
        needSex = jobInfo.get('needSex', 0)
        if needSex > 0:
            if p.physique.sex == needSex:
                jobCondition += gameStrings.TEXT_ROLEINFOPROXY_2729 % const.SEX_NAME.get(needSex, '')
            else:
                jobCondition += gameStrings.TEXT_ROLEINFOPROXY_2731 % const.SEX_NAME.get(needSex, '')
        socLv = jobInfo.get('socLv', 0)
        if p.socLv >= socLv:
            jobCondition += gameStrings.TEXT_ROLEINFOPROXY_2735 % socLv
        else:
            jobCondition += gameStrings.TEXT_ROLEINFOPROXY_2737 % socLv
        socProps = jobInfo.get('socProps', ((),))
        if socProps != ((),):
            for key, value in socProps:
                propData = LSPTD.data[key]
                scoPropVal = getattr(p.socProp, LIFE_SKILL_PROP_MAP[key])
                if scoPropVal >= value:
                    jobCondition += gameStrings.TEXT_ROLEINFOPROXY_2745 % (propData['name'], value)
                else:
                    jobCondition += gameStrings.TEXT_ROLEINFOPROXY_2747 % (propData['name'], value)

        socMoney = jobInfo.get('socMoney', 0)
        if p.cash + p.bindCash >= socMoney:
            jobCondition += gameStrings.TEXT_ROLEINFOPROXY_2751 % socMoney
        else:
            jobCondition += gameStrings.TEXT_ROLEINFOPROXY_2753 % socMoney
        socItems = jobInfo.get('socItems', ((),))
        if socItems != ((),):
            itemFit = True
            itemCondition = ''
            for itemId, needNum in socItems:
                if itemCondition != '':
                    itemCondition += '  '
                name = ID.data.get(itemId, {}).get('name', '')
                quality = ID.data.get(itemId, {}).get('quality', 1)
                qualityColor = FCD.data.get(('item', quality), {}).get('color', '#CCCCCC')
                itemCondition += "<font color=\'%s\'>%s</font>" % (qualityColor, name)
                num = p.inv.countItemInPages(itemId)
                if num >= needNum:
                    itemCondition += '(%d/%d)' % (num, needNum)
                else:
                    itemCondition += "<font color = \'#F43804\'>(%d/%d)</font>" % (num, needNum)
                    itemFit = False

            if itemFit:
                jobCondition += gameStrings.TEXT_ROLEINFOPROXY_2775 + itemCondition
            else:
                jobCondition += gameStrings.TEXT_ROLEINFOPROXY_2777 + itemCondition
        ret['jobCondition'] = jobCondition
        return uiUtils.dict2GfxDict(ret, True)

    def onGetSocialSkillInfo(self, *arg):
        jobIdx = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        ret = {}
        ret['jobName'] = SSD.data.get(jobIdx, {}).get('job', '')
        ret['jobError'] = jobIdx != p.socialSchool
        ret['skill'] = {}
        ret['line'] = []
        self.selectedJob = jobIdx
        self.socialSkillDict = {}
        schoolSkillsData = SSSD.data.get(jobIdx, {})
        self.preSkillPoint = socialSkillCommon.getPreSkillPoint(p, schoolSkillsData)
        ret['jobPoint'] = gameStrings.TEXT_ROLEINFOPROXY_2796 % self.preSkillPoint
        for sid, skillInfo in schoolSkillsData.iteritems():
            self.socialSkillDict[sid] = jobIdx
            ret['skill'][sid] = {}
            skillItem = ret['skill'][sid]
            dragable = skillInfo.get('skillType', 1) == gametypes.GUILD_PSKILL_TYPE_ACTIVE
            if dragable and jobIdx != p.socialSchool:
                dragable = False
            skillItem['dragable'] = dragable
            posX, posY = skillInfo.get('skillPos', (0, 0))
            skillItem['x'] = 50 + (posX - 1) * 120
            skillItem['y'] = (posY - 1) * 80
            sVal = p.skills.get(sid, None)
            nowLevel = sVal.level if sVal else 0
            socialLvNeed = skillInfo.get('socialLvNeed', ())
            maxLevel = len(socialLvNeed)
            skillItem['nowLevel'] = nowLevel
            skillItem['maxLevel'] = maxLevel
            skillItem['iconPath'] = 'skill/icon/%d.dds' % SKCD.data.get((sid, 1), {}).get('icon', 0)
            canLevelUp = border = jobIdx == p.socialSchool
            if nowLevel >= maxLevel:
                canLevelUp = False
            nextLevel = nowLevel
            if nextLevel < maxLevel:
                socLv = socialLvNeed[nextLevel]
                if p.socLv < socLv:
                    canLevelUp = border = False
            if nextLevel == 0:
                preSkillPointNeed = skillInfo.get('preSkillPointNeed', 0)
                if preSkillPointNeed:
                    if self.preSkillPoint < preSkillPointNeed:
                        canLevelUp = border = False
                preSkillNeed = skillInfo.get('preSkillNeed', ())
                preSkillLvNeed = skillInfo.get('preSkillLvNeed', ())
                offset = skillInfo.get('offset', (((),),))
                skillLvNeed = zip(preSkillNeed, preSkillLvNeed, offset)
                for sid, slv, soffset in skillLvNeed:
                    sVal = p.skills.get(sid, None)
                    sline = {}
                    sline['startPos'] = (skillItem['x'] + 18, skillItem['y'] + 18)
                    if not sVal or sVal.level < slv:
                        canLevelUp = border = False
                        sline['col'] = 'gray'
                    else:
                        sline['col'] = 'green'
                    sline['offset'] = soffset
                    ret['line'].append(sline)

            else:
                offset = skillInfo.get('offset', (((),),))
                if offset != (((),),):
                    for soffset in offset:
                        sline = {}
                        sline['startPos'] = (skillItem['x'] + 18, skillItem['y'] + 18)
                        if nowLevel == maxLevel:
                            sline['col'] = 'gold'
                        else:
                            sline['col'] = 'green'
                        sline['offset'] = soffset
                        ret['line'].append(sline)

            if nextLevel < maxLevel:
                socialExpReduce = skillInfo.get('socialExpReduce', ())
                socExp = socialExpReduce[nextLevel]
                if p.socExp < socExp:
                    canLevelUp = False
                cashReduce = skillInfo.get('cashReduce', ())
                socMoney = cashReduce[nextLevel]
                if p.cash + p.bindCash < socMoney:
                    canLevelUp = False
            skillItem['canLevelUp'] = canLevelUp
            skillItem['border'] = border

        return uiUtils.dict2GfxDict(ret, True)

    def getLevelUpCondition(self, sid):
        if sid not in self.socialSkillDict:
            return ''
        else:
            p = BigWorld.player()
            schoolSkillsData = SSSD.data.get(self.socialSkillDict[sid], {})
            skillInfo = schoolSkillsData.get(sid, {})
            ret = ''
            sVal = p.skills.get(sid, None)
            socialLvNeed = skillInfo.get('socialLvNeed', ())
            if sVal:
                if sVal.level >= len(socialLvNeed):
                    return ret
                nextLevel = sVal.level
            else:
                if not socialLvNeed:
                    return ret
                nextLevel = 0
            socLv = socialLvNeed[nextLevel]
            if p.socLv >= socLv:
                ret += gameStrings.TEXT_ROLEINFOPROXY_2906 % socLv
            else:
                ret += gameStrings.TEXT_ROLEINFOPROXY_2908 % socLv
            if nextLevel == 0:
                preSkillPointNeed = skillInfo.get('preSkillPointNeed', 0)
                if preSkillPointNeed:
                    if self.preSkillPoint >= preSkillPointNeed:
                        ret += gameStrings.TEXT_ROLEINFOPROXY_2914 % preSkillPointNeed
                    else:
                        ret += gameStrings.TEXT_ROLEINFOPROXY_2916 % preSkillPointNeed
                preSkillNeed = skillInfo.get('preSkillNeed', ())
                preSkillLvNeed = skillInfo.get('preSkillLvNeed', ())
                skillLvNeed = zip(preSkillNeed, preSkillLvNeed)
                sNum = 0
                preSkillText = ''
                fitFlag = True
                for sid, slv in skillLvNeed:
                    skillName = SGTD.data.get(sid, {}).get('name', '')
                    sVal = p.skills.get(sid, None)
                    if not sVal or sVal.level < slv:
                        fitFlag = False
                        if sNum:
                            preSkillText += '               '
                        preSkillText += gameStrings.TEXT_ROLEINFOPROXY_2932 % (skillName, slv)
                    else:
                        if sNum:
                            preSkillText += '               '
                        preSkillText += gameStrings.TEXT_ROLEINFOPROXY_2936 % (skillName, slv)
                    sNum += 1

                if sNum:
                    if fitFlag:
                        ret += gameStrings.TEXT_ROLEINFOPROXY_2941
                    else:
                        ret += gameStrings.TEXT_ROLEINFOPROXY_2943
                    ret += preSkillText
            socialExpReduce = skillInfo.get('socialExpReduce', ())
            socExp = socialExpReduce[nextLevel]
            if p.socExp >= socExp:
                ret += gameStrings.TEXT_ROLEINFOPROXY_2949 % socExp
            else:
                ret += gameStrings.TEXT_ROLEINFOPROXY_2951 % socExp
            cashReduce = skillInfo.get('cashReduce', ())
            socMoney = cashReduce[nextLevel]
            if p.cash + p.bindCash >= socMoney:
                ret += gameStrings.TEXT_ROLEINFOPROXY_2956 % socMoney
            else:
                ret += gameStrings.TEXT_ROLEINFOPROXY_2958 % socMoney
            return ret

    def removeSocialSkill(self, oldSocSchool):
        skillList = SSSD.data.get(oldSocSchool, {}).keys()
        gameglobal.rds.ui.actionbar.removeItemBySkillIdList(skillList, False)

    def updateSocialExp(self):
        if self.mediator:
            self.mediator.Invoke('updateSocialExp')

    def updateSocialLv(self):
        if self.mediator:
            self.mediator.Invoke('updateSocialLv')

    def onGetSocialExp(self, *arg):
        p = BigWorld.player()
        socialLvData = SLD.data[p.socLv]
        info = {}
        info['curSocExp'] = p.socExp
        info['maxSocExp'] = socialLvData.get('upExp', 0)
        return uiUtils.dict2GfxDict(info)

    def onGetSocialLv(self, *arg):
        p = BigWorld.player()
        return GfxValue(p.socLv)

    def _setSocialPropTestData(self):
        p = BigWorld.player()
        p.socProp.str = 230
        p.socProp.dex = 110
        p.socProp.know = 200
        p.socProp.sense = 35
        p.socProp.study = 160
        p.socProp.charm = 148
        p.socProp.lucky = 20
        p.lifeEquipment[1, 1] = Item(100100)
        p.socLv = 33
        p.labour = 10
        p.mLabour = 100

    def onUnEquipSocialItem(self, *arg):
        subType = int(arg[3][0].GetNumber())
        part = int(arg[3][1].GetNumber())
        p = BigWorld.player()
        page, pos = p.inv.searchEmptyInPages()
        if pos != const.CONT_NO_POS:
            p.cell.unequipLifeEqu(subType, part, page, pos)
        else:
            p.showGameMsg(GMDD.data.SHOP_BAG_FULL, ())

    def onUnEquipFishItem(self, *arg):
        part = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        page, pos = p.inv.searchEmptyInPages()
        if pos != const.CONT_NO_POS:
            if not p.stateMachine.checkStatus(const.CT_TAKE_OFF_FISHING_EQUIP):
                return
            p.cell.exchangeInvFishingEqu(page, pos, part)
        else:
            p.showGameMsg(GMDD.data.SHOP_BAG_FULL, ())

    def onUnEquipExploreItem(self, *arg):
        p = BigWorld.player()
        page, pos = p.inv.searchEmptyInPages()
        if pos != const.CONT_NO_POS:
            p.cell.exchangeInvExploreEqu(page, pos, gametypes.EXPLORE_EQUIP_COMPASS)
        else:
            p.showGameMsg(GMDD.data.SHOP_BAG_FULL, ())

    def updateRuneSlotState(self):
        p = BigWorld.player()
        if self.mediator and p.runeBoard.runeEquip:
            for runeDataVal in p.runeBoard.runeEquip.runeData:
                if runeDataVal.item == const.CONT_EMPTY_VAL:
                    return
                key = gameglobal.rds.ui.runeView._getKey(runeDataVal.runeSlotsType, runeDataVal.part)
                if not gameglobal.rds.ui.runeView.binding.has_key(key):
                    return
                if runeDataVal.runeSlotsType == gameglobal.rds.ui.runeReforging.runePage and runeDataVal.part == gameglobal.rds.ui.runeReforging.runePart or runeDataVal.runeSlotsType == gameglobal.rds.ui.runeForging.runePage and runeDataVal.part == gameglobal.rds.ui.runeForging.runePart:
                    gameglobal.rds.ui.runeView.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_DISABLE))
                else:
                    gameglobal.rds.ui.runeView.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_NORMAL))

    def initItemArr(self, it, pos):
        arr = self.movie.CreateArray()
        icon = uiUtils.getItemIconFile64(it.id)
        idValue = GfxValue(it.id)
        name = GfxValue('item')
        iconPath = GfxValue(icon)
        obj = self.movie.CreateObject()
        obj.SetMember('id', idValue)
        obj.SetMember('name', name)
        obj.SetMember('iconPath', iconPath)
        arr.SetElement(0, GfxValue(pos))
        arr.SetElement(1, obj)
        if hasattr(it, 'quality'):
            quality = it.quality
        else:
            quality = ID.data.get(it.id, {}).get('quality', 1)
        color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
        arr.SetElement(2, GfxValue(color))
        runeSlotsType = pos / 10
        part = pos % 10
        if runeSlotsType == gameglobal.rds.ui.runeReforging.runePage and part == gameglobal.rds.ui.runeReforging.runePart or runeSlotsType == gameglobal.rds.ui.runeForging.runePage and part == gameglobal.rds.ui.runeForging.runePart:
            arr.SetElement(3, GfxValue(uiConst.ITEM_DISABLE))
        elif pos == BENYUAN_RUNE_POS:
            p = BigWorld.player()
            if p.runeBoard.runeEquip:
                juexingValid = bool(REQD.data.get(p.runeBoard.runeEquip.id, {}).get('juexingValid', 1))
                tianlunAwake = p.runeBoard.awakeDict[const.RUNE_TYPE_TIANLUN] and juexingValid
                dilunAwake = p.runeBoard.awakeDict[const.RUNE_TYPE_DILUN] and juexingValid
            else:
                tianlunAwake = False
                dilunAwake = False
            if tianlunAwake == False or dilunAwake == False:
                arr.SetElement(3, GfxValue(uiConst.EQUIP_NOT_USE))
            else:
                arr.SetElement(3, GfxValue(uiConst.ITEM_NORMAL))
        else:
            arr.SetElement(3, GfxValue(uiConst.ITEM_NORMAL))
        return arr

    def onClickExpUp(self, *arg):
        if BigWorld.player().runeBoard.runeEquip:
            pass

    def onClickChongXi(self, *arg):
        if self.isRuneChongXiState:
            self.clearRuneChongXiState()
        else:
            self.setRuneChongXiState()

    def playLunEffect(self, type):
        if self.mediator:
            self.mediator.Invoke('playLunEffect', GfxValue(type))

    def updateRuneChongXiState(self):
        if self.mediator:
            if self.isRuneChongXiState:
                self.mediator.Invoke('updateRuneChongXiState', GfxValue(True))
            else:
                self.mediator.Invoke('updateRuneChongXiState', GfxValue(False))

    def onsSlotChongXi(self, *arg):
        if self.isRuneChongXiState:
            self.clearRuneChongXiState()
            key = arg[3][0].GetString()
            bar, slot = key.split('.')
            runeSlotsType = int(bar[14:])
            part = int(slot[4:])
            p = BigWorld.player()
            if p.runeBoard.runeEquip:
                for key, value in p.runeBoard.runeEquip.runeEquipXiLianData.iteritems():
                    _runeSlotsType, _part = key
                    if runeSlotsType == _runeSlotsType and part == _part:
                        gameglobal.rds.ui.runeChongXi.show(runeSlotsType, part)

    def onRuneView(self, *arg):
        if not gameglobal.rds.ui.runeView.mediator:
            gameglobal.rds.ui.runeView.show()

    def onClickRuneItem(self, *arg):
        p = BigWorld.player()
        key = arg[3][0].GetString()
        page, pos = gameglobal.rds.ui.runeView.getSlotID(key)
        if page == uiConst.RUNE_TYPE_EQUIP:
            it = p.runeBoard.runeEquip
        else:
            it = None
            for runeDataVal in p.runeBoard.runeEquip.runeData:
                if runeDataVal.runeSlotsType == page and runeDataVal.part == pos:
                    it = runeDataVal.item

        if not it:
            return
        else:
            if page != uiConst.RUNE_TYPE_EQUIP:
                if gameglobal.rds.ui.runeForging.mediator:
                    if it.isRune() and it.canRuneQiFu():
                        gameglobal.rds.ui.runeForging.runePage = page
                        gameglobal.rds.ui.runeForging.runePart = pos
                        gameglobal.rds.ui.runeForging.source = uiConst.RUNE_SOURCE_ROLE
                        gameglobal.rds.ui.runeForging.invPage = const.CONT_NO_PAGE
                        gameglobal.rds.ui.runeForging.invPos = const.CONT_NO_POS
                        gameglobal.rds.ui.runeForging.addItem(it, uiConst.RUNE_FORGING_EQUIP, 0)
                    return
                if gameglobal.rds.ui.runeReforging.mediator:
                    if it.isRune() and it.canRuneReforging():
                        gameglobal.rds.ui.runeReforging.runePart = pos
                        gameglobal.rds.ui.runeReforging.runePage = page
                        gameglobal.rds.ui.runeReforging.source = uiConst.RUNE_SOURCE_ROLE
                        gameglobal.rds.ui.runeReforging.invPage = const.CONT_NO_PAGE
                        gameglobal.rds.ui.runeReforging.invPos = const.CONT_NO_POS
                        gameglobal.rds.ui.runeReforging.addItem(it, uiConst.RUNE_REFORGING_EQUIP, 0)
                    return
            emptyPg, emptyPos = p.inv.searchBestInPages(it.id, it.cwrap, it)
            if emptyPg != const.CONT_NO_PAGE:
                if page == uiConst.RUNE_TYPE_EQUIP:
                    cellCmd.unequipRuneEquipment(emptyPg, emptyPos)
                else:
                    p.cell.removeRune(page, pos, emptyPg, emptyPos)
            else:
                msgId = GMDD.data.RUNE_EQUIP_BAG_FULL if page == uiConst.RUNE_TYPE_EQUIP else GMDD.data.RUNE_BAG_FULL
                p.showGameMsg(msgId, ())
            return

    def equipRuneEquip(self):
        if self.mediator:
            self.mediator.Invoke('equipRuneEquip')

    def unEquipRuneEquip(self):
        if self.mediator:
            self.mediator.Invoke('unEquipRuneEquip')

    def updateRuneAwake(self):
        p = BigWorld.player()
        if self.mediator:
            if p.runeBoard.runeEquip:
                juexingValid = bool(REQD.data.get(p.runeBoard.runeEquip.id, {}).get('juexingValid', 1))
                runeEquipUuid = p.runeBoard.runeEquip.uuid
                tianlunAwake = p.runeBoard.awakeDict[const.RUNE_TYPE_TIANLUN] and juexingValid
                dilunAwake = p.runeBoard.awakeDict[const.RUNE_TYPE_DILUN] and juexingValid
            else:
                runeEquipUuid = 0
                tianlunAwake = False
                dilunAwake = False
            self.mediator.Invoke('updateRuneAwake', (GfxValue(tianlunAwake), GfxValue(dilunAwake), GfxValue(str(runeEquipUuid))))

    def onResetPoint(self, *arg):
        gameglobal.rds.ui.propScheme.showReset()

    def onGetRadarData(self, *arg):
        p = BigWorld.player()
        ret = commcalc.createSelfRadarChartData(p, True)
        return uiUtils.array2GfxAarry(ret)

    def calAttrPreview(self):
        potAdded = [self.powAdd,
         self.intAdd,
         self.phyAdd,
         self.sprAdd,
         self.agiAdd]
        p = BigWorld.player()
        equips = [ equip for equip in p.equipment if equip ]
        pskills = []
        for pskVal in p.pskills.values():
            for subVal in pskVal.values():
                pskills.append(subVal)

        titles = []
        props = commcalc.calcSelfPropVal(p, equips, pskills, titles, p.guildGrowth)
        for i, propId in enumerate(PDD.data.PRIMARY_PROPERTIES):
            props[propId] += potAdded[i]

        propsFilter = []
        for idx in xrange(1, 6):
            data = RCDD.data.get(idx, {})
            propsFilter += data.get('formual1Params%d' % (p.realSchool - 2), [])

        propsFilter = [ PRD.data.get(id, {}).get('property', 0) for id in propsFilter ]
        preview = commcalc.calcAllPropVal(p, props, equips, pskills, titles, propsFilter, p.guildGrowth)
        ret = commcalc.createRadarChartData(p, preview, True)
        if self.mediator != None:
            self.mediator.Invoke('drawPreview', uiUtils.array2GfxAarry(ret))

    def clearPreivew(self):
        if self.mediator != None:
            self.mediator.Invoke('clearPreviewData')

    def takePhoto3D(self, modelId = 3001, tintMs = None, photoAction = None):
        if self.isShow:
            if not self.headGen:
                self.headGen = capturePhoto.RolePhotoGen.getInstance('gui/taskmask.tga', 442)
            self.headGen.startCapture(modelId, tintMs, ('1103', '1101'))

    def takeWeaponPhoto(self, weapon):
        if self.isShow and self.headGen:
            self.headGen.updateWeapon(BigWorld.player(), weapon)

    def takeWearPhoto(self, wear):
        if self.isShow:
            if self.headGen:
                self.headGen.updateWear(BigWorld.player(), wear)

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.RolePhotoGen.getInstance('gui/taskmask.tga', 442)
        self.headGen.initFlashMesh()

    def onGetRadarTip(self, *arg):
        dim = int(arg[3][0].GetNumber())
        school = BigWorld.player().realSchool
        tips = RCDD.data.get(dim, {}).get('tips%d' % (school - 2), gameStrings.TEXT_BATTLEFIELDPROXY_1605)
        return GfxValue(gbk2unicode(tips))

    def updateSlotState(self):
        p = BigWorld.player()
        if not p:
            return
        if self.isShow:
            if self.tabIdx == uiConst.ROLEINFO_TAB_FASHION:
                fashions = self.getFashionEquipment()
                for pos, item in enumerate(fashions):
                    if not item:
                        continue
                    state = self.calcSlotState(item, True)
                    self.setSlotState(pos, state)

            elif self.tabIdx == uiConst.ROLEINFO_TAB_ROLE:
                for pos in gametypes.EQU_PART_MAIN:
                    item = p.equipment.get(pos)
                    if not item:
                        continue
                    state = self.calcSlotState(item, False)
                    self.setSlotState(pos, state)

                for pos in gametypes.EQU_PART_SUB:
                    item = commcalc.getAlternativeEquip(p, pos)
                    if not item:
                        continue
                    state = self.calcSlotState(item, False)
                    self.setSlotState(pos + const.SUB_EQUIP_PART_OFFSET, state)

    def calcSlotState(self, item, isFashion):
        p = BigWorld.player()
        isDye = gameglobal.rds.ui.inventory.isDyeState
        isSign = gameglobal.rds.ui.inventory.isSignEquipState
        isRenewal = ui.get_cursor_state() == ui.RENEWAL_STATE
        isRenewal2 = ui.get_cursor_state() == ui.RENEWAL_STATE2
        if isDye and not gameglobal.rds.ui.inventory.isShowInDyeState(item):
            state = uiConst.ITEM_GRAY
        elif not item.isCanSign() and isSign:
            state = uiConst.ITEM_GRAY
        elif isRenewal and (item.getRenewalType() != gameglobal.rds.ui.inventory.getRenewalType() or not item.canRenewalIndependent()):
            state = uiConst.ITEM_GRAY
        elif isRenewal2 and not item.isMallFashionRenewable() and isFashion:
            state = uiConst.ITEM_GRAY
        elif item.isLatchOfTime():
            state = uiConst.ITEM_LATCH_TIME
        elif hasattr(item, 'shihun') and item.shihun == True:
            state = uiConst.EQUIP_SHIHUN_REPAIR
        elif hasattr(item, 'latchOfCipher'):
            state = uiConst.ITEM_LATCH_CIPHER
        elif not item.canUseNow(p.physique.sex, p.realSchool, p.physique.bodyType, p.realLv, p):
            state = uiConst.EQUIP_NOT_USE
        else:
            state = uiConst.ITEM_NORMAL
        return state

    def onOpenScheme(self, *arg):
        gameglobal.rds.ui.propScheme.show()

    def onTraceRoad(self, *arg):
        p = BigWorld.player()
        seekId = SCD.data.get('WUXING_SEEKID', '')
        mapName = MCD.data.get(p.mapID, {}).get('name', '')
        msg = SCD.data.get('WUXING_SEEK_DESC', gameStrings.TEXT_ROLEINFOPROXY_3334) % mapName
        uiUtils.findPosWithAlert(seekId, msg)

    def onGetVpTransformInfo(self, *arg):
        p = BigWorld.player()
        desc1 = VTD.data.get(uiConst.VP_TRANSFORM_1, {}).get('desc', gameStrings.TEXT_ROLEINFOPROXY_3339) % (p.lv, VLD.data.get(p.lv, {}).get('transformLimit', 0))
        desc2 = VTD.data.get(uiConst.VP_TRANSFORM_2, {}).get('desc', gameStrings.TEXT_ROLEINFOPROXY_3340)
        desc3 = VTD.data.get(uiConst.VP_TRANSFORM_3, {}).get('desc', gameStrings.TEXT_ROLEINFOPROXY_3341)
        info = (p.getAvailableVp(p.savedVp),
         desc1,
         desc2,
         desc3)
        return uiUtils.array2GfxAarry(info, True)

    def onSendVpValue(self, *arg):
        self.vpTransform = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if self.vpTransform:
            if not self.vpTransformTipMediator:
                if p.statesServerAndOwn.has_key(SCD.data.get('vpStateId', 39078)):
                    gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_ROLEINFOPROXY_3351, None)
                else:
                    gameglobal.rds.ui.loadWidget(uiConst.WIDGET_VP_TRANSFORM_TIP)
        else:
            p.showGameMsg(GMDD.data.TRANSFORM_VP_FAILD, ())
        self.onCloseVpTransform()

    def onGetVpTransformValue(self, *arg):
        p = BigWorld.player()
        vpValue = self.vpTransform
        stateId = SCD.data.get('vpStateId', 39078)
        stateInfo = StateInfo(stateId, 1)
        sttime = stateInfo.getStateData('interval', 5)
        transformRatio = VLD.data.get(p.lv, {}).get('transformRatio', 0)
        qData = SCD.data.get('quickTransfromVpData', ())
        if not qData:
            return
        itemId, fId = qData
        fData = FCCD.data[fId]
        func = fData['formula']
        res = func({'vp': float(self.vpTransform)})
        itemNum = int(math.ceil(res))
        leftNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
        itemName = uiUtils.getItemColorName(itemId)
        desc = gameStrings.TEXT_ROLEINFOPROXY_3378 % (vpValue * sttime,
         sttime,
         transformRatio,
         itemNum,
         itemName,
         itemName,
         leftNum)
        return GfxValue(gbk2unicode(desc))

    def onConfirmVpTransformDirect(self, *arg):
        qData = SCD.data.get('quickTransfromVpData', ())
        p = BigWorld.player()
        if not qData:
            return
        else:
            itemId, fId = qData
            fData = FCCD.data[fId]
            func = fData['formula']
            res = func({'vp': float(self.vpTransform)})
            itemNum = math.ceil(res)
            useNum = itemNum
            leftNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
            p = BigWorld.player()
            itemName = uiUtils.getItemColorName(itemId)
            if useNum > leftNum:
                msg = gameStrings.TEXT_ROLEINFOPROXY_3397 % itemName
                gameglobal.rds.ui.messageBox.showMsgBox(msg, None)
            else:
                p.cell.calcVpTransformToExp(self.vpTransform, True)
                self.onCloseVpTransformTip()
            return

    def onConfirmVpTransform(self, *arg):
        p = BigWorld.player()
        p.cell.calcVpTransformToExp(self.vpTransform, False)
        self.onCloseVpTransformTip()

    def onCloseVpTransformTip(self, *arg):
        self.vpTransformTipMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_VP_TRANSFORM_TIP)

    def onGetVpTransformDesc(self, *arg):
        p = BigWorld.player()
        vp = p.getAvailableVp(p.savedVp)
        return GfxValue(gbk2unicode(SCD.data.get('vpTip', gameStrings.TEXT_ROLEINFOPROXY_3421) % vp))

    def onGetTraceRoadBtnDesc(self, *arg):
        msg = GMD.data.get(GMDD.data.TRACE_ROAD_WUXING_TIPS, {}).get('text', gameStrings.TEXT_ROLEINFOPROXY_3424)
        return GfxValue(gbk2unicode(msg))

    def onRotateFigure(self, *arg):
        index = arg[3][0].GetNumber()
        deltaYaw = -0.104 * index
        if self.headGen:
            self.headGen.rotateYaw(deltaYaw)

    def onGetInitEquipData(self, *arg):
        p = BigWorld.player()
        ret = []
        for pos in gametypes.EQU_PART_MAIN:
            item = p.equipment.get(pos)
            if not item:
                continue
            iconPath = uiUtils.getItemIconFile64(item.id)
            itemInfo = {'partPos': pos,
             'iconPath': iconPath,
             'overIconPath': iconPath,
             'color': uiUtils.getItemColorByItem(item),
             'state': self.calcSlotState(item, False),
             'cornerMark': itemToolTipUtils.getCornerMark(item),
             'specialPropLen': item.getSpecialPropLevel()}
            ret.append(itemInfo)

        for pos in gametypes.EQU_PART_SUB:
            item = commcalc.getAlternativeEquip(p, pos)
            if not item:
                continue
            iconPath = uiUtils.getItemIconFile64(item.id)
            itemInfo = {'partPos': pos + const.SUB_EQUIP_PART_OFFSET,
             'iconPath': iconPath,
             'overIconPath': iconPath,
             'color': uiUtils.getItemColorByItem(item),
             'state': self.calcSlotState(item, False),
             'cornerMark': itemToolTipUtils.getCornerMark(item),
             'specialPropLen': item.getSpecialPropLevel()}
            ret.append(itemInfo)

        return uiUtils.array2GfxAarry(ret, True)

    def onLoadComplete(self, *arg):
        self.initHeadGen()
        self.takePhoto3D(0)

    def novicePushCheck(self):
        push = gameglobal.rds.loginManager.serverMode() != gametypes.SERVER_MODE_NOVICE
        push = push or BigWorld.player().lv < gameglobal.rds.configData.get('noviceServerMaxPlayerLv')
        return push

    def getLvUpBtnInfo(self):
        p = BigWorld.player()
        aldData = ALD.data.get(p.lv, {})
        upExp = aldData.get('upExp', sys.maxint)
        upMode = aldData.get('upMode', gametypes.LEVEL_UP_MODE_FORBID)
        enhPoint = aldData.get('skillEnhancePointLimit', 0)
        enhTips = ''
        showLvUpBtn = upMode == gametypes.LEVEL_UP_MODE_MANUAL
        canManualLvUp = showLvUpBtn and p.exp >= upExp
        lvLabel = gameStrings.ROLE_INFO_LV_UP_BTN_LABEL_LV_BREAK if canManualLvUp and p.canLvBreak() else gameStrings.ROLE_INFO_LV_UP_BTN_LABEL_MANUAL
        if canManualLvUp and MCD.data.get(formula.getMapId(p.spaceNo), {}).get('canNotLevelUp', 0):
            enhTips = gameStrings.ROLE_INFO_LV_UP_SPACE_INVALID
            canManualLvUp = False
        if canManualLvUp and utils.getTotalSkillEnhancePoint(p) < enhPoint:
            enhTips = gameStrings.ROLE_INFO_LV_UP_SKILL_ENHANCE_INVALID % enhPoint
            canManualLvUp = False
        return (showLvUpBtn,
         canManualLvUp,
         enhTips,
         lvLabel)

    def refreshLvUpBtn(self, pushLvUp = False):
        showLvUpBtn, canManualLvUp, enhTips, lvLabel = self.getLvUpBtnInfo()
        msgId = uiConst.MESSAGE_TYPE_MANUAL_LV_UP
        pushMsg = gameglobal.rds.ui.pushMessage
        if not canManualLvUp:
            pushMsg.removeData(msgId, {'data': 'data'})
        elif pushLvUp and self.novicePushCheck() and not pushMsg.getDataList(msgId):
            pushMsg.addPushMsg(msgId, {'data': 'data'})
        if self.mediator:
            self.mediator.Invoke('refreshLvUpBtn', (GfxValue(showLvUpBtn),
             GfxValue(canManualLvUp),
             GfxValue(showLvUpBtn and canManualLvUp),
             GfxValue(gbk2unicode(enhTips)),
             GfxValue(gbk2unicode(lvLabel))))

    def addManualLvUpPush(self, lv, pushLvUp):
        _, canManualLvUp, _, _ = self.getLvUpBtnInfo()
        msgId = uiConst.MESSAGE_TYPE_MANUAL_LV_UP
        pushMsg = gameglobal.rds.ui.pushMessage
        if canManualLvUp and lv != self.oldLv:
            self.oldLv = lv
            if pushLvUp and self.novicePushCheck() and not pushMsg.getDataList(msgId):
                pushMsg.addPushMsg(msgId, {'data': 'data'})
        elif not canManualLvUp:
            self.oldLv = 0
            pushMsg.removeData(msgId, {'data': 'data'})

    def clickManualLvUpPush(self):
        gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_MANUAL_LV_UP, {'data': 'data'})
        self.show()

    def onShowEarType(self, *arg):
        pass

    def onShowBack(self, *arg):
        show = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if bool(show) != bool(p.showBackWaist):
            BigWorld.player().cell.setSignal(gametypes.SIGNAL_SHOW_BACK, show)

    def onIsInTrainingFuben(self, *arg):
        p = BigWorld.player()
        return GfxValue(p._isSchoolSwitch())

    def onPlaySound(self, *arg):
        soundNo = int(arg[3][0].GetNumber())
        gameglobal.rds.sound.playSound(soundNo)

    def onSaveSetting(self, *arg):
        ret = int(arg[3][0].GetNumber())
        savingKey = keys.SET_UI_INFO + '/' + 'roleInfo' + '/open/raid'
        if AppSettings.get(savingKey, 1) != ret:
            AppSettings[savingKey] = ret
            AppSettings.save()

    def onGoToFameShop(self, *args):
        fameId = args[3][0].GetNumber()
        seekId = 0
        shortest = -1
        for shopSeekId in FD.data.get(fameId, {}).get('shopSeekId', ()):
            seekData = SEEKD.data.get(shopSeekId, {})
            dis = distance2D(BigWorld.player().position, (seekData.get('xpos', 0), seekData.get('ypos', 0), seekData.get('zpos', 0)))
            if shortest == -1 or dis < shortest:
                shortest = dis
                seekId = shopSeekId

        if seekId:
            uiUtils.findPosById(str(seekId))

    def onOpenGrowth(self, *args):
        gameglobal.rds.ui.guildGrowth.show(0, isNPCFlag=True)

    def getZhanXunAttrByRank(self, rank):
        ret = gameStrings.TEXT_BATTLEFIELDPROXY_1605
        for key, val in ZRD.data.iteritems():
            if key[0] <= rank and key[1] >= rank:
                ret = val.get('desc', '')
                break

        return ret

    def getZhanXunRewardByRank(self, rank):
        reward = 0
        for key, val in ZRD.data.iteritems():
            if key[0] <= rank and key[1] >= rank:
                reward = val.get('rewardJunJie', 0)
                break

        return reward

    def setJunZiWeekVal(self, weekVal):
        self.junziWeekVal = weekVal

    @ui.callAfterTime()
    def refreshJunjiePanel(self):
        if self.mediator:
            self.mediator.Invoke('refreshJunjiePanel')

    @ui.callAfterTime()
    def refreshQumoPanel(self):
        if self.mediator:
            self.mediator.Invoke('refreshQumoPanel')

    def getCurMaxJunZi(self):
        p = BigWorld.player()
        if not hasattr(p, 'fameWeek'):
            return 0
        if not p.fameWeek.has_key(const.JUN_ZI_FAME_ID):
            return 0
        return p.fameWeek[const.JUN_ZI_FAME_ID][1]

    def onGetJunjieInfo(self, *arg):
        p = BigWorld.player()
        info = {}
        lv = p.junJieLv
        nowLevelData = JCD.data.get(lv, {})
        bigIcon = {}
        bigIcon['name'] = nowLevelData.get('name', '')
        bigIcon['icon'] = 'junjie/%d.dds' % nowLevelData.get('icon', 0)
        info['bigIcon'] = bigIcon
        nowRight = {}
        nowRight['name'] = nowLevelData.get('name', '')
        desc = nowLevelData.get('desc', '')
        desc += gameStrings.TEXT_ROLEINFOPROXY_3636 % int(nowLevelData.get('maxJunZi', 0) * p.getMaxJunziRate())
        desc += gameStrings.TEXT_ROLEINFOPROXY_3637 % int(nowLevelData.get('curMaxJunJie', 0) * p.getMaxZhanxunRate())
        nowRight['desc'] = desc
        info['nowRight'] = nowRight
        info['nowJunzi'] = gameStrings.TEXT_ROLEINFOPROXY_3641 % p.getFame(const.JUN_ZI_FAME_ID)
        thisWeekJunzi = nowLevelData.get('maxJunZi', 0) * p.getMaxJunziRate()
        extraJunzi = nowLevelData.get('extraJunZi', 0)
        curMaxJunZi = self.getCurMaxJunZi() if self.getCurMaxJunZi() > 0 else thisWeekJunzi + extraJunzi
        info['thisWeekJunzi'] = gameStrings.TEXT_ROLEINFOPROXY_3647 % (self.junziWeekVal, curMaxJunZi)
        info['hasExtraJunzi'] = nowLevelData.get('extraJunZi', 0) > 0
        junziActivityTime = SCD.data.get('junziActivityTime', '')
        extraJunziTip = uiUtils.getTextFromGMD(GMDD.data.EXTRA_LIMIT_TIP, gameStrings.TEXT_ROLEINFOPROXY_3651) % (thisWeekJunzi, extraJunzi, junziActivityTime)
        info['extraJunziTips'] = extraJunziTip
        if p.zhanXunRank:
            info['lastWeekRank'] = gameStrings.TEXT_ROLEINFOPROXY_3655 % p.zhanXunRank
        else:
            limitRank = 0
            for _, high in ZRD.data.keys():
                limitRank = max(limitRank, high)

            info['lastWeekRank'] = gameStrings.TEXT_ROLEINFOPROXY_3660 % limitRank
        curZhanXunFame = p.getFame(const.ZHAN_XUN_FAME_ID)
        info['thisWeekZhanXun'] = gameStrings.TEXT_ROLEINFOPROXY_3662 % (curZhanXunFame - getattr(p, 'zhanXunExtraBonus', 0), getattr(p, 'zhanXunExtraBonus', 0))
        info['lastWeekRankAttr'] = gameStrings.TEXT_ROLEINFOPROXY_3663 % self.getZhanXunAttrByRank(p.zhanXunRank)
        if lv in (const.MAX_JUN_JIE_LV, const.PRIMARY_JUN_JIE_LV, const.SECONDARY_JUN_JIE_LV):
            info['isMax'] = True
            secondaryData = JCD.data.get(const.SECONDARY_JUN_JIE_LV, {})
            secondaryRight = {}
            secondaryRight['name'] = secondaryData.get('name', '')
            secondaryRight['state'] = gameStrings.TEXT_ROLEINFOPROXY_3670 % SCD.data.get('junJieTitleRank', (10, 200))[1]
            desc = secondaryData.get('desc', '')
            desc += gameStrings.TEXT_ROLEINFOPROXY_3636 % int(secondaryData.get('maxJunZi', 0) * p.getMaxJunziRate())
            desc += gameStrings.TEXT_ROLEINFOPROXY_3637 % int(secondaryData.get('curMaxJunJie', 0) * p.getMaxZhanxunRate())
            secondaryRight['desc'] = desc
            info['secondaryRight'] = secondaryRight
            primaryData = JCD.data.get(const.PRIMARY_JUN_JIE_LV, {})
            primaryRight = {}
            primaryRight['name'] = primaryData.get('name', '')
            primaryRight['state'] = gameStrings.TEXT_ROLEINFOPROXY_3670 % SCD.data.get('junJieTitleRank', (10, 200))[0]
            desc = primaryData.get('desc', '')
            desc += gameStrings.TEXT_ROLEINFOPROXY_3636 % int(primaryData.get('maxJunZi', 0) * p.getMaxJunziRate())
            desc += gameStrings.TEXT_ROLEINFOPROXY_3637 % int(primaryData.get('curMaxJunJie', 0) * p.getMaxZhanxunRate())
            primaryRight['desc'] = desc
            info['primaryRight'] = primaryRight
        else:
            info['isMax'] = False
            nextLevelData = JCD.data.get(lv + 1, {})
            nextRight = {}
            nextRight['name'] = nextLevelData.get('name', '')
            desc = nextLevelData.get('desc', '')
            desc += gameStrings.TEXT_ROLEINFOPROXY_3636 % int(nextLevelData.get('maxJunZi', 0) * p.getMaxJunziRate())
            desc += gameStrings.TEXT_ROLEINFOPROXY_3637 % int(nextLevelData.get('curMaxJunJie', 0) * p.getMaxZhanxunRate())
            nextRight['desc'] = desc
            info['nextRight'] = nextRight
            reward = self.getZhanXunRewardByRank(p.zhanXunRank)
            totalWeekValue = p.junJieValFromZhanXun + p.junJieValFromOther + reward
            info['lastWeekValue'] = gameStrings.TEXT_ROLEINFOPROXY_3700 % (totalWeekValue, p.junJieValFromZhanXun, reward)
            info['currentValue'] = p.junJieVal * 100.0 / nowLevelData.get('needJunJie', 1)
            info['nowJunjie'] = p.junJieVal
            info['needJunjie'] = nowLevelData.get('needJunJie', 1)
            info['maxJunJieLimit'] = nowLevelData.get('maxJunJieLimit', 0)
            curMaxJunJie = int(nowLevelData.get('curMaxJunJie', const.MAX_ZHAN_XUN_FAME) * p.getMaxZhanxunRate())
            exchangeRatio = nowLevelData.get('exchangeRatio', 1)
            diffVal = int(round(curZhanXunFame * exchangeRatio))
            finalVal = min(diffVal, curMaxJunJie)
            info['thisWeekZhanXun'] += gameStrings.TEXT_ROLEINFOPROXY_3712 % (finalVal, curMaxJunJie)
        rewardZXScores = nowLevelData.get('rewardZXScores', [])
        rewardZXBonusList = nowLevelData.get('rewardZXBonusList', [])
        awardItemList = []
        getAwardBtnEnabled = False
        if len(rewardZXScores) == len(rewardZXBonusList):
            for i in xrange(len(rewardZXScores)):
                itemBonus = clientUtils.genItemBonus(rewardZXBonusList[i])
                if len(itemBonus) <= 0:
                    continue
                itemInfo = uiUtils.getGfxItemById(itemBonus[0][0], itemBonus[0][1])
                itemInfo['state'] = uiConst.ITEM_GRAY
                awardItemInfo = {}
                awardItemInfo['itemInfo'] = itemInfo
                awardItemInfo['state'] = gameStrings.TEXT_XINMORECORDPROXY_183 % rewardZXScores[i]
                awardItemInfo['arrowState'] = 'dislight'
                if curZhanXunFame >= rewardZXScores[i]:
                    itemInfo['state'] = uiConst.ITEM_NORMAL
                    awardItemInfo['arrowState'] = 'light'
                    if p.zhanXunReward.get((p.junJieLv, i), False):
                        awardItemInfo['state'] = gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_187
                    else:
                        awardItemInfo['state'] = gameStrings.TEXT_XINMORECORDPROXY_187
                        getAwardBtnEnabled = True
                elif i > 0 and curZhanXunFame > rewardZXScores[i - 1]:
                    awardItemInfo['arrowState'] = 'half'
                awardItemList.append(awardItemInfo)

        info['awardItemList'] = awardItemList
        info['getAwardBtnEnabled'] = getAwardBtnEnabled
        zxActivityId = self.getZxActivityId()
        if zxActivityId:
            zxActivityTips = SCD.data.get('ZX_ACTIVITY_TIPS', gameStrings.TEXT_ROLEINFOPROXY_3748)
            zxData = ASCD.data.get(zxActivityId, {}).get('rewardZXInfo', {}).get(p.junJieLv, None)
            if zxData:
                needPoint = zxData[0]
                bounsItemId = zxData[1]
                itemBonus = clientUtils.genItemBonus(bounsItemId)
                if len(itemBonus) <= 0:
                    itemId = 0
                else:
                    itemId = itemBonus[0][0]
                isGetedZxBouns = p.zhanXunActivityBonusApplied
                canGetZxBonus = False
                zxBonusItemInfo = uiUtils.getGfxItemById(itemId)
                if curZhanXunFame >= needPoint:
                    if not isGetedZxBouns:
                        canGetZxBonus = True
                        bonusZXState = gameStrings.TEXT_XINMORECORDPROXY_187
                    else:
                        bonusZXState = gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_187
                    zxBonusItemInfo['state'] = uiConst.ITEM_NORMAL
                else:
                    zxBonusItemInfo['state'] = uiConst.ITEM_GRAY
                    bonusZXState = gameStrings.TEXT_XINMORECORDPROXY_183 % needPoint
                info['bonusZXState'] = bonusZXState
                info['zxBonusItemInfo'] = zxBonusItemInfo
                info['canGetZxBonus'] = canGetZxBonus
            else:
                zxActivityTips = SCD.data.get('ZX_ACTIVITY_NO_TIPS', gameStrings.TEXT_ROLEINFOPROXY_3776)
        else:
            zxActivityTips = SCD.data.get('ZX_ACTIVITY_NO_TIPS', gameStrings.TEXT_ROLEINFOPROXY_3776)
        info['zxBounsTips'] = zxActivityTips
        return uiUtils.dict2GfxDict(info, True)

    def onGetAward(self, *arg):
        BigWorld.player().cell.applyZXBonus()

    @ui.callFilter(1, True)
    def onGetJunziBonus(self, *arg):
        BigWorld.player().cell.applyZXBonusFromActivity()

    @ui.callFilter(1, True)
    def onGetQumoActBonus(self, *arg):
        BigWorld.player().cell.getQumoFameFromWeeklyPointsFromActivity()

    def onGetQumoInfo(self, *arg):
        ret = {}
        p = BigWorld.player()
        qumoLv = p.qumoLv
        gongxianData = SCD.data.get('pointsToFame', [])
        qumoData = QLD.data.get(qumoLv, {})
        title = qumoData.get('name', gameStrings.TEXT_ROLEINFOPROXY_3800)
        rewardFameId = qumoData.get('basicFameID', 453)
        basicFameVal = qumoData.get('basicFameVal', 0)
        basicCashVal = qumoData.get('basicCashVal', 0)
        basicCashType = qumoData.get('basicCashType', gametypes.BASIC_CASH_TYPE_MONEY)
        basicCashName = ''
        if basicCashType == gametypes.BASIC_CASH_TYPE_MONEY:
            basicCashName = gameStrings.TEXT_INVENTORYPROXY_3296
        elif basicCashType == gametypes.BASIC_CASH_TYPE_BIND_MONEY:
            basicCashName = gameStrings.TEXT_INVENTORYPROXY_3297
        percentArr = [0.5, 0.5, 0.2]
        if len(gongxianData) > 0:
            percentArr[0] = gongxianData[0][1]
            percentArr[1] = gongxianData[1][1]
            percentArr[2] = gongxianData[2][1]
        famePercent = qumoData.get('famePercent', percentArr)
        gongxianPoint = [180, 300, 560]
        if len(gongxianData) > 0:
            gongxianPoint[0] = gongxianData[0][0]
            gongxianPoint[1] = gongxianData[1][0]
            gongxianPoint[2] = gongxianData[2][0]
        ret['qumoLv'] = qumoLv
        ret['lv'] = p.lv
        ret['title'] = title
        ret['fameName'] = FD.data.get(rewardFameId, {}).get('name', gameStrings.TEXT_INVENTORYPROXY_3299)
        ret['basicFameVal'] = basicFameVal
        ret['basicCashVal'] = basicCashVal
        ret['basicCashType'] = basicCashType
        ret['basicCashName'] = basicCashName
        ret['famePercent'] = famePercent
        ret['gongxianPoint'] = gongxianPoint
        ret['maxGongxian'] = gongxianPoint[2] * p.getMaxWeeklyQumoPointsRate()
        ret['currentGongxian'] = p.weeklyQumoPoints
        weeklyQumoCollectPointsFame = 0
        weeklyQumoCollectPointsCash = 0
        if p.weeklyQumoCollectPoints:
            for points, pointsQumoLv in p.weeklyQumoCollectPoints:
                pointsQumoData = QLD.data.get(pointsQumoLv, {})
                if points in gongxianPoint:
                    weeklyQumoCollectPointsFame += pointsQumoData.get('famePercent', percentArr)[gongxianPoint.index(points)] * pointsQumoData.get('basicFameVal', 0)
                    weeklyQumoCollectPointsCash += pointsQumoData.get('famePercent', percentArr)[gongxianPoint.index(points)] * pointsQumoData.get('basicCashVal', 0)

        ret['currentGotGongxian'] = weeklyQumoCollectPointsFame
        ret['currentGotCash'] = weeklyQumoCollectPointsCash
        ret['gotBtnTip'] = GMD.data.get(GMDD.data.QUMO_REWARD_GET_TIP, {}).get('text', gameStrings.TEXT_ROLEINFOPROXY_3856)
        qumoFameId = SCD.data.get('fameNulinID', 0)
        qumoFameName = FD.data.get(qumoFameId, {}).get('name', gameStrings.TEXT_ROLEINFOPROXY_3860)
        ret['qumoFameName'] = qumoFameName
        qumoScore = p.fame.get(qumoFameId)
        if qumoScore == None:
            ret['qumoScore'] = 0
        else:
            ret['qumoScore'] = p.fame.get(qumoFameId)
        ret['weeklyQumoScore'] = int(self.weeklyQumoScore)
        ret['weeklyMaxQumoScore'] = int(self.weeklyMaxQumoScore)
        gotGongxian = p.weeklyQumoCollectPoints if p.weeklyQumoCollectPoints else []
        if len(gotGongxian) == 0 and p.weeklyQumoPoints >= gongxianPoint[0]:
            ret['canGetReward'] = True
        elif len(gotGongxian) == 1 and p.weeklyQumoPoints >= gongxianPoint[1]:
            ret['canGetReward'] = True
        elif len(gotGongxian) == 2 and p.weeklyQumoPoints >= gongxianPoint[2]:
            ret['canGetReward'] = True
        else:
            ret['canGetReward'] = False
        nextQumoLv = qumoLv + 1
        nextQumoData = QLD.data.get(nextQumoLv, {})
        ret['curLv'] = p.lv
        ret['reqLv'] = nextQumoData.get('reqLv', 0)
        ret['curQumoExp'] = p.qumoExp
        ret['reqQumoExp'] = nextQumoData.get('reqQumoExp', 0)
        ret['qumoExpLimit'] = qumoData.get('maxLvQumoExp', 0)
        if p.statsInfo.has_key(const.QUMO_STATS_VAR_FBSSS):
            ret['curFb'] = p.statsInfo[const.QUMO_STATS_VAR_FBSSS]
        else:
            ret['curFb'] = 0
        ret['reqFb'] = nextQumoData.get('reqFb', 0)
        basicFameVal = nextQumoData.get('basicFameVal', 1200)
        basicCashVal = nextQumoData.get('basicCashVal', 1200)
        ret['nextMaxScore'] = basicFameVal * (famePercent[0] + famePercent[1] + famePercent[2])
        ret['nextMaxCash'] = basicCashVal * (famePercent[0] + famePercent[1] + famePercent[2])
        nextRewardItems = nextQumoData.get('rewardItems', [])
        nextJunziItems = nextQumoData.get('junziItems', [])
        ret['nextRewardItems'] = self.getItemsInfo(nextRewardItems)
        ret['nextBuyJunziItems'] = self.getItemsInfo(nextJunziItems)
        exchangeNpcID = qumoData.get('exchangeNpc', 10040)
        ret['exchangeNpcID'] = exchangeNpcID
        npcId = SEEKD.data.get(exchangeNpcID, {}).get('npcId', 0)
        if npcId == 0:
            ret['exchangeNpcName'] = SEEKD.data.get(exchangeNpcID, {}).get('name', gameStrings.TEXT_EASYPAYPROXY_538)
        else:
            ret['exchangeNpcName'] = ND.data.get(npcId, {}).get('name', gameStrings.TEXT_EASYPAYPROXY_538)
        lvupNpcID = qumoData.get('lvupNpc', 10040)
        ret['lvupNpcID'] = lvupNpcID
        npcId = SEEKD.data.get(lvupNpcID, {}).get('npcId', 0)
        if npcId == 0:
            ret['lvupNpcName'] = SEEKD.data.get(lvupNpcID, {}).get('name', gameStrings.TEXT_EASYPAYPROXY_538)
        else:
            ret['lvupNpcName'] = ND.data.get(npcId, {}).get('name', gameStrings.TEXT_EASYPAYPROXY_538)
        ret['qumoQuests'] = self.getQumoQuests()
        if gameglobal.rds.configData.get('enableRandomChallenge', False):
            challengeId = SCD.data.get('qumoXichenRandomChallengeId', 0)
            BigWorld.callback(0.1, Functor(p.cell.getRandomChallenge, challengeId))
        ret['joinQumoNpcId'] = SCD.data.get('joinQumoNpcId', 0)
        ret['joinQumoText'] = GMD.data.get(GMDD.data.JOIN_QUMO_GUILD, {}).get('text', gameStrings.TEXT_ROLEINFOPROXY_3932)
        qumoActId = self.getQumoActivityId()
        if qumoActId:
            activityTips = SCD.data.get('QUMO_ACTIVITY_TIPS', gameStrings.TEXT_ROLEINFOPROXY_3937)
            qmDataList = ASCD.data.get(qumoActId, {}).get('pointsToFame', {})
            bonusAwardIdList = []
            coverBonus = []
            for qmData in qmDataList:
                qmBonusItem = {}
                qmBonusItem['actBonusGongxianNeed'] = qmData[0]
                if qmBonusItem['actBonusGongxianNeed'] <= p.weeklyQumoPoints:
                    coverBonus.append(qmBonusItem['actBonusGongxianNeed'])
                qmBonusItem['actBonusPercent'] = qmData[1]
                bonusAwardIdList.append(qmBonusItem)

            ret['actBonusList'] = bonusAwardIdList
            if len(coverBonus):
                ret['canGetQumoActBonus'] = False
                weeklyQumoCollectPointsForActivity = p.weeklyQumoCollectPointsForActivity
                for canGetPoint in coverBonus:
                    canGet = True
                    for wcItem in weeklyQumoCollectPointsForActivity:
                        getedPoint = wcItem[0]
                        if getedPoint == canGetPoint:
                            canGet = False

                    if canGet:
                        ret['canGetQumoActBonus'] = True
                        break

            else:
                ret['canGetQumoActBonus'] = False
        else:
            activityTips = SCD.data.get('QUMO_ACTIVITY_NO_TIPS', gameStrings.TEXT_ROLEINFOPROXY_3776)
        ret['actBonusTips'] = activityTips
        ret['hasQuMoBonusAct'] = qumoActId
        ret['doubleQumoScore'] = getattr(p, 'doubleQumo', 0)
        ret['doubleQumoGongxian'] = getattr(p, 'doubleQumoExp', 0)
        ret['rewards'] = []
        rewards = qumoData.get('bonusSet', {500: 0,
         850: 0,
         1000: 0})
        rewards = sorted(rewards.iteritems(), key=lambda e: e[0])
        for reward in rewards:
            bonusId = reward[1]
            fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', ())
            fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
            if fixedBonus:
                itemId = fixedBonus[0][1]
            else:
                itemId = 0
            ret['rewards'].append(ID.data.get(itemId, {}).get('name', ''))

        ret['isUp'] = self.qumoScoreExtraLimit > 0
        extraWeekDesc = SCD.data.get('qumoExtraWeekLimitTime', '')
        ret['extraWeekLimit'] = uiUtils.getTextFromGMD(GMDD.data.EXTRA_LIMIT_TIP, gameStrings.TEXT_ROLEINFOPROXY_3651) % (self.weeklyMaxQumoScore - self.qumoScoreExtraLimit, self.qumoScoreExtraLimit, extraWeekDesc)
        return uiUtils.dict2GfxDict(ret, True)

    def getZxActivityId(self):
        p = BigWorld.player()
        if not hasattr(p, 'zxActivityId'):
            return 0
        else:
            return p.zxActivityId

    def getQumoActivityId(self):
        p = BigWorld.player()
        if not hasattr(p, 'qumoActivityId'):
            return 0
        else:
            return p.qumoActivityId

    def getItemsInfo(self, itemArr):
        info = []
        for item in itemArr:
            if item != None:
                itemId = item[0]
                itemCount = item[1]
                itemInfo = uiUtils.getGfxItemById(itemId, itemCount)
                info.append(itemInfo)

        return info

    def refreshQumoQuests(self, refId):
        self.qumoXichenRefId = refId
        if self.mediator:
            qumoQuests = self.getQumoQuests()
            self.mediator.Invoke('refreshQumoQuests', uiUtils.dict2GfxDict(qumoQuests, True))

    def getQumoQuests(self):
        p = BigWorld.player()
        quests = p.quests
        qumoQuests = {}
        qumoQuests['qumoXichen'] = {}
        qumoQuests['qumoPomo'] = {}
        qumoQuests['qumoJiehuo'] = {}
        questData = QD.data
        dailyQuests = self.getDefinedLoopQuest(gametypes.QUEST_REFRESH_DAILY)
        qumoQuests['xichenFinished'] = self.isQumoFinished(dailyQuests, uiConst.QUMO_XICHEN_QUEST)
        for questId in quests:
            for dailyQuestId in dailyQuests:
                currentQuestId = p.questLoopInfo[dailyQuestId].getCurrentQuest()
                if currentQuestId and questId == currentQuestId:
                    if questData.get(questId, {}).get('activityType', 0) == uiConst.QUMO_XICHEN_QUEST:
                        qumoXichenObj = self.getQumoQuestsInfo(dailyQuestId, questId, self.qumoXichenRefId)
                        qumoQuests['qumoXichen'] = qumoXichenObj
                        break

        weeklyQuests = self.getDefinedLoopQuest(gametypes.QUEST_REFRESH_WEEKLY)
        qumoQuests['pomoFinished'] = self.isQumoFinished(weeklyQuests, uiConst.QUMO_POMO_QUEST)
        for questId in quests:
            for weeklyQuestId in weeklyQuests:
                currentQuestId = p.questLoopInfo[weeklyQuestId].getCurrentQuest()
                if currentQuestId and currentQuestId == questId:
                    if questData.get(questId, {}).get('activityType', 0) == uiConst.QUMO_POMO_QUEST:
                        qumoPomoObj = self.getQumoQuestsInfo(weeklyQuestId, questId, 0)
                        qumoQuests['qumoPomo'] = qumoPomoObj
                        break

        qumoQuests['jiehuoFinished'] = self.isQumoFinished(weeklyQuests, uiConst.QUMO_JIEHUO_QUEST)
        for questId in quests:
            for weeklyQuestId in weeklyQuests:
                currentQuestId = p.questLoopInfo[weeklyQuestId].getCurrentQuest()
                if currentQuestId and currentQuestId == questId:
                    if questData.get(questId, {}).get('activityType', 0) == uiConst.QUMO_JIEHUO_QUEST:
                        qumoJiehuoObj = self.getQumoQuestsInfo(weeklyQuestId, questId, 0)
                        qumoQuests['qumoJiehuo'] = qumoJiehuoObj
                        break

        return qumoQuests

    def isQumoFinished(self, loopQuests, qumoType):
        isFinish = False
        for questLoopId in loopQuests:
            loopCnt = 0
            loopData = BigWorld.player().questLoopInfo.get(questLoopId, None)
            if loopData and QLOOPD.data.get(questLoopId, {}).get('activityType', 0) == qumoType:
                loopCnt = loopData.loopCnt
                maxCnt = QLOOPD.data.get(questLoopId, {}).get('maxLoopCnt', 1)
                isFinish = loopCnt == maxCnt
                break

        return isFinish

    def getQumoQuestsInfo(self, questLoopId, questId, refId):
        questData = QD.data
        questLoopData = QLOOPD.data
        questInfo = {}
        questInfo['questId'] = questId
        questInfo['questLoopId'] = questLoopId
        questInfo['name'] = questLoopData.get(questLoopId, {}).get('name', '')
        questInfo['weeklyQumoPoints'] = questData.get(questId, {}).get('weeklyQumoPoints', 0)
        rewardItemId = questData.get(questId, {}).get('qumoReward', 0)
        questInfo['itemId'] = rewardItemId
        linkActivityId = questData.get(questId, {}).get('linkActivityId', 0)
        if refId != 0 and gameglobal.rds.configData.get('enableRandomChallenge', False):
            linkActivityId = FBD.data.get(refId, {}).get('relateActId', 0)
        picId = ABD.data.get(linkActivityId, {}).get('bgId', '10010')
        questInfo['picPath'] = 'scheduleBg/%s.dds' % picId
        questInfo['lvRange'] = questData.get(questId, {}).get('qumoLvRange', gameStrings.TEXT_GAME_1747)
        return questInfo

    def getDefinedLoopQuest(self, refreshType):
        p = BigWorld.player()
        loopQuests = []
        questLoopData = p.questLoopInfo
        for questLoopId in questLoopData.keys():
            if QLOOPD.data.get(questLoopId, {}).get('refreshTime', 0) == refreshType:
                loopQuests.append(questLoopId)

        return loopQuests

    def onRefreshVpPanel(self, *args):
        p = BigWorld.player()
        expParam, transformRatio = p.getVpLvData()
        vpStage = p.getVpStage()
        tips = VTD.data
        ret = {}
        ret['vpStage'] = 'stage' + str(vpStage)
        expParam = vp_stage_data.data.get(vpStage)['expParam']
        if vpStage == 0:
            ret['line0'] = gameStrings.TEXT_EXPBARPROXY_173
            ret['line1'] = ''
        else:
            ret['line0'] = tips.get(uiConst.VP_PANEL_DESC1, {}).get('desc', '') % (expParam - 1)
            ret['line1'] = tips.get(uiConst.VP_PANEL_DESC2, {}).get('desc', '') % (expParam - 1)
        vData = VLD.data.get(p.lv, {})
        ret['line2'] = tips.get(uiConst.VP_PANEL_DESC3, {}).get('desc', '') % ((vData['vpDefaultLower'] + vData['vpDefaultUpper']) / 2)
        ret['line3'] = tips.get(uiConst.VP_PANEL_DESC4, {}).get('desc', '') % vData['dailyVp']
        upMode = ALD.data.get(p.lv, {}).get('upMode', gametypes.LEVEL_UP_MODE_FORBID)
        if p.lv < const.MAX_LEVEL and upMode != gametypes.LEVEL_UP_MODE_FORBID:
            nextLvData = VLD.data.get(p.lv + 1, {})
            ret['line4'] = tips.get(uiConst.VP_PANEL_DESC5, {}).get('desc', '') % (p.lv + 1, nextLvData.get('lvUpVp', 0))
        else:
            ret['line4'] = gameStrings.TEXT_ROLEINFOPROXY_4136
        if p.getVpVip(0) == 0 and p.vpAdd[1] == 0:
            ret['isVip'] = False
        else:
            ret['isVip'] = True
        ret['line5'] = gameStrings.TEXT_ROLEINFOPROXY_4143 % p.getVpVip(0)
        ret['line6'] = ''
        ret['baseVp'] = p.baseVp
        ret['savedVp'] = p.savedVp
        ret['maxVp'] = vData['maxVp']
        ret['maxVpAdd'] = p.vpAdd[2]
        if self.mediator:
            self.mediator.Invoke('setVpInfo', uiUtils.dict2GfxDict(ret, True))
        self.refreshVpKey()

    def updateQumoFame(self, value, nWeek, mWeek, extraLimit):
        self.weeklyQumoScore = nWeek
        self.weeklyMaxQumoScore = mWeek
        self.qumoScoreExtraLimit = extraLimit

    def onGetQumoPoints(self, *arg):
        p = BigWorld.player()
        p.cell.getQumoFameFromWeeklyPoints()

    def onGenMaxVpTip(self, *args):
        p = BigWorld.player()
        vData = VLD.data.get(p.lv, {})
        desc = gameStrings.TEXT_ROLEINFOPROXY_4170 % (vData['maxVp'] + p.vpAdd[2])
        desc += gameStrings.TEXT_ROLEINFOPROXY_4171
        desc += gameStrings.TEXT_ROLEINFOPROXY_4172 % vData['maxVp']
        if p.vpAdd[2] != 0:
            desc += gameStrings.TEXT_ROLEINFOPROXY_4174 % p.vpAdd[2]
        return GfxValue(gbk2unicode(desc))

    def onGenVpTip(self, *args):
        p = BigWorld.player()
        expParam, transformRatio = p.getVpLvData()
        desc = gameStrings.TEXT_ROLEINFOPROXY_4181 % (p.baseVp + p.savedVp)
        desc += gameStrings.TEXT_ROLEINFOPROXY_4171
        delta = int(p.baseVp * transformRatio)
        maxRatio = SCD.data.get('maxVpTransformRatio', 1.6)
        if transformRatio + p.getVpVip(3) > maxRatio:
            allDelta = p.baseVp * maxRatio
            deltaVip = p.baseVp * maxRatio - delta
        else:
            allDelta = int(p.baseVp * (transformRatio + p.getVpVip(3)))
            deltaVip = allDelta - delta
        if deltaVip > 0:
            desc += gameStrings.TEXT_ROLEINFOPROXY_4193 + gameStrings.TEXT_ROLEINFOPROXY_4194 % (p.baseVp,
             allDelta,
             delta,
             deltaVip)
        else:
            desc += gameStrings.TEXT_ROLEINFOPROXY_4193 + gameStrings.TEXT_ROLEINFOPROXY_4197 % (p.baseVp, allDelta)
        desc += gameStrings.TEXT_ROLEINFOPROXY_4198 % p.savedVp
        return GfxValue(gbk2unicode(desc))

    def onGenBottleVipTip(self, *args):
        tips = VTD.data
        p = BigWorld.player()
        nowText = tips.get(uiConst.VP_PANEL_VP_STORAGE, {}).get('desc', gameStrings.TEXT_ROLEINFOPROXY_4204)
        txt = nowText % p.vpStorage
        return GfxValue(gbk2unicode(txt))

    def onGenVpExpireTimeTip(self, *args):
        tips = VTD.data
        p = BigWorld.player()
        nowText = ''
        if utils.getNow() < p.vpStorageExpireTime:
            timeText = time.strftime('%Y.%m.%d  %H:%M', time.localtime(p.vpStorageExpireTime))
            nowText = tips.get(uiConst.VP_PANEL_VP_KEY_NOT_LOCK, {}).get('desc', gameStrings.TEXT_ROLEINFOPROXY_4214)
            txt = nowText % timeText
        else:
            txt = tips.get(uiConst.VP_PANEL_VP_KEY_LOCK, {}).get('desc', gameStrings.TEXT_ROLEINFOPROXY_4217)
        return GfxValue(gbk2unicode(txt))

    def updateGotWeeklyQumoPoints(self):
        p = BigWorld.player()
        percentArr = [0.5, 0.5, 0.2]
        gongxianPoint = [180, 300, 560]
        gongxianData = SCD.data.get('pointsToFame', [])
        if len(gongxianData) > 0:
            percentArr[0] = gongxianData[0][1]
            percentArr[1] = gongxianData[1][1]
            percentArr[2] = gongxianData[2][1]
        if len(gongxianData) > 0:
            gongxianPoint[0] = gongxianData[0][0]
            gongxianPoint[1] = gongxianData[1][0]
            gongxianPoint[2] = gongxianData[2][0]
        weeklyQumoCollectPointsFame = 0
        weeklyQumoCollectPointsCash = 0
        if p.weeklyQumoCollectPoints:
            for points, pointsQumoLv in p.weeklyQumoCollectPoints:
                pointsQumoData = QLD.data.get(pointsQumoLv, {})
                if points in gongxianPoint:
                    weeklyQumoCollectPointsFame += pointsQumoData.get('famePercent', percentArr)[gongxianPoint.index(points)] * pointsQumoData.get('basicFameVal', 0)
                    weeklyQumoCollectPointsCash += pointsQumoData.get('famePercent', percentArr)[gongxianPoint.index(points)] * pointsQumoData.get('basicCashVal', 0)

        canGetReward = False
        gotGongxian = p.weeklyQumoCollectPoints if p.weeklyQumoCollectPoints else []
        if len(gotGongxian) == 0 and p.weeklyQumoPoints >= gongxianPoint[0]:
            canGetReward = True
        elif len(gotGongxian) == 1 and p.weeklyQumoPoints >= gongxianPoint[1]:
            canGetReward = True
        elif len(gotGongxian) == 2 and p.weeklyQumoPoints >= gongxianPoint[2]:
            canGetReward = True
        else:
            canGetReward = False
        if self.mediator:
            self.mediator.Invoke('updateQumoWeeklyCollectPoints', (GfxValue(weeklyQumoCollectPointsFame), GfxValue(weeklyQumoCollectPointsCash), GfxValue(canGetReward)))

    def onGetJingJieNotifyInfo(self, *arg):
        p = BigWorld.player()
        canOpenJingjie = p.checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_JINGJIE)
        if gameglobal.rds.configData.get('enableYSCheck', False):
            result = utils.checkUpgradeJingJie(BigWorld.player())
        else:
            result = True
        result = result and canOpenJingjie
        return GfxValue(result)

    def refreshJingjieInfo(self):
        if self.mediator:
            jingjieName = JD.data.get(BigWorld.player().jingJie, {}).get('name', '')
            self.mediator.Invoke('setJingJie', GfxValue(gbk2unicode(jingjieName)))
            self.mediator.Invoke('refreshJingJieNotify')

    def refreshHieroNotify(self):
        if self.mediator:
            self.mediator.Invoke('refreshHieroNotify')

    def onGetHieroHasAvailablePos(self, *args):
        p = BigWorld.player()
        canOpenRune = p.checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_HIEROGRAM)
        has = gameglobal.rds.ui.roleInformationHierogram.isHasAvailablePos() and canOpenRune
        return GfxValue(has)

    def _getShowTitleStyle(self):
        name = ''
        style = 1
        p = BigWorld.player()
        if p:
            name, style = p.getActivateTitleStyle()
        if not name:
            name = gameStrings.TEXT_ROLEINFOPROXY_4297
        return (name, style)

    def onOpenWingAndMount(self, *args):
        idx = int(args[3][0].GetNumber())
        gameglobal.rds.ui.wingAndMount.show(idx)

    def onCanOpenTab(self, *args):
        idx = int(args[3][0].GetNumber())
        showMsg = args[3][1].GetBool()
        p = BigWorld.player()
        if p.crossServerFlag == const.CROSS_SERVER_STATE_IN:
            if idx in SCD.data.get('crossServerRoleTabBlack', ()) and not p.isUsingTemp():
                showMsg and p.showGameMsg(GMDD.data.ROLE_TAB_IN_BLACK_LIST, ())
                return GfxValue(False)
        return GfxValue(True)

    def refreshVpKey(self):
        p = BigWorld.player()
        storageText = '%d' % p.vpStorage
        if storageText == '0':
            storageText = ''
        iconPath = 'state/22/' + str(SCD.data.get('VP_KEY_ICON', 11010)) + '.dds'
        canUse = False
        timeText = ''
        if utils.getNow() < p.vpStorageExpireTime:
            canUse = True
            leftTime = p.vpStorageExpireTime - utils.getNow()
            timeText = utils.formatDurationShortVersion(leftTime)
        if self.mediator:
            self.mediator.Invoke('setVpKeyInfo', (GfxValue(gbk2unicode(iconPath)),
             GfxValue(gbk2unicode(timeText)),
             GfxValue(gbk2unicode(storageText)),
             GfxValue(canUse)))

    def onOpenZhanXunList(self, *arg):
        gameglobal.rds.ui.zhanXunRankList.show()

    def onGetNeiYiConfig(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableFashionNeiYi', False))

    def onGetMingPaiInfo(self, *args):
        mpDatas = []
        p = BigWorld.player()
        result = {'mpDatas': mpDatas,
         'ownMingPai': p.mingpaiInfo.keys()}
        for key, data in MPD.data.items():
            active = False
            if p.mingpaiInfo.has_key(key):
                start, last = p.mingpaiInfo.get(key)
                if start + last > utils.getNow() or last < 0:
                    active = True
            elif data.get('showOnlyOwn', 0):
                continue
            mpData = {'mpId': key,
             'mpIconPath': uiConst.MING_PAI_ICON_PATH_40 + str(data.get('icon', '')) + '.dds',
             'tip': tipUtils.getMingPaiTip(key, p),
             'active': active}
            if p.selectedMPId == key:
                result['currentMP'] = mpData
            mpDatas.append(mpData)

        emptyData = {'mpId': 0,
         'mpIconPath': uiConst.MING_PAI_ICON_PATH_40 + '0.dds',
         'active': True}
        mpDatas.insert(0, emptyData)
        if p.selectedMPId == 0:
            result['currentMP'] = emptyData
        return uiUtils.dict2GfxDict(result, True)

    @ui.callFilter(1, True)
    def onApplyMingPai(self, *args):
        mpId = int(args[3][0].GetNumber())
        p = BigWorld.player()
        if mpId != p.selectedMPId:
            p.base.selectMingpai(mpId)

    def onGetRoleNameWithMingPai(self, *args):
        p = BigWorld.player()
        roleName = uiUtils.getNameWithMingPain(p.roleName, p.selectedMPId)
        return GfxValue(gbk2unicode(roleName))

    def refreshMingPai(self):
        if self.mediator:
            self.mediator.Invoke('refreshMingPai')

    def onOpenGuanYin(self, *arg):
        p = BigWorld.player()
        equip = p.equipment[gametypes.EQU_PART_CAPE]
        if not gameconfigCommon.enableGuanYinThirdPhase():
            if not equip:
                return
            if equip.hasLatch():
                p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                return
            if not equip.validGuanYinPos(0, 0):
                p.showGameMsg(GMDD.data.GUANYIN_OPEN_NO_SKILL_SLOT_HINT, ())
                return
        gameglobal.rds.ui.guanYin.show()

    def onOpenYaoPei(self, *arg):
        p = BigWorld.player()
        equip = p.equipment[gametypes.EQU_PART_YAOPEI]
        if not equip:
            return
        if equip.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        gameglobal.rds.ui.yaoPeiFeed.showInEquip()

    def onOpenEquipChange(self, *arg):
        gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_ENHANCE, 0)

    def onOpenGuiBaoge(self, *arg):
        gameglobal.rds.ui.guibaoge.show()

    def onOpenSkillAppearance(self, *args):
        gameglobal.rds.ui.skillAppearance.show()

    def onActEffectAppearance(self, *args):
        gameglobal.rds.ui.actEffectAppearance.show()

    def onIsSkillAppearanceVisible(self, *args):
        if not gameglobal.rds.configData.get('enableSkillAppearance', False):
            return GfxValue(False)
        return GfxValue(True)

    def onSwitchEquip(self, *arg):
        self.realSwitchEquip()

    @ui.checkEquipChangeOpen()
    def realSwitchEquip(self):
        p = BigWorld.player()
        if gameglobal.rds.ui.guanYin.chechPanelOpen():
            p.showGameMsg(GMDD.data.SWITCH_EQUIP_ERROR_GUANYIN_PANEL_OPEN, ())
            return
        if gameglobal.rds.ui.yaoPeiFeed.mediator:
            p.showGameMsg(GMDD.data.SWITCH_EQUIP_ERROR_YAOPEI_FEED_PANEL_OPEN, ())
            return
        p.cell.switchEquip()

    def switchEquipBegin(self):
        pass

    def switchEquipSucc(self):
        if self.mediator:
            self.mediator.Invoke('changeToMain')

    def onEnableHideFashionHead(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableHideFashionHead', False))

    def onEnableYuanLing(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableYuanLing', False))

    def onHideFashionHead(self, *args):
        show = args[3][0].GetBool()
        BigWorld.player().cell.setSignal(gametypes.SIGNAL_HIDE_FASHION_HEAD, show)

    def onGetRuneTransInfo(self, *args):
        ret = {}
        p = BigWorld.player()
        gameglobal.rds.ui.roleInformationHierogram.appendEquipData(ret, p.hierogramDict)
        num = 0
        if ret.get('itemInfos', {}).get('hieroEquipItem', None):
            num += 1
        if ret.get('itemInfos', {}).get('benyuanItem', None):
            num += 1
        if len(ret.get('itemInfos', {}).get('dilunItems', [])):
            num += len(ret.get('itemInfos', {}).get('dilunItems', []))
        if len(ret.get('itemInfos', {}).get('tianlunItems', [])):
            num += len(ret.get('itemInfos', {}).get('tianlunItems', []))
        info = {}
        info['transNum'] = num
        info['isTrans'] = p.isClearAndTransitToRune()
        _str = gameStrings.TEXT_ROLEINFOPROXY_4481 % num
        info['transStr'] = _str
        gamelog.debug('@zq info', info)
        return uiUtils.dict2GfxDict(info, True)

    def onResetRuneFunc(self, *args):
        p = BigWorld.player()
        p.cell.clearAndTransitToRune()
        gamelog.debug('@zq onResetRuneFunc')

    def onGetEnableGuiBaoGe(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableGuiBaoGe'), False)

    def onCheckHideFashionHead(self, *args):
        check = False
        if getattr(BigWorld.player(), 'hidingPower', 0):
            BigWorld.player().showGameMsg(GMDD.data.CANNOT_CHANGE_HEAD_VISIBLE_IN_HIDING, ())
            check = True
        return uiUtils.dict2GfxDict({'check': check,
         'select': BigWorld.player().isHideFashionHead()})

    def onIsHadNewFame(self, *args):
        if gameglobal.rds.configData.get('enableHonorV2', False):
            return GfxValue(BigWorld.player().isHadNewFame)
        else:
            return GfxValue(False)

    def onInitPanel(self, *args):
        proxyName = args[3][0].GetString()
        widget = ASObject(args[3][1])
        if proxyName == 'roleInformationProp':
            proxy = self
        else:
            proxy = getattr(self.uiAdapter, proxyName, None)
        if proxy and hasattr(proxy, 'initPanel'):
            proxy.initPanel(widget)

    def onUnRegisterPanel(self, *args):
        proxyName = args[3][0].GetString()
        if proxyName == 'roleInformationProp':
            proxy = self
        else:
            proxy = getattr(self.uiAdapter, proxyName, None)
        if proxy and hasattr(proxy, 'unRegisterPanel'):
            proxy.unRegisterPanel()

    def onGetTemplateName(self, *args):
        p = BigWorld.player()
        templateName = getattr(p, 'templateName', '')
        return GfxValue(gbk2unicode(templateName))

    def onCanChangeTemplate(self, *args):
        p = BigWorld.player()
        return GfxValue(p.canChangeTemplate())

    def onIsUsingTemp(self, *args):
        p = BigWorld.player()
        return GfxValue(p.isUsingTemp())

    def initPanel(self, widget):
        self.widget = widget
        self.widget.role.refineSuitsBtn.visible = gameconfigCommon.enableEquipEnhanceSuit()
        if gameconfigCommon.enableEquipEnhanceSuit():
            currentLv, nextLv = self.uiAdapter.equipRefineSuitsProp.getRefineLv()
            showLv = currentLv if currentLv else nextLv
            self.widget.role.refineSuitsBtn.label = uiUtils.intToRoman(showLv[0])
            self.widget.role.refineSuitsBtn.addEventListener(events.BUTTON_CLICK, self.handleRefineSuitsBtnClick, False, 0, True)

    def refreshRefineSuitsBtn(self):
        if not self.widget:
            return
        if gameconfigCommon.enableEquipEnhanceSuit():
            currentLv, nextLv = self.uiAdapter.equipRefineSuitsProp.getRefineLv()
            showLv = currentLv if currentLv else nextLv
            self.widget.role.refineSuitsBtn.label = uiUtils.intToRoman(showLv[0])

    def handleRefineSuitsBtnClick(self, *args):
        if self.uiAdapter.equipRefineSuitsProp.widget:
            self.uiAdapter.equipRefineSuitsProp.hide()
        else:
            self.uiAdapter.equipRefineSuitsProp.show()

    def unRegisterPanel(self):
        self.widget = None
        self.uiAdapter.equipRefineSuitsProp.hide()
