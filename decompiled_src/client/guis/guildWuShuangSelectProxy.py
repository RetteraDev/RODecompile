#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildWuShuangSelectProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import uiConst
from uiProxy import UIProxy
from data import ws_daoheng_data as WDD
from cdata import game_msg_def_data as GMDD
from cdata import ws_skill_lvup_data as WSLD

class GuildWuShuangSelectProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildWuShuangSelectProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm}
        self.mediator = None
        self.tabIdx = 0
        self.idx = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_WUSHUANG_SELECT, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_WUSHUANG_SELECT:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_WUSHUANG_SELECT)

    def reset(self):
        self.tabIdx = 0
        self.idx = 0

    def show(self, tabIdx, idx):
        self.tabIdx = tabIdx
        self.idx = idx
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_WUSHUANG_SELECT)

    def refreshInfo(self):
        if self.mediator:
            info = {}
            if self.tabIdx == uiConst.GUILD_WUSHUANG_XINDE:
                info['nameTitle'] = gameStrings.TEXT_GUILDWUSHUANGSELECTPROXY_50
                info['showValueAmount'] = True
            elif self.tabIdx == uiConst.GUILD_WUSHUNAG_DAOHENG:
                info['nameTitle'] = gameStrings.TEXT_GUILDWUSHUANGSELECTPROXY_53
                info['showValueAmount'] = False
            else:
                return
            info['skillList'] = [gameglobal.rds.ui.skill._genSpecialSkillContent(0), gameglobal.rds.ui.skill._genSpecialSkillContent(1)]
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        skType = int(arg[3][0].GetNumber())
        idx = int(arg[3][1].GetNumber())
        skillId = gameglobal.rds.ui.skill.specialSkills[skType][idx]
        p = BigWorld.player()
        if self.tabIdx == uiConst.GUILD_WUSHUANG_XINDE:
            for wsVal in p.guildWSPractice:
                if wsVal and wsVal.skillId == skillId:
                    p.showGameMsg(GMDD.data.GUILD_WS_PRACTICE_IN_PRACTICE, ())
                    return

        elif self.tabIdx == uiConst.GUILD_WUSHUNAG_DAOHENG:
            for wsVal in p.guildWSDaoheng:
                if wsVal and wsVal.skillId == skillId:
                    p.showGameMsg(GMDD.data.GUILD_WS_DAOHENG_IN_DAOHENG, ())
                    return

        else:
            return
        skInfoVal = p.wsSkills.get(skillId, None)
        lv = skInfoVal.level if skInfoVal else 1
        if self.tabIdx == uiConst.GUILD_WUSHUANG_XINDE:
            if WSLD.data.get((skillId, lv), {}).get('maxXd', 0) == 0:
                p.showGameMsg(GMDD.data.GUILD_WS_PRACTICE_MAX_LEVEL, ())
                return
        elif self.tabIdx == uiConst.GUILD_WUSHUNAG_DAOHENG:
            slotNum = len(skInfoVal.slots) if skInfoVal.slots else 0
            if WDD.data.get((skillId, slotNum + 1), {}).get('addSlotDh', 0) == 0:
                p.showGameMsg(GMDD.data.WS_DAOHENG_FULL, ())
                return
            daoHengInfo = gameglobal.rds.ui.skill._genDirectionInfo(skillId)
            if daoHengInfo['daohang'][slotNum][0] == uiConst.DAOHENG_LOCK:
                p.showGameMsg(GMDD.data.GUILD_WS_DAOHENG_JINJIE_LIMIT, daoHengInfo['daohang'][slotNum][1])
                return
        else:
            return
        gameglobal.rds.ui.guildWuShuang.selectSkill(self.tabIdx, self.idx, skillId)
        self.hide()
