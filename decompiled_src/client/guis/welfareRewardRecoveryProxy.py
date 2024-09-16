#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/welfareRewardRecoveryProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import uiConst
import events
import gametypes
import gamelog
import clientUtils
import utils
from gamestrings import gameStrings
from callbackHelper import Functor
from guis.asObject import TipManager
import questLoops
from uiProxy import UIProxy
from guis import uiUtils
from guis import ui
from guis.asObject import ASObject
from data import sys_config_data as SCD
from data import reward_getback_data as RGD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from data import fame_data as FD
from data import log_src_data as LSD
RECOVERY_TYPE_PERFECT = gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_COIN
RECOVERY_TYPE_NORMAL = gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_FAME1
REWARD_ITEM_MAX_CNT = 6
REWARD_ICON_MAX_CNT = 4
REWARD_COST_ICON_MAX_CNT = 2
EXP_ITEM_ID = 441002
FIND_BEAST_ACTIVITY_ID = 1114
COST_FAME_TYPE_DISHE = 0
COST_FMAE_TYPE_YUNCHUI = 1
PAR_Y = 85
PAR_X_LEFT_INTERNAL = 15
PAR_X_RIGHT_INTERNAL = 5
LEFTTIME_Y = 88
QU_MO_SUB_TYPE_IDS = (3001, 3002, 3003)
JUN_JIE_NORMAL_SUB_TYPE_IDS = (3101, 3102, 3103)
JUN_JIE_WING_WORLD_SUB_TYPE_IDS = (3101, 3102, 3103, 3104, 3105)

class WelfareRewardRecoveryProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WelfareRewardRecoveryProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.recoveryType = RECOVERY_TYPE_PERFECT
        self.isActivityMode = False
        self.expandDic = {}

    def initRewardRecovery(self, widget):
        self.widget = widget
        self.initUI()
        self.getInfoList()
        self.recoveryType = RECOVERY_TYPE_PERFECT if self.isActivityMode else RECOVERY_TYPE_NORMAL
        self.widget.txtActivityTime.htmlText = SCD.data.get('rewardRecoveryActivityTime', '') if self.isActivityMode else ''
        self.refreshInfo()

    def initUI(self):
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_REWARD_RECOVERY)
        if not self.widget or not self.widget.perfectRetrieveBtn:
            return
        self.widget.perfectRetrieveBtn.addEventListener(events.BUTTON_CLICK, self.handlePerfectRetrieveBtnClick, False, 0, True)
        self.widget.perfectRetrieveBtn.selected = True
        self.widget.normalRetrieveBtn.addEventListener(events.BUTTON_CLICK, self.handleNormalRetrieveBtnClick, False, 0, True)
        self.widget.helpIcon.helpKey = SCD.data.get('rewardRecoveryHelpKey', 0)
        self.widget.removeAllInst(self.widget.scrollWndList.canvas)
        self.widget.scrollWndList.itemRenderer = 'WelfareRewardRecovery_ItemRender'
        self.widget.scrollWndList.lableFunction = self.lableFunction
        self.widget.scrollWndList.itemHeightFunction = self.itemHeightFunction

    def itemHeightFunction(self, *args):
        itemData = ASObject(args[3][0])
        if not itemData.canExpand:
            return GfxValue(112)
        return GfxValue(134)

    def unRegisterRewardRecovery(self):
        self.uiAdapter.rewardRecoveryNormal.hide()
        self.uiAdapter.rewardRecoveryDiKou.hide()
        self.widget.scrollWndList.dataArray = []
        self.widget = None
        self.reset()

    def processSubType(self, info, infoList, activityId):
        p = BigWorld.player()
        if not self.recoveryType == RECOVERY_TYPE_PERFECT:
            info['canExpand'] = False
            return
        activityType = RGD.data.get(activityId, {}).get('activityType', 0)
        if activityId == gametypes.REWARD_RECOVER_ACTIVITY_ID_FOR_QU_MO:
            subIdList = QU_MO_SUB_TYPE_IDS
        elif activityId == gametypes.REWARD_RECOVER_ACTIVITY_ID_FOR_JUN_JIE:
            if p.canOpenWingWorldUI():
                subIdList = JUN_JIE_WING_WORLD_SUB_TYPE_IDS
            else:
                subIdList = JUN_JIE_NORMAL_SUB_TYPE_IDS
        else:
            return
        getBackRewardAndConsumeInfoList = []
        activity = p.rewardRecoveryActivity.getActivity(activityType)
        subIdList = [ subId for subId in subIdList if activity.calcHistoryGetBackNum({'subId': subId,
         'tp': self.recoveryType}) ]
        addSubInfoList = []
        for subId in subIdList:
            subInfo = self.getInfoByActivityId(subId, {'subId': subId})
            subInfo and addSubInfoList.append(subInfo)

        if not len(addSubInfoList):
            info['canExpand'] = False
        else:
            info['canExpand'] = True
        if self.expandDic.get(activityType, False):
            info['subList'] = addSubInfoList

    def processInfoItemList(self, info, getBackRewardAndConsumeInfo):
        itemList = []
        itemDic = {}
        for bonusId in getBackRewardAndConsumeInfo.get('bonusIds', []):
            for itemId, cnt in clientUtils.genItemBonus(bonusId):
                itemDic[itemId] = itemDic.get(itemId, 0) + cnt

        itemList = [ uiUtils.getGfxItemById(key, value) for key, value in itemDic.iteritems() ]
        if getBackRewardAndConsumeInfo.get('exp', 0):
            itemList.append(uiUtils.getGfxItemById(EXP_ITEM_ID, 1))
        info['itemList'] = itemList

    def processInfoIconList(self, info, getBackRewardAndConsumeInfo, configData):
        info['iconList'] = []
        info['iconList'].append(('exp', getBackRewardAndConsumeInfo.get('exp', 0)))
        rewardFames = getBackRewardAndConsumeInfo.get('rewardFames', {})
        for fameId, fame in rewardFames.iteritems():
            info['iconList'].append(('shenwang', fame, fameId))

        info['isExpAddSprite'] = configData.get('isExpAddSprite', 0)
        if configData.get('isExpAddSprite', 0):
            info['iconList'].append(('yljingyan', getBackRewardAndConsumeInfo.get('exp', 0) * LSD.data.get('spriteExpCoef', 0)))
        info['infoList'] = []
        specialInfo = configData.get('specialInfo', ())
        if specialInfo and self.recoveryType == RECOVERY_TYPE_PERFECT:
            for fameId, fameNum in specialInfo:
                fameIcon = FD.data.get(fameId, {}).get('icon', '')
                info['infoList'].append((fameIcon, fameNum))

    def processInfoCostList(self, info, activityId, getBackRewardAndConsumeInfo, getBackRewardAndConsumeInfoByFame1 = None, getBackRewardAndConsumeInfoByFame2 = None):
        info['exp'] = getBackRewardAndConsumeInfo.get('exp', 0)
        p = BigWorld.player()
        info['costList'] = []
        if self.recoveryType == RECOVERY_TYPE_PERFECT:
            if not gameglobal.rds.configData.get('enableRewardRecoveryNew', False):
                info['costList'].append(('tianBi', getBackRewardAndConsumeInfo.get('consumeCoin', 0)))
                info['originPrice'] = getBackRewardAndConsumeInfo.get('consumeCoin', 0)
                info['nowPrice'] = getBackRewardAndConsumeInfo.get('consumeCoin', 0)
            else:
                nowPrice = getBackRewardAndConsumeInfo.get('consumeCoin', 0)
                originPrice = getBackRewardAndConsumeInfo.get('consumeCoinOriginal', 0)
                info['originPrice'] = originPrice
                info['nowPrice'] = nowPrice
                if self.canUseItemDiKou(activityId):
                    diKouItemId = RGD.data.get(activityId, {}).get('rewardGetBackConsumeItem', 0)
                    daiKouItemCount = p.inv.countItemInPages(diKouItemId, enableParentCheck=True)
                    if originPrice - daiKouItemCount < nowPrice:
                        info['costList'].append(('tianBi', max(0, originPrice - daiKouItemCount)))
                    else:
                        info['costList'].append(('tianBi', nowPrice))
                else:
                    info['costList'].append(('tianBi', nowPrice))
        else:
            fame1, fameVal1 = getBackRewardAndConsumeInfoByFame1['consumeFames'][0]
            fame2, fameVal2 = getBackRewardAndConsumeInfoByFame2['consumeFames'][0]
            info['costList'].append(('yunChui', fameVal1))
            info['costList'].append(('gongJiDian', fameVal2))

    def processOtherInfo(self, info, activityId, getBackNum):
        configData = RGD.data.get(activityId, {})
        sortOrder = configData.get('sortOrder', activityId)
        activityType = configData.get('activityType', 0)
        info['activityId'] = activityId
        info['activityType'] = activityType
        title = configData.get('ItemTitle', 'title(%d)')
        try:
            info['title'] = title % getBackNum
        except:
            info['title'] = title

        info['itemList'] = []
        info['sortOrder'] = sortOrder

    def processActivityMode(self, info, activityId):
        if self.canUseItemDiKou(activityId):
            self.isActivityMode = True
            info['isActivityMode'] = True
        else:
            info['isActivityMode'] = False

    def getInfoByActivityId(self, activityId, extraInfo = {}):
        p = BigWorld.player()
        configData = RGD.data.get(activityId, {})
        activityType = configData.get('activityType', 0)
        activity = p.rewardRecoveryActivity.getActivity(activityType)
        getBackNum = activity.calcHistoryGetBackNum({'tp': self.recoveryType})
        if self.recoveryType == RECOVERY_TYPE_PERFECT:
            getBackRewardAndConsumeInfo = activity.calcHistoryRewardAndConsume(p, self.recoveryType, extraInfo)
            getBackRewardAndConsumeInfoByFame1 = None
            getBackRewardAndConsumeInfoByFame2 = None
        else:
            getBackRewardAndConsumeInfoByFame1 = activity.calcHistoryRewardAndConsume(p, gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_FAME2, extraInfo)
            getBackRewardAndConsumeInfo = getBackRewardAndConsumeInfoByFame1
            getBackRewardAndConsumeInfoByFame2 = activity.calcHistoryRewardAndConsume(p, gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_FAME1, extraInfo)
            getBackRewardAndConsumeInfo = getBackRewardAndConsumeInfoByFame2
        if not getBackRewardAndConsumeInfo:
            return
        else:
            info = {}
            if extraInfo:
                pass
            self.processOtherInfo(info, activityId, getBackNum)
            self.processInfoItemList(info, getBackRewardAndConsumeInfo)
            self.processInfoIconList(info, getBackRewardAndConsumeInfo, configData)
            self.processInfoCostList(info, activityId, getBackRewardAndConsumeInfo, getBackRewardAndConsumeInfoByFame1, getBackRewardAndConsumeInfoByFame2)
            self.processActivityMode(info, activityId)
            return info

    def checkConfigData(self, configData):
        blackList = []
        try:
            blackStrList = gameglobal.rds.configData.get('rewardRecoveryBlackList', '').split(',')
            for str in blackStrList:
                blackList.append(int(str))

        except Exception as e:
            pass

        p = BigWorld.player()
        activityStartTime = configData.get('activityCanGetbackStartTime', None)
        if activityStartTime and utils.getNow() < utils.getDisposableCronTabTimeStamp(activityStartTime):
            return False
        elif not configData:
            return False
        lvLimit = configData.get('lv', (1, 99))
        if p.lv < lvLimit[0] or p.lv > lvLimit[1]:
            return False
        activityType = configData.get('activityType', 0)
        activity = p.rewardRecoveryActivity.getActivity(activityType)
        getBackNum = activity.calcHistoryGetBackNum({'tp': self.recoveryType})
        if not getBackNum:
            return False
        elif (activityType == gametypes.REWARD_RECOVER_ACTIVITY_TYPE_GUILD_DAILY or activityType == gametypes.REWARD_RECOVER_ACTIVITY_TYPE_SUI_XING_YU) and p.guildNUID == 0L:
            return False
        if activityType == gametypes.REWARD_RECOVER_ACTIVITY_ID_FOR_LUN_ZHAN_YUN_DIAN:
            LZYDServerProgress = SCD.data.get('LZYDServerProgress', [])
            if p.isServerProgressFinished(LZYDServerProgress[0]):
                if p.lv < 60:
                    return False
        if activityType in blackList:
            return False
        else:
            return True

    def getInfoList(self):
        infoList = []
        p = BigWorld.player()
        blackList = []
        try:
            blackStrList = gameglobal.rds.configData.get('rewardRecoveryBlackList', '').split(',')
            for str in blackStrList:
                blackList.append(int(str))

        except Exception as e:
            pass

        for activityType, activityInfo in getattr(p, 'rewardRecoveryActivity', {}).iteritems():
            try:
                activityId = activityInfo.activityId
                configData = RGD.data.get(activityId, {})
                if not self.checkConfigData(configData):
                    continue
                info = self.getInfoByActivityId(activityId)
                if not info:
                    continue
                infoList.append(info)
                self.processSubType(info, infoList, activityId)
            except Exception as e:
                gamelog.info('@jbx:error', e.message, activityId)

        self.appendFindBeastInfo(infoList, blackList)
        infoList.sort(cmp=self.cmpInfo)
        insertIndexs = []
        insertCnt = 0
        for index, info in enumerate(infoList):
            if info.has_key('subList'):
                insertIndexs.append((index + 1 + insertCnt, info['subList']))
                insertCnt += len(info['subList'])

        for index, subList in insertIndexs:
            for startIdx, info in enumerate(subList):
                infoList.insert(index + startIdx, info)

        return infoList

    def cmpInfo(self, infoA, infoB):
        if infoA['isActivityMode'] != infoB['isActivityMode']:
            if infoA['isActivityMode']:
                return -1
            return 1
        return cmp(infoA['sortOrder'], infoB['sortOrder'])

    def appendFindBeastInfo(self, infoList, blackList):
        info = {}
        info['activityType'] = gametypes.REWARD_RECOVER_ACTIVITY_TYPE_XUN_LING
        if gametypes.REWARD_RECOVER_ACTIVITY_TYPE_XUN_LING in blackList:
            return
        p = BigWorld.player()
        activityId = FIND_BEAST_ACTIVITY_ID
        info['activityId'] = activityId
        configData = RGD.data.get(activityId, {})
        if not configData:
            return
        lvLimit = configData.get('lv', (1, 99))
        if p.lv < lvLimit[0] or p.lv > lvLimit[1]:
            return
        chain = p.questLoopChain.getChain()
        getBackNum = self.calcGetBackFreeCnt(p, chain)
        sortOrder = configData.get('sortOrder', activityId)
        info['sortOrder'] = sortOrder
        if not getBackNum:
            return
        title = configData.get('ItemTitle', 'title(%d)')
        info['title'] = title % getBackNum
        info['itemList'] = []
        itemList = []
        itemList.append(uiUtils.getGfxItemById(EXP_ITEM_ID, 1))
        bonusIds = chain.calcHistoryBonusIds(p, self.recoveryType == RECOVERY_TYPE_PERFECT)
        itemDic = {}
        for bonusId in bonusIds:
            for itemId, cnt in clientUtils.genItemBonus(bonusId):
                itemDic[itemId] = itemDic.get(itemId, 0) + cnt

        itemList.extend([ uiUtils.getGfxItemById(key, value) for key, value in itemDic.iteritems() ])
        info['itemList'] = itemList
        info['iconList'] = []
        exp = chain.calcHistoryExp(p, self.recoveryType == RECOVERY_TYPE_PERFECT)
        info['iconList'].append(('exp', exp))
        if configData.get('isExpAddSprite', 0):
            info['iconList'].append(('yljingyan', exp * LSD.data.get('spriteExpCoef', 0)))
        info['isExpAddSprite'] = configData.get('isExpAddSprite', 0)
        info['exp'] = exp
        if not exp:
            return
        if self.canUseItemDiKou(activityId):
            self.isActivityMode = True
            info['isActivityMode'] = True
        else:
            info['isActivityMode'] = False
        info['costList'] = []
        originPrice = chain.calcGetBackCoin(p)
        if self.recoveryType == RECOVERY_TYPE_PERFECT:
            if not gameglobal.rds.configData.get('enableRewardRecoveryNew', False):
                info['costList'].append(('tianBi', chain.calcGetBackCoin(p)))
                info['nowPrice'] = originPrice
                info['originPrice'] = originPrice
            else:
                nowPrice = chain.calcGetBackCoin(p)
                if self.isActivityMode:
                    diKouItemId = RGD.data.get(activityId, {}).get('rewardGetBackConsumeItem', 0)
                    daiKouItemCount = p.inv.countItemInPages(diKouItemId, enableParentCheck=True)
                    if originPrice - daiKouItemCount < nowPrice:
                        info['costList'].append(('tianBi', max(0, originPrice - daiKouItemCount)))
                    else:
                        info['costList'].append(('tianBi', nowPrice))
                else:
                    info['costList'].append(('tianBi', nowPrice))
                info['originPrice'] = nowPrice
                info['nowPrice'] = nowPrice
        else:
            fameVal1 = chain.calcGetBackConsumeFame(p, COST_FMAE_TYPE_YUNCHUI)
            fameVal2 = chain.calcGetBackConsumeFame(p, COST_FAME_TYPE_DISHE)
            if not fameVal1 or not fameVal2:
                return
            info['costList'].append(('yunChui', fameVal1[0][1]))
            info['costList'].append(('gongJiDian', fameVal2[0][1]))
        infoList.append(info)

    def calcGetBackFreeCnt(self, owner, chain):
        nodeIds = questLoops.getQuestLoopChainNodeIds(chain.questLoopId, hasExp=True)
        freeCnt = 0
        for v in chain.getHistories(owner):
            for nodeId in nodeIds:
                if nodeId not in v.acNodeIds:
                    freeCnt += 1
                    break

        return min(freeCnt, chain.getHistoryDays())

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.scrollWndList.data = []
        self.widget.scrollWndList.validateNow()
        infoList = self.getInfoList()
        if not infoList:
            self.widget.noItemMc.visible = True
            self.widget.scrollWndList.visible = False
        else:
            self.widget.noItemMc.visible = False
            self.widget.scrollWndList.dataArray = infoList
            self.widget.scrollWndList.validateNow()
            self.widget.scrollWndList.visible = True
        if self.isActivityMode:
            self.widget.banner.loadImage('welfare/%s.dds' % SCD.data.get('rewardRecoveryActivityBannerName', 'test'))
        else:
            self.widget.banner.loadImage('welfare/%s.dds' % SCD.data.get('rewardRecoveryBannerName', ''))
        self.widget.normalRetrieveBtn.selected = self.recoveryType == RECOVERY_TYPE_NORMAL
        self.widget.perfectRetrieveBtn.selected = self.recoveryType == RECOVERY_TYPE_PERFECT

    def getRedFlagVisible(self):
        return len(self.getInfoList()) > 0

    def doChangeRetrieveType(self, retrieveType):
        if self.recoveryType != retrieveType:
            self.recoveryType = retrieveType
            self.refreshInfo()

    def handlePerfectRetrieveBtnClick(self, *args):
        self.doChangeRetrieveType(RECOVERY_TYPE_PERFECT)

    def handleNormalRetrieveBtnClick(self, *args):
        self.doChangeRetrieveType(RECOVERY_TYPE_NORMAL)

    def handleNewExpandBtnClick(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget.parent
        activityType = int(itemMc.itemData.activityType)
        oldPositon = self.widget.scrollWndList.scrollbar.position
        self.expandDic[activityType] = not self.expandDic.get(activityType, False)
        self.refreshInfo()
        self.widget.scrollWndList.validateNow()
        self.widget.scrollWndList.scrollbar.position = oldPositon

    def lableFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        if itemData.canExpand:
            itemMc.gotoAndStop('expand')
            itemMc.newExpandBtn.addEventListener(events.MOUSE_CLICK, self.handleNewExpandBtnClick, False, 0, True)
            itemMc.itemIcon.addEventListener(events.MOUSE_CLICK, self.handleNewExpandBtnClick, False, 0, True)
            activityType = int(itemData.activityType)
            if self.expandDic.get(activityType, False):
                itemMc.newExpandBtn.gotoAndStop('expanded')
                itemMc.newExpandBtn.txtExpand.text = gameStrings.WELFARE_REWARD_RECOVERY_EXPANDED
            else:
                itemMc.newExpandBtn.gotoAndStop('expand')
                itemMc.newExpandBtn.txtExpand.text = gameStrings.WELFARE_REWARD_RECOVERY_EXPAND
        else:
            itemMc.gotoAndStop('normal')
            itemMc.itemIcon.removeEventListener(events.MOUSE_CLICK, self.handleNewExpandBtnClick)
        itemMc.itemData = itemData
        itemMc.txtTitile.text = itemData.title
        itemList = itemData.itemList
        for i in xrange(REWARD_ITEM_MAX_CNT):
            itemSlot = itemMc.getChildByName('item%d' % i)
            if i >= len(itemList):
                itemSlot.visible = False
                continue
            itemSlot.visible = True
            itemSlot.dragable = False
            itemSlot.setItemSlotData(itemList[i])

        for i in xrange(REWARD_ICON_MAX_CNT):
            bonusIcon = itemMc.getChildByName('rewardIcon%d' % i)
            rewardTxt = itemMc.getChildByName('rewardTxt%d' % i)
            bonusIcon.visible = False
            rewardTxt.visible = False

        iconList = itemData.iconList
        index = 0
        for j in xrange(len(iconList)):
            if iconList[j][1] == 0:
                continue
            bonusIcon = itemMc.getChildByName('rewardIcon%d' % index)
            rewardTxt = itemMc.getChildByName('rewardTxt%d' % index)
            bonusIcon.visible = True
            rewardTxt.visible = True
            index = index + 1
            bonusIcon.bonusType = iconList[j][0]
            rewardTxt.text = str(int(iconList[j][1]))
            if iconList[j][0] == 'shenwang':
                TipManager.addTip(bonusIcon, FD.data.get(iconList[j][2], {}).get('name', ''))
            if iconList[j][0] == 'yljingyan':
                TipManager.addTip(bonusIcon, gameStrings.WELFARE_REWARD_RECOVERY_SPRITE_EXP)

        infoList = itemData.infoList
        leftPar = itemMc.leftPar
        rightPar = itemMc.rightPar
        timeLeft = itemMc.timeLeft
        if not infoList:
            leftPar.visible = False
            rightPar.visible = False
            timeLeft.visible = False
        else:
            for j in xrange(len(infoList)):
                if infoList[j][1] == 0:
                    continue
                bonusIcon = itemMc.getChildByName('rewardIcon%d' % index)
                rewardTxt = itemMc.getChildByName('rewardTxt%d' % index)
                bonusIcon.visible = True
                rewardTxt.visible = True
                index = index + 1
                bonusIcon.bonusType = infoList[j][0]
                rewardTxt.text = str(int(infoList[j][1]))
                tipText = SCD.data.get('bonusDict', {}).get(infoList[j][0], '')
                if tipText:
                    TipManager.addTip(bonusIcon, tipText)
                if j == 0:
                    leftPar.visible = True
                    leftPar.x = bonusIcon.x - PAR_X_LEFT_INTERNAL
                    leftPar.y = PAR_Y
                if j == len(infoList) - 1:
                    timeLeft.visible = True
                    timeLeft.x = rewardTxt.x + rewardTxt.textWidth + PAR_X_RIGHT_INTERNAL
                    timeLeft.y = LEFTTIME_Y
                    activityId = itemData.activityId
                    weekEndCron = '0 0 * * 0'
                    endTimes = RGD.data.get(activityId, {}).get('endTimes', None)
                    if not utils.inDateRange(weekEndCron, endTimes[0]):
                        remainSeconds = utils.getWeekSecond() + const.TIME_INTERVAL_WEEK - utils.getNow()
                        remainDays = int(remainSeconds / const.SECONDS_PER_DAY)
                        remainHours = int(remainSeconds % const.SECONDS_PER_DAY / const.SECONDS_PER_HOUR)
                        remainMins = int(remainSeconds % const.SECONDS_PER_HOUR / const.SECONDS_PER_MIN)
                        timeLeft.timeTf.text = gameStrings.WELFARE_REWARD_RECOVERY_LEFT_TIME % (remainDays, remainHours, remainMins)
                    else:
                        timeLeft.timeTf.text = gameStrings.WELFARE_REWARD_RECOVERY_EXPIRE
                    timeLeft.timeTf.width = timeLeft.timeTf.textWidth + 5
                    rightPar.visible = True
                    rightPar.x = timeLeft.x + timeLeft.timeTf.width
                    rightPar.y = PAR_Y

        costList = itemData.costList
        itemMc.costIcon0.bonusType = costList[0][0]
        itemMc.costTxt0.text = str(int(costList[0][1]))
        isActivityMode = itemData.isActivityMode
        itemMc.consumeItem.visible = bool(isActivityMode)
        if self.recoveryType == RECOVERY_TYPE_NORMAL and len(costList) >= 0:
            itemMc.desc.visible = True
            itemMc.costIcon1.visible = True
            itemMc.costTxt1.visible = True
            itemMc.costIcon1.bonusType = costList[1][0]
            itemMc.costTxt1.gotoAndStop('xianjia')
            itemMc.costTxt1.costTxt1.text = str(int(costList[1][1]))
        else:
            itemMc.desc.visible = False
            itemMc.costIcon1.visible = False
            itemMc.costTxt1.visible = False
            if gameglobal.rds.configData.get('enableRewardRecoveryNew', False):
                if itemData.isActivityMode:
                    itemMc.desc.visible = False
                    itemMc.costIcon1.visible = True
                    itemMc.costIcon1.bonusType = 'jiari'
                    itemMc.costTxt1.visible = True
                    itemMc.costTxt1.gotoAndStop('xianjia')
                    itemMc.costTxt1.costTxt1.text = itemData.originPrice
                elif itemData.originPrice == itemData.nowPrice:
                    itemMc.desc.visible = False
                    itemMc.costIcon1.visible = False
                    itemMc.costTxt1.visible = False
                else:
                    itemMc.desc.visible = True
                    itemMc.desc.text = gameStrings.WELFARE_REWARD_RECOVERY_ORIGIN_PRICE
                    itemMc.costIcon1.visible = False
                    itemMc.costTxt1.visible = True
                    itemMc.costTxt1.gotoAndStop('yuanjia')
                    itemMc.costTxt1.delFlag.width = len(str(int(itemData.originPrice))) * 7.5
                    itemMc.costTxt1.costTxt1.text = itemData.originPrice
        itemMc.gainRewrdBtn.label = gameStrings.WELFARE_REWARD_RETRIEVE_PERFECT if self.recoveryType == RECOVERY_TYPE_PERFECT else gameStrings.WELFARE_REWARD_RETRIEVE_NORMAL
        itemMc.gainRewrdBtn.addEventListener(events.BUTTON_CLICK, self.handleGainRewardBtnClick, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleIemOver, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleItemOut, False, 0, True)

    def handleIemOver(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.itemIcon.gotoAndStop('over')

    def handleItemOut(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.itemIcon.gotoAndStop('normal')

    def canUseItemDiKou(self, activityId, checkItemCnt = False):
        p = BigWorld.player()
        startTime = RGD.data.get(activityId, {}).get('consumeItemStartTime', None)
        endTime = RGD.data.get(activityId, {}).get('consumeItemEndTime', None)
        diKouItemId = RGD.data.get(activityId, {}).get('rewardGetBackConsumeItem', 0)
        if not startTime or not endTime:
            return False
        elif checkItemCnt and not p.inv.countItemInPages(diKouItemId, enableParentCheck=True):
            return False
        else:
            return utils.inTimeTuplesRange(startTime, endTime)

    def handleGainRewardBtnClick(self, *args):
        e = ASObject(args[3][0])
        itemData = e.currentTarget.parent.itemData
        if self.recoveryType != gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_COIN:
            if not self.uiAdapter.messageBox.checkOnceMap.get(uiConst.CHECK_ONCE_TYPE_REWARD_RECOVERY, False) and self.canUseItemDiKou(itemData['activityId'], True):
                msg = GMD.data.get(GMDD.data.REWARD_RECOVERY_DIKOU_CONFIRM, {}).get('text', '')
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.messageBoxYesCallback, noCallback=Functor(self.messageBoxNoCallback, itemData), isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_REWARD_RECOVERY)
            else:
                self.uiAdapter.rewardRecoveryNormal.show(itemData)
        elif self.canUseItemDiKou(itemData['activityId']):
            p = BigWorld.player()
            activityId = int(itemData['activityId'])
            configData = RGD.data.get(activityId, {})
            diKouItemId = configData.get('rewardGetBackConsumeItem', 0)
            itemCount = p.inv.countItemInPages(diKouItemId, enableParentCheck=True)
            (itemData['originPrice'], itemCount)
            if int(itemData['nowPrice']) <= int(itemData['originPrice'] - itemCount):
                msg = GMD.data.get(GMDD.data.REWARD_RECOVERY_CONFIRM, {}).get('text', '%d') % itemData['costList'][0][1]
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.yesCallback, itemData))
            else:
                self.uiAdapter.rewardRecoveryDiKou.show(itemData)
        else:
            msg = GMD.data.get(GMDD.data.REWARD_RECOVERY_CONFIRM, {}).get('text', '%d') % itemData['costList'][0][1]
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.yesCallback, itemData))

    def messageBoxYesCallback(self):
        self.widget.perfectRetrieveBtn.selected = True
        self.doChangeRetrieveType(RECOVERY_TYPE_PERFECT)

    def messageBoxNoCallback(self, itemData):
        self.uiAdapter.rewardRecoveryNormal.show(itemData)

    @ui.checkInventoryLock()
    def yesCallback(self, itemData):
        if itemData['activityType'] == gametypes.REWARD_RECOVER_ACTIVITY_TYPE_XUN_LING:
            fun = Functor(BigWorld.player().cell.getBackQuestLoopChainExp, gametypes.QUEST_LOOP_CHAIN_GET_BACK_EXP_TYPE_COIN)
            self.getBackActivityReward(fun, itemData)
        else:
            gamelog.info('jbx:getBackActivityRewardEx', int(itemData['activityId']), gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_COIN)
            fun = Functor(BigWorld.player().base.getBackActivityRewardEx, int(itemData['activityId']), gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_COIN)
            self.getBackActivityReward(fun, itemData)
        self.hide()

    def getBackActivityReward(self, func, itemData):
        p = BigWorld.player()
        if itemData['isExpAddSprite'] and not p.summonedSpriteInWorld and not self.uiAdapter.messageBox.checkOnceMap.get(uiConst.CHECK_ONCE_TYPE_REWARD_RECOVERY_SUMMON_SPRITE, False):
            gamelog.info('jbx:getBackActivityReward')
            text = GMD.data.get(GMDD.data.REWARD_RECOVERY_SUMMON_SPRITE_NOT_IN_WORLD, {}).get('text', '')
            self.uiAdapter.messageBox.showYesNoMsgBox(text, func, yesBtnText=gameStrings.WELFARE_REWARD_RECOVERY_GET_BACK, isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_REWARD_RECOVERY_SUMMON_SPRITE)
        else:
            func()

    def addPushIcon(self):
        if not gameglobal.rds.configData.get('enableRewardRecoveryClient', False):
            return
        if BigWorld.player().lv < SCD.data.get('welfareRewardRecoveryTabLv', 20):
            return
