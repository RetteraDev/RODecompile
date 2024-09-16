#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ziXunInfoProxy.o
from gamestrings import gameStrings
import math
import urllib
import urlparse
import base64
import BigWorld
CEFModule = None
try:
    import CEFManager as CEFModule
except:
    CEFModule = None

import uiConst
import uiUtils
import clientcom
import gameglobal
import gametypes
import utils
import clientUtils
import keys
import cefUIManager
import const
from helpers import CEFControl
from uiProxy import UIProxy
from guis import ui
from gameclass import Singleton
from appSetting import Obj as AppSettings
from gameclass import ClientMallVal as cmv
from data import sys_config_data as SCD
from data import item_data as ID
from cdata import update_bonus_data as UBD
from cdata import personal_zone_config_data as PZCD
from data import mall_item_data as MID
NOT_STICKTOP_INDEX = -1
BONUS_TYPE_CLAIM = 1
BONUS_TYPE_BUY = 2
LIMIT_TYPE_NONE = 0
LIMIT_TYPE_DAY = 6
LIMIT_TYPE_WEEK = 7
LIMIT_TYPE_MONTH = 8
LIMIT_TYPE_FIRST_BUY = 9

class ZiXunInfoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ZiXunInfoProxy, self).__init__(uiAdapter)
        self.modelMap = {'enterFrame': self.onEnterFrame,
         'handleClickTab': self.onHandleClickTab,
         'handleClickAccBtn': self.onHandleClickAccBtn}
        self.mediator = None
        self.width = 900
        self.height = 480
        self.swfPath = 'gui/widgets/TianYuZiXunWidget' + uiAdapter.getUIExt()
        self.insName = 'unitWeb'
        self.homeUrl = ''
        self.oldX = 0
        self.oldY = 0
        self.reset()
        self.timer = 0
        self.lastOperateTime = 0
        self.needAutoShow = True
        self.urlProcessor = URLProcessor.getInstance()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ZIXUN_PLAY, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ZIXUN_PLAY:
            self.mediator = mediator
            if self.showTabIndex != -1:
                stickTopIdx = self.showTabIndex
            else:
                stickTopIdx, configIdx = self.getStickTopIdx()
                if stickTopIdx != NOT_STICKTOP_INDEX:
                    self.url = self.getUrlPath(stickTopIdx)
                    self.saveOldStickIdx(configIdx)
            self.startPlay()
            info = {'TabBtnNum': SCD.data.get('ZiXunTabNum', 3),
             'rewardItems': self.getBonusInfo(),
             'disableTabs': self.getDisableTabs(),
             'stickTopIdx': stickTopIdx}
            return uiUtils.dict2GfxDict(info, True)

    def reset(self):
        self.url = ''
        self.showTabIndex = -1
        self.personalZone = {}

    def clearWidget(self):
        cefUIManager.getInstance().unregisterCefUI(uiConst.WIDGET_ZIXUN_PLAY)
        CEFModule.setVisible(False)
        CEFModule.setPosition(0, 0)
        self.mediator = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ZIXUN_PLAY)

    def canShow(self):
        if not gameglobal.rds.configData.get('enablePushZixun', False):
            return False
        return BigWorld.player().lv >= SCD.data.get('ziXunMinLv', 0)

    def show(self, tabIndex = -1, personalZone = {}, gotoUrl = ''):
        if not self.canShow():
            return
        if not CEFModule:
            return
        if not CEFModule.isCefProcessRunning():
            swShow = gameglobal.SW_HIDE if BigWorld.isPublishedVersion() else gameglobal.SW_SHOW
            CEFModule.openCefProcess(gameglobal.CEF_PROCESS_NAME, self.width, self.height, swShow)
        if not cefUIManager.getInstance().registerCefUI(uiConst.WIDGET_ZIXUN_PLAY, closeFunc=self.hide, forceOpen=True):
            return
        self.showTabIndex = tabIndex
        if tabIndex == -1:
            tabIndex = 0
        self.personalZone = personalZone
        if gotoUrl:
            try:
                gotoUrl = base64.b64decode(gotoUrl)
            except:
                pass

            self.url = gotoUrl
        else:
            self.url = self.getUrlPath(tabIndex)
        if self.mediator:
            self.startPlay()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ZIXUN_PLAY)

    def recordTime(self):
        self.lastOperateTime = utils.getNow()
        if not self.timer and self.needAutoShow:
            self.timer = BigWorld.callback(10, self.circleCheck, -1)

    def circleCheck(self):
        zixunAutoOpen = SCD.data.get('zixunAutoOpen', {})
        p = BigWorld.player()
        if not self.mediator and p and utils.getNow() - self.lastOperateTime > zixunAutoOpen.get('time', 120) and getattr(p, 'mapID', 0) in zixunAutoOpen.get('mapIDs', ()):
            self.show(zixunAutoOpen.get('index', 4))
            self.needAutoShow = False
            BigWorld.cancelCallback(self.timer)
            self.timer = 0

    def getWidgetScale(self):
        widget = self.mediator.Invoke('getWidget')
        scaleX = widget.GetMember('scaleX').GetNumber()
        scaleY = widget.GetMember('scaleY').GetNumber()
        return (scaleX, scaleY)

    def getOffset(self):
        widget = self.mediator.Invoke('getWidget')
        widgetX = widget.GetMember('x').GetNumber()
        widgetY = widget.GetMember('y').GetNumber()
        iconX = widget.GetMember('picture').GetMember('x').GetNumber()
        iconY = widget.GetMember('picture').GetMember('y').GetNumber()
        scaleX, scaleY = self.getWidgetScale()
        return (int(iconX + widgetX * scaleX), int(iconY + widgetY * scaleY))

    def startPlay(self):
        CEFModule.setConnBindedCallback(self.connectionBindedCallback)
        CEFModule.setTextureChangeCallback(self.textureChangeCallback)
        self.refreshDrawToFlash()
        self.oldX, self.oldY = self.getOffset()
        CEFModule.initImgBuff()
        CEFModule.setPosition(self.oldX, self.oldY)
        CEFModule.resize(self.width, self.height)
        CEFModule.setVisible(True)
        CEFModule.loadURL(self.url)
        CEFModule.setCefRequestCallback(self.handleCEFRequest)

    def onEnterFrame(self, *args):
        topWidgetId = self.uiAdapter.getTopWidgetId()[0]
        if topWidgetId != uiConst.WIDGET_ZIXUN_PLAY:
            x, y = BigWorld.getScreenSize()
        else:
            x, y = self.getOffset()
        if self.oldX != x or self.oldY != y:
            CEFModule.setPosition(x, y)
            self.oldX = x
            self.oldY = y
            scale = CEFControl.getDPIScale()
            scaleX, scaleY = self.getWidgetScale()
            CEFModule.setScale(scaleX / scale, scaleY / scale)

    def refreshDrawToFlash(self):
        CEFModule.drawToFlash(self.swfPath, self.insName, 0, 0, self.width, self.height)

    def textureChangeCallback(self, width, height):
        self.refreshDrawToFlash()

    def connectionBindedCallback(self, bind):
        CEFModule.loadURL(self.url)
        CEFModule.resize(self.width, self.height)
        self.refreshDrawToFlash()

    def handleCEFRequest(self, request, requestLen):
        if len(request) != requestLen:
            return
        oldUrl = request.split('.com')
        newUrl = self.url.split('.com')
        if len(oldUrl) > 1 and len(newUrl) > 1 and oldUrl[1] == newUrl[1]:
            self.homeUrl = request
            self.url = request
            return
        if request == self.url or request.find('163.com/news/kuang') != -1:
            self.url = request
            return
        if self.urlProcessor.process(request):
            pass
        else:
            if gameglobal.rds.GameState == gametypes.GS_LOADING:
                return
            self.url = request
            if request != self.homeUrl:
                clientcom.openFeedbackUrl(request)
        if request.find('personalZone') != -1:
            pass
        else:
            CEFModule.loadURL(self.homeUrl)

    def getDisableTabs(self):
        disableTabIndex = gameglobal.rds.configData.get('disableZixunTab', '')
        disableTabs = []
        if disableTabIndex:
            try:
                disableTabs = [ int(x) for x in disableTabIndex.split(',') ]
            except:
                pass

        return disableTabs

    def readOldStickIdx(self):
        return AppSettings.get(keys.SET_ZIXUN_TABTOP, -1)

    def saveOldStickIdx(self, oldIdx):
        AppSettings[keys.SET_ZIXUN_TABTOP] = oldIdx
        AppSettings.save()

    def getStickTopIdx(self):
        stickTopIdx = gameglobal.rds.configData.get('setZixunTabTop', NOT_STICKTOP_INDEX)
        configIdx = stickTopIdx
        if stickTopIdx == NOT_STICKTOP_INDEX:
            return (NOT_STICKTOP_INDEX, stickTopIdx)
        if stickTopIdx == self.readOldStickIdx():
            return (NOT_STICKTOP_INDEX, stickTopIdx)
        if stickTopIdx >= 10:
            num = len(str(stickTopIdx))
            stickTopIdx = int(stickTopIdx / math.pow(10, num - 1))
        return (stickTopIdx, configIdx)

    def getUrlPath(self, index):
        disableTabs = self.getDisableTabs()
        while index in disableTabs:
            index += 1

        urlPaths = SCD.data.get('ZiXunUrl', ())
        if index < len(urlPaths):
            gbId = self.personalZone.get('gbId', 0)
            if urlPaths[index] == 'personalZone':
                if gbId:
                    try:
                        param = urllib.urlencode(self.personalZone)
                        prettyGirlshowUrl = PZCD.data.get('prettyGirlShowUrl', '')
                        url = PZCD.data.get('prettyGirlNavUrl', '')
                        if prettyGirlshowUrl:
                            url = prettyGirlshowUrl + param
                        self.personalZone = {}
                        return url
                    except:
                        self.personalZone = {}
                        return PZCD.data.get('prettyGirlNavUrl', '')

                else:
                    return PZCD.data.get('prettyGirlNavUrl', '')
            else:
                return urlPaths[index]
        return ''

    def onHandleClickTab(self, *arg):
        self.showTabIndex = int(arg[3][0].GetNumber())
        self.url = self.getUrlPath(self.showTabIndex)
        CEFModule.loadURL(self.url)

    def getBonusInfo(self):
        p = BigWorld.player()
        ids = p.getUpdateBonus()
        ret = []
        for id in ids:
            data = UBD.data.get(id, {})
            if data.has_key('tStartApply'):
                tStartApply = int(data['tStartApply'])
                tEndApply = int(data['tEndApply']) + 1
            elif data.has_key('startCron') and utils.inCrontabRange(data['startCron'], data['endCron']):
                tStartApply = int(utils.getPreCrontabTime(data['startCron']))
                tEndApply = int(utils.getNextCrontabTime(data['endCron']) + 1)
            startDate = utils.formatDate(tStartApply)
            endDate = utils.formatDate(tEndApply)
            dateStr = gameStrings.TEXT_ZIXUNINFOPROXY_315 % tuple(endDate.split('-'))
            bonusId = data.get('bonusId', 0)
            bonus = clientUtils.genItemBonus(bonusId)
            nameStr = ''
            itemInfo = {}
            bonusType = data.get('bonusType', 1)
            mallId = data.get('mallId', 0)
            if not self.checkBonusCanBuy(mallId):
                continue
            if bonus:
                itemInfo = uiUtils.getGfxItemById(*bonus[0])
                nameStr = ID.data.get(bonus[0][0], {}).get('name')
            ret.append({'name': nameStr,
             'date': dateStr,
             'item': itemInfo,
             'updateBonusId': id,
             'bonusType': bonusType,
             'mallId': mallId})

        return ret

    def refreshRewardPanel(self):
        if self.mediator:
            rewardItems = self.getBonusInfo()
            self.mediator.Invoke('refreshRewardPanel', uiUtils.array2GfxAarry(rewardItems, True))

    def onHandleClickAccBtn(self, *arg):
        id = int(arg[3][0].GetNumber())
        bonusType = int(arg[3][1].GetNumber())
        if bonusType == BONUS_TYPE_CLAIM:
            BigWorld.player().cell.applyUpdateBonus(id)
        elif bonusType == BONUS_TYPE_BUY:
            gameglobal.rds.ui.tianyuMall.show(mallId=id)

    def checkBonusCanBuy(self, mallId):
        p = BigWorld.player()
        itemInfo = MID.data.get(mallId, {})
        itemId = itemInfo.get('itemId', 0)
        sexReq = ID.data.get(itemId, {}).get('sexReq', 0)
        physique = getattr(p, 'physique', None)
        pSex = getattr(physique, 'sex', -1)
        if sexReq > 0 and sexReq != pSex:
            return False
        if ID.data.get(itemId, {}).has_key('schReq'):
            if getattr(p, 'realSchool', const.SCHOOL_DEFAULT) not in ID.data.get(itemId, {}).get('schReq', 0):
                return False
        if not utils.inAllowBodyType(itemId, getattr(physique, 'bodyType', -1), ID):
            return False
        leftNum = 0
        limitType = LIMIT_TYPE_NONE
        if itemInfo.get('dayLimit', 0) > 0:
            limitType = LIMIT_TYPE_DAY
            leftNum = itemInfo.get('dayLimit', 0) - p.mallInfo.get(mallId, cmv()).nDay / itemInfo.get('many', 1)
        elif itemInfo.get('weekLimit', 0) > 0:
            limitType = LIMIT_TYPE_WEEK
            leftNum = itemInfo.get('weekLimit', 0) - p.mallInfo.get(mallId, cmv()).nWeek / itemInfo.get('many', 1)
        elif itemInfo.get('monthLimit', 0) > 0:
            limitType = LIMIT_TYPE_MONTH
            leftNum = itemInfo.get('monthLimit', 0) - p.mallInfo.get(mallId, cmv()).nMonth / itemInfo.get('many', 1)
        elif itemInfo.get('totalLimit', 0) > 0:
            limitType = LIMIT_TYPE_FIRST_BUY
            leftNum = itemInfo.get('totalLimit', 0) - p.mallInfo.get(mallId, cmv()).nTotal / itemInfo.get('many', 1)
        leftNum = max(leftNum, 0)
        if limitType != LIMIT_TYPE_NONE and leftNum == 0:
            return False
        else:
            return True


class ProcessUnit(object):

    def __init__(self, keyStr):
        self.keyStr = keyStr.lower()

    def process(self, url):
        url = url.lower()
        index = url.rfind(self.keyStr)
        value = 0
        if index != -1:
            try:
                value = url[index + len(self.keyStr):]
            except:
                value = 0

        if index != -1:
            self.use(value)
            return True
        return False

    def use(self, value):
        pass


class MallProcessUnit(ProcessUnit):

    def __init__(self):
        super(MallProcessUnit, self).__init__('tianyuMall.com/')

    def use(self, value):
        gameglobal.rds.ui.tianyuMall.showMallTab(int(value), 0)


class ScheduleProcessUnit(ProcessUnit):

    def __init__(self):
        super(ScheduleProcessUnit, self).__init__('schedule.com')

    def use(self, value):
        pass


class MallBuyProcessUnit(ProcessUnit):

    def __init__(self):
        super(MallBuyProcessUnit, self).__init__('mallId=')

    def use(self, value):
        gameglobal.rds.ui.tianyuMall.mallBuyConfirm(value, 1, 'mallWeb.0')


class SeekerProcessUnit(ProcessUnit):

    def __init__(self):
        super(SeekerProcessUnit, self).__init__('seekId=')

    def use(self, value):
        uiUtils.findPosWithAlert(value)


class ShareZiXunUnit(ProcessUnit):

    def __init__(self):
        super(ShareZiXunUnit, self).__init__('shareZiXunIndex=')

    def use(self, value):
        value = value.split('&')
        index = value[0]
        title = urlparse.parse_qsl(value[1])[0][1]
        title = ui.unicode2gbk(title, title)
        gotoUrl = ''
        if len(value) == 3:
            gotoUrl = urlparse.parse_qsl(value[2])[0][1]
        msg = SCD.data.get('SHARE_ZIXUN_MSG', '%s') % title
        msg = "[<a href = \'event:shareZiXun-%s-%s\'><u>%s</u></a>]" % (index, base64.b64encode(gotoUrl), msg)
        gameglobal.rds.ui.sendLink(msg)


class PersonalZoneUnit(ProcessUnit):

    def __init__(self):
        super(PersonalZoneUnit, self).__init__('personalZone')

    def use(self, value):
        try:
            data = urlparse.parse_qsl(value[1:])
            gbId = 0
            serverId = 0
            for k, v in data:
                if k == 'gbid':
                    gbId = int(v)
                if k == 'serverid':
                    serverId = int(v)

            if gbId:
                p = BigWorld.player()
                p.getPersonalSysProxy().openZoneOther(gbId, hostId=serverId)
        except:
            return


class URLProcessor(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.processUnits = [MallProcessUnit(),
         ScheduleProcessUnit(),
         MallBuyProcessUnit(),
         SeekerProcessUnit(),
         ShareZiXunUnit(),
         PersonalZoneUnit()]

    def process(self, url):
        for unit in self.processUnits:
            if unit.process(url):
                return True

        return False
