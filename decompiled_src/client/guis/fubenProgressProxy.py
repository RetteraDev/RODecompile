#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fubenProgressProxy.o
from gamestrings import gameStrings
import BigWorld
import uiConst
import utils
from uiProxy import UIProxy
from guis import uiUtils
from callbackHelper import Functor
from data import fb_progress_boss_data as FPBD
from data import fb_data as FD
from data import sys_config_data as SCD

class FubenProgressProxy(UIProxy):
    FBUEN_CHECK_CD = 2.5

    def __init__(self, uiAdapter):
        super(FubenProgressProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickConfirm': self.onClickConfirm,
         'getInitData': self.onGetInitData,
         'clickCancel': self.onClickCancel}
        uiAdapter.registerEscFunc(uiConst.WIDGET_FUBEN_PROGRESS, self.hide)
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FUBEN_PROGRESS:
            self.mediator = mediator

    def show(self, fbNo, pg, fbVars):
        self.fbNo = fbNo
        self.pg = pg
        self.fbVars = fbVars
        if FPBD.data.get(self.fbNo, None):
            self.openTime = utils.getNow()
            self.uiAdapter.loadWidget(uiConst.WIDGET_FUBEN_PROGRESS)

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FUBEN_PROGRESS)

    def reset(self):
        self.mediator = None
        self.fbNo = 0
        self.pg = []
        self.fbVars = []
        self.openTime = 0

    def onClickConfirm(self, *arg):
        self.afterFbProgressCheck(self.fbNo, True)
        self.hide()

    def onClickCancel(self, *arg):
        self.afterFbProgressCheck(self.fbNo, False)
        self.hide()

    def onGetInitData(self, *arg):
        return uiUtils.dict2GfxDict(self.getProgressText(), True)

    def getProgressText(self):
        ret = {}
        leftHideBossStr = ''
        leftBossStr = ''
        leftHideBossNumber = 0
        data = FPBD.data.get(self.fbNo, None)
        if data:
            dataFbProgress = data.get('fbProgress')
            dataHideBoss = data.get('fbHideBoss')
            dataProgressVars = FD.data.get(self.fbNo).get('progressVars', {})
            progressVarsKeys = sorted(dataProgressVars.keys())
            index = 0
            if dataHideBoss and self.fbVars:
                for key in progressVarsKeys:
                    hideBoss = dataHideBoss.get(key, 0)
                    if hideBoss:
                        if index < len(self.fbVars) and self.fbVars[index]:
                            leftHideBossNumber += 1
                        else:
                            leftHideBossStr = leftHideBossStr + hideBoss + ','
                    index += 1

            dataFbProgressKeys = sorted(dataFbProgress.keys())
            progressBoss = sorted(list(set(self.pg) & set(dataFbProgressKeys)))
            endProgressBoss = progressBoss[-1] if progressBoss else 1
            leftBoss = []
            for i in dataFbProgressKeys:
                if i > endProgressBoss:
                    leftBoss.append(i)

            ret['killBossNumber'] = gameStrings.TEXT_FUBENPROGRESSPROXY_96 % (len(progressBoss) + leftHideBossNumber, len(dataFbProgressKeys) + (len(dataHideBoss.keys()) if dataHideBoss else 0))
            for i in leftBoss:
                leftBossStr = leftBossStr + dataFbProgress.get(i, '') + ','

            ret['progressBoss'] = leftBossStr + leftHideBossStr
            ret['fubenProgressDesc'] = SCD.data.get('fubenProgressDescText', '')
        return ret

    def afterFbProgressCheck(self, fbNo, fCover):
        p = BigWorld.player()
        deltaTime = self.FBUEN_CHECK_CD - (utils.getNow() - self.openTime)
        if fCover and deltaTime > 0:
            BigWorld.callback(deltaTime, Functor(p.afterFbProgressCheck, fbNo, fCover, self.pg, self.fbVars))
        else:
            p.afterFbProgressCheck(fbNo, fCover, self.pg, self.fbVars)
