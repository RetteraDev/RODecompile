#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/partnerMainProxy.o
import BigWorld
import gameglobal
import gamelog
import gametypes
import const
import ui
import utils
import clientUtils
import events
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from asObject import ASUtils
from asObject import ASObject
from asObject import TipManager
from asObject import MenuManager
from gamestrings import gameStrings
from callbackHelper import Functor
from helpers import capturePhoto
from helpers import charRes
from data import partner_config_data as PCD
from data import title_data as TD
from cdata import game_msg_def_data as GMDD
PHOTO_RES_NAME = 'PartnerMain_Unit'
OTHER_NAME_COLOR = '#FFFFE6'
SELF_NAME_COLOR = '#7ACC29'
ACTIVATION_RATE = 1000
DAYSECOND = 86400

class PartnerMainProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PartnerMainProxy, self).__init__(uiAdapter)
        self.widget = None
        self.photoArr = []
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PARTENR_MAIN, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PARTENR_MAIN:
            self.widget = widget
            self.initUI()

    def initPhotoData(self):
        self.photoArr = []
        for x in xrange(0, 5):
            photoGen = capturePhoto.PartnerPhotoGen('gui/taskmask.tga', 345, PHOTO_RES_NAME + str(x))
            photoGen.initFlashMesh()
            photoGen.setModelFinishCallback(Functor(self.setLoadingMcVisible, False, x))
            self.photoArr.append(photoGen)

    def show(self):
        p = BigWorld.player()
        if p._isSoul():
            p.showGameMsg(GMDD.data.PARTNER_WIDGET_FORBIDDEN_SOUL, ())
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PARTENR_MAIN)
        BigWorld.player().cell.queryPartnersEquipment()

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PARTENR_MAIN)
        self.widget = None
        self.endCapture()

    def reset(self):
        pass

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        self.initPhotoData()

    def initState(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.actMc.visible = False
        self.widget.stage.addEventListener(events.MOUSE_CLICK, self.handleClickStage, False, 0, True)
        TipManager.addTip(self.widget.rewardMc.rewardTitleTxt, gameStrings.PARTNER_REWARD_TIPS)
        self.refreshInfo()

    def refreshInfo(self):
        if self.hasBaseData():
            p = BigWorld.player()
            hasPartner = False
            if bool(p.partnerNUID):
                self.widget.mainBgMc.gotoAndStop('partner')
                hasPartner = True
            else:
                self.widget.mainBgMc.gotoAndStop('single')
                hasPartner = False
                self.widget.mainBgMc.partnerNoneTips.htmlText = PCD.data.get('PARTNER_NONE_TIPS', '')
            self.refreshRewardMc()
            if hasPartner:
                titleStr = p.getCurPartnerTitleName()
                partnerTitleId = PCD.data.get('partnerTitleId', 0)
                tData = TD.data.get(partnerTitleId, {})
                titleStr = uiUtils.toHtml(titleStr, uiConst.TITLE_COLOR_DIC.get(tData.get('style', 0), ''))
                self.widget.mainBgMc.titleMc.titleTxt.htmlText = titleStr
            partnerInfo = self.calcPartnerInfo()
            for x in xrange(0, const.PARTNER_MAX_NUM):
                playerName = getattr(self.widget, 'playerName' + str(x), None)
                if playerName:
                    playerName.pTag = x
                    MenuManager.getInstance().unRegister(playerName)
                    if x < len(partnerInfo) and hasPartner:
                        self.setPlayerNameMc(playerName, partnerInfo[x])
                    else:
                        playerName.visible = False
                photoBg = getattr(self.widget, 'photoBg' + str(x), None)
                if photoBg:
                    photoBg.pTag = x
                    photoBg.addEventListener(events.MOUSE_ROLL_OVER, self.handleRollOverPhoto, False, 0, True)
                    photoBg.addEventListener(events.MOUSE_ROLL_OUT, self.handleRollOutPhoto, False, 0, True)
                    if hasPartner and False:
                        if x < len(partnerInfo):
                            menuParam = {'roleName': partnerInfo[x].get('roleName', ''),
                             'gbId': partnerInfo[x].get('gbId', 0)}
                            MenuManager.getInstance().registerMenuById(photoBg, uiConst.MENU_PARTNER_SHOW, menuParam)
                        else:
                            photoBg.gotoAndStop('disable')
                    else:
                        photoBg.visible = False
                loadingMc = getattr(self.widget, 'loadingMc' + str(x), None)
                if loadingMc:
                    loadingMc.pTag = x
                    ASUtils.setHitTestDisable(loadingMc, True)
                    loadingMc.visible = False
                playerPhoto = getattr(self.widget, 'playerPhoto' + str(x), None)
                if playerPhoto:
                    playerPhoto.pTag = x
                    MenuManager.getInstance().unRegister(playerPhoto)
                    if x < len(partnerInfo) and hasPartner:
                        playerPhoto.visible = True
                        gbId = partnerInfo[x].get('gbId', 0)
                        if gbId in p.partnerEquipment:
                            self.takePhoto(x, p.partnerEquipment.get(gbId, {}))
                        elif p.gbId == gbId:
                            self.takePhoto(x, p.partnerEquipment.get(gbId, {}), True)
                        menuParam = {'roleName': partnerInfo[x].get('roleName', ''),
                         'gbId': partnerInfo[x].get('gbId', 0)}
                        MenuManager.getInstance().registerMenuById(playerPhoto, uiConst.MENU_PARTNER_SHOW, menuParam)
                    else:
                        playerPhoto.visible = False

    def refreshRewardMc(self):
        if self.hasBaseData():
            p = BigWorld.player()
            aRewards = PCD.data.get('activationRewards', ())
            lastPoint = 0
            allPoint = self.calcAllActivePoint()
            for i, rData in enumerate(aRewards):
                aPoint, bonusId = rData
                rewardItem = getattr(self.widget.rewardMc, 'reward' + str(i), None)
                rewardItem.enabled = True
                text = gameStrings.PARTNER_REWARD_ACTIVE_POINT % (aPoint / ACTIVATION_RATE,)
                bGray = False
                tJoin = p.partner.get(p.gbId, {}).get('tJoin', 0)
                if p.dailyActivationRewardDict.get(i, None) == True:
                    text = gameStrings.PARTNER_REWARD_ALREADY
                elif p.dailyActivationRewardDict.get(i, None) == None or self.judgeJoinTime(tJoin):
                    bGray = True
                rewardItem.state.text = text
                items = clientUtils.genItemBonus(bonusId)
                itemId, num = items[0]
                gfxItem = uiUtils.getGfxItemById(itemId, num)
                gfxItem['state'] = uiConst.ITEM_GRAY if bGray else uiConst.ITEM_NORMAL
                rewardItem.slot.setItemSlotData(gfxItem)
                rewardItem.slot.dragable = False
                arrow = getattr(self.widget.rewardMc, 'arrow' + str(i), None)
                if arrow:
                    arrowState = 'dislight'
                    if allPoint == lastPoint:
                        arrowState = 'dislight'
                    elif allPoint > lastPoint and allPoint < aPoint:
                        arrowState = 'half'
                    elif allPoint >= aPoint:
                        arrowState = 'light'
                    arrow.gotoAndStop(arrowState)
                lastPoint = aPoint

            activationLimit = PCD.data.get('activationLimit', 40)
            self.widget.rewardMc.activePointLimitTxt.text = gameStrings.PARTNER_REWARD_ACTIVE_LIMIT % (activationLimit / ACTIVATION_RATE,)
            self.refreshGetBtnState()
            self.widget.rewardMc.actStateBtn.enabled = bool(p.partnerNUID)

    def setPlayerNameMc(self, mc, data, upDown = 'up'):
        if not self.hasBaseData():
            return
        else:
            if mc and data:
                p = BigWorld.player()
                gbId = data.get('gbId', 0)
                school = data.get('school', 0)
                labelName = 'self' if gbId == p.gbId else 'other'
                mc.gotoAndStop(labelName)
                nameContent = None
                nameContent = getattr(mc, 'nameContent2', None) if gbId == p.gbId else getattr(mc, 'nameContent1', None)
                if nameContent:
                    nameContent.gotoAndStop(upDown)
                    nameContent.schoolMc.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(school, ''))
                    nameContent.roleNameTxt.text = data.get('roleName', '')
                    nameContent.lvTxt.text = data.get('level', '')
                menuParam = {'roleName': data.get('roleName', ''),
                 'gbId': data.get('gbId', 0)}
                MenuManager.getInstance().registerMenuById(mc, uiConst.MENU_PARTNER_SHOW, menuParam)
                mc.visible = True
            return

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False

    def handleRollOverPhoto(self, *arg):
        if not self.hasBaseData():
            return
        else:
            e = ASObject(arg[3][0])
            t = e.target
            pTag = t.pTag
            p = BigWorld.player()
            partnerInfo = self.calcPartnerInfo()
            if pTag < len(partnerInfo):
                t.gotoAndStop('over')
                playerName = getattr(self.widget, 'playerName' + str(pTag), None)
                self.setPlayerNameMc(playerName, partnerInfo[pTag], 'over')
            else:
                t.gotoAndStop('disable')
            return

    def handleRollOutPhoto(self, *arg):
        if not self.hasBaseData():
            return
        else:
            e = ASObject(arg[3][0])
            t = e.target
            pTag = t.pTag
            p = BigWorld.player()
            partnerInfo = self.calcPartnerInfo()
            if pTag < len(partnerInfo):
                t.gotoAndStop('up')
                playerName = getattr(self.widget, 'playerName' + str(pTag), None)
                self.setPlayerNameMc(playerName, partnerInfo[pTag], 'up')
            else:
                t.gotoAndStop('disable')
            return

    def refreshPhotoByGbId(self, gbId):
        if self.hasBaseData():
            p = BigWorld.player()
            orderIndex = p.partner.get(gbId, {}).get('orderIndex', 0)
            if orderIndex and orderIndex - 1 < len(p.partner):
                if gbId in p.partnerEquipment:
                    self.takePhoto(orderIndex - 1, p.partnerEquipment.get(gbId, {}))
                elif p.gbId == gbId:
                    self.takePhoto(orderIndex - 1, {}, True)

    def takePhoto(self, num, info, isPlayer = False):
        if not self.hasBaseData():
            return
        else:
            p = BigWorld.player()
            if num >= len(p.partner):
                return
            aspect = info.get('aspect', None)
            physique = info.get('physique', None)
            avatarConfig = info.get('avatarConfig', None)
            if isPlayer:
                aspect = p.aspect
                physique = p.physique
                avatarConfig = p.avatarConfig
            if not aspect or not physique or not avatarConfig:
                return
            modelId = charRes.transDummyBodyType(physique.sex, physique.bodyType, True)
            showFashion = self.isShowFashion(aspect)
            self.photoArr[num].startCaptureRes(modelId, aspect, physique, avatarConfig, ('1101',), showFashion)
            self.setLoadingMcVisible(True, num)
            return

    def isShowFashion(self, aspect):
        for partName in charRes.PARTS_ASPECT_FASHION:
            if partName != 'fashionHead' and getattr(aspect, partName, None):
                return True

        return False

    def _onGetBtnClick(self, e):
        BigWorld.player().cell.applyPartnerActivationReward()

    def _onActStateBtnClick(self, e):
        if self.hasBaseData():
            if self.widget.actMc.visible:
                self.widget.actMc.visible = False
            else:
                self.showActivePointMc()

    def calcPartnerInfo(self):
        p = BigWorld.player()
        pData = []
        for k, v in p.partner.iteritems():
            v['gbId'] = k
            pData.append(v)

        pData.sort(key=lambda k: k.get('orderIndex'))
        return pData

    def setLoadingMcVisible(self, visible, num):
        if not self.hasBaseData():
            return
        else:
            p = BigWorld.player()
            if num >= len(p.partner):
                return
            loadingMc = getattr(self.widget, 'loadingMc' + str(num), None)
            if loadingMc:
                loadingMc.visible = visible
            return

    def endCapture(self):
        for photo in self.photoArr:
            photo.endCapture()

    def calcAllActivePoint(self):
        point = 0
        p = BigWorld.player()
        for k, v in p.partner.iteritems():
            tOff = v.get('tOff', 0)
            isOn = v.get('isOn', False)
            if isOn or not tOff or utils.isSameDay(tOff):
                point += v.get('activation')

        return point

    def showActivePointMc(self):
        if self.hasBaseData():
            p = BigWorld.player()
            self.widget.actMc.visible = True
            partnerInfo = self.calcPartnerInfo()
            for x in xrange(0, const.PARTNER_MAX_NUM):
                gbId = None
                if x < len(partnerInfo):
                    gbId = partnerInfo[x].get('gbId', '')
                color = SELF_NAME_COLOR if p.gbId == gbId else OTHER_NAME_COLOR
                roleName = getattr(self.widget.actMc, 'roleName' + str(x), None)
                if roleName:
                    if x < len(partnerInfo):
                        roleName.visible = True
                        roleName.htmlText = uiUtils.toHtml(partnerInfo[x].get('roleName', ''), color)
                    else:
                        roleName.visible = False
                activePointTxt = getattr(self.widget.actMc, 'activePointTxt' + str(x), None)
                if activePointTxt:
                    if x < len(partnerInfo):
                        activePointTxt.visible = True
                        point = 0
                        tOff = partnerInfo[x].get('tOff', 0)
                        isOn = partnerInfo[x].get('isOn', False)
                        if isOn or not tOff or utils.isSameDay(tOff):
                            point = partnerInfo[x].get('activation', 0)
                        activePointTxt.htmlText = uiUtils.toHtml(str(point / ACTIVATION_RATE), color)
                    else:
                        activePointTxt.visible = False
                roleIcon = getattr(self.widget.actMc, 'roleIcon' + str(x), None)
                if roleIcon:
                    if x < len(partnerInfo):
                        roleIcon.visible = True
                        roleIcon.icon.imgType = 2
                        roleIcon.icon.fitSize = True
                        fVal = None
                        if gbId == p.gbId:
                            fVal = p
                        else:
                            fVal = p.friend.get(gbId, None)
                        roleIcon.icon.url = p._getFriendPhoto(fVal)
                    else:
                        roleIcon.visible = False

            self.widget.actMc.allPoint.text = self.calcAllActivePoint() / ACTIVATION_RATE

    def refreshGetBtnState(self):
        if self.hasBaseData():
            p = BigWorld.player()
            canGetReward = False
            if p.dailyActivationRewardDict:
                for k, v in p.dailyActivationRewardDict.iteritems():
                    if v == False:
                        canGetReward = True

            selfActPoint = p.partner.get(p.gbId, {}).get('activation', 0)
            activationLimit = PCD.data.get('activationLimit', 40)
            tJoin = p.partner.get(p.gbId, {}).get('tJoin', 0)
            self.widget.rewardMc.getBtn.enabled = bool(p.partnerNUID) and selfActPoint >= activationLimit and canGetReward and not self.judgeJoinTime(tJoin)

    def handleClickStage(self, *arg):
        e = ASObject(arg[3][0])
        t = e.target
        if self.hasBaseData() and self.widget.actMc.visible and e.target != self.widget.actMc:
            if e.target != self.widget.rewardMc.actStateBtn:
                self.widget.actMc.visible = False

    def addPushMessage(self):
        BigWorld.player().cell.queryPartnersEquipment()
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_PARTNER_SHOW, {'click': self.pushMessageClick})
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_PARTNER_SHOW)

    def pushMessageClick(self):
        self.show()

    def isPlayerActivationEnough(self):
        p = BigWorld.player()
        selfActPoint = p.partner.get(p.gbId, {}).get('activation', 0)
        activationLimit = PCD.data.get('activationLimit', 40)
        if selfActPoint < activationLimit:
            return False
        else:
            return True

    def close(self):
        pass

    def judgeJoinTime(self, tJoin):
        if tJoin <= 1499904000:
            return False
        return utils.isSameDay(tJoin)
