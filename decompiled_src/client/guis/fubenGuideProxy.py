#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fubenGuideProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import formula
import gametypes
import const
from uiProxy import UIProxy
from guis import uiUtils
from data import fb_data as FD
from data import sys_config_data as SCD
GUIDE_TIP = ['FB_GUIDE_CHECK_SUCC',
 'FB_GUIDE_LV_CHECK',
 'FB_GUIDE_TIMES_CHECK',
 'FB_GUIDE_MAC_CHECK',
 'FB_GUIDE_MEMBER_CHECK']

class FubenGuideProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FubenGuideProxy, self).__init__(uiAdapter)
        self.modelMap = {}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_FUBEN_GUIDE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FUBEN_GUIDE:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_GUIDE)

    def show(self):
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_GUIDE)

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            fbNo = formula.getFubenNo(p.spaceNo)
            info = {}
            p.guideDataCheck(fbNo)
            guideState, mode, memberList = p.fbGuideModeLoginInfo(fbNo)
            info['guideState'] = guideState
            info['mode'] = mode
            if guideState == gametypes.FB_GUIDE_SUC:
                info['hint'] = gameStrings.TEXT_FUBENGUIDEPROXY_51
                info['playerList'] = [ member['roleName'] for member in memberList ]
                guideMode = FD.data.get(fbNo, {}).get('guideMode', gametypes.FB_GUIDE_MODE_NOTHING)
                if guideMode != gametypes.FB_GUIDE_MODE_AVE_LV:
                    info['lv'] = ''
                else:
                    lv = p.fbAvgLv
                    info['lv'] = gameStrings.TEXT_FUBENGUIDEPROXY_59 % lv
                rate = self.getGuideRate(fbNo, len(memberList))
                info['rate'] = '' if rate == 0 else gameStrings.TEXT_FUBENGUIDEPROXY_61 % (rate * 100)
            else:
                info['hint'] = gameStrings.TEXT_FUBENGUIDEPROXY_63
                info['playerList'] = []
                info['lv'] = ''
                info['rate'] = ''
            guideTip = GUIDE_TIP[guideState]
            info['guideTip'] = SCD.data.get(guideTip, '')
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def getGuideRate(self, fbNo, rookieCnt):
        guideMode = FD.data.get(fbNo, {}).get('guideMode', 0)
        if guideMode == gametypes.FB_GUIDE_MODE_RANK_DIFF:
            return const.FB_GUIDE_HONOR_RATE_FOR_RANK_DIFF_MODE
        fubenGuideHonorRate = SCD.data.get('fubenGuideHonorRate')
        if fubenGuideHonorRate:
            for baseCnt, rate in fubenGuideHonorRate:
                if rookieCnt >= baseCnt:
                    return rate

        return 0
