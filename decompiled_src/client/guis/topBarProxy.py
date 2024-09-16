#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/topBarProxy.o
from gamestrings import gameStrings
import re
import time
import BigWorld
from Scaleform import GfxValue
import gameconfigCommon
import gameglobal
import const
import uiConst
import utils
import menuManager
import formula
from appSetting import Obj as AppSettings
import keys
import appSetting
import gameChunk
import gametypes
import hotkey as HK
import clientcom
from gamestrings import gameStrings
from guis import uiUtils
from guis import ui
from guis import events
from uiProxy import UIProxy
from ui import gbk2unicode
from helpers import ccControl
from callbackHelper import Functor
from sfx import keyboardEffect
from data import chunk_mapping_data as CMD
from data import multiline_digong_data as MDD
from data import sys_config_data as SCD
from data import topbar_config_data as TCD
from cdata import game_msg_def_data as GMDD
from data import apprentice_config_data as ACD
from data import fame_data as FD
from data import map_config_data as MCD
from data import game_msg_data as GMD
from data import activity_achieve_score_config_data as AASCFD
from data import activity_signin_type_data as ASTD
from data import fb_data as FBD
from data import ftb_config_data as FCD
from cdata import personal_zone_config_data as PZCD
from guis.worldBossHelper import WorldBossHelper
CLOSE_RANK_TIME = SCD.data.get('closeRankAferClanWar', 3600)
SETTING_SPLIT_CHAR = ','
FAME_LIST = [404, 405, 406]

class TopBarProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TopBarProxy, self).__init__(uiAdapter)
        self.modelMap = {'getLatency': self.onGetLatency,
         'getShortcuts': self.onGetShortcuts,
         'initData': self.onInitData,
         'showWindow': self.onShowWindow,
         'selectedMode': self.onSelectedMode,
         'clickMenuItem': self.onClickMenuItem,
         'getTopBarInfo': self.onGetTopBarInfo,
         'clickActionButton': self.onClickActionButton,
         'getNowTime': self.onGetNowTime,
         'saveSetting': self.onSaveSetting,
         'isShowCC': self.isShowCC,
         'isShowZiXun': self.onIsShowZiXun,
         'isShowFtb': self.onIsShowFtb,
         'isShowYixin': self.isShowYixin,
         'isShowCustomerService': self.isShowCustomerService,
         'isBindYixin': self.isBindYixin,
         'getActiveConfigData': self.onGetActiveConfigData,
         'isShowBaoDian': self.onIsShowBaoDian,
         'getMapNameTip': self.onGetMapNameTip,
         'getActivityTip': self.onGetActivityTip,
         'isReward': self.onIsReward,
         'isShowReward': self.onIsShowReward,
         'isShowWelfare': self.onIsShowWelfare,
         'isShowExtendChatBox': self.onIsShowExtendChatBox,
         'isShowPersonalZone': self.onIsShowPersonalZone,
         'mediatorRegisterDone': self.onMediatorRegisterDone}
        self.mediator = None
        self.fpsShow = False
        self.closeRankCallback = None
        self.setting = []
        self.fbType = 1
        self.getTopBarSetting()
        self.showClanWarResult = False
        self.xingJitimer = None
        self.isQuitBF = False

    def isBindYixin(self, *args):
        return GfxValue(getattr(BigWorld.player(), 'yixinOpenId', 0))

    def setMpaNameTxtVisible(self, visible):
        if self.mediator:
            self.mediator.Invoke('setMapNameTxtVisible', GfxValue(visible))

    def checkTopBarCanShine(self):
        canShine = True
        if BigWorld.player().lv > SCD.data.get('LimitShineLv', 30):
            canShine = False
        isCCShine = gameglobal.rds.configData.get('enableCCShine', False)
        if self.mediator:
            self.mediator.Invoke('setCanShine', (GfxValue(canShine), GfxValue(isCCShine)))

    def isShowCC(self, *arg):
        isCCVersion = gameglobal.rds.configData.get('isCCVersion', False)
        enbaleCCBox = gameglobal.rds.configData.get('enableCCBox', False)
        return GfxValue(isCCVersion and enbaleCCBox)

    def isShowYixin(self, *arg):
        isShowYixin = gameglobal.rds.configData.get('enableYixin', False)
        return GfxValue(isShowYixin)

    def isShowCustomerService(self, *arg):
        isShowCustomerService = gameglobal.rds.configData.get('enableCustomerService', True)
        return GfxValue(isShowCustomerService)

    def isShowMallEntry(self):
        return gameglobal.rds.ui.tianyuMall.showMallConfig()

    def onIsShowMallEntry(self, *arg):
        return GfxValue(self.isShowMallEntry())

    def onIsShowZiXun(self, *arg):
        p = BigWorld.player()
        visArray = [gameglobal.rds.ui.ziXunInfo.canShow(), p.getUpdateBonus() != []]
        return uiUtils.array2GfxAarry(visArray)

    def onIsShowFtb(self, *args):
        return uiUtils.array2GfxAarry([self.checkFtbBarShow(), self.checkFtbPrequest()])

    def onIsShowPersonalZone(self, *args):
        return uiUtils.array2GfxAarry([self.checkPersonalZoneShow(), self.checkPersonalZoneNews()])

    def onIsShowReward(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableAward', False))

    def onIsReward(self, *arg):
        ret = False
        if gameglobal.rds.configData.get('enableNewRewardHall', False):
            ret = gameglobal.rds.ui.rewardHall.isShowRewardNotify
        else:
            ret = False
        return GfxValue(ret)

    def refreshPhotoNotify(self, ret):
        if self.mediator:
            self.mediator.Invoke('refreshPhotoNotify', GfxValue(ret))

    def onIsShowBaoDian(self, *arg):
        return GfxValue(True)

    def onUpdateClientCfg(self):
        if self.mediator:
            self.mediator.Invoke('refershTopbarCfg')

    def onGetMapNameTip(self, *arg):
        color = arg[3][0].GetString()
        if color == 'red':
            ret = GMD.data.get(GMDD.data.TOPBAR_PKMODE2, {}).get('text', '')
        elif color == 'green':
            ret = GMD.data.get(GMDD.data.TOPBAR_PKMODE1, {}).get('text', '')
        else:
            ret = GMD.data.get(GMDD.data.TOPBAR_PKMODE3, {}).get('text', '')
        return GfxValue(gbk2unicode(ret))

    def setCCStatus(self, status):
        if self.mediator:
            self.mediator.Invoke('setCCStatus', GfxValue(status))

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def onMediatorRegisterDone(self, *arg):
        self.refreshPlayerMapInfo()
        self.refreshFbStart()
        self.onNewMailNotice(gameglobal.rds.ui.mail.newMailCount)
        self.startXingJiTimer()
        if BigWorld.player():
            if BigWorld.player().IsAvatar:
                self.checkTopBarCanShine()
                BigWorld.player().registerEvent(const.EVENT_YIXIN_BIND_SUCCESS, self.bindYixinSuccess)
                BigWorld.player().registerEvent(const.EVENT_YIXIN_UNBIND_SUCCESS, self.unBindYixinSuccess)
        self.refreshFTBBarState()
        self.onUpdateClientCfg()

    def bindYixinSuccess(self, params):
        self.mediator.Invoke('yixinShine', GfxValue(False))

    def unBindYixinSuccess(self, params):
        self.mediator.Invoke('yixinShine', GfxValue(True))

    def clearWidget(self):
        self.mediator = None
        self.closeRankCallback = None
        if BigWorld.player():
            if BigWorld.player().__class__.__name__ == 'PlayerAvatar':
                BigWorld.player().unRegisterEvent(const.EVENT_YIXIN_BIND_SUCCESS, self.bindYixinSuccess)
                BigWorld.player().unRegisterEvent(const.EVENT_YIXIN_BIND_FAILED, self.unBindYixinSuccess)

    def startXingJiTimer(self):
        self.stopXingJiTimer()
        self.sendXingJiTimerInfo()

    def stopXingJiTimer(self):
        if self.xingJitimer:
            BigWorld.cancelCallback(self.xingJitimer)
            self.xingJitimer = None

    def sendXingJiTimerInfo(self):
        if not BigWorld.player():
            self.stopXingJiTimer()
            return
        if not utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
            return
        nowTime = formula.getXingJiTime()
        if self.mediator:
            info = {}
            intTime = int(nowTime)
            idx = uiUtils.getXingJiWordIdx(intTime)
            info['left'] = uiUtils.convertToXingJiWord(idx)
            info['right'] = uiUtils.convertToXingJiWord(idx + 1)
            if nowTime < 6 or nowTime >= 18:
                info['sm'] = 'moon'
            else:
                info['sm'] = 'sun'
            info['smX'] = (nowTime + 1) % 24 / 24
            currentValue = (nowTime - intTime) * 50.0
            if intTime % 2 == 0:
                currentValue += 50.0
            info['currentValue'] = currentValue
            self.mediator.Invoke('sendXingJiTimerInfo', uiUtils.dict2GfxDict(info, True))
        else:
            self.stopXingJiTimer()
            return
        self.xingJitimer = BigWorld.callback(5, self.sendXingJiTimerInfo)

    def onGetLatency(self, *arg):
        latency = BigWorld.LatencyInfo()
        return GfxValue(latency.value[3])

    def onSaveSetting(self, *arg):
        self.setting = []
        settingGfx = uiUtils.gfxArray2Array(arg[3][0])
        if not settingGfx:
            return
        for item in settingGfx:
            self.setting.append(item.GetString())

        self.saveTopBarSetting()

    def saveTopBarSetting(self):
        settingStr = ''
        if self.setting:
            settingStr = SETTING_SPLIT_CHAR.join(self.setting)
        AppSettings[keys.SET_UI_TOPBAR_BLACK] = settingStr
        AppSettings.save()

    def getTopBarSetting(self):
        try:
            settingStr = AppSettings.get(keys.SET_UI_TOPBAR_BLACK, '')
            if '[' in settingStr:
                settingStr = re.sub("&apos;|\\[|\\]|\'|\\s?", '', settingStr)
            if settingStr:
                if SETTING_SPLIT_CHAR in settingStr:
                    self.setting = settingStr.split(SETTING_SPLIT_CHAR)
                else:
                    self.setting = [settingStr]
            else:
                self.setting = []
        except:
            self.setting = []

    def showNotice(self, wgtName, notice = None):
        ret = {}
        ret['wgtName'] = wgtName
        ret['notice'] = notice
        if self.mediator:
            self.mediator.Invoke('showNotice', uiUtils.dict2GfxDict(ret, True))

    def onNewMailNotice(self, cnt):
        self.showNotice('mail', cnt)
        if cnt:
            keyboardEffect.addKeyboardEffect('effect_mail')
        else:
            keyboardEffect.removeKeyboardEffect('effect_mail')

    def onIsShowWelfare(self, *arg):
        return GfxValue(True)

    def onIsShowExtendChatBox(self, *arg):
        return GfxValue(clientcom.enableExtendChatBox())

    def updatePk(self):
        if self.mediator:
            self.mediator.Invoke('updatePk', GfxValue(getattr(BigWorld.player(), 'pkPunishTime', 0)))

    def onGetTopBarInfo(self, *arg):
        sType = self.getSpaceType()
        ret = self.getInfo(sType)
        self.fbType = sType
        return uiUtils.dict2GfxDict(ret, True)

    def onGetNowTime(self, *arg):
        p = BigWorld.player()
        timeWrap = time.localtime(p.getServerTime())
        return GfxValue(timeWrap.tm_hour * 3600 + timeWrap.tm_min * 60 + timeWrap.tm_sec)

    def getInfo(self, fbType):
        p = BigWorld.player()
        hideWidth = SCD.data.get('topbarHideWidth', 1360)
        ret = {'type': fbType,
         'hideWidth': hideWidth,
         'data': []}
        fbData = {}
        fbId = p.mapID
        if fbId:
            fbData = FBD.data.get(fbId, {})
        for item in TCD.data.values():
            if item.get('lv', -1) > p.lv:
                continue
            if item['type'] == 'left' or item['type'] == 'middle':
                if fbType in item['mode'] and item['name'] not in self.setting:
                    item['visible'] = 1
                else:
                    item['visible'] = 0
                if item['type'] == 'middle':
                    item['value'] = self.getDropMenuValueByName(item['name'])
                if item['name'] == 'ccControl':
                    if gameglobal.rds.configData.get('isCCVersion', False) and gameglobal.rds.configData.get('enableCCBox', False):
                        ret['data'].append(item)
                elif item['name'] == 'yixinControl':
                    if gameglobal.rds.configData.get('enableYixin', False):
                        ret['data'].append(item)
                elif item['name'] == 'bugFeedBack':
                    if gameglobal.rds.configData.get('enableCustomerService', True):
                        ret['data'].append(item)
                elif item['name'] == 'extendChatBox':
                    if clientcom.enableExtendChatBox():
                        ret['data'].append(item)
                elif item['name'] == 'chat':
                    if gameglobal.rds.configData.get('enableTopChatRoom', True):
                        ret['data'].append(item)
                else:
                    ret['data'].append(item)
            elif fbType in item['mode']:
                if item['type'] == 'right' and item['controlClass'] == 'Value':
                    item['value'] = self.getValueByName(item['name'])
                if item['name'] not in self.setting:
                    item['visible'] = 1
                else:
                    item['visible'] = 0
                if item['name'] == 'clanWarResult':
                    if self.showClanWarResult:
                        item['visible'] = 1
                    else:
                        item['visible'] = 0
                if item['name'] == 'clanWarRank':
                    if p.clanWarStatus or self.showClanWarResult:
                        item['visible'] = 1
                    else:
                        item['visible'] = 0
                if item['name'] == 'suiXingYuResult':
                    mlgNo = formula.getMLGNo(p.spaceNo)
                    item['visible'] = mlgNo in const.ML_SPACE_NO_SXY
                if item['name'] == 'quitDG':
                    mlgNo = formula.getMLGNo(p.spaceNo)
                    mlData = MDD.data.get(mlgNo, {})
                    showLeaveButton = mlData.get('canLeave', 1)
                    item['visible'] = showLeaveButton
                if item['name'] == 'trainingVal':
                    item['visible'] = 1 if self.isHasApprentice() else 0
                if item['name'] == 'setShishenMode':
                    showModeSetButton = gameglobal.rds.ui.currentShishenMode > 0 and gameglobal.rds.ui.currentShishenMode < 4 and p.isInTeamOrGroup() and p.isTeamLeader()
                    item['visible'] = showModeSetButton
                if item['name'] == 'wenQuanDetail':
                    item['visible'] = gameglobal.rds.configData.get('enableWenQuanDetail', False)
                if item['name'] == 'exitWorldWar':
                    item['visible'] = not p._isSoul() and p.inWorldWar()
                if item['name'] == 'quitWingWorldWar':
                    item['visible'] = p.inWingCity()
                if item['name'] == 'exitPeaceCity':
                    item['visible'] = p.inWingPeaceCity()
                if item['name'] == 'exitEnemyWorldWar':
                    item['visible'] = p._isSoul() and p.inWorldWar()
                if item['name'] == 'exitWingBornIsland':
                    item['visible'] = p.inWingBornIsland()
                if item['name'] == 'exitCrossClanWar':
                    item['visible'] = p.isInCrossClanWarStatus()
                if item['name'] == 'exitWorldWarBattle':
                    item['visible'] = not p._isSoul() and p.inWorldWarBattle() and self.uiAdapter.worldWar.enableWorldWarBattle()
                if item['name'] == 'exitEnemyWorldWarBattle':
                    item['visible'] = p._isSoul() and p.inWorldWarBattle() and self.uiAdapter.worldWar.enableWorldWarBattle()
                if item['name'] == 'showYaBiao':
                    item['visible'] = hasattr(p, 'yabiaoData') and bool(p.yabiaoData)
                if item['name'] == 'worldWarBattle':
                    item['visible'] = p.inWorldWarBattle() and self.uiAdapter.worldWar.enableWorldWarBattle()
                if item['name'] == 'gotoWorldFromHall':
                    item['visible'] = not p._isSoul() and (p.myHome.inHomeEntrance() or p.myHome.inHomeFloor() or p.myHome.inHomeRoom())
                if item['name'] == 'gotoHallFromFloor':
                    item['visible'] = not p._isSoul() and (p.myHome.inHomeFloor() or p.myHome.inHomeRoom())
                if item['name'] == 'gotoFloorFromRoom':
                    item['visible'] = not p._isSoul() and p.myHome.inHomeRoom()
                if item['name'] == 'gotoWorldFromSoulRoom':
                    item['visible'] = p._isSoul() and p.myHome.inHomeRoom()
                if item['name'] == 'gotoWorldFromFloor':
                    item['visible'] = p.myHome.inHomeFloor()
                if item['name'] == 'showRunMan':
                    item['visible'] = gameglobal.rds.ui.guildRunner.runManType != 0
                if item['name'] == 'sidiGuide':
                    item['visible'] = gameglobal.rds.ui.sidiGuide.isOnMission
                if item['name'] == 'showBangDai':
                    item['visible'] = fbData.get('fbHelp', 0) == 1
                if item['name'] == 'showGuide':
                    item['visible'] = fbData.get('guideMode', 0) != 0
                showOBMc = not (hasattr(p, 'inFightObserve') and p.inFightObserve())
                fubenNo = formula.getFubenNo(BigWorld.player().spaceNo)
                if fubenNo == const.FB_NO_GUILD_QDRQ and item['name'] in ('quitFb',):
                    item['label'] = gameStrings.TEXT_DEBUGPROXY_37
                if item['name'] in ('quitFb', 'showStat', 'showHate'):
                    if item['name'] == 'quitFb':
                        item['visible'] = showOBMc
                    else:
                        item['visible'] = showOBMc and not formula.inHuntBattleField(p.mapID) and not p.inFightForLoveFb() and not formula.inRaceBattleField(fubenNo)
                if item['name'] == 'gotoWorldFromMarriageHall':
                    item['visible'] = p.inFubenType(const.FB_TYPE_MARRIAGE_HALL)
                if item['name'] == 'gotoWorldFromMarriageRoom':
                    item['visible'] = p.inFubenType(const.FB_TYPE_MARRIAGE_ROOM)
                if item['name'] == 'showStat':
                    if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_HOOK):
                        item['visible'] = False
                if item['name'] == 'worldBoss':
                    item['visible'] = WorldBossHelper.getInstance().isInWorldBossActivity()
                if item['name'] == 'huntGhost':
                    item['visible'] = gameglobal.rds.ui.huntGhost.isOpen()
                ret['data'].append(item)

        return ret

    def getValueByName(self, name):
        p = BigWorld.player()
        if name == 'killPoint':
            pkVal = getattr(BigWorld.player(), 'pkPunishTime', 0)
            if 0 < pkVal < 60:
                return 1
            else:
                return pkVal / 60
        else:
            if name == 'bindCash':
                return getattr(BigWorld.player(), 'bindCash', 0)
            if name == 'cash':
                return getattr(BigWorld.player(), 'cash', 0)
            if name == 'workPoint':
                return getattr(BigWorld.player(), 'labour', 0) / 10
            if name == 'brainPoint':
                return getattr(BigWorld.player(), 'mental', 0) / 10
            if name == 'guildCash':
                if p.guild:
                    return p.guild.bindCash
                return 0
            if name == 'guildWood':
                if p.guild:
                    return p.guild.wood
                return 0
            if name == 'guildMojing':
                if p.guild:
                    return p.guild.mojing
                return 0
            if name == 'guildXirang':
                if p.guild:
                    return p.guild.xirang
                return 0
            if name == 'guildContrib':
                return p.guildContrib
            if name == 'expRate':
                return getattr(BigWorld.player(), 'baseVp', 0) + getattr(BigWorld.player(), 'savedVp', 0)
            if name == 'trainingVal':
                return getattr(BigWorld.player(), 'trainingVal', 0)
            if self.isFameValue(name):
                return p.getFame(self.getFameIdByName(name))
            if name == 'haoqiVal':
                return getattr(p, 'haoqiVal', 0)
            if name == 'renpinVal':
                return getattr(p, 'renpinVal', 0)

    def isFameValue(self, name):
        if name.find('fame_') != -1:
            return True
        return False

    def getFameIdByName(self, name):
        _, fameId = name.split('_')
        return int(fameId)

    def getFameNameById(self, fameId):
        name = FD.data.get(fameId, 'name')
        return name

    def setValueByName(self, name):
        if not self.mediator:
            return
        if self.isFameValue(name):
            fameId = self.getFameIdByName(name)
            if fameId not in FAME_LIST:
                return
        val = self.getValueByName(name)
        self.mediator.Invoke('setValueByName', (GfxValue(name), GfxValue(val)))

    def getDropMenuValueByName(self, name):
        p = BigWorld.player()
        if name == 'renderMode':
            return appSetting.getShaderIndex()
        if name == 'avatarMode':
            return gameglobal.gHideMode
        if name == 'actionMode':
            return p.getOperationMode()

    def setDropMenuValueByName(self, name):
        if not self.mediator:
            return
        val = self.getDropMenuValueByName(name)
        self.mediator.Invoke('setDropMenuValueByName', (GfxValue(name), GfxValue(val)))

    def onInitData(self, *arg):
        if BigWorld.player().lv < SCD.data.get('shaderVisibleLv', 30):
            visibleLv = False
        else:
            visibleLv = True
        shaderModeName = SCD.data.get('shaderModeName', [gameStrings.TEXT_CAMERAPROXY_389,
         gameStrings.TEXT_CAMERAPROXY_389_1,
         gameStrings.TEXT_CAMERAPROXY_389_2,
         gameStrings.TEXT_CAMERAPROXY_389_3,
         gameStrings.TEXT_CAMERAPROXY_389_4,
         gameStrings.TEXT_CAMERAPROXY_389_5,
         gameStrings.TEXT_CAMERAPROXY_389_6])
        shaderModeData = []
        for name in shaderModeName:
            shaderModeData.append({'label': name})

        data = [shaderModeData,
         appSetting.getShaderIndex(),
         visibleLv,
         getattr(BigWorld.player(), 'pkPunishTime', 0)]
        self.checkTopBarCanShine()
        return uiUtils.array2GfxAarry(data, True)

    def onClickActionButton(self, *arg):
        buttonName = arg[3][0].GetString()
        p = BigWorld.player()
        if buttonName == 'photo':
            if not gameglobal.rds.configData.get('enableNewCamera', False):
                gameglobal.rds.ui.camera.show()
            else:
                gameglobal.rds.ui.cameraV2.show()
        elif buttonName == 'booth':
            gameglobal.rds.ui.skill.enterBooth()
        elif buttonName == 'chat':
            if gameglobal.rds.configData.get('enableChatGroup', False):
                gameglobal.rds.ui.groupChatMembers.show(uiConst.GROUP_CHAT_MEMBERS_TYPE_CREATE)
            elif BigWorld.player().chatRoomNUID:
                BigWorld.player().showGameMsg(GMDD.data.CHATROOM_JOINED, ())
            else:
                gameglobal.rds.ui.chatRoomCreate.show(uiConst.CHATROOM_CREATE)
        elif buttonName == 'battleCloth':
            p = BigWorld.player()
            if not p.stateMachine.checkStatus(const.CT_CLAN_WAR_ARMOR):
                return
            if p.isInSSCorTeamSSC():
                p.showGameMsg(GMDD.data.SWITCH_ARMOR_FAILED_IN_SSC, ())
                return
            p.operation['commonSetting'][17] = not p.operation['commonSetting'][17]
            p.sendOperation()
            uiUtils.setClanWarArmorMode()
        elif buttonName == 'fangKaDian':
            BigWorld.player().fangKaDian()
        elif buttonName == 'editUI':
            gameglobal.rds.ui.dragButton.dragHotKeyDown()
        elif buttonName == 'action':
            if not gameglobal.rds.ui.newGuiderOpera.mediator:
                gameglobal.rds.ui.newGuiderOpera.show()
            else:
                gameglobal.rds.ui.newGuiderOpera.hide()
        elif buttonName == 'ccControl':
            if not ccControl.toggle():
                gameglobal.rds.ui.cCControl.toggle()
        elif buttonName == 'yixinControl':
            self.yixinClick()
        elif buttonName == 'hideMode':
            gameglobal.rds.ui.hideModeSetting.show()
        elif buttonName == 'bugFeedBack':
            self.showCustomerService()
        elif buttonName == 'extendChatBox':
            p = BigWorld.player()
            p.setWindowStyle(gameglobal.WINDOW_STYLE_CHAT)

    def yixinClick(self):
        if not BigWorld.player().yixinOpenId:
            gameglobal.rds.ui.yixinBind.toggle()
        else:
            gameglobal.rds.ui.yixinRewards.toggle()

    def onSelectedMode(self, *arg):
        name = arg[3][0].GetString()
        index = int(arg[3][1].GetNumber())
        if index == self.getDropMenuValueByName(name):
            return
        if name == 'renderMode':
            self.selectRenderMode(index)
        elif name == 'avatarMode':
            self.selectAvatarMode(index)
        elif name == 'actionMode':
            self.selectActionMode(index)

    def selectRenderMode(self, index):
        appSetting.VideoQualitySettingObj.apply(appSetting.VideoQualitySettingObj._value)
        appSetting.setShaderIndex(index)
        gameglobal.rds.ui.videoSetting.updateMode()

    def selectAvatarMode(self, index):
        BigWorld.player().switchHideMode(getattr(gameglobal, 'HIDE_MODE' + str(index)))

    def selectActionMode(self, index):
        uiUtils.setAvatarPhysics(index)

    def onShowWindow(self, *arg):
        wType = arg[3][0].GetString()
        if wType == 'award':
            gameglobal.rds.ui.rewardHall.show()
        elif wType == 'active':
            gameglobal.rds.ui.welfare.show(uiConst.WELFARE_TAB_SUMMER)
        elif wType == 'sprite':
            gameglobal.rds.ui.help.show()
        elif wType == 'strong':
            gameglobal.rds.ui.playRecomm.show()
            gameglobal.rds.uiLog.addClickLog(uiConst.WIDGET_PLAY_RECOMM * 100 + 6)
        elif wType == 'map':
            if not gameglobal.rds.ui.map.isShow:
                BigWorld.player().showMap(True)
        elif wType == 'daily':
            gameglobal.rds.ui.welfare.show(uiConst.WELFARE_TAB_EVERYDAY_REWARD)
        elif wType == 'mail':
            gameglobal.rds.ui.mail.show()
        elif wType == 'bugFeedbk':
            self.showCustomerService()
        elif wType == 'mall':
            if self.isShowMallEntry():
                gameglobal.rds.ui.tianyuMall.toggleShowMall()
        elif wType == 'baodian':
            gameglobal.rds.ui.baoDian.show()
        elif wType == 'zixun':
            if gameglobal.rds.configData.get('enablePushZixun', False):
                if not gameglobal.rds.ui.ziXunInfo.mediator:
                    gameglobal.rds.ui.ziXunInfo.show()
                else:
                    gameglobal.rds.ui.ziXunInfo.hide()
        elif wType == 'fuxitongbao':
            p = BigWorld.player()
            if gameglobal.rds.ui.realNameCheck.isPlayerThirdParty():
                p.showGameMsg(GMDD.data.FTB_DIG_ACCOUNT_TYPE_INVALID, ())
            elif not gameglobal.rds.ui.realNameCheck.checkPlayerIndulgeState():
                gameglobal.rds.ui.realNameCheck.clearAll()
                gameglobal.rds.ui.realNameCheck.checkRealName()
                p.showGameMsg(GMDD.data.FTB_REAL_NAME_CHECK, ())
            elif hasattr(p.base, 'queryFTBCondition'):
                p.base.queryFTBCondition()
        elif wType == 'personalZone':
            p = BigWorld.player()
            p.getPersonalSysProxy().openZoneMyself(const.PERSONAL_ZONE_SRC_SYSTEM)

    def showCustomerService(self):
        p = BigWorld.player()
        if not BigWorld.player():
            return
        if gameglobal.rds.configData.get('enableCustomerVipService', False):
            vipLevel = utils.getVipGrade(p)
            level1 = gameglobal.rds.configData.get('vipServiceLevel1', 3)
            level2 = gameglobal.rds.configData.get('vipServiceLevel2', 6)
            if vipLevel <= level1:
                gameglobal.rds.ui.customerService.queryToShow()
            elif vipLevel > level1 and vipLevel <= level2:
                gameglobal.rds.ui.customerServiceVip.queryToShow()
            else:
                xinYiOnline = p.getXinYiOnline()
                if xinYiOnline != 1 and xinYiOnline != 2:
                    gameglobal.rds.ui.customerServiceVip.queryToShow()
                else:
                    txt = uiUtils.getTextFromGMD(GMDD.data.FIND_YOUR_XINYI_MANAGER, gameStrings.TEXT_TOPBARPROXY_741)
                    txtConfirm = uiUtils.getTextFromGMD(GMDD.data.CONTRACT_XINYI, gameStrings.TEXT_TOPBARPROXY_742)
                    txtCancel = uiUtils.getTextFromGMD(GMDD.data.SUBMITE_YOUR_QUESTION, gameStrings.TEXT_TOPBARPROXY_743)
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, Functor(gameglobal.rds.ui.friend.beginChat, const.XINYI_MANAGER_ID), txtConfirm, gameglobal.rds.ui.customerServiceVip.queryToShow, txtCancel)

    def onClickMenuItem(self, *arg):
        menuName = arg[3][0].GetString()
        p = BigWorld.player()
        if menuName == 'showStat':
            fbNo = formula.getFubenNo(p.spaceNo)
            if formula.whatFubenType(fbNo) in const.FB_TYPE_BATTLE_FIELD:
                if formula.inDotaBattleField(p.mapID):
                    self.uiAdapter.bfDotaDetail.show()
                else:
                    gameglobal.rds.ui.battleField.showBFTmpResultWidget()
            elif p.inFubenTypes(const.FB_TYPE_ARENA) or formula.whatFubenType(p.mapID) == const.FB_TYPE_SCHOOL_TOP_MATCH:
                gameglobal.rds.ui.arena.showArenaTmpResult()
            else:
                gameglobal.rds.ui.fubenStat.show(None, True)
        elif menuName == 'quitFb':
            if p.inFuben() and not p.inFubenTypes(const.FB_TYPE_ARENA):
                menuManager.getInstance().leaveFuben()
            elif formula.inPhaseSpace(p.spaceNo):
                uiUtils.exitPhase()
        elif menuName == 'quitBattlefield':
            if p.isInPUBG():
                p.leavePUBG()
            elif self.isQuitBF or p.battleFieldPhase == gametypes.DUEL_PHASE_END or p.inFightObserve() and not p.isInBfDota():
                p.cell.quitBattleField()
            elif p.inFubenType(const.FB_TYPE_BATTLE_FIELD_RACE):
                msg = gameStrings.BATTLE_RACE_LEAVE_FB_TEXT
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, p.cell.quitBattleField)
            else:
                msg = uiUtils.getTextFromGMD(GMDD.data.QUIT_BATTLE_FIELD_MSG)
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, p.cell.quitBattleField)
        elif menuName == 'showGuide':
            if BigWorld.player().isFbGuideMode:
                gameglobal.rds.ui.fubenGuide.show()
            else:
                p.showGameMsg(GMDD.data.TOPBAR_NOT_IN_GUIDEMODE, ())
        elif menuName == 'swichLine':
            gameglobal.rds.ui.diGong.show()
        elif menuName == 'quitGuild':
            p.cell.exitGuildScene()
        elif menuName == 'quitDG':
            if formula.inPhaseSpace(p.spaceNo):
                uiUtils.exitPhase()
            else:
                gameglobal.rds.ui.diGong.onDiGongButtonClick(None)
        elif menuName == 'arenaSum':
            gameglobal.rds.ui.arena.showArenaTmpResult()
        elif menuName == 'quitArena':
            if p.inClanChallenge():
                msg = GMD.data.get(GMDD.data.QUIT_CLAN_CHALLENGE_CONFIRM, {}).get('text', 'GMDD.data.QUIT_CLAN_CHALLENGE_CONFIRM')
            elif utils.isCrossArenaPlayoffsFb(formula.getFubenNo(p.spaceNo)):
                msg = uiUtils.getTextFromGMD(GMDD.data.QUIT_ARENA_PLAYOFFS_MSG)
            elif formula.whatFubenType(p.mapID) == const.FB_TYPE_SCHOOL_TOP_MATCH:
                msg = uiUtils.getTextFromGMD(GMDD.data.QUIT_SCHOOL_TOP)
            elif p.inFightObserve():
                msg = uiUtils.getTextFromGMD(GMDD.data.QUIT_ARENA_CHALLENGE_INLIVE)
            elif p.getArenaMode() in const.ARENA_CHALLENDE_MODE_LIST:
                msg = uiUtils.getTextFromGMD(GMDD.data.QUIT_ARENA_CHALLENGE)
            elif p.getArenaMode() == const.ARENA_MODE_CROSS_MS_ROUND_2V2_DOUBLE_ARENA:
                msg = uiUtils.getTextFromGMD(GMDD.data.QUIT_DOUBLE_ARENA)
            else:
                msg = uiUtils.getTextFromGMD(GMDD.data.QUIT_3V3_FIELD_MSG)
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, p.abortArena)
        elif menuName == 'showHate':
            gameglobal.rds.ui.fubenStat.showHateList(True)
        elif menuName == 'clanWarRank':
            gameglobal.rds.ui.clanWar.showRankList()
        elif menuName == 'clanWarResult':
            gameglobal.rds.ui.clanWar.showClanWarResult()
        elif menuName == 'setShishenMode':
            gameglobal.rds.ui.fubenDegree.show()
        elif menuName == 'suiXingYuResult':
            gameglobal.rds.ui.suiXingYu.showResult()
        elif menuName == 'guildExploreState':
            gameglobal.rds.ui.guildExploreState.show()
        elif menuName == 'guildResidentHired':
            gameglobal.rds.ui.guildResidentHired.show()
        elif menuName == 'wenQuanDetail':
            gameglobal.rds.ui.wenQuanDetail.show()
        elif menuName == 'showYaBiao':
            gameglobal.rds.ui.yaBiao.show()
        elif menuName in ('exitWorldWar', 'exitEnemyWorldWar'):
            p.cell.exitWorldWar()
        elif menuName == 'quitWingWorldWar':
            msg = uiUtils.getTextFromGMD(GMDD.data.EXIT_WING_WAR_BATTLE_MSG)
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, p.cell.teleportToWingBornIsland)
        elif menuName in ('exitEnemyWorldWarBattle', 'exitWorldWarBattle'):
            msg = uiUtils.getTextFromGMD(GMDD.data.EXIT_WORLD_WAR_BATTLE_MSG)
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, p.cell.exitWorldWar)
        elif menuName == 'showYaBiao':
            gameglobal.rds.ui.yaBiao.show()
        elif menuName == 'worldWarBattle':
            self.uiAdapter.worldWar.showWorldWarBattle()
        elif menuName == 'showBangDai':
            gameglobal.rds.ui.fubenBangDai.show()
        elif menuName == 'gotoWorldFromHall':
            p.cell.quitHome(const.QUIT_HOME_DEST_BIGWORLD)
        elif menuName == 'gotoHallFromFloor':
            if p.myHome.inHomeRoom():
                p.cell.quitHome(const.QUIT_HOME_DEST_COMMUNITY)
            else:
                p.cell.leaveFloor()
        elif menuName == 'gotoWorldFromFloor':
            p.cell.quitHome(const.QUIT_HOME_DEST_BIGWORLD)
        elif menuName in ('gotoFloorFromRoom', 'gotoWorldFromSoulRoom'):
            p.cell.leaveRoom()
        elif menuName == 'showRunMan':
            gameglobal.rds.ui.guildRunner.show()
        elif menuName == 'sidiGuide':
            if gameglobal.rds.ui.sidiGuide.isOnMission:
                gameglobal.rds.ui.sidiGuide.autoClose = False
                gameglobal.rds.ui.sidiGuide.show()
        elif menuName == 'exitWorldWarRob':
            gameglobal.rds.ui.worldWarRobOverview.exitWorldWarRob()
        elif menuName == 'gotoWorldFromMarriageHall':
            p.cell.leaveMarriageHall()
        elif menuName == 'gotoWorldFromMarriageRoom':
            p.cell.leaveMarriageRoom()
        elif menuName == 'quitAnnalReplay':
            p._stopAnnalReplay(bExit=True)
        elif menuName == 'exitPeaceCity':
            text = GMD.data.get(GMDD.data.EXIT_PEACE_CITY_CONFRIM, {}).get('text', '')
            self.uiAdapter.messageBox.showYesNoMsgBox(text, p.cell.teleportToBigWorldFromWingWorld)
        elif menuName == 'exitWingBornIsland':
            text = GMD.data.get(GMDD.data.EXIT_WING_BORN_ISLAND_CONFRIM, {}).get('text', '')
            self.uiAdapter.messageBox.showYesNoMsgBox(text, p.cell.leaveWingBornIsland)
        elif menuName == 'exitCrossClanWar':
            text = GMD.data.get(GMDD.data.EXIT_CROSS_CLAN_WAR_CONFRIM, {}).get('text', '')
            self.uiAdapter.messageBox.showYesNoMsgBox(text, p.cell.leaveClanWar)
        elif menuName == 'worldBoss':
            gameglobal.rds.ui.worldBossDetail.show()
        elif menuName == 'huntGhost':
            gameglobal.rds.ui.huntGhost.show()

    def setAreaBooth(self, canBooth):
        if self.mediator:
            self.mediator.Invoke('setAreaBooth', GfxValue(canBooth))

    def setAreaFly(self, canFly):
        if self.mediator:
            self.mediator.Invoke('setAreaFly', GfxValue(canFly))

    def refreshIcon(self, mcName, flag):
        if self.mediator:
            self.mediator.Invoke('refreshIcon', (GfxValue(mcName), GfxValue(flag)))

    def sendLatency(self):
        if self.mediator:
            self.mediator.Invoke('showLatency', self.onGetLatency())

    def refreshFps(self):
        if self.mediator:
            self.mediator.Invoke('setFps', GfxValue(BigWorld.getFps()))

    def updateMode(self, name):
        self.setDropMenuValueByName(name)

    def setFpsVisible(self, visible):
        if self.mediator:
            self.mediator.Invoke('setFpsVisible', GfxValue(visible))
            self.fpsShow = visible

    @ui.callAfterTime()
    def refreshFbStart(self):
        if self.mediator:
            if self.closeRankCallback:
                BigWorld.cancelCallback(self.closeRankCallback)
            p = BigWorld.player()
            if not p.clanWarStatus:
                if p.getServerTime() - p.lastClanWarEndTime >= CLOSE_RANK_TIME:
                    self.showClanWarResult = False
                else:
                    self.showClanWarResult = True
                    self.closeRankCallback = BigWorld.callback(p.lastClanWarEndTime + CLOSE_RANK_TIME - p.getServerTime(), self.refreshFbStart)
            else:
                self.showClanWarResult = False
            self.refreshTopBarWidgets()

    def refreshPlayerMapInfo(self):
        if BigWorld.player() and self.mediator:
            color = 'yellow'
            chunckName = BigWorld.ChunkInfoAt(BigWorld.player().position)
            mapName = formula.whatLocationName(BigWorld.player().spaceNo, chunckName)
            if not BigWorld.player().inFuben():
                fortId = CMD.data.get(chunckName, {}).get('fortId')
                if fortId and self.isOwnerGuild(fortId):
                    mapName = gameStrings.TOP_BAR_ZHAN_LING + '-' + mapName
                elif fortId:
                    mapName = gameStrings.TOP_BAR_ZHEN_DUO + '-' + mapName
            color = self.getAreaColor()
            if self.mediator:
                self.mediator.Invoke('refreshInfo', (GfxValue(round(BigWorld.player().position[0])),
                 GfxValue(round(BigWorld.player().position[2])),
                 GfxValue(round(BigWorld.player().position[1])),
                 GfxValue(gbk2unicode(mapName)),
                 GfxValue(color)))

    def setFbButtons(self, fbType):
        if self.mediator:
            self.mediator.Invoke('setFbSetButtons', GfxValue(fbType))

    def setTopBarWidgets(self, fbType, Force = False):
        if not Force and fbType == self.fbType:
            return
        self.fbType = fbType
        if not self.mediator:
            return
        ret = self.getInfo(fbType)
        gfxRet = uiUtils.dict2GfxDict(ret, True)
        if self.mediator:
            self.mediator.Invoke('setTopBarWidgets', gfxRet)

    def refreshTopBarWidgets(self):
        if not self.mediator:
            return
        self.setTopBarWidgets(self.fbType, True)

    def getAreaColor(self):
        p = BigWorld.player()
        mapId = formula.getMapId(p.spaceNo)
        mData = MCD.data.get(mapId)
        limitPk = mData and mData.get('limitPk', 0)
        noPkPunish = mData and mData.get('noPkPunish', 0)
        inBigWorld = p.spaceNo == const.SPACE_NO_BIG_WORLD
        color = 'yellow'
        if gameChunk.resideInSafetyZone(p) or not inBigWorld and limitPk:
            color = 'green'
        elif gameChunk.resideInFreePk(p) or not inBigWorld and not limitPk and noPkPunish:
            color = 'red'
        return color

    def isOwnerGuild(self, fortId):
        p = BigWorld.player()
        fort = p.clanWar.fort.get(fortId, {})
        if p.guildNUID != 0 and fort and fort.ownerGuildNUID == p.guildNUID:
            return True
        return False

    def setArmorBtnVisible(self, visible):
        if self.mediator:
            self.mediator.Invoke('setArmorBtnVisible', GfxValue(visible))
        if visible:
            self.setArmorBtnSelect(BigWorld.player().operation['commonSetting'][17])

    def setArmorBtnSelect(self, select):
        if self.mediator:
            self.mediator.Invoke('setArmorBtnSelect', GfxValue(select))

    def shineActionBtn(self):
        pass

    def switchTopBar(self, force = False):
        sType = self.getSpaceType()
        self.setTopBarWidgets(sType, force)

    def isNeedRefreshLv(self, lv):
        for item in TCD.data.values():
            if item.get('lv', -1) == lv:
                return True

        return False

    def getSpaceType(self):
        p = BigWorld.player()
        sType = uiConst.TOPBAR_TYPE_WORLD
        if p.inFuben():
            if p.inFubenTypes(const.FB_TYPE_ARENA):
                sType = uiConst.TOPBAR_TYPE_ARENA
            elif p.isInSSCorTeamSSC():
                sType = uiConst.TOPBAR_TYPE_SSC
            elif p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
                sType = uiConst.TOPBAR_TYPE_BATTLE
            elif p.inFubenTypes(const.FB_TYPE_GUILD_CHALLENGE):
                sType = uiConst.TOPBAR_TYPE_GUILD_CHALLENGE
            elif formula.whatFubenType(p.mapID) == const.FB_TYPE_SCHOOL_TOP_MATCH:
                sType = uiConst.TOPBAR_TYPE_SCHOOL_TOP
            else:
                sType = uiConst.TOPBAR_TYPE_FUBEN
        if formula.spaceInMultiLine(p.spaceNo):
            sType = uiConst.TOPBAR_TYPE_DIGONG
        if formula.inPhaseSpace(p.spaceNo):
            sType = uiConst.TOPBAR_TYPE_PHASE
        if p.inGuildSpace():
            sType = uiConst.TOPBAR_TYPE_GUILD
        if hasattr(BigWorld.player(), 'mapID') and BigWorld.player().mapID == const.ML_SPACE_NO_WENQUAN_FLOOR1:
            sType = uiConst.TOPBAR_TYPE_WENQUAN
        if formula.spaceInWorldWarEx(p.spaceNo):
            sType = uiConst.TOPBAR_TYPE_WORLD_WAR
        if p.myHome.inHomeEntrance():
            return uiConst.TOPBAR_TYPE_HOME_ENTRANCE
        if p.myHome.inHomeFloor():
            return uiConst.TOPBAR_TYPE_HOME_FLOOR
        if p.myHome.inHomeRoom():
            return uiConst.TOPBAR_TYPE_HOME_ROOM
        if formula.spaceInWorldWarRob(p.spaceNo):
            return uiConst.TOPBAR_TYPE_WORLD_WAR_ROB
        if p.inFubenType(const.FB_TYPE_MARRIAGE_HALL):
            return uiConst.TOPBAR_TYPE_MARRIAGE_HALL
        if p.inFubenType(const.FB_TYPE_MARRIAGE_ROOM):
            return uiConst.TOPBAR_TYPE_MARRIAGE_ROOM
        if formula.spaceInAnnalReplay(p.spaceNo):
            return uiConst.TOPBAR_TYPE_ANNAL_REPLAY
        if p.inWingWarCity():
            return uiConst.WING_WORLD_WAR
        if p.inWingPeaceCity():
            return uiConst.WING_WORLD_PEACE_CITY
        if formula.spaceInWingBornIsland(p.spaceNo):
            return uiConst.TOPBAR_TYPE_WING_BORN_ISLAND
        if p.isInCrossClanWarStatus():
            return uiConst.TOPBAR_TYPE_CROSS_CLAN_WAR
        if p.isInPUBG():
            return uiConst.TOPBAR_TYPE_PUBG
        return sType

    def onGetActiveConfigData(self, *arg):
        return GfxValue(False)

    def isHasApprentice(self):
        ret = False
        p = BigWorld.player()
        if hasattr(p, 'apprenticeGbIds') and p.apprenticeGbIds:
            for gbId, isGraduate in p.apprenticeGbIds:
                if not isGraduate:
                    ret = True
                    break

        return ret

    @ui.uiEvent(uiConst.WIDGET_TOPBAR, (events.EVENT_ADD_APPRENTICE_IFNO, events.EVENT_REMOVE_APPRENTICE_IFNO))
    def refWhenApprenticeChanged(self):
        p = BigWorld.player()
        mapId = formula.getMapId(p.spaceNo)
        traningMaps = ACD.data.get('traningMaps', ())
        if mapId in traningMaps:
            self.refreshTopBarWidgets()

    def addTutorialTip(self, data, msg):
        if not self.mediator:
            return
        if data:
            ret = {'name': data[0],
             'type': data[6],
             'msg': msg,
             'iconType': data[5]}
            self.mediator.Invoke('addTutorialTip', uiUtils.dict2GfxDict(ret, True))

    def removeTutorialTip(self):
        if not self.mediator:
            return
        self.mediator.Invoke('removeTutorialTip')

    def onGetShortcuts(self, *arg):
        hotKey = int(arg[3][0].GetNumber())
        try:
            detial = HK.HKM[hotKey]
            if detial.key != 0:
                return GfxValue(detial.getBrief())
        except:
            return GfxValue('')

        return GfxValue('')

    def onGetActivityTip(self, *args):
        activityTip = ASTD.data.get(uiUtils.getActivitySignId(), {}).get('title', '')
        activityScoreTip = AASCFD.data.get(uiUtils.getActivityScoreId(), {}).get('topic', '')
        if activityTip:
            return GfxValue(gbk2unicode(activityTip))
        if activityScoreTip:
            return GfxValue(gbk2unicode(activityScoreTip))
        return GfxValue(gbk2unicode(gameStrings.TEXT_TOPBARPROXY_1128))

    def refreshActivityIcon(self):
        if self.mediator:
            self.mediator.Invoke('refreshActivityIcon', GfxValue(False))

    def checkGudeGoal(self):
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableGuideGoal', False):
            if p.lv < SCD.data.get('guideGoalMinLv', 0):
                return False
            if gameglobal.rds.ui.guideGoal.checkAllAwardGain():
                return False
            guideGoalSpecialStartTime = SCD.data.get('guideGoalSpecialStartTime', {}).get(utils.getHostId())
            if guideGoalSpecialStartTime:
                startTime = utils.getTimeSecondFromStr(guideGoalSpecialStartTime)
            else:
                guideGoalDefaultStartTime = SCD.data.get('guideGoalDefaultStartTime')
                if guideGoalDefaultStartTime:
                    startTime = utils.getTimeSecondFromStr(guideGoalDefaultStartTime)
                else:
                    startTime = 0
            return p.enterWorldTime >= startTime
        else:
            return False

    def checkPersonalZoneShow(self):
        p = BigWorld.player()
        pyqOpenLv = PZCD.data.get('pyqOpenLv', 0)
        return gameconfigCommon.enablePYQ() and p.lv >= pyqOpenLv

    def checkPersonalZoneNews(self):
        return BigWorld.player().pyqNewsNum

    def checkFtbBarShow(self):
        p = BigWorld.player()
        return gameglobal.rds.configData.get('enableFTB', False) and p.lv >= FCD.data.get('lvLimit', 5)

    def checkFtbPrequest(self):
        p = BigWorld.player()
        if not hasattr(p, 'ftbDataDetail'):
            return False
        result = not p.getQuestFlag(FCD.data.get('preQuestLoopId', 0))
        result |= uiUtils.hasVipBasicSimple() and not p.ftbDataDetail.hasVipRewardTaken
        result &= not gameglobal.rds.ui.realNameCheck.isPlayerThirdParty()
        return result

    @ui.uiEvent(uiConst.WIDGET_TOPBAR, (events.EVNET_FTB_CONDITIONDATA_CHANGE, events.EVNET_FTB_HASVIPREWARDTAKEN_CHANGE))
    def onFtbConditionDataChange(self, event):
        self.onUpdateClientCfg()

    @ui.uiEvent(uiConst.WIDGET_TOPBAR, events.EVNET_FTB_DIGINGSTATE_CHANGE)
    def onUpdateFTBBarState(self, event):
        self.refreshFTBBarState()

    def refreshFTBBarState(self):
        isDiging = BigWorld.player().ftbDataDetail.isDigging
        if self.mediator:
            self.mediator.Invoke('refershFTBState', GfxValue(isDiging))

    def refreshPersonalZoneEffect(self, newsNum):
        if self.mediator:
            self.mediator.Invoke('refreshPersonalZoneEffect', GfxValue(newsNum))
