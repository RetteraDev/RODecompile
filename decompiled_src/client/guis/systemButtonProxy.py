#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/systemButtonProxy.o
import BigWorld
from Scaleform import GfxValue
import gamelog
import gametypes
import const
import gameglobal
import utils
import copy
import gameconfigCommon
import hotkey as HK
from guis import events
from guis import ui
from uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from callbackHelper import Functor
from asObject import ASObject
from sfx import keyboardEffect
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from data import apprentice_new_config_data as ANCD
from data import wing_world_config_data as WWCD
from data import guild_config_data as GCD

class SystemButtonProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SystemButtonProxy, self).__init__(uiAdapter)
        self.bindType = 'systemButton'
        self.modelMap = {'click': self.onClick,
         'clickFriendBtn': self.onClickFriendBtn,
         'getShortcuts': self.onGetShortcuts,
         'isActionMode': self.onIsActionMode,
         'getFriendMsgList': self.onGetFriendMsgList,
         'showCursorKey': self.onShowCursorKey,
         'inAim': self.onInAim,
         'checkMenuEnabeld': self.onCheckMenuEnabeld,
         'getDaShanNum': self.onGetDaShanNum,
         'getButtonShow': self.onGetButtonShow,
         'checkNpcFavor': self.onCheckNpcFavor}
        self.mediator = None
        self.friendFlowBackType = 0
        self.showTipCallBackHandler = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SYS_BUTTON:
            self.mediator = mediator
            p = BigWorld.player()
            p._checkBlink()
            numDict = {}
            numDict['inventory'] = gameglobal.rds.ui.inventory.tempBagNum + gameglobal.rds.ui.inventory.tempMallBagNum
            if self.checkNeedShowFightSkill():
                numDict['fightSkill'] = utils.getCurSkillPoint(p.lv) - p.skillPoint
            else:
                numDict['fightSkill'] = 0
            numDict['userBack'] = int(p.flowbackBonus.isValid())
            roleInfoNotifyNum = 0
            has = gameglobal.rds.ui.roleInformationHierogram.isHasAvailablePos()
            if has:
                roleInfoNotifyNum += 1
            numDict['roleInfo'] = roleInfoNotifyNum
            self.refreshSysBtn()
            partnerNum = self.getPartnerNotifyNum()
            numDict['partner'] = partnerNum
            return uiUtils.dict2GfxDict({'numDict': numDict})

    def clearWidget(self):
        self.mediator = None
        self.friendFlowBackType = 0

    def checkNeedShowFightSkill(self):
        p = BigWorld.player()
        minLv = SCD.data.get('minShowFightSkill', 40)
        if p.lv < minLv:
            return False
        return True

    def onGetDaShanNum(self, *args):
        return GfxValue(len(gameglobal.rds.ui.daShan.data))

    def onGetShortcuts(self, *arg):
        hotKey = int(arg[3][0].GetNumber())
        try:
            detial = HK.HKM[hotKey]
            if detial.key != 0:
                return GfxValue(detial.getBrief())
        except:
            return GfxValue('')

        return GfxValue('')

    def onClick(self, *arg):
        buttonName = arg[3][0].GetString()
        if BigWorld.player() and getattr(BigWorld.player(), 'crossServerFlag', None) == const.CROSS_SERVER_STATE_IN:
            if buttonName == 'guild' and not BigWorld.player().inWingCity():
                BigWorld.player().showGameMsg(GMDD.data.WIDGET_IN_BLACK_LIST, ())
                return
            if buttonName in ('achiv', 'userBack'):
                BigWorld.player().showGameMsg(GMDD.data.WIDGET_IN_BLACK_LIST, ())
                return
        if buttonName.endswith('roleInfo'):
            if gameglobal.rds.ui.roleInfo.isShow:
                gameglobal.rds.ui.roleInfo.hide()
            else:
                gameglobal.rds.ui.roleInfo.show()
        elif buttonName.endswith('qinggong'):
            gameglobal.rds.ui.wingAndMount.toggle()
        elif buttonName.endswith('personalZone'):
            p = BigWorld.player()
            p.getPersonalSysProxy().openZoneMyself(const.PERSONAL_ZONE_SRC_SYSTEM)
        elif buttonName.endswith('equipChange'):
            gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_ENHANCE, 0)
        elif buttonName.endswith('equipSoul'):
            gameglobal.rds.ui.equipSoul.show(False)
        elif buttonName.endswith('manualEquip'):
            gameglobal.rds.ui.manualEquip.show(0)
        elif buttonName.endswith('summonedSprite'):
            gameglobal.rds.ui.summonedWarSprite.show(uiConst.WAR_SPRITE_TAB_INDEX0)
        elif buttonName.endswith('inventory'):
            if BigWorld.player()._isSoul() and gameglobal.rds.configData.get('enableCrossServerBag', False):
                if gameglobal.rds.ui.crossServerBag.isShow():
                    gameglobal.rds.ui.crossServerBag.hide()
                else:
                    gameglobal.rds.ui.crossServerBag.show()
            elif gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
            else:
                gameglobal.rds.ui.inventory.show()
        elif buttonName.endswith('consign'):
            openLv = SCD.data.get('openConsignLv', 20)
            if BigWorld.player().lv < openLv:
                BigWorld.player().showGameMsg(GMDD.data.FORBIDDEN_OPEN_CONSIGN, ())
                return
            if gameglobal.rds.ui.consign.mediator or gameglobal.rds.ui.tabAuction.mediator:
                BigWorld.player().closeAuctionFun()
            else:
                BigWorld.player().openAuctionFun()
        if buttonName.endswith('booth'):
            gameglobal.rds.ui.skill.enterBooth()
        elif buttonName.endswith('fightSkill'):
            if gameglobal.rds.ui.skill.isShow:
                gameglobal.rds.ui.skill.hide()
            else:
                gameglobal.rds.ui.skill.show()
        elif buttonName.endswith('generalSkill'):
            if gameglobal.rds.ui.skill.generalMediator:
                gameglobal.rds.ui.skill.closeGeneralSkill()
            else:
                gameglobal.rds.ui.skill.showGeneralSkill()
        elif buttonName.endswith('emoteAction'):
            if gameglobal.rds.ui.emoteAction.widget:
                gameglobal.rds.ui.emoteAction.clearWidget()
            else:
                gameglobal.rds.ui.emoteAction.show()
        elif buttonName.endswith('lifeSkill'):
            gameglobal.rds.ui.lifeSkillNew.toggle()
        elif buttonName.endswith('pvpEnhance'):
            if gameglobal.rds.ui.pvpEnhance.mediator:
                gameglobal.rds.ui.pvpEnhance.hide()
            else:
                gameglobal.rds.ui.pvpEnhance.checkShow()
        elif buttonName.endswith('team'):
            BigWorld.player().showTeamInfo(True)
        elif buttonName.endswith('showMessageBoard'):
            pass
        elif buttonName.endswith('guild'):
            if BigWorld.player().guild:
                if gameglobal.rds.ui.guild.mediator:
                    gameglobal.rds.ui.guild.hide()
                elif BigWorld.player().guild:
                    gameglobal.rds.ui.guild.show()
            else:
                gameglobal.rds.ui.guildQuickJoin.show()
        elif buttonName.endswith('questLog'):
            if gameglobal.rds.ui.questLog.isShow:
                gameglobal.rds.ui.questLog.hide()
            else:
                gameglobal.rds.ui.questLog.showTaskLog()
        elif buttonName.endswith('delegation'):
            if gameglobal.rds.ui.delegationBook.med:
                gameglobal.rds.ui.delegationBook.hide()
            else:
                gameglobal.rds.ui.delegationBook.show()
        elif buttonName.endswith('rolecard'):
            gameglobal.rds.ui.rolecard.show()
        elif buttonName.endswith('fengWuZhi'):
            gameglobal.rds.ui.fengWuZhi.show()
        elif buttonName.endswith('friend'):
            friendListLen = len(gameglobal.rds.ui.friendFlowBack.friendList)
            p = BigWorld.player()
            if friendListLen != 0:
                gameglobal.rds.ui.friendFlowBack.show()
            if p.friend.tempMsgs:
                newMsgs = copy.deepcopy(p.friend.tempMsgs)
                for _gbId, type, _, _ in newMsgs:
                    if type == gametypes.FRIEND_MSG_TYPE_CHAT:
                        if gameglobal.rds.ui.groupChat.checkChatedId(_gbId):
                            continue
                        else:
                            p.handleFriendMsg(0, 0)
                    else:
                        p.handleFriendMsg(0, 0)

            if p.groupUnreadMsgs:
                p.handleGroupUnreadMsgs()
            if gameglobal.rds.ui.friend.isShow:
                gameglobal.rds.ui.friend.hide(False)
            else:
                gameglobal.rds.ui.friend.show()
        elif buttonName.endswith('mentor'):
            if self.uiAdapter.mentorEx.mediator:
                self.uiAdapter.mentorEx.hideMentor()
            else:
                self.uiAdapter.mentorEx.show()
        elif buttonName.endswith('jieqi'):
            if gameconfigCommon.enableJieQiV2():
                if self.uiAdapter.jieQiV2.widget:
                    self.uiAdapter.jieQiV2.hide()
                else:
                    self.uiAdapter.jieQiV2.show()
            elif self.uiAdapter.jieQi.mediator:
                self.uiAdapter.jieQi.hide()
            else:
                self.uiAdapter.jieQi.show()
        elif buttonName.endswith('chatRoom'):
            if BigWorld.player().chatRoomNUID:
                BigWorld.player().showGameMsg(GMDD.data.CHATROOM_JOINED, ())
            else:
                gameglobal.rds.ui.chatRoomCreate.show(uiConst.CHATROOM_CREATE)
        elif buttonName.endswith('camera'):
            if not gameglobal.rds.configData.get('enableNewCamera', False):
                gameglobal.rds.ui.camera.show()
            else:
                gameglobal.rds.ui.cameraV2.show()
        elif buttonName.endswith('dashan'):
            self.uiAdapter.daShan.show()
        elif buttonName.endswith('showAll'):
            BigWorld.player().handleAcceptFriendMsg()
            if len(gameglobal.rds.ui.friendFlowBack.friendList) != 0:
                gameglobal.rds.ui.friendFlowBack.show()
        elif buttonName.endswith('ignoreAll'):
            BigWorld.player().handleIgnoreFriendMsg()
            if len(gameglobal.rds.ui.friendFlowBack.friendList) != 0:
                gameglobal.rds.ui.friendFlowBack.clearData()
        elif buttonName.endswith('friendRequest'):
            BigWorld.player().handleFriendMsg(0, 0)
        elif buttonName.endswith('pvp'):
            gameglobal.rds.ui.pvPPanel.show(2)
        elif buttonName.endswith('pvpjjc'):
            gameglobal.rds.ui.pvPPanel.show(1)
        elif buttonName.endswith('worldWar'):
            self.uiAdapter.worldWar.show()
        elif buttonName.endswith('achiv'):
            if gameglobal.rds.ui.achvment.widget:
                gameglobal.rds.ui.achvment.hide()
            else:
                gameglobal.rds.ui.achvment.getAchieveData()
        elif buttonName.endswith('rank'):
            if gameglobal.rds.ui.ranking.mediator:
                gameglobal.rds.ui.ranking.hide()
            else:
                gameglobal.rds.ui.ranking.show()
        elif buttonName.endswith('guibao'):
            if gameglobal.rds.ui.guibaoge.mediator:
                gameglobal.rds.ui.guibaoge.hide()
            else:
                gameglobal.rds.ui.guibaoge.show()
        elif buttonName.endswith('active'):
            pass
        elif buttonName.endswith('summonFriend'):
            if gameglobal.rds.ui.summonFriend.mediator or gameglobal.rds.ui.summonFriendNew.widget or gameglobal.rds.ui.summonFriendBGV2.widget:
                gameglobal.rds.ui.summonFriend.hide()
                gameglobal.rds.ui.summonFriendNew.hide()
                gameglobal.rds.ui.summonFriendBGV2.hide()
            elif gameglobal.rds.configData.get('enableInvitePoint', False):
                if gameglobal.rds.configData.get('enableSummonFriendV2', False):
                    gameglobal.rds.ui.summonFriendBGV2.show(uiConst.SUMMON_FRIEND_TAB_INDEX1, 'inviteBtn')
                else:
                    gameglobal.rds.ui.summonFriendNew.show(2)
            else:
                gameglobal.rds.ui.summonFriend.show(0)
        elif buttonName.endswith('userBack'):
            if gameglobal.rds.ui.backflow.widget:
                gameglobal.rds.ui.backflow.hide()
            else:
                gameglobal.rds.ui.backflow.show()
        elif buttonName.endswith('config'):
            if gameglobal.rds.ui.systemSettingV2.isShow():
                gameglobal.rds.ui.systemSettingV2.hide()
            else:
                gameglobal.rds.ui.systemSettingV2.show()
        elif buttonName.endswith('mail'):
            if gameglobal.rds.ui.mail.mediator:
                gameglobal.rds.ui.mail.hide()
            else:
                gameglobal.rds.ui.mail.show()
        elif buttonName.endswith('fashionbag'):
            if gameglobal.rds.ui.fashionBag.mediator:
                gameglobal.rds.ui.fashionBag.hide()
            else:
                gameglobal.rds.ui.fashionBag.askForShow()
        elif buttonName.startswith('flowBackFriend'):
            gameglobal.rds.ui.friendFlowBack.show()
        elif buttonName.endswith('jinenghong'):
            if not gameglobal.rds.configData.get('enableSkillMacro', False) and BigWorld.isPublishedVersion():
                return
            gameglobal.rds.ui.skillMacroOverview.showOverviewPanel()
        elif buttonName.endswith('partner'):
            gameglobal.rds.ui.partnerMain.show()
        elif buttonName.endswith('teamHall'):
            gameglobal.rds.ui.team.changeTeamHallVisible()
        elif buttonName.endswith('dota'):
            gameglobal.rds.ui.bfDotaHeros.show()
        elif buttonName == 'cardSystem':
            if gameglobal.rds.ui.cardSystem.widget is None:
                gameglobal.rds.ui.cardSystem.show()
        elif buttonName == 'wingWorld':
            gameglobal.rds.ui.wingWorld.show()
        elif buttonName == 'wardrobe':
            BigWorld.player().openWardrobe()
        elif buttonName == 'assassination':
            gameglobal.rds.ui.assassinationMain.show()
        elif buttonName == 'npcFavor' and gameconfigCommon.enableNpcFavor() and BigWorld.player().checkNpcFrindLv():
            self.uiAdapter.npcRelationship.show(uiConst.NPC_RELATIONSHIP_TAB_OVERVIEW, fromNpc=False)

    def onClickFriendBtn(self, *arg):
        try:
            idx = int(arg[3][0].GetNumber())
            id = int(arg[3][1].GetString())
            BigWorld.player().handleFriendMsg(idx, id)
        except:
            import traceback
            gamelog.error('jbx:onClickFriendBtn', traceback.print_exc())

    def showIndicator(self):
        if self.mediator != None:
            self.mediator.Invoke('showIndicator')

    def showFriendShine(self, show):
        if self.mediator != None:
            self.mediator.Invoke('showFriendShine', GfxValue(show))
        if show:
            friendMsgTipsTime = SCD.data.get('friendMsgTipsTime', 10)
            if self.showTipCallBackHandler == None:
                self.showTipCallBackHandler = BigWorld.callback(friendMsgTipsTime, Functor(self.showFriendTipsShine, show))
            keyboardEffect.addKeyboardEffect('effect_friendMsg')
        else:
            if self.showTipCallBackHandler:
                BigWorld.cancelCallback(self.showTipCallBackHandler)
                self.showTipCallBackHandler = None
            self.showFriendTipsShine(show)
            keyboardEffect.removeKeyboardEffect('effect_friendMsg')
        gameglobal.rds.ui.extendChatBox.showFriendTip(show)

    def showFriendTipsShine(self, show):
        if self.mediator != None:
            self.mediator.Invoke('showFriendMsgTips', GfxValue(show))

    def onIsActionMode(self, *arg):
        return GfxValue(BigWorld.player().getOperationMode() == gameglobal.ACTION_MODE)

    def onShowCursorKey(self, *arg):
        operation = getattr(BigWorld.player(), 'operation', {})
        return GfxValue(operation.get(gameglobal.ACTION_PLUS, {}).get(gameglobal.PLUS_SHOW_CURSOR_KEY, 0))

    def onInAim(self, *arg):
        aim = not getattr(BigWorld.player().ap, 'showCursor', True)
        return GfxValue(aim)

    def onGetFriendMsgList(self, *arg):
        p = BigWorld.player()
        msgList = []
        listLen = 0
        otherLen = len(p.friend.tempMsgOther)
        num = gameglobal.rds.ui.friendRequest.getFriendRequestNum()
        if num > 0:
            msgList.append((num, 'friendRequest', gametypes.FRIEND_ADD_MSG_DESC))
        for i in xrange(otherLen):
            if p.friend.tempMsgOther[otherLen - i - 1][-1] == gametypes.FRIEND_ADD_MSG_DESC:
                continue
            if listLen >= 10:
                break
            msgList.append(p.friend.tempMsgOther[otherLen - i - 1])
            listLen += 1

        photoList = []
        if not gameglobal.rds.configData.get('enableChatGroup', False):
            chatLen = len(p.friend.tempMsgChat)
            for i in xrange(chatLen):
                if listLen >= 10:
                    break
                msgList.append(p.friend.tempMsgChat[chatLen - i - 1])
                friendGbId = p.friend.tempMsgChat[chatLen - i - 1][1]
                if friendGbId != const.XINYI_MANAGER_ID:
                    photo = self.getPhotoByGnId(friendGbId)
                elif BigWorld.player().xinYiManager:
                    photo = p.getXinYiMsgPhoto()
                photoList.append([friendGbId, photo])
                listLen += 1

        if self.friendFlowBackType:
            for friendInfo in gameglobal.rds.ui.friendFlowBack.friendList:
                tmpList = (0, friendInfo[1], friendInfo[2])
                if tmpList not in msgList:
                    msgList.append(tmpList)
                photoList.append([friendInfo[1], self.getPhotoByGnId(friendInfo[1])])

        self.setFriendPhoto(photoList)
        return uiUtils.array2GfxAarry(msgList, True)

    def getPhotoByGnId(self, friendGbId):
        p = BigWorld.player()
        ent = p.getFValByGbId(friendGbId)
        photo = p._getFriendPhoto(ent)
        if uiUtils.isDownloadImage(photo):
            p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, None, (None,))
            photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
        return photo

    def onCheckMenuEnabeld(self, *args):
        menuName = args[3][0].GetString()
        result = True
        p = BigWorld.player()
        if menuName == 'mentor':
            result = p.lv >= ANCD.data.get('minApprenticeLv', 19)
        elif menuName == 'rolecard':
            result = self.uiAdapter.rolecard.showConfig()
        elif menuName == 'worldWar':
            result = self.uiAdapter.worldWar.enableWorldWar()
        elif menuName == 'jieqi':
            result = gameglobal.rds.configData.get('enableIntimacyEvent', False)
        elif menuName == 'pvpEnhance':
            result = gameglobal.rds.configData.get('enablePvpEnhance', False)
        elif menuName == 'guibao':
            result = gameglobal.rds.configData.get('enableGuiBaoGe', False)
        elif menuName == 'showMessageBoard':
            result = gameglobal.rds.configData.get('enableMessageBoard', False)
        elif menuName == 'fengWuZhi':
            result = gameglobal.rds.configData.get('enableFengWuZhi', False)
        elif menuName == 'summonFriend':
            result = gameglobal.rds.configData.get('enableFriendInvite', False)
        elif menuName == 'delegation':
            result = gameglobal.rds.configData.get('enableDelegation', True)
        elif menuName == 'equipSoul':
            result = gameglobal.rds.configData.get('enableEquipSoul', False)
            if result:
                result = BigWorld.player().lv >= SCD.data.get('equipSoulMinLv', 0) and p.checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_EQUIPSOUL)
        elif menuName == 'summonedSprite':
            result = gameglobal.rds.configData.get('enableSummonedSprite', False)
        elif menuName == 'jinenghong':
            result = (gameglobal.rds.configData.get('enableSkillMacro', True) or not BigWorld.isPublishedVersion()) and gameglobal.rds.configData.get('enableOpenSkillMacroEntry', True)
        elif menuName == 'qinggong':
            result = p.checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_QINGGONG) or p.checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_RIDE) or p.checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_WING)
        elif menuName == 'partner':
            result = p.lv >= const.PARTNER_LEVEL_LIMIT and gameglobal.rds.configData.get('enablePartnerEquipment', False)
        elif menuName == 'dota':
            result = p.lv >= SCD.data.get('bfDotaOpenLv', 40) and gameglobal.rds.configData.get('enableBfDotaHeros', False)
        elif menuName == 'cardSystem':
            result = gameglobal.rds.configData.get('enableCardSys', False) and p.isBaseCardSysOpen()
        elif menuName == 'wingWorld':
            result = p.canOpenWingWorldUI()
        elif menuName == 'wardrobe':
            result = gameglobal.rds.configData.get('enableWardrobe', False)
        elif menuName == 'assassination':
            result = gameglobal.rds.configData.get('enableAssassination', False)
        return GfxValue(result)

    def setFriendPhoto(self, photoList):
        if self.mediator:
            self.mediator.Invoke('setFriendPhoto', uiUtils.array2GfxAarry(photoList, True))

    def setActionModeIndicator(self, visible, key, aim = True):
        if self.mediator:
            aim = not getattr(BigWorld.player().ap, 'showCursor', True)
            self.mediator.Invoke('setActionModeIndicator', (GfxValue(visible), GfxValue(key), GfxValue(aim)))

    @ui.uiEvent(uiConst.WIDGET_SYS_BUTTON, events.EVENT_ROLE_SET_LV)
    def showSkillPoint(self):
        if not self.checkNeedShowFightSkill():
            return
        if self.mediator:
            curMaxSkillPoints = utils.getCurSkillPoint(BigWorld.player().lv)
            self.mediator.Invoke('showNum', (GfxValue('fightSkill'), GfxValue(curMaxSkillPoints - BigWorld.player().skillPoint)))

    def showInventoryNewItem(self):
        if self.mediator:
            newItemCount = gameglobal.rds.ui.inventory.tempBagNum + gameglobal.rds.ui.inventory.tempMallBagNum
            self.mediator.Invoke('showNum', (GfxValue('inventory'), GfxValue(newItemCount)))

    def hideUserBackHint(self):
        if self.mediator:
            self.mediator.Invoke('showNum', (GfxValue('userBack'), GfxValue(0)))

    def showRoleInfoNotify(self):
        if self.mediator:
            p = BigWorld.player()
            num = 0
            has = gameglobal.rds.ui.roleInformationHierogram.isHasAvailablePos()
            if has:
                num += 1
            if gameglobal.rds.configData.get('enableHonorV2', False) and getattr(p, 'isHadNewFame', False):
                num += 1
            self.mediator.Invoke('showNum', (GfxValue('roleInfo'), GfxValue(num)))

    def showPartnerNotify(self):
        if self.mediator:
            num = self.getPartnerNotifyNum()
            self.mediator.Invoke('showNum', (GfxValue('partner'), GfxValue(num)))

    def getPartnerNotifyNum(self):
        p = BigWorld.player()
        num = 0
        tJoin = p.partner.get(p.gbId, {}).get('tJoin', 0)
        if self.uiAdapter.partnerMain.isPlayerActivationEnough() and p.partner:
            for k, v in p.dailyActivationRewardDict.iteritems():
                if v == False and not self.uiAdapter.partnerMain.judgeJoinTime(tJoin):
                    num += 1

        return num

    def setFriendFlowBack(self, type):
        self.friendFlowBackType = type
        if self.mediator:
            self.mediator.Invoke('setFriendFlowBack', GfxValue(self.friendFlowBackType))

    def clearMenu(self):
        if self.mediator:
            self.mediator.Invoke('clearMenu', ())

    def refreshSysBtn(self):
        if self.mediator:
            pass

    def onGetButtonShow(self, *args):
        buttonName = args[3][0].GetString()
        p = BigWorld.player()
        if buttonName == 'guild':
            return GfxValue(p.lv >= GCD.data.get('guildLimitLv', 1))
        if buttonName == 'assassination':
            if not gameglobal.rds.configData.get('enableAssassination', False):
                return GfxValue(False)
        return GfxValue(True)

    def onCheckNpcFavor(self, *args):
        if not BigWorld.player():
            return GfxValue(False)
        return GfxValue(gameconfigCommon.enableNpcFavor() and BigWorld.player().checkNpcFrindLv())

    def relayoutByLv(self, newLv, oldLv):
        needRelayout = False
        joinGuildLv = GCD.data.get('joinLv', const.GUILD_JOIN_LV)
        if oldLv < joinGuildLv <= newLv:
            needRelayout = True
        if self.mediator:
            needRelayout and self.mediator.Invoke('relayoutButton')
