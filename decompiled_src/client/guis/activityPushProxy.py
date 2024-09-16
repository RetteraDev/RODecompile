#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activityPushProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import utils
import gameglobal
import uiConst
import uiUtils
import clientUtils
import gametypes
from guis import tipUtils
from callbackHelper import Functor
from item import Item
from ui import gbk2unicode
from uiProxy import UIProxy
from guis import activityFactory
from cdata import activity_reverse_data as ARD
from data import special_award_data as SAD
from data import stats_target_data as STD
from data import item_data as ID
from cdata import font_config_data as FCD
from data import bonus_data as BD
from data import login_time_reward_data as LTRD
from data import sys_config_data as SCD

class ActivityPushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivityPushProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'applyReward': self.onApplyReward,
         'initData': self.onInitData,
         'gotoSchedule': self.onGotoSchedule}
        self.mediator = None
        self.detailId = 0
        self.erefType = 0
        self.itemBonus = []
        self.isFirst = True
        self.actFactory = activityFactory.getInstance()
        self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GET_REWARD, {'click': self.show,
         'refresh': self.refresh})

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ACTIVITY_PUSH:
            self.mediator = mediator

    def refresh(self):
        pass

    def show(self):
        if self.mediator:
            return
        self.erefType, self.detailId = gameglobal.rds.ui.pushMessage.getLastData(uiConst.MESSAGE_TYPE_GET_REWARD).get('data', (0, 0))
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ACTIVITY_PUSH)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ACTIVITY_PUSH)

    def reset(self):
        super(self.__class__, self).reset()
        self.detailId = 0
        self.erefType = 0
        self.itemBonus = []
        self.isFirst = True

    def isInMsg(self, data):
        if (uiConst.MESSAGE_TYPE_GET_REWARD, {'data': data}) in gameglobal.rds.ui.pushMessage.showBirdMsg:
            return True
        for item in gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_GET_REWARD):
            if item['data'] == data:
                return True

        return False

    def onClickClose(self, *arg):
        self.hide()

    def onGotoSchedule(self, *arg):
        if self.erefType == uiConst.ACT_STAT:
            actId = ARD.data[uiConst.ACT_STAT].get(self.detailId, 0)
        elif self.erefType == uiConst.ACT_SPECIAL_AWD:
            pass

    def onApplyReward(self, *arg):
        p = BigWorld.player()
        if self.erefType == uiConst.ACT_STAT:
            p.cell.applyStatsReward(self.detailId)
        elif self.erefType == uiConst.ACT_SPECIAL_AWD:
            p.cell.applySpecialAward(self.detailId)

    def getActName(self, id):
        actIns = self.actFactory.actIns
        if actIns.has_key(id):
            ins = self.actFactory.actIns[id]
            return ins.getName()
        else:
            return ''

    def onInitData(self, *arg):
        movie = arg[0]
        obj = movie.CreateObject()
        itemList = self.movie.CreateArray()
        activityData = {}
        if self.erefType == uiConst.ACT_STAT:
            activityData = STD.data.get(self.detailId, None)
            actId = ARD.data[uiConst.ACT_STAT].get(self.detailId, 0)
            actName = self.getActName(actId)
            actType = activityData['type']
            if activityData:
                obj.SetMember('type', GfxValue(actType))
                if actType == 1:
                    obj.SetMember('actName', GfxValue(gbk2unicode(actName + '-' + activityData['name'])))
                else:
                    obj.SetMember('actName', GfxValue(activityData['name']))
                if activityData.get('cashBonus', 0) != 0:
                    obj.SetMember('cash', GfxValue(activityData.get('cashBonus', 0)))
                if activityData.get('expBonus', 0) != 0:
                    obj.SetMember('exp', GfxValue(activityData.get('expBonus', 0)))
        elif self.erefType == uiConst.ACT_SPECIAL_AWD:
            activityData = SAD.data.get(self.detailId, None)
            actId = ARD.data[uiConst.ACT_SPECIAL_AWD].get(self.detailId, 0)
            actName = self.getActName(actId)
            if activityData:
                obj.SetMember('actName', GfxValue(gbk2unicode(actName + '-' + activityData['desc'])))
        bonusId = activityData.get('bonusId', 0)
        itemBonus = clientUtils.genItemBonus(bonusId)
        self.itemBonus = itemBonus
        if itemBonus:
            i = 0
            for item in itemBonus:
                ar = self.movie.CreateArray()
                path = uiUtils.getItemIconFile40(item[0])
                ar.SetElement(0, GfxValue(path))
                ar.SetElement(1, GfxValue(item[1]))
                quality = ID.data.get(item[0], {}).get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                ar.SetElement(2, GfxValue(color))
                ar.SetElement(3, GfxValue(item[0]))
                itemList.SetElement(i, ar)
                i += 1

            obj.SetMember('icon', itemList)
        return obj

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        id = int(key[17:])
        return gameglobal.rds.ui.inventory.GfxToolTip(Item(self.itemBonus[id][0]))

    def showLoginTimeReward(self, loginId):
        if not self.isFirst:
            return
        self.isFirst = False
        if not gameglobal.rds.configData.get('enableLoginReward', False):
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_LOGIN_AWARD_PUSH)
            return
        loginData = LTRD.data.get(loginId, {})
        bonusId = loginData.get('bonusId', 0)
        fixedBonus = BD.data[bonusId].get('fixedBonus', ())
        fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        if fixedBonus:
            itemId = fixedBonus[0][1]
        else:
            itemId = 0
        itemData = tipUtils.getItemInfoById(itemId)
        msg = loginData.get('content', gameStrings.TEXT_ACTIVITYPUSHPROXY_174)
        title = SCD.data.get('LOGIN_TIME_TITLE', gameStrings.TEXT_ACTIVITYPUSHPROXY_175)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.pushConfirm, yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noCallback=self.pushCancel, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1, itemData=itemData, title=title, isModal=False)

    def showLoginPush(self, loginId):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_LOGIN_AWARD_PUSH)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_LOGIN_AWARD_PUSH, {'click': Functor(self.showLoginTimeReward, loginId)})

    def pushCancel(self):
        self.isFirst = True

    def pushConfirm(self):
        self.isFirst = True
        p = BigWorld.player()
        p.base.applyLoginTimeReward()
