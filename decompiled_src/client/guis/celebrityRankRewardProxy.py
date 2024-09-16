#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/celebrityRankRewardProxy.o
import BigWorld
import gameglobal
import const
import uiConst
import gametypes
import clientUtils
from uiProxy import UIProxy
from guis import uiUtils
from cdata import top_reward_data as TRD
from data import hall_of_fame_config_data as HOFCD
MAX_RANK_NUM = 7
MAX_SLOT_NUM = 7
RANK_MC_NAMES = [ 'rank%d' % n for n in xrange(MAX_RANK_NUM) ]
SLOT_MC_NAMES = [ 'slot%d' % n for n in xrange(MAX_SLOT_NUM) ]
LV_KEY_INDEX_MAP = {'1_69': 1,
 '70_79': 2}

class CelebrityRankRewardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CelebrityRankRewardProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CELEBRITY_REWARD, self.hide)

    def reset(self):
        self.rewardInfo = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CELEBRITY_REWARD:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CELEBRITY_REWARD)

    def show(self, topType, myRank, lvKey = '', school = 0):
        if not self.widget:
            self.rewardInfo = self.genRewardInfo(topType, myRank, lvKey, school)
            self.uiAdapter.loadWidget(uiConst.WIDGET_CELEBRITY_REWARD)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget or not self.rewardInfo:
            return
        myRank = self.rewardInfo.get('myRank', '')
        rewardList = self.rewardInfo.get('rewardList', [])
        self.widget.titleText.text = self.rewardInfo.get('mainTitle', '')
        self.widget.listTitleText.text = self.rewardInfo.get('subTitle', '')
        if myRank == 0:
            self.widget.voidRankMc.visible = True
            self.widget.myRankMc.visible = False
        else:
            self.widget.voidRankMc.visible = False
            self.widget.myRankMc.visible = True
            self.widget.myRankMc.rankText.text = myRank
        for rankIdx, name in enumerate(RANK_MC_NAMES):
            rankMc = getattr(self.widget, name)
            if not rankMc:
                return
            if rankIdx + 1 > len(rewardList):
                rankMc.visible = False
            else:
                data = rewardList[rankIdx]
                rankMc.visible = True
                rankDesc = data.get('desc', '')
                rankMc.rankText.text = rankDesc
                slotIdList = data.get('slotIdList', [])
                for slotIdx, slotName in enumerate(SLOT_MC_NAMES):
                    slotMc = getattr(rankMc, slotName)
                    if not slotMc:
                        return
                    if slotIdx + 1 > len(slotIdList):
                        slotMc.visible = False
                    else:
                        slotMc.visible = True
                        slotMc.slot.dragable = False
                        slotData = uiUtils.getGfxItemById(slotIdList[slotIdx][0])
                        slotMc.slot.setItemSlotData(slotData)

    def genRewardInfo(self, topType, myRank, lvKey = '', school = 0):
        lvIdx = LV_KEY_INDEX_MAP.get(lvKey, 0)
        topData = TRD.data.get((topType, lvIdx, school), {})
        if not topData:
            return
        rewardInfo = {}
        titleData = HOFCD.data.get('celebrityRankRewardTitle', {}).get(topType, {})
        rewardInfo['mainTitle'] = titleData.get('main', {})
        if topType in [gametypes.TOP_TYPE_HALL_OF_FAME_XIUWEI, gametypes.TOP_TYPE_HALL_OF_FAME_SHENBING]:
            rewardInfo['subTitle'] = titleData.get('sub', {}).get((lvKey, school), '')
        else:
            rewardInfo['subTitle'] = titleData.get('sub', '')
        rewardInfo['myRank'] = myRank if not gameglobal.rds.ui.celebrityRank.getCurrentBlockState() else '**'
        rewardInfo['rewardList'] = []
        for data in topData:
            info = {}
            bonusId = data.get('bonusId', 0)
            info['slotIdList'] = clientUtils.genItemBonus(bonusId)
            info['desc'] = data.get('desc', '')
            rewardInfo['rewardList'].append(info)

        return rewardInfo
