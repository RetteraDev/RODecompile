#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildCallMemberProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import gametypes
from uiProxy import UIProxy
from callbackHelper import Functor
from data import guild_skill_data as GSD
from cdata import game_msg_def_data as GMDD

class GuildCallMemberProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildCallMemberProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm}
        self.mediator = None
        self.timer = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_CALL_MEMBER, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_CALL_MEMBER:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_CALL_MEMBER)

    def reset(self):
        self.stopTimer()

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def show(self):
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_CALL_MEMBER)

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            gametypes.GUILD_SKILL_GATHER = 3
            skillData = GSD.data.get(gametypes.GUILD_SKILL_GATHER, {})
            info = {}
            info['descField'] = skillData.get('desc', '')
            info['levelField'] = guild.level
            levelCD = skillData.get('cd', 0)
            if guild.level <= len(skillData.get('levelCD', ())):
                levelCD = skillData.get('levelCD')[guild.level - 1]
            info['coolDownField'] = uiUtils.formatTime(levelCD)
            canUse = False
            positionField = ''
            roleIds = skillData.get('roleId', ())
            for roleId in roleIds:
                if positionField != '':
                    positionField += gameStrings.TEXT_ACTIVITYFACTORY_280
                positionField += gametypes.GUILD_PRIVILEGES.get(roleId, {}).get('name', '')
                if p.guild.memberMe.roleId == roleId:
                    canUse = True

            info['positionField'] = positionField
            consumeItems = skillData.get('consumeItems')
            if consumeItems:
                itemId, needNum = consumeItems[0]
            else:
                itemId, needNum = (0, 0)
            itemInfo = uiUtils.getGfxItemById(itemId)
            itemInfo['itemName'] = uiUtils.getItemColorName(itemId)
            if p._isSoul():
                ownNum = p.crossInv.countItemInPages(itemId, enableParentCheck=True)
            else:
                ownNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
            itemInfo['itemNum'] = uiUtils.convertNumStr(ownNum, needNum, needThousand=True)
            if ownNum < needNum:
                canUse = False
            info['itemInfo'] = itemInfo
            info['canUse'] = canUse
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
            self.stopTimer()
            self.updateTime()

    def updateTime(self):
        if self.mediator:
            leftTime = self.getLeftTime()
            info = {}
            if leftTime <= 0:
                info['needShow'] = False
            else:
                info['needShow'] = True
                info['leftTime'] = gameStrings.TEXT_GUILDCALLMEMBERPROXY_109 % uiUtils.formatTime(leftTime)
            self.mediator.Invoke('updateTime', uiUtils.dict2GfxDict(info, True))
            if leftTime > 0:
                self.timer = BigWorld.callback(1, self.updateTime)

    def getLeftTime(self):
        p = BigWorld.player()
        if not p.guild:
            return 0
        skillInfo = p.guild.skills.get(gametypes.GUILD_SKILL_GATHER)
        if skillInfo and hasattr(skillInfo, 'nextTime'):
            return skillInfo.nextTime - int(p.getServerTime())
        return 0

    def onConfirm(self, *arg):
        p = BigWorld.player()
        leftTime = self.getLeftTime()
        if leftTime > 0:
            p.showGameMsg(GMDD.data.GUILD_SKILL_CD, (uiUtils.formatTime(leftTime),))
            return
        msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_GATHER_USE_HINT, '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.secondConfirm)

    def secondConfirm(self):
        BigWorld.player().cell.guildGather()
        self.hide()

    def showCallMemberPushMsg(self, fromGbId):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_GATHER)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_GATHER, {'click': Functor(self.showPushMsg, fromGbId)})

    def hideCallMemberPushMsg(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_GATHER)
        msgBoxId = getattr(self, 'msgBoxId', None)
        if msgBoxId:
            gameglobal.rds.ui.messageBox.dismiss(msgBoxId)

    def showPushMsg(self, fromGbId):
        p = BigWorld.player()
        if not p.guild:
            return
        else:
            memberInfo = p.guild.member.get(fromGbId, None)
            if not memberInfo:
                return
            nameText = '%s%s' % (gametypes.GUILD_PRIVILEGES.get(memberInfo.roleId, {}).get('name', ''), memberInfo.role)
            msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_GATHER_NOTIFY, '%s') % nameText
            self.msgBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, p.cell.acceptGuildGather, gameStrings.TEXT_IMPFRIEND_2211, p.cell.rejectGuildGather, gameStrings.TEXT_IMPFRIEND_963)
            return
