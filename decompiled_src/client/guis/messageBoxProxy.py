#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/messageBoxProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gamelog
import gametypes
import clientcom
import re
import keys
import random
import utils
import const
from callbackHelper import Functor
from guis import uiConst
from guis.ui import unicode2gbk
from guis.ui import gbk2unicode
from guis.uiProxy import UIProxy
from guis.asObject import ASObject
from gamestrings import gameStrings
from data import sys_config_data as SCD
from cdata import item_fame_score_cost_data as IFSCD
from cdata import item_parentId_data as IPD
from cdata import item_coin_dikou_cost_data as ICDCD

class MBButton(object):

    def __init__(self, buttonTitle = 'empty', onClickCallback = None, enable = True, dismissOnClick = True, fastKey = keys.KEY_Y, forbidFastKey = False):
        self.title = buttonTitle
        self.onClickCallback = onClickCallback
        self.enable = enable
        self.dismissOnClick = dismissOnClick
        self.fastKey = fastKey
        self.forbidFastKey = forbidFastKey


class MessageBoxProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MessageBoxProxy, self).__init__(uiAdapter)
        self.modelMap = {'getMsgData': self.onGetMsgData,
         'clickBtn': self.onClickBtn,
         'completeCountDown': self.onCompleteCountDown,
         'getPhone': self.onGetPhone,
         'getQueueDesc': self.onGetQueueDesc,
         'quitQueue': self.onQuitQueue,
         'clickLink': self.onClickLink,
         'clickConfirm': self.onClickConfirm,
         'clickCancel': self.onClickCancel,
         'clickRefresh': self.onClickRefresh,
         'getQueueRefreshLimit': self.onGetQueueRefreshLimit,
         'checkBox': self.onCheckBox,
         'dismissMsgBox': self.onDismissMsgBox,
         'counterChange': self.onCounterChange,
         'clickBtnMin': self.onClickBtnMin}
        self.loadeds = {}
        self.loadings = {}
        self.reset()
        self.msgBoxShowMap = {}
        self.msgBoxType = ''
        self.isShowCheckBox = False
        self.checkBoxSelected = False
        self.checkText = ''
        self.checkOnceMap = {}
        self.checkOnceType = None
        self.isWeeklyCheckOnce = False
        self.initWeeklyCheckOnceType()
        self.counterCallback = None

    def reset(self):
        self.queueCnt = 0
        self.queueMsgBoxId = 0
        self.queueMed = None
        self.queryCallbackId = 0
        self.checkCallbackId = 0
        self.msgBoxShowMap = {}
        self.msgBoxType = ''
        self.tipsDesc = ''
        self.isShowCheckBox = False
        self.checkBoxSelected = False
        self.checkText = ''

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_QUEUE_TIP:
            self.queueMed = mediator
            self.checkConnectServer()
            from guis import uiUtils
            _, channelId = uiUtils.getCCRoom()
            self.loadMicCard(channelId)

    def initWeeklyCheckOnceType(self):
        from appSetting import Obj as AppSettings
        saveStr = AppSettings.get(keys.SET_MSG_BOX_WEEKLY_CHECK_ONCE, '')
        for recordStr in saveStr.split(','):
            if recordStr:
                checkType, timeStr = recordStr.split('_')
                if utils.isSameWeek(utils.getNow(), int(timeStr)):
                    self.checkOnceMap[int(checkType)] = True

    def _hasQueryCallback(self):
        return self.queryCallbackId > 0

    def cancelQueryCallback(self):
        if self.queryCallbackId:
            BigWorld.cancelCallback(self.queryCallbackId)
            self.queryCallbackId = 0

    def checkConnectServer(self):
        self.cancelQueryCallback()
        self.checkCallbackId = BigWorld.callback(random.randint(20, 30), self.checkConnectServer)
        self.onClickRefresh()

    def cancelCheckCallback(self):
        if self.checkCallbackId:
            BigWorld.cancelCallback(self.checkCallbackId)
            self.checkCallbackId = 0

    def onClickRefresh(self, *arg):
        gamelog.debug('@hjx queue#onClickRefresh:', self.queryCallbackId)
        if self._hasQueryCallback():
            self.cancelQueryCallback()
        self.queryCallbackId = BigWorld.callback(10, self.queryTimeout)
        p = BigWorld.player()
        if p and p.base and hasattr(p.base, 'queryQueuePlace'):
            p.base.queryQueuePlace()

    def onCheckBox(self, *arg):
        checkBoxSelect = int(arg[3][0].GetBool())
        self.checkBoxSelected = checkBoxSelect
        if self.checkOnceType:
            self.checkOnceMap[self.checkOnceType] = checkBoxSelect
            if self.isWeeklyCheckOnce:
                self.saveWeeklyCheckOnce()
        if self.msgBoxType:
            self.msgBoxShowMap[self.msgBoxType] = not checkBoxSelect

    def saveWeeklyCheckOnce(self):
        from appSetting import Obj as AppSettings
        weeklyCheckDic = {}
        weeklyCheckDic[self.checkOnceType] = utils.getNow()
        for saveStr in AppSettings.get(keys.SET_MSG_BOX_WEEKLY_CHECK_ONCE, '').split(','):
            if saveStr:
                msgType, timeStr = saveStr.split('_')
                if utils.isSameWeek(utils.getNow(), int(timeStr)):
                    weeklyCheckDic[int(msgType)] = int(timeStr)

        saveStrList = [ '%d_%d' % (msgType, weeklyCheckDic[msgType]) for msgType in weeklyCheckDic ]
        AppSettings[keys.SET_MSG_BOX_WEEKLY_CHECK_ONCE] = ','.join(saveStrList)
        AppSettings.save()

    def hasChecked(self, msgBoxType):
        return not self.msgBoxShowMap.get(msgBoxType, True)

    def setTipsDesc(self, desc):
        self.tipsDesc = desc
        if self.queueMed:
            self.queueMed.Invoke('setTipsDesc', GfxValue(gbk2unicode(desc)))

    def queryTimeout(self):
        gamelog.debug('@hjx queue#queryTimeout:', gameglobal.rds.GameState, self.queryCallbackId, self.queueMed)
        if gameglobal.rds.GameState == gametypes.GS_LOGIN:
            self.cancelCheckCallback()
            self.cancelQueryCallback()
            return
        elif not self.queueMed:
            return
        else:
            self.showMsgBox(gameStrings.TEXT_MESSAGEBOXPROXY_172, callback=self._doQuit)
            self.queueMed = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_QUEUE_TIP)
            return

    def _doQuit(self):
        from guis import uiUtils
        uiUtils.onQuit()

    def onGetQueueRefreshLimit(self, *arg):
        queueRereshLimit = SCD.data.get('queueRereshLimit', 20)
        return GfxValue(queueRereshLimit)

    def onQueryQueuePlace(self, queueCnt):
        gamelog.debug('@hjx queue#onQueryQueuePlace:', self.queryCallbackId, self.queueMed, queueCnt)
        self.cancelQueryCallback()
        if queueCnt <= 0:
            return
        self.refreshQueueCnt(queueCnt)

    def onGetMsgData(self, *arg):
        from guis import uiUtils
        multiId = int(arg[3][0].GetString())
        movie = arg[0]
        messageBox = movie.CreateObject()
        messageBoxBtns = movie.CreateArray()
        buttonEnbales = movie.CreateArray()
        title, content, buttonList, freeze, repeat, types, countDownFunctor, linkOverTip, repeatText, itemData, itemFameData, style, defaultInput, inputMax, bonusIcon, textAlign, needDissMissCallBack, canEsc, counterData, counterRange, minCallback = self.loadings.pop(multiId)
        self.loadeds[multiId] = (buttonList,
         types,
         countDownFunctor,
         needDissMissCallBack,
         canEsc,
         minCallback)
        interval = 1000.0
        repeat = 3 if freeze else repeat
        if repeat != 0:
            timer = movie.CreateArray()
            timer.SetElement(0, GfxValue(interval))
            timer.SetElement(1, GfxValue(repeat))
            messageBox.SetMember('timer', timer)
        for i, btn in enumerate(buttonList):
            messageBoxBtns.SetElement(i, GfxValue(gbk2unicode(btn.title)))
            buttonEnbales.SetElement(i, GfxValue(btn.enable))

        messageBox.SetMember('title', GfxValue(gbk2unicode(title)))
        messageBox.SetMember('contenttext', GfxValue(gbk2unicode(content)))
        messageBox.SetMember('repeatText', GfxValue(gbk2unicode(repeatText)))
        messageBox.SetMember('btnList', messageBoxBtns)
        messageBox.SetMember('btnEnable', buttonEnbales)
        messageBox.SetMember('linkOverTip', GfxValue(gbk2unicode(linkOverTip)))
        messageBox.SetMember('isShowCheckBox', GfxValue(self.isShowCheckBox))
        messageBox.SetMember('checkText', GfxValue(gbk2unicode(self.checkText)))
        messageBox.SetMember('type', GfxValue(style))
        messageBox.SetMember('defaultInput', GfxValue(defaultInput))
        messageBox.SetMember('inputMax', GfxValue(inputMax))
        messageBox.SetMember('textAlign', GfxValue(textAlign))
        messageBox.SetMember('needDissMissCallBack', GfxValue(needDissMissCallBack))
        messageBox.SetMember('canEsc', GfxValue(canEsc))
        messageBox.SetMember('minBtnVisible', GfxValue(bool(minCallback)))
        if itemData:
            if type(itemData) != list:
                messageBox.SetMember('itemData', uiUtils.dict2GfxDict(itemData, True))
            else:
                messageBox.SetMember('itemData', uiUtils.array2GfxAarry(itemData, True))
        if itemFameData:
            itemFameTxt = {}
            if itemFameData['deltaNum'] and itemFameData['deltaNum'] > 0:
                deltaNum = itemFameData['deltaNum']
                itemId = itemFameData['itemId']
                itemIds = IPD.data.get(itemId, [])
                itemIds.append(itemId)
                if itemFameData.has_key('type'):
                    moneyType = itemFameData['type']
                    if moneyType == 'tianbi':
                        for id in itemIds:
                            if ICDCD.data.has_key(id):
                                itemCoinData = ICDCD.data.get(id, [])
                                itemCost = itemCoinData[1]

                        totalCost = deltaNum * itemCost
                        itemFameTxt['line1'] = gameStrings.ITEM_FAME_INSTANTLY_PURCHASE_1
                        itemFameTxt['line2'] = gameStrings.ITEM_YUNBI_INSTANTLY_PURCHASE_3 % totalCost
                else:
                    for id in itemIds:
                        if IFSCD.data.has_key(id):
                            itemFameData = IFSCD.data.get(id, {})
                            itemCost = itemFameData.get(const.YUN_CHUI_JI_FEN_FAME_ID, 0)

                    totalCost = deltaNum * itemCost
                    itemFameTxt['line1'] = gameStrings.ITEM_FAME_INSTANTLY_PURCHASE_1
                    itemFameTxt['line2'] = gameStrings.ITEM_FAME_INSTANTLY_PURCHASE_2 % totalCost
            from guis import uiUtils
            messageBox.SetMember('itemFameTxt', uiUtils.dict2GfxDict(itemFameTxt, True))
        if bonusIcon:
            from guis import uiUtils
            messageBox.SetMember('bonusIcon', uiUtils.dict2GfxDict(bonusIcon, True))
        messageBox.SetMember('counterData', uiUtils.dict2GfxDict(counterData, True))
        messageBox.SetMember('counterRange', uiUtils.array2GfxAarry(counterRange))
        messageBox.SetMember('isWeeklyCheckOnce', GfxValue(self.isWeeklyCheckOnce))
        return messageBox

    def onCompleteCountDown(self, *arg):
        multiId = int(arg[3][0].GetString())
        _, _, countDownFunctor, needDissMissCallBack, _, _ = self.loadeds.get(multiId, (None, None, None, None, None, None))
        countDownFunctor() if countDownFunctor else None
        self.dismiss(multiId, needDissMissCallBack=needDissMissCallBack)

    def onClickKey(self, multiId, key):
        buttonList = self.loadeds[multiId][0]
        for button in buttonList:
            if button.fastKey == key:
                if button.forbidFastKey:
                    return True
                if button.enable and callable(button.onClickCallback):
                    button.onClickCallback()
                else:
                    gamelog.debug('zt: can not response to click, enable=', button.enable, 'callable=', callable(button.onClickCallback))
                if button.dismissOnClick:
                    self.dismiss(multiId, needDissMissCallBack=False)
                return True

        return False

    def onClickBtn(self, *arg):
        ids = arg[3][0].GetString()
        if ids == '':
            return
        idx = int(ids)
        multiId = int(arg[3][1].GetString())
        type = int(arg[3][2].GetNumber())
        buttonList = self.loadeds[multiId][0]
        button = buttonList[idx]
        if button.enable and callable(button.onClickCallback):
            if type == uiConst.MSG_BOX_INPUT_INT:
                inputNum = int(arg[3][3].GetNumber())
                button.onClickCallback(inputNum)
            elif type == uiConst.MSG_BOX_INPUT_STRING:
                inputStr = unicode2gbk(arg[3][3].GetString())
                button.onClickCallback(inputStr)
            elif type == uiConst.MSG_BOX_COUNTER:
                cnt = int(arg[3][3].GetNumber())
                button.onClickCallback(cnt)
            else:
                button.onClickCallback()
        else:
            gamelog.debug('zt: can not response to click, enable=', button.enable, 'callable=', callable(button.onClickCallback))
        if multiId == gameglobal.rds.ui.funcNpc.msgBoxId:
            gameglobal.rds.ui.funcNpc.msgBoxId = 0
        if button.dismissOnClick:
            self.dismiss(multiId, needDissMissCallBack=False)

    def onClickBtnMin(self, *args):
        multiId = int(args[3][0].GetString())
        minClickCallBack = self.loadeds[multiId][5]
        if minClickCallBack:
            minClickCallBack()
        self.dismiss(multiId, needDissMissCallBack=False)

    def dismiss(self, msgBoxId = 0, isUnLoadedId = True, needDissMissCallBack = True):
        if msgBoxId == gameglobal.rds.ui.funcNpc.msgBoxId:
            gameglobal.rds.ui.funcNpc.msgBoxId = 0
        index = len(self.loadeds) - 1
        if index < 0 and not self.loadings:
            return
        if msgBoxId:
            if isUnLoadedId:
                if msgBoxId in self.loadeds:
                    buttonList = self.loadeds[msgBoxId][0]
                    button = buttonList[len(buttonList) - 1]
                    if button.enable and callable(button.onClickCallback) and needDissMissCallBack:
                        button.onClickCallback()
                    self.uiAdapter.unLoadWidget(msgBoxId)
                    del self.loadeds[msgBoxId]
                    if msgBoxId in gameglobal.rds.ui.inventory.dropMBIds:
                        gameglobal.rds.ui.inventory.dropMBIds.remove(msgBoxId)
                elif msgBoxId in self.loadings:
                    self.uiAdapter.unLoadWidget(msgBoxId)
                    del self.loadings[msgBoxId]
            else:
                loadeds = self.loadeds.copy()
                for id in loadeds:
                    if loadeds[id][1] == msgBoxId:
                        self.uiAdapter.unLoadWidget(id)
                        del self.loadeds[id]
                        if id in gameglobal.rds.ui.inventory.dropMBIds:
                            gameglobal.rds.ui.inventory.dropMBIds.remove(id)

        else:
            for id in self.loadings:
                self.uiAdapter.unLoadWidget(id)

            for id in self.loadeds:
                self.uiAdapter.unLoadWidget(id)

            self.loadeds = {}
            self.loadings = {}
            gameglobal.rds.ui.inventory.dropMBIds = []
        gameglobal.rds.ui.callTeammate.clearGbId()

    def getCheckOnceData(self, type):
        return self.checkOnceMap.get(type, False)

    def show(self, isModal, title, content, buttonList, freeze = False, repeat = 0, type = 0, countDownFunctor = None, linkOverTip = None, repeatText = '', msgType = '', isShowCheckBox = False, checkText = '', itemData = None, itemFameData = None, style = 0, defaultInput = 0, inputMax = 0, bonusIcon = None, textAlign = 'center', checkOnceType = None, isWeeklyCheckOnce = False, forbidFastKey = False, needDissMissCallBack = True, canEsc = True, counterData = None, counterRange = (0, 0), counterChangeCallback = None, minCallback = None):
        self.checkOnceType = checkOnceType
        self.isWeeklyCheckOnce = isWeeklyCheckOnce
        self.isShowCheckBox = isShowCheckBox
        self.checkText = checkText
        self.checkBoxSelected = False
        self.counterCallback = counterChangeCallback
        length = len(buttonList)
        if length < 3:
            for i in xrange(length):
                if i == 0:
                    if not forbidFastKey:
                        buttonList[i].title = buttonList[i].title + '(Y)'
                    buttonList[i].fastKey = keys.KEY_Y
                    buttonList[i].forbidFastKey = forbidFastKey
                elif i == 1:
                    if not forbidFastKey:
                        buttonList[i].title = buttonList[i].title + '(N)'
                    buttonList[i].fastKey = keys.KEY_N
                    buttonList[i].forbidFastKey = forbidFastKey

        if msgType:
            self.msgBoxType = msgType
            if msgType in self.msgBoxShowMap:
                if not self.msgBoxShowMap[msgType]:
                    buttonList[0].onClickCallback()
                    return
            else:
                self.msgBoxShowMap[msgType] = True
        if content.find('uiShow:') != -1 and isModal == False:
            widgetId = uiConst.WIDGET_MESSAGEBOX_LOW
        else:
            widgetId = uiConst.WIDGET_MESSAGEBOX
        layoutType = uiConst.LAYOUT_NPC_FUNC if gameglobal.CURRENT_WINDOW_STYLE == gameglobal.WINDOW_STYLE_CHAT else uiConst.LAYOUT_DEFAULT
        multiId = self.uiAdapter.loadWidget(widgetId, isModal, layoutType=layoutType)
        self.loadings[multiId] = (title,
         content,
         tuple(buttonList),
         freeze,
         repeat,
         type,
         countDownFunctor,
         linkOverTip,
         repeatText,
         itemData,
         itemFameData,
         style,
         defaultInput,
         inputMax,
         bonusIcon,
         textAlign,
         needDissMissCallBack,
         canEsc,
         counterData,
         counterRange,
         minCallback)
        return multiId

    def showMsgBox(self, msg, callback = None, hideBtn = False, autoHide = 0, yesBtnText = gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, msgType = '', isShowCheckBox = False, itemData = None, itemFameData = None, style = 0, bonusIcon = None, showTitle = '', isModal = True, textAlign = 'center', checkOnceType = None, needDissMissCallBack = True):
        buttons = [] if hideBtn else [MBButton(yesBtnText, callback, fastKey=keys.KEY_Y)]
        return self.show(isModal, showTitle, msg, buttons, False, autoHide, msgType=msgType, isShowCheckBox=isShowCheckBox, itemData=itemData, itemFameData=itemFameData, style=style, bonusIcon=bonusIcon, textAlign=textAlign, checkOnceType=checkOnceType, needDissMissCallBack=needDissMissCallBack)

    def showYesNoMsgBox(self, msg, yesCallback = None, yesBtnText = gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noCallback = None, noBtnText = gameStrings.TEXT_PLAYRECOMMPROXY_494_1, isModal = True, linkOverTip = '', msgType = '', isShowCheckBox = False, checkText = '', itemData = None, itemFameData = None, style = 0, title = '', bonusIcon = None, repeat = 0, repeatText = '', yesBtnEnable = True, countDownFunctor = None, textAlign = 'center', checkOnceType = None, isWeeklyCheckOnce = False, forbidFastKey = False, needDissMissCallBack = True, canEsc = True, minCallback = None):
        buttons = [MBButton(yesBtnText, yesCallback, enable=yesBtnEnable, fastKey=keys.KEY_Y, forbidFastKey=forbidFastKey), MBButton(noBtnText, noCallback, fastKey=keys.KEY_N, forbidFastKey=forbidFastKey)]
        return self.show(isModal, title, msg, buttons, linkOverTip=linkOverTip, msgType=msgType, repeat=repeat, repeatText=repeatText, isShowCheckBox=isShowCheckBox, checkText=checkText, itemData=itemData, itemFameData=itemFameData, style=style, bonusIcon=bonusIcon, countDownFunctor=countDownFunctor, textAlign=textAlign, checkOnceType=checkOnceType, isWeeklyCheckOnce=isWeeklyCheckOnce, forbidFastKey=forbidFastKey, needDissMissCallBack=needDissMissCallBack, canEsc=canEsc, minCallback=minCallback)

    def showYesNoInput(self, msg, yesCallback = None, yesBtnText = gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noCallback = None, noBtnText = gameStrings.TEXT_PLAYRECOMMPROXY_494_1, title = '', defaultInput = 0, inputMax = 0, isModal = True, textAlign = 'center', style = uiConst.MSG_BOX_INPUT_INT, dismissOnClick = True, checkOnecType = None):
        buttons = [MBButton(yesBtnText, yesCallback, fastKey=keys.KEY_Y, dismissOnClick=dismissOnClick), MBButton(noBtnText, noCallback, fastKey=keys.KEY_N)]
        return self.show(isModal, title, msg, buttons, style=style, defaultInput=defaultInput, inputMax=inputMax, textAlign=textAlign, checkOnceType=checkOnecType)

    def showAlertBox(self, msg, btnText = gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, isModal = True, linkOverTip = None, itemData = None, itemFameData = None, style = 0, repeat = 0, textAlign = 'center', title = '', checkOnceType = None):
        buttons = [MBButton(btnText, None, fastKey=keys.KEY_Y)]
        return self.show(isModal, title, msg, buttons, linkOverTip=linkOverTip, itemData=itemData, itemFameData=itemFameData, style=style, repeat=repeat, textAlign=textAlign, checkOnceType=checkOnceType)

    def showCounterMsgBox(self, msg, yesCallback = None, yesBtnText = gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noCallback = None, noBtnText = gameStrings.TEXT_PLAYRECOMMPROXY_494_1, title = '', counterData = None, counterRange = (0, 0), isModal = True, style = uiConst.MSG_BOX_COUNTER, countDownFunctor = None, counterChangeCallback = None):
        buttons = [MBButton(yesBtnText, yesCallback), MBButton(noBtnText, noCallback)]
        return self.show(isModal, title, msg, buttons, style=style, counterData=counterData, counterRange=counterRange, forbidFastKey=True, countDownFunctor=countDownFunctor, counterChangeCallback=counterChangeCallback)

    def showItemCheckMsgBox(self, msg, yesCallback = None, yesBtnText = gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noCallback = None, noBtnText = gameStrings.TEXT_PLAYRECOMMPROXY_494_1, title = '', itemData = None, checkText = ''):
        buttons = [MBButton(yesBtnText, yesCallback), MBButton(noBtnText, noCallback)]
        return self.show(True, title, msg, buttons, style=uiConst.MSG_BOX_ITEM_CHECK, itemData=itemData, checkText=checkText, isShowCheckBox=True)

    def showRichTextMsgBox(self, msg, yesCallback = None, yesBtnText = gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noCallback = None, noBtnText = gameStrings.TEXT_PLAYRECOMMPROXY_494_1, title = '', itemData = None, checkOnceType = None, canEsc = True, textAlign = 'left'):
        buttons = [MBButton(yesBtnText, yesCallback), MBButton(noBtnText, noCallback)]
        return self.show(True, title, msg, buttons, style=uiConst.MSG_BOX_RICH_TEXT, isShowCheckBox=True, textAlign=textAlign, canEsc=canEsc, checkOnceType=checkOnceType)

    def refreshQueueCnt(self, queueCnt):
        self.queueCnt = queueCnt
        queueNotifyCnt = SCD.data.get('queueNotifyCnt', 100)
        if self.queueCnt == queueNotifyCnt:
            gameglobal.rds.sound.playSound(gameglobal.SD_458)
        if self.queueMed:
            self.queueMed.Invoke('refreshQueueCnt')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_QUEUE_TIP, True)

    def onGetPhone(self, *arg):
        BigWorld.player().base.getAccountPhone()

    def _getCCRoom(self):
        titleName = gameglobal.rds.loginManager.titleName()
        roomId, channelId = SCD.data.get('CCServerRoom', {}).get(titleName, [1314, 0])
        return (roomId, channelId)

    def onGetQueueDesc(self, *arg):
        from guis import uiUtils
        if self.queueCnt > uiConst.QUEUE_CNT_LIMIT:
            numText = "<font color = \'#7ACC29\'>%d+</font>" % uiConst.QUEUE_CNT_LIMIT
        else:
            numText = "<font color = \'#7ACC29\'>%d</font>" % self.queueCnt
        isVipQueue = utils.isVipQueueMember(BigWorld.player())
        if isVipQueue:
            queueText = gameStrings.TEXT_MESSAGEBOXPROXY_514 % numText
            vipQueueHint = gameStrings.TEXT_MESSAGEBOXPROXY_515
        else:
            queueText = gameStrings.TEXT_MESSAGEBOXPROXY_517 % numText
            vipQueueHint = ''
        if not gameglobal.rds.configData.get('enableCCliveBroadcast', False):
            enterText = ''
            ccSmallText = ''
            ccBigText = ''
        else:
            enterText = uiUtils.getCCHyperLink('unknown', False, 0, gameStrings.TEXT_MESSAGEBOXPROXY_525)
            ccSmallText = SCD.data.get('QueueCCSmallText', gameStrings.TEXT_MESSAGEBOXPROXY_526) + enterText
            ccBigText = SCD.data.get('QueueCCBigText', gameStrings.TEXT_MESSAGEBOXPROXY_527)
        queueInfoDict = {'queueText': queueText,
         'isVipQueue': isVipQueue,
         'vipQueueHint': vipQueueHint,
         'tipsDesc': self.tipsDesc,
         'linkDesc': gameStrings.TEXT_MESSAGEBOXPROXY_530,
         'lunTanLinkDesc': gameStrings.TEXT_MESSAGEBOXPROXY_530_1,
         'ccSmallText': ccSmallText,
         'ccBigText': ccBigText}
        return uiUtils.dict2GfxDict(queueInfoDict, True)

    def onQuitQueue(self, *arg):
        buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.confirmQuitQueue)), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
        self.queueMsgBoxId = gameglobal.rds.ui.messageBox.show(True, '', gameStrings.TEXT_MESSAGEBOXPROXY_536, buttons)

    def onClickLink(self, *arg):
        sType = arg[3][0].GetString()
        url = ''
        if sType == 'linkDesc':
            url = 'http://tianyu.163.com/'
        elif sType == 'lunTanLinkDesc':
            url = 'http://ty.netease.com/'
        if url:
            clientcom.openFeedbackUrl(url)
        else:
            gamelog.error('@hjx error onClickLink url is null')

    def onClickConfirm(self, *arg):
        defaultPhone = arg[3][0].GetString()
        nowPhone = arg[3][1].GetString()
        p = re.compile('1[3-8]\\d{9}$')
        result = p.match(str(nowPhone))
        if not result:
            self.queueMsgBoxId = gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_MESSAGEBOXPROXY_557)
            return
        if defaultPhone != nowPhone:
            BigWorld.player().base.setAccountPhone(int(nowPhone))
        else:
            BigWorld.player().base.applyMessageRemind(True)

    def onClickCancel(self, *arg):
        defaultPhone = arg[3][0].GetString()
        if defaultPhone != '0':
            BigWorld.player().base.applyMessageRemind(False)
        else:
            self.gotoFirstPanel()

    def gotoFirstPanel(self):
        if self.queueMed:
            self.queueMed.Invoke('gotoFirstPanel')

    def gotoThirdPanel(self):
        if self.queueMed:
            self.queueMed.Invoke('gotoThirdPanel')

    def setAlreadyState(self, state):
        if self.queueMed:
            self.queueMed.Invoke('setAlreadyState', GfxValue(state))

    def setDefaultPhone(self, phone):
        if self.queueMed:
            self.queueMed.Invoke('setDefaultPhone', GfxValue(str(phone)))

    def confirmQuitQueue(self):
        self.queueMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_QUEUE_TIP)
        self.cancelCheckCallback()
        if BigWorld.player():
            BigWorld.player().base.giveUpHoldQueue()
        BigWorld.disconnect()
        gameglobal.rds.ui.characterDetailAdjust.closeTips()
        gameglobal.rds.ui.loginSelectServer.onRefreshServerList()

    def dismissQueue(self):
        self.queueMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_QUEUE_TIP)
        self.dismiss()
        self.cancelCheckCallback()
        self.cancelQueryCallback()

    def loadMicCard(self, channelId = 0):
        if not gameglobal.rds.configData.get('enableCCliveBroadcast', False):
            return
        from helpers import ccControl
        ccControl.loadMicCard(channelId)

    def showMicCard(self, pathPicture = 'test.png'):
        gamelog.debug('showMicCard', pathPicture)
        if self.queueMed:
            self.queueMed.Invoke('loadPicture', GfxValue(pathPicture))

    def isShow(self, msgBoxId):
        if msgBoxId:
            return msgBoxId in self.loadeds
        return False

    def onCounterChange(self, *args):
        if not self.counterCallback:
            return
        mediator = args[3][0]
        count = int(args[3][1].GetNumber())
        self.counterCallback(mediator, count)

    def onDismissMsgBox(self, *args):
        multiId = int(args[3][0].GetString())
        self.dismiss(multiId, needDissMissCallBack=False)

    def hasMsgBox(self, msgBoxId):
        if msgBoxId in self.loadeds or msgBoxId in self.loadings:
            return True
        return False
