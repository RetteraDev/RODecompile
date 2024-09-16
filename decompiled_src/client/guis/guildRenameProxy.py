#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildRenameProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import uiUtils
import gametypes
import const
import utils
from uiProxy import UIProxy
from helpers import taboo
from ui import unicode2gbk
from data import guild_config_data as GCD
from cdata import game_msg_def_data as GMDD

class GuildRenameProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildRenameProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_RENAME, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_RENAME:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_RENAME)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def show(self):
        p = BigWorld.player()
        if not p.guildNUID:
            p.showGameMsg(GMDD.data.GUILD_NOT_JOINED, (const.YOU,))
            return
        if not p.guild.memberMe.roleId == gametypes.GUILD_ROLE_LEADER:
            BigWorld.player().showGameMsg(GMDD.data.GUILD_AUTHORIZATION_FAILED, ())
            return
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_RENAME)

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            if not p.guild:
                return
            info = {}
            if p.guild.options.get(gametypes.GUILD_OPTION_RENAME):
                consumeItems = None
            else:
                consumeItems = GCD.data.get('renameConsumeItems', None)
            if consumeItems:
                itemId, needNum = consumeItems[0]
                itemInfo = uiUtils.getGfxItemById(itemId)
                ownNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
                itemInfo['count'] = uiUtils.convertNumStr(ownNum, needNum)
                info['itemInfo'] = itemInfo
                if ownNum < needNum:
                    info['confirmEnable'] = False
                else:
                    info['confirmEnable'] = True
                info['isFree'] = False
            else:
                info['confirmEnable'] = True
                info['isFree'] = True
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
            if utils.isInternationalVersion():
                guildNameInput = self.mediator.Invoke('getWidget').GetMember('guildNameInput')
                guildNameInput.SetMember('maxChars', GfxValue(const.GUILD_NAME_MAX_LEN))

    def checkRenamePushMsg(self):
        guild = BigWorld.player().guild
        if guild and guild.options.get(gametypes.GUILD_OPTION_RENAME) and guild.memberMe.roleId == gametypes.GUILD_ROLE_LEADER:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_RENAME)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_RENAME, {'click': self.showPushMsg})
            return
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_RENAME)

    def showPushMsg(self):
        msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_FREE_RENAME_HINT, '')
        gameglobal.rds.ui.messageBox.showAlertBox(msg, isModal=False)
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_RENAME)

    def onConfirm(self, *arg):
        name = unicode2gbk(arg[3][0].GetString())
        p = BigWorld.player()
        result, _ = taboo.checkNameDisWord(name)
        if not result:
            p.showGameMsg(GMDD.data.GUILD_NAME_TABOO, ())
            return
        if p.guild.options.get(gametypes.GUILD_OPTION_RENAME):
            p.cell.renameGuild(name, True)
        else:
            p.cell.renameGuild(name, False)
        self.hide()
