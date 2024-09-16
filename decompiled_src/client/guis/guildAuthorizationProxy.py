#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildAuthorizationProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import uiConst
import uiUtils
import utils
from ui import gbk2unicode
from uiProxy import UIProxy
ACTIONS = [gametypes.GUILD_ACTION_NEW_MEMBER,
 gametypes.GUILD_ACTION_KICKOUT_MEMBER,
 gametypes.GUILD_ACTION_APPOINT,
 gametypes.GUILD_ACTION_DISMISS,
 gametypes.GUILD_ACTION_UPDATE_FLAG,
 gametypes.GUILD_ACTION_ARMOR_COLOR,
 gametypes.GUILD_ACTION_UPDATE_PRIVILEGE,
 gametypes.GUILD_ACTION_DECLARE_WAR,
 gametypes.GUILD_ACTION_UPDATE_ANNOUNCEMENT,
 gametypes.GUILD_ACTION_BUILDING,
 gametypes.GUILD_ACTION_HIRE_RESIDENT,
 gametypes.GUILD_ACTION_STORAGE_MGR,
 gametypes.GUILD_ACTION_FACTORY,
 gametypes.GUILD_ACTION_SKILL_LEARN,
 gametypes.GUILD_ACTION_ACTIVITY_MGR,
 gametypes.GUILD_ACTION_RESEARCH,
 gametypes.GUILD_ACTION_STONE_SHIELD,
 gametypes.GUILD_ACTION_DESTROY_CLAN_WAR_BUILDING,
 gametypes.GUILD_ACTION_GUILD_CHALLENGE,
 gametypes.GUILD_ACTION_OPEN_ROBBER_TREASURE_BOX,
 gametypes.GUILD_ACTION_MASS_ASTROLOGY,
 gametypes.GUILD_ACTION_RED_PACKET,
 gametypes.GUILD_ACTION_CLAN_WAR_BUILDING_STONE,
 gametypes.GUILD_ACTION_CLAN_WAR_BUILDING_AIR_DEFENDER,
 gametypes.GUILD_ACTION_CLAN_WAR_BUILDING_GATE,
 gametypes.GUILD_ACTION_CLAN_WAR_BUILDING_RELIVE_BOARD,
 gametypes.GUILD_ACTION_APPLY_BUSINESS_MAN,
 gametypes.GUILD_ACTION_FETCH_FROM_STORAGE]

class GuildAuthorizationProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildAuthorizationProxy, self).__init__(uiAdapter)
        self.modelMap = {'getGameCfg': self.onGetGameCfg,
         'confirm': self.onConfirm,
         'initData': self.onInitData,
         'getPrivileges': self.onGetPrivileges,
         'setPrivileges': self.onSetPrivileges,
         'getMyRoleId': self.onGetMyRoleId,
         'getRoleIdPriority': self.onGetRoleIdProprity,
         'isGuildLeader': self.onIsGuildLeader}
        self.mediator = None
        self.rolePrivileges = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_AUTHORIZATION, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_AUTHORIZATION:
            self.mediator = mediator

    def show(self):
        p = BigWorld.player()
        if not p.guildNUID:
            return
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_AUTHORIZATION)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_AUTHORIZATION)

    def reset(self):
        self.rolePrivileges = {}

    def onGetGameCfg(self, *arg):
        info = {'enableGuildRobber': gameglobal.rds.configData.get('enableGuildRobber', False),
         'enableGuildMassAstrology': gameglobal.rds.configData.get('enableGuildMassAstrology', False),
         'enableGuildRedPacket': gameglobal.rds.configData.get('enableGuildRedPacket', False)}
        return uiUtils.dict2GfxDict(info, True)

    def onConfirm(self, *arg):
        rolePrivileges = []
        for roleId in self.rolePrivileges:
            if utils.getGuildRoleIdPriority(roleId) <= utils.getGuildRoleIdPriority(BigWorld.player().guild.memberMe.roleId) or BigWorld.player().guild.memberMe.roleId == gametypes.GUILD_ROLE_LEADER:
                rolePrivileges.append({'roleId': roleId,
                 'privileges': self.rolePrivileges[roleId]})

        BigWorld.player().cell.updateGuildPrivileges(rolePrivileges)
        self.hide()

    def onGetMyRoleId(self, *arg):
        return GfxValue(BigWorld.player().guild.memberMe.roleId)

    def onGetRoleIdProprity(self, *args):
        roleId = int(args[3][0].GetNumber())
        return GfxValue(utils.getGuildRoleIdPriority(roleId))

    def onIsGuildLeader(self, *args):
        roleId = int(args[3][0].GetNumber())
        return GfxValue(roleId in gametypes.GUILD_ROLE_LEADERS_EX)

    def onInitData(self, *arg):
        dataList = []
        enableWingWorldGuildRoleOptimization = gameglobal.rds.configData.get('enableWingWorldGuildRoleOptimization', False)
        for id, roleId in enumerate(gametypes.GUILD_ROLE_LIST):
            if roleId in gametypes.GUILD_ROLE_IN_WING_WORLD and not enableWingWorldGuildRoleOptimization:
                continue
            if roleId == gametypes.GUILD_ROLE_LADY and not gameglobal.rds.configData.get('enableGuildLady', False):
                continue
            dataList.append({'label': gametypes.GUILD_ROLE_DICT.get(roleId, ''),
             'id': roleId})

        dataList.sort(cmp=self.cmpRoleId)
        return uiUtils.array2GfxAarry(dataList, True)

    def cmpRoleId(self, a, b):
        roleIdA = a['id']
        roleIdB = b['id']
        return cmp(gametypes.GUILD_PRIVILEGES[roleIdA]['sortv'], gametypes.GUILD_PRIVILEGES[roleIdB]['sortv'])

    def onGetPrivileges(self, *arg):
        return self.getPrivileges(int(arg[3][0].GetNumber()))

    def onSetPrivileges(self, *arg):
        roleId = int(arg[3][0].GetNumber())
        if BigWorld.player().guild.memberMe.roleId != gametypes.GUILD_ROLE_LEADER and utils.getGuildRoleIdPriority(roleId) >= utils.getGuildRoleIdPriority(BigWorld.player().guild.memberMe.roleId):
            return
        arLen = int(arg[3][1].GetNumber())
        ar = arg[3][2]
        privilegesList = []
        for id in range(0, arLen):
            privilegesList.append(ACTIONS[int(ar.GetElement(id).GetNumber())])

        self.rolePrivileges[roleId] = privilegesList

    def getPrivileges(self, roleId):
        p = BigWorld.player()
        privilegesList = []
        for action in ACTIONS:
            if roleId in self.rolePrivileges:
                if action in self.rolePrivileges[roleId]:
                    privilegesList.append(True)
                    continue
            else:
                privileges = p.guild.privileges.get(roleId)
                if privileges and action in privileges:
                    privilegesList.append(True)
                    continue
            privilegesList.append(gameglobal.rds.ui.guild._hasPrivilege(roleId, action))

        privilegesList.append(roleId not in [gametypes.GUILD_ROLE_ELITE, gametypes.GUILD_ROLE_NORMAL])
        return uiUtils.array2GfxAarry(privilegesList, True)

    def updateRoleID(self):
        p = BigWorld.player()
        if p.guild.memberMe.roleId not in (gametypes.GUILD_ROLE_LEADER,
         gametypes.GUILD_ROLE_VICE_LEADER,
         gametypes.GUILD_ROLE_EXECUTOR,
         gametypes.GUILD_ROLE_LADY):
            self.hide()
