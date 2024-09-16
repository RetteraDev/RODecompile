#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fbDeadDataProxy.o
from gamestrings import gameStrings
import math
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import formula
import clientcom
from gamescript import FormularEvalEnv
from ui import gbk2unicode
from uiProxy import SlotDataProxy
from guis import uiConst
from gameclass import SkillInfo
from guis import uiUtils
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import fb_data as FD
from data import sys_config_data as SCD
DEFAULT_AVG_EQUIP = 2000

class FbDeadDataProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(FbDeadDataProxy, self).__init__(uiAdapter)
        self.binding = {}
        self.bindType = 'fbDeadData'
        self.type = 'fbDeadData'
        self.modelMap = {'getStronger': self.onGetStronger,
         'initData': self.onInitData,
         'openDetail': self.onOpenDetail,
         'gotoLearnVideo': self.onGotoLearnVideo,
         'getKeyDetail': self.onGetKeyDetail,
         'getUiConfig': self.onGetUiConfig}
        self.mediator = None
        self.totalReduceHp = 0
        self.totalAddHp = 0
        self.lastHit = None
        self.maxReduceResult = None
        self.msgList = None
        self.teamEquipEva = 0
        self.onLineMembers = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_FB_DEAD_DATA, self.hide)

    def show(self, teamEquipEva):
        p = BigWorld.player()
        if not p.inFubenTypes(const.FB_TYPE_ALL_FB):
            return
        self.onLineMembers = 0
        for key in p.members:
            if p.members[key].get('isOn', ''):
                self.onLineMembers += 1

        if self.onLineMembers == 0:
            self.onLineMembers = 1
        self.teamEquipEva = teamEquipEva / self.onLineMembers
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FB_DEAD_DATA)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FB_DEAD_DATA:
            self.mediator = mediator

    def getMsg(self, msg):
        self.totalReduceHp = msg[0]
        self.totalAddHp = msg[1]
        self.lastHit = msg[2]
        self.maxReduceResult = msg[3]
        self.msgList = msg[4]

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        if self.mediator:
            self.mediator = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FB_DEAD_DATA)

    def reset(self):
        super(self.__class__, self).reset()
        self.mediator = None
        self.totalReduceHp = 0
        self.totalAddHp = 0
        self.lastHit = None
        self.maxReduceResult = None
        self.msgList = None
        self.teamEquipEva = 0
        self.onLineMembers = 0

    def onGotoLearnVideo(self, *arg):
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        link = FD.data[fbNo].get('keyLink', '')
        clientcom.openFeedbackUrl(link)

    def onGetStronger(self, *arg):
        gameglobal.rds.ui.playRecomm.show(tabIdx=uiConst.PLAY_RECOMMV2_TAB_STRONGER_IDX)
        if gameglobal.rds.ui.fbDeadDetailData.mediator:
            gameglobal.rds.ui.fbDeadDetailData.hide()

    def onOpenDetail(self, *arg):
        if not gameglobal.rds.ui.fbDeadDetailData.mediator:
            gameglobal.rds.ui.fbDeadDetailData.show(self.msgList, self.totalReduceHp, self.totalAddHp)
        else:
            gameglobal.rds.ui.fbDeadDetailData.hide()

    def onGetKeyDetail(self, *arg):
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        ret = {}
        ret['show'] = FD.data.get(fbNo, {}).get('showKey', 0)
        ret['name'] = FD.data.get(fbNo, {}).get('keyName', '')
        return uiUtils.dict2GfxDict(ret, True)

    def onInitData(self, *arg):
        p = BigWorld.player()
        DEAD_HARM_TREAT = gameStrings.TEXT_FBDEADDATAPROXY_121
        DEAD_MOSTER_SKILL = gameStrings.TEXT_FBDEADDATAPROXY_122
        DEAD_HARM_PRECENT = gameStrings.TEXT_FBDEADDATAPROXY_123
        obj = self.movie.CreateObject()
        harmAndTreat = DEAD_HARM_TREAT % ('#d9482b',
         self.totalReduceHp,
         '#48d92b',
         self.totalAddHp)
        obj.SetMember('harmAndTreat', GfxValue(gbk2unicode(harmAndTreat)))
        if self.lastHit is not None:
            lastHarmSkill = DEAD_MOSTER_SKILL % (self.lastHit[1][0], '#d9482b', self.lastHit[4])
            obj.SetMember('lastHarmSkill', GfxValue(gbk2unicode(lastHarmSkill)))
            lastHarmPrecent = DEAD_HARM_PRECENT % ('#d9482b', self.lastHit[5], float(self.lastHit[5] * 100.0 / self.totalReduceHp))
            obj.SetMember('lastHarmPrecent', GfxValue(gbk2unicode(lastHarmPrecent)))
            mainHarmSkill = DEAD_MOSTER_SKILL % (self.maxReduceResult[1][0], '#d9482b', self.maxReduceResult[4])
            obj.SetMember('mainHarmSkill', GfxValue(gbk2unicode(mainHarmSkill)))
            mainHarmPrecent = DEAD_HARM_PRECENT % ('#d9482b', self.maxReduceResult[5], float(self.maxReduceResult[5] * 100.0 / self.totalReduceHp))
            obj.SetMember('mainHarmPrecent', GfxValue(gbk2unicode(mainHarmPrecent)))
            obj.SetMember('lastAdvise', GfxValue(gbk2unicode(self.getAdvise(self.lastHit))))
            obj.SetMember('mainAdvise', GfxValue(gbk2unicode(self.getAdvise(self.maxReduceResult))))
            p = BigWorld.player()
            avgEquipEva = DEFAULT_AVG_EQUIP
            isShowRecommEquipTexts = True
            if p.inFubenTypes(const.FB_TYPE_ALL_FB):
                fbNo = formula.getFubenNo(p.spaceNo)
                func = FD.data[fbNo].get('recommendScore', '')
                if func:
                    avgEquipEva = FormularEvalEnv.evaluate(str(func), {'lv': p.lv})
                else:
                    isShowRecommEquipTexts = False
            myEquipEva = p.combatScoreList[const.COMBAT_SCORE]
            obj.SetMember('recommendEquipEva', GfxValue(avgEquipEva))
            obj.SetMember('teamEquipEva', GfxValue(self.teamEquipEva))
            obj.SetMember('myEquipEva', GfxValue(myEquipEva))
            obj.SetMember('isShowRecommendEquipTexts', GfxValue(isShowRecommEquipTexts))
            if math.fabs(myEquipEva - avgEquipEva) < 200:
                obj.SetMember('status', GfxValue(1))
            elif myEquipEva < avgEquipEva:
                obj.SetMember('status', GfxValue(0))
            elif myEquipEva > avgEquipEva:
                obj.SetMember('status', GfxValue(2))
            self.mediator.Invoke('initData', obj)
            self.mediator.Invoke('setEquipEva', (GfxValue(0), GfxValue(self.teamEquipEva), GfxValue(avgEquipEva)))
            self.mediator.Invoke('setEquipEva', (GfxValue(1), GfxValue(myEquipEva), GfxValue(avgEquipEva)))

    def getAdvise(self, skillResult):
        if skillResult[13] == 0:
            skillID = skillResult[9]
            skillLv = skillResult[10]
            if skillID > 0:
                skillInfo = SkillInfo(skillID, skillLv)
                skillStrategy = skillInfo.getSkillData('skillStrategy', '')
                if skillStrategy:
                    return GMD.data[GMDD.data.COMBAT_MSG_SKILL_STRATEGY].get('text', '') % skillStrategy
                else:
                    return GMD.data[GMDD.data.COMBAT_MSG_SKILL_NO_STRATEGY].get('text', '')
            else:
                return GMD.data[GMDD.data.COMBAT_MSG_SKILL_NO_STRATEGY].get('text', '')
        else:
            return GMD.data[GMDD.data.COMBAT_MSG_SKILL_RECAST_STRATEGY].get('text', '')

    def onGetUiConfig(self, *args):
        p = BigWorld.player()
        return GfxValue(p.lv >= SCD.data.get('getStrongerVisibleLv', 30))
