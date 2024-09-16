#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mailProxy.o
from gamestrings import gameStrings
import time
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import const
import commcalc
import utils
from helpers import taboo
from guis import uiConst
from guis import uiUtils
from ui import gbk2unicode
from ui import unicode2gbk
from uiProxy import SlotDataProxy
from guis import ui
from callbackHelper import Functor
from guis import events
from data import item_data as ID
from data import game_msg_data as GMD
from data import mail_config_data as MCD
from data import mail_template_data as MTD
from cdata import game_msg_def_data as GMDD
from gamestrings import gameStrings
TYPE_RECEIVE = 0
TYPE_SEND = 1
TYPE_RETREAT = 2

class MailProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(MailProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeMailBox': self.onCloseMailBox,
         'getMailList': self.onGetMailList,
         'receiveAllMail': self.onReceiveAllMail,
         'deleteMail': self.onDeleteMail,
         'openMail': self.onOpenMail,
         'getMailTypes': self.onGetMailTypes,
         'sendMail': self.onSendMail,
         'getPostage': self.onGetPostage,
         'getNameList': self.onGetNameList,
         'openInventory': self.onOpenInventory,
         'getMailContent': self.onGetMailContent,
         'closeMail': self.onCloseMail,
         'replyMail': self.onReplyMail,
         'rejectMail': self.onRejectMail,
         'payMail': self.onPayMail,
         'getAttachments': self.onGetAttachments,
         'getSingleAttachment': self.onGetSingleAttachment,
         'getMoney': self.onGetMoney,
         'removeItem': self.onRemoveItem,
         'getMailListByType': self.onGetMailListByType,
         'changeTab': self.onChangeTab,
         'getFriendNames': self.onGetFriendNames,
         'getTab': self.onGetTab,
         'getSentMailList': self.onGetSentMailList,
         'retreatMail': self.onRetreatMail,
         'getReceiverName': self.onGetReceiverName,
         'getMailCount': self.onGetMailCount,
         'recordMailBody': self.onRecordMailBody,
         'getMailBody': self.onGetMailBody,
         'openHelp': self.onOpenHelp,
         'prosecute': self.onProsecute,
         'cashChange': self.onCashChange,
         'setCashTaxMode': self.onSetCashTaxMode,
         'getSingleMailAttachments': self.onGetSingleMailAttachments,
         'getFriendList': self.onGetFriendList,
         'purchaseMail': self.onPurchaseMail,
         'getMailTotalSize': self.onGetMailTotalSize,
         'getTaxRate': self.onGetTaxRate,
         'getTianBiTaxRate': self.onGetTianBiTaxRate,
         'checkAbility': self.onCheckAbility,
         'isInCrossServer': self.onIsInCrossServer}
        self.mediator = None
        self.purchaseMed = None
        self.isInit = True
        self.mailContent = None
        self.bindType = 'mail'
        self.type = 'mail'
        self.curPage = 1
        self.pageTotal = 1
        self.curMailId = None
        self.posMap = {}
        self.npcId = 0
        self.itemNum = {}
        self.nameList = []
        self.curTab = TYPE_RECEIVE
        self.newMailCount = 0
        self.mails = []
        self.filterOption = gametypes.MAIL_FILTER_OPTION_ALL
        self.midToReturn = 0
        self.totalMails = 0
        self.totalSentMails = 0
        self.fetchItemMids = []
        self.withdrawMids = []
        self.readMids = []
        self.cash = 0
        self.taxMode = 2
        self.mailTypes = [{'label': gameStrings.TEXT_MAILPROXY_107,
          'data': gametypes.MAIL_FILTER_OPTION_ALL},
         {'label': gameStrings.TEXT_MAILPROXY_108,
          'data': gametypes.MAIL_FILTER_OPTION_ATTACH_WITHOUT_PAY},
         {'label': gameStrings.TEXT_MAILPROXY_109,
          'data': gametypes.MAIL_FILTER_OPTION_PAY},
         {'label': gameStrings.TEXT_MAILPROXY_110,
          'data': gametypes.MAIL_FILTER_OPTION_SYS},
         {'label': gameStrings.TEXT_MAILPROXY_111,
          'data': gametypes.MAIL_FILTER_OPTION_SCENARIO},
         {'label': gameStrings.TEXT_MAILPROXY_112,
          'data': gametypes.MAIL_FILTER_OPTION_CONSIGN}]
        self.receiverName = ''
        self.mailBody = ''
        self.unreadMailCnt = 0
        self.unHandleMailCnt = 0
        self.abilityLackMsgId = 0
        self.fetchFailedCallback = 0
        self.totalLen = 0
        self.getSingleItemFlag = False
        self.getSingleItemIndex = -1
        self.flNeedRefresh = True
        self.friendList = []
        self.payAndGet = 0
        self.mailMediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_MAIL_PURCHASE, self.closePurchase)
        uiAdapter.registerEscFunc(uiConst.WIDGET_MAIL_BOX, self.closeMailBox)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_MAIL_BOX:
            self.mediator = mediator
            if self.curTab == TYPE_RECEIVE:
                self.filterOption = gametypes.MAIL_FILTER_OPTION_ALL
                self.setMailTypeIndex(0)
                self.setPostage()
            elif self.curTab == TYPE_SEND:
                self.mediator.Invoke('setReceiver', GfxValue(gbk2unicode(self.receiverName)))
        elif widgetId == uiConst.WIDGET_MAIL_PURCHASE:
            self.purchaseMed = mediator
            ret = self._getPurchaseList()
            return ret

    def isShow(self):
        return self.mediator != None

    @ui.checkEquipChangeOpen()
    @ui.callFilter(1)
    def show(self, npcId = 0, layoutType = uiConst.LAYOUT_DEFAULT, mailBoxType = TYPE_RECEIVE):
        p = BigWorld.player()
        if not p.checkMapLimitUI(gametypes.MAP_LIMIT_UI_MAIL):
            return
        BigWorld.player().checkSetPassword()
        self.npcId = npcId
        self.curTab = mailBoxType
        if not self.isShow():
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_MAIL_BOX, layoutType=layoutType)

    def showPurchasePanel(self, payAndGet):
        self.payAndGet = payAndGet
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_MAIL_PURCHASE)

    def _getPurchaseList(self):
        ret = {}
        if self.mailContent:
            ret['cash'] = self.mailContent['payment']
            ret['moneyType'] = self.mailContent.get('moneyType', 0)
            ret['itemList'] = []
            items = self.mailContent['items']
            for i, item in enumerate(items):
                obj = {}
                obj['itemName'] = uiUtils.getItemColorNameByItem(item)
                obj['count'] = 'X%d' % item.cwrap
                obj['srcType'] = 'mail'
                obj['itemId'] = item.id
                obj['posInfo'] = 'mail1.slot%d' % i
                ret['itemList'].append(obj)

        return uiUtils.dict2GfxDict(ret, True)

    @ui.checkInventoryLock()
    def onPurchaseMail(self, *arg):
        e = self._getEntity(True)
        if self.payAndGet:
            if e:
                self.getSingleItemFlag = True
                e.cell.payMail(self.curMailId, BigWorld.player().cipherOfPerson)
        elif e:
            e.cell.payMail(self.curMailId, BigWorld.player().cipherOfPerson)
        self.closePurchase()

    def abilityLackMsgBoxCallback(self):
        self.abilityLackMsgId = 0

    def clearWidget(self):
        self.closeMailBox()
        self.closePurchase()
        self.npcId = 0
        self.abilityLackMsgId = 0
        self.cash = 0
        self.payAndGet = 0
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def closeMailBox(self):
        self.mediator = None
        self.clearItem()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MAIL_BOX)

    def clearItem(self):
        for slot in range(const.MAIL_ITEM_NUM_LIMIT):
            self.removeItem(0, slot)

    def _setMailList(self, pageNo, pageTotal, mails):
        self.curPage = pageNo
        self.pageTotal = pageTotal
        info = []
        self.mails = mails
        for index, mail in enumerate(mails):
            if mail['kind'] == gametypes.MAIL_TYPE_SYS and mail['subject'] == gameStrings.TEXT_MAILPROXY_223 and not mail.get('taxed'):
                mail['income'] -= self.calcTax(mail['income'])
                mail['taxed'] = True
            leftTime = int(round((mail['tEnd'] - utils.getNow()) * 1.0 / 60))
            info.append([mail['fromRole'],
             mail['subject'],
             leftTime,
             mail['mid'],
             mail['read'],
             index,
             self._getMailType(mail),
             self.isMailHandled(mail),
             mail['paid']])

        if self.isInit:
            self.mediator.Invoke('setMailPanel', (uiUtils.array2GfxAarry(info, True), GfxValue(pageTotal)))
            self.setMailTypeIndex(self._getMailTypeIndex(self.filterOption))
        else:
            self.mediator.Invoke('setMailList', (uiUtils.array2GfxAarry(info, True), GfxValue(pageNo)))

    def setMailList(self, pageNo, pageTotal, totalSize, mails):
        if not self.mediator or self.curTab != TYPE_RECEIVE:
            return
        if pageNo == 1 and self.filterOption == gametypes.MAIL_FILTER_OPTION_ALL:
            self.totalMails = totalSize
        self._setMailList(pageNo, pageTotal, mails)

    def updateMailObj(self, mid, data):
        for mailObj in self.mails:
            if mailObj['mid'] == mid:
                needUpdate = False
                for k, v in data.iteritems():
                    if mailObj[k] != v:
                        needUpdate = True
                        break

                if not needUpdate:
                    return
                mailObj.update(data)
                BigWorld.callback(0.2, Functor(self.setMailList, self.curPage, self.pageTotal, self.totalMails, self.mails))
                break

    def findMailObj(self, mid):
        for mailObj in self.mails:
            if mailObj['mid'] == mid:
                return mailObj

    def readMail(self, mid, params):
        for slot in range(const.MAIL_ITEM_NUM_LIMIT):
            self.removeItem(1, slot)

        self.updateMailObj(mid, {'read': 1})
        self.mailContent = params
        self.curMailId = mid
        info = self._createMailContent()
        self.mediator.Invoke('setMailContent', uiUtils.array2GfxAarry(info, True))

    def onFetchMailItem(self, mid, index):
        mailObj = self.findMailObj(mid)
        if mailObj:
            if mailObj['items'] and index >= 0 and index < len(mailObj['items']):
                mailObj['items'].pop(index)
            else:
                mailObj['items'] = []
            if self.mailContent and mailObj['mid'] == self.mailContent['mid']:
                self.mailContent = mailObj
            self._updateRead(mailObj, hasIncomeOrItem=True)
            self._refreshMail()
        else:
            if self.curMailId != mid or not self.mailContent:
                return
            if self.mailContent['items'] and index >= 0 and index < len(self.mailContent['items']):
                self.mailContent['items'].pop(index)
            else:
                self.mailContent['items'] = []
            self._updateRead(self.mailContent, hasIncomeOrItem=True)
            self._refreshMail()
        if self.fetchItemMids:
            self.fetchItemMids.pop(0)
            self.nextBatchFetch()

    def onPay(self, mid):
        mailObj = self.findMailObj(mid)
        if mailObj:
            mailObj['paid'] = 1
            self._refreshMail()
            if self.getSingleItemFlag and self._checkBatchFetch():
                e = self._getEntity(True)
                if e:
                    e.cell.fetchMailItem(self.curMailId, self.getSingleItemIndex)
                self.getSingleItemFlag = False
                self.getSingleItemIndex = -1
        else:
            if self.curMailId != mid or not self.mailContent:
                self.getSingleItemFlag = False
                return
            self.mailContent['paid'] = 1
            self._refreshMail()

    def onWithdraw(self, mid):
        mailObj = self.findMailObj(mid)
        if mailObj:
            mailObj['withdrew'] = 1
            self.mailContent = mailObj
            self._updateRead(self.mailContent, hasIncomeOrItem=True)
            self._refreshMail()
        else:
            if self.curMailId != mid or not self.mailContent:
                return
            self.mailContent['withdrew'] = 1
            self._updateRead(self.mailContent, hasIncomeOrItem=True)
            self._refreshMail()
        if self.withdrawMids:
            self.withdrawMids.pop(0)
            self.nextBatchFetch()

    def _refreshMail(self):
        if self.mediator:
            info = self._createMailContent()
            if info == None:
                return
            self.mediator.Invoke('setMailContent', uiUtils.array2GfxAarry(info, True))
            self.setMailCount()
            self.setMailList(self.curPage, self.pageTotal, self.totalMails, self.mails)

    def clearMail(self):
        self.bindingData = {}
        self.itemNum = {}
        self.cash = 0
        for slot in range(const.MAIL_ITEM_NUM_LIMIT):
            self.removeItem(0, slot)

        if self.mediator:
            self.mediator.Invoke('clearMailContent')
        BigWorld.player().cell.getMailCount(gametypes.MAIL_FILTER_OPTION_ALL)

    def _createMailContent(self):
        if self.mailContent == None:
            return
        else:
            sendTime = time.localtime(self.mailContent['tWhen'])
            attachments = self.mailContent['items']
            if not attachments:
                attachments = []
            items = []
            for i, attach in enumerate(attachments):
                data = uiUtils.getGfxItem(attach)
                items.append([data, data['color']])
                key = self._getKey(1, i)
                self.bindingData[key] = attach
                self.itemNum[key] = data['count']

            for i in xrange(len(attachments), 6):
                items.append([{'iconPath': 'notFound'}, 'nothing'])
                key = self._getKey(1, i)
                self.bindingData[key] = None
                self.itemNum[key] = 0

            kind = self.mailContent.get('kind', 0)
            canReply = kind == gametypes.MAIL_TYPE_USER
            if kind == gametypes.MAIL_TYPE_USER_REJECT:
                kind = 0
            bindType = self.mailContent.get('bind', 0)
            moneyType = self.mailContent.get('moneyType', 0)
            mailKind = self._getMailType(self.mailContent)
            template = MTD.data.get(self.mailContent.get('template', 0), {})
            alignType = template.get('alignType', 0)
            schoolSignatureType = 0
            signatureType, sParam = template.get('signatureType', (0, 0))
            if signatureType == uiConst.MAIL_SIGNATURE_SCHOOL:
                schoolSignatureType = sParam
            ret = [self.mailContent['fromRole'],
             '%d.%d.%d %d:%d:%d' % sendTime[0:6],
             self.mailContent['subject'],
             self.mailContent['msg'],
             items,
             0 if self.mailContent['withdrew'] else self.mailContent['income'],
             self.mailContent['payment'],
             BigWorld.player().cash,
             self.mailContent['paid'],
             canReply,
             bindType,
             mailKind,
             alignType,
             schoolSignatureType,
             moneyType]
            return ret

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[4:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'mail%d.slot%d' % (bar, slot)

    def setItem(self, srcBar, srcSlot, destBar, destSlot, item, num):
        key = self._getKey(destBar, destSlot)
        if self.binding.has_key(key):
            self.bindingData[key] = item
            count = num
            self.itemNum[key] = count
            data = uiUtils.getGfxItem(item, appendInfo={'count': num})
            self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
            self.registerSimpleTip(False, destSlot)
            oldPageInfo = self.posMap.get((destBar, destSlot), [])
            self.posMap[destBar, destSlot] = [srcBar, srcSlot]
            gameglobal.rds.ui.inventory.updateSlotState(srcBar, srcSlot)
            if oldPageInfo:
                gameglobal.rds.ui.inventory.updateSlotState(oldPageInfo[0], oldPageInfo[1])
            self.setTitle(item, num)
            self.setPostage(self._getMailFee())
            if self.mediator != None:
                hasAttachItems = self.getAttachItemCount() > 0
                self.mediator.Invoke('hasAttachItem', GfxValue(hasAttachItems))

    def getAttachItemCount(self):
        count = 0
        for i in self.itemNum:
            if self.itemNum[i] != None and self.itemNum[i] != 0:
                count += 1

        return count

    def removeItem(self, bar, slot):
        key = self._getKey(bar, slot)
        if self.binding.has_key(key):
            self.bindingData[key] = None
            self.itemNum[key] = None
            data = GfxValue(0)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
            self.registerSimpleTip(True, slot)
            srcBar, srcSlot = self.posMap.get((bar, slot), (None, None))
            if srcBar != None:
                self.posMap.pop((bar, slot))
                gameglobal.rds.ui.inventory.updateSlotState(srcBar, srcSlot)
        self.setPostage(self._getMailFee())
        if self.mediator != None:
            hasAttachItems = self.getAttachItemCount() > 0
            self.mediator.Invoke('hasAttachItem', GfxValue(hasAttachItems))

    def registerSimpleTip(self, state, slot):
        if self.mediator != None:
            self.mediator.Invoke('registerSimpleTip', (GfxValue(state), GfxValue(slot)))

    def isFill(self, page, pos):
        key = self._getKey(page, pos)
        if self.bindingData.get(key, None):
            return True
        else:
            return False

    def findFirstEmptyPos(self):
        for idx in xrange(6):
            key = self._getKey(0, idx)
            if not self.bindingData.has_key(key) or not self.bindingData[key]:
                return idx

        return 0

    def _createNameList(self):
        ret = []
        for name in self.nameList:
            ret.append({'label': name})

        return ret

    def setMailTypeIndex(self, index):
        if self.mediator != None:
            self.mediator.Invoke('setMailTypeIndex', GfxValue(index))

    def onCloseMailBox(self, *arg):
        self.hide()

    def onGetMailList(self, *arg):
        self.curPage = int(arg[3][0].GetNumber())
        self.isInit = arg[3][1].GetBool()
        e = self._getEntity()
        if e:
            if self.curTab == TYPE_RECEIVE:
                e.cell.fetchMails(self.curPage, self.filterOption, False)
            elif self.curTab == TYPE_RETREAT:
                e.cell.fetchSentMails(self.curPage)

    def onReceiveAllMail(self, *arg):
        e = self._getEntity(True)
        if e:
            e.cell.fetchAllMailItems()

    def onDeleteMail(self, *arg):
        if not self._checkBatchFetch():
            return
        mids = arg[3][0].GetString().split(',')
        mids = [ int(mid) for mid in mids ]
        for mid in mids:
            mailObj = self.findMailObj(mid)
            if mailObj:
                if mailObj['payment'] > 0 and mailObj['paid'] == 0:
                    BigWorld.player().showGameMsg(GMDD.data.MAIL_CANNOT_DELETE_PAY_MAIL, ())
                    return
                if self._hasValuableItem(mailObj):
                    BigWorld.player().showGameMsg(GMDD.data.MAIL_CANNOT_DELETE_VALUABLE_MAIL, ())
                    return

        attachmentLeft = False
        for mid in mids:
            mailObj = self.findMailObj(mid)
            if mailObj and (mailObj['items'] or mailObj['income'] and not mailObj['withdrew']):
                attachmentLeft = True
                break

        e = self._getEntity(True)
        if not e:
            return
        if not attachmentLeft:
            self._doDeleteMails(mids)
        elif attachmentLeft:
            gameglobal.rds.ui.doubleCheckWithInput.show(uiUtils.getTextFromGMD(GMDD.data.DELETE_MAIL_WITH_ATTACHMENTS_WARN, gameStrings.TEXT_MAILPROXY_559), 'DELETE', title=gameStrings.TEXT_DIGONGPROXY_207_4, confirmCallback=Functor(self._doDeleteMails, mids))
        else:
            msg = gameStrings.TEXT_MAILPROXY_562
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._doDeleteMails, mids))

    def _hasValuableItem(self, mailObj):
        if mailObj and mailObj['items']:
            for item in mailObj['items']:
                if ID.data.get(item.id, {}).get('valuable', False):
                    return True

        return False

    def _doDeleteMails(self, mids):
        e = self._getEntity(True)
        if e:
            e.cell.deleteMails(mids)

    def _cancelBatchDelete(self):
        if self.mediator:
            self.mediator.Invoke('cancelBatchDelete')

    def _updateEnd(self, mailObj):
        if mailObj.get('kind', 0) == gametypes.MAIL_TYPE_MALL:
            keepTime = MCD.data.get('mallReadKeepTime')
        else:
            if self.checkMailIncomeOrItems(mailObj):
                return
            keepTime = mailObj.get('payment') and MCD.data.get('paymentReadKeepTime') or MCD.data.get('normalReadKeepTime') or const.MAIL_READ_DEL_TIME
        mailObj['tEnd'] = utils.getNow() + keepTime

    def _updateRead(self, mailObj, hasIncomeOrItem = False):
        if mailObj and not mailObj['read']:
            mailObj['read'] = 1
            if hasIncomeOrItem and not self.checkMailIncomeOrItems(mailObj):
                mailObj['tEnd'] = min(mailObj['tEnd'], utils.getNow() + MCD.data.get('simpleKeepTime', const.MAIL_SIMPLE_KEEP_TIME))
            else:
                self._updateEnd(mailObj)

    def onOpenMail(self, *arg):
        mid = int(arg[3][0].GetString())
        mailObj = self.findMailObj(mid)
        if not mailObj:
            e = self._getEntity()
            if e:
                e.cell.readMail(mid)
        else:
            if not mailObj['read']:
                self._updateEnd(mailObj)
                e = self._getEntity()
                if e:
                    self._addQueuedRead(mid)
            self.readMail(mid, mailObj)

    def onGetMailTypes(self, *arg):
        ret = self.mailTypes
        return uiUtils.array2GfxAarry(ret, True)

    def _getMailTypeIndex(self, filterOption):
        for index, entry in enumerate(self.mailTypes):
            if entry['data'] == filterOption:
                return index

        return 0

    def onSendMail(self, *arg):
        p = BigWorld.player()
        roleName = arg[3][0].GetString().strip()
        if not roleName:
            p.showGameMsg(GMDD.data.MAIL_ROLE_CANNOT_EMPTY, ())
            return
        else:
            roleName = unicode2gbk(roleName)
            if roleName == p.realRoleName:
                p.showGameMsg(GMDD.data.MAIL_CANNOT_TO_SELF, ())
                return
            subject = arg[3][1].GetString().strip()
            if not subject:
                p.showGameMsg(GMDD.data.MAIL_SUBJECT_CANNOT_EMPTY, ())
                return
            subject = unicode2gbk(subject)
            isNormal, subject = taboo.checkNameDisWordWithReplace(subject)
            if isNormal:
                p.showGameMsg(GMDD.data.MAIL_BLOCK_WORD, ())
                return
            content = arg[3][2].GetString().strip()
            if content:
                content = unicode2gbk(content)
                isNormal, content = taboo.checkPingBiWord(content)
                if not isNormal:
                    p.showGameMsg(GMDD.data.CHAT_TABOO_WORD, ())
                    return
                isNormal, content = taboo.checkTiHuanWord(content, False)
                if not isNormal:
                    p.showGameMsg(GMDD.data.MAIL_BLOCK_WORD, ())
                    return
                result, content = taboo.checkBSingle(content)
                if not result:
                    p.showGameMsg(GMDD.data.CHAT_TABOO_WORD, ())
                    p.cell.reportProsecute(p.realRoleName, gametypes.PROSECUTE_TYPE_MAIL_TABOO_MIYU, -1, utils.getNow(), '%s_%s' % (subject, content), '')
                    return
            payment = arg[3][3].GetString().strip()
            income = arg[3][4].GetString().strip()
            moneyType = const.MONEY_TYPE_CASH
            if len(arg[3]) > 5:
                moneyType = arg[3][5].GetNumber()
                if not moneyType:
                    moneyType = const.MONEY_TYPE_CASH
            payment = payment and int(payment) or 0
            income = income and int(income) or 0
            if (income or payment) and utils.getGameLanuage() in ('en',):
                if not gameglobal.rds.configData.get('enableMailCash', False):
                    p.showGameMsg(GMDD.data.ABANDON_MAIL_CASH, ())
                    return
            gbId = 0
            itemIds = []
            itemCnts = []
            pages = []
            poses = []
            for key, val in self.bindingData.items():
                if key.find('mail0') != -1 and val:
                    it, pg, ps = p.inv.findItemByUUID(val.uuid)
                    if it != const.CONT_EMPTY_VAL:
                        itemIds.append(it.id)
                        pages.append(pg)
                        poses.append(ps)
                        itemCnts.append(self.itemNum.get(key, val.cwrap))
                    else:
                        p.showGameMsg(GMDD.data.MAIL_ITEM_DIRTY, ())
                        return

            postage = self._getMailFee()
            if income and itemIds:
                if gameglobal.rds.configData.get('enableInventoryLock', False):
                    BigWorld.player().getCipher(self.onTrueSendMail, (roleName,
                     gbId,
                     subject,
                     content,
                     payment,
                     income,
                     itemIds,
                     itemCnts,
                     pages,
                     poses,
                     postage,
                     moneyType))
                else:
                    self.onTrueSendMail('', roleName, gbId, subject, content, payment, income, itemIds, itemCnts, pages, poses, postage, moneyType)
            elif income or itemIds:
                if gameglobal.rds.configData.get('enableInventoryLock', False):
                    BigWorld.player().getCipher(self.onTrueSendMailS, (roleName,
                     gbId,
                     subject,
                     content,
                     payment,
                     income,
                     itemIds,
                     itemCnts,
                     pages,
                     poses,
                     postage,
                     moneyType))
                else:
                    self.onTrueSendMailS('', roleName, gbId, subject, content, payment, income, itemIds, itemCnts, pages, poses, postage, moneyType)
            else:
                self.popConfirmPostage(roleName, gbId, subject, content, payment, income, itemIds, itemCnts, pages, poses, postage, '', moneyType)
            if not income and not itemIds and not content:
                p.showGameMsg(GMDD.data.MAIL_CONTENT_CANNOT_EMPTY, ())
                return
            if roleName not in self.nameList:
                self.nameList.insert(0, roleName)
            if self.mediator != None:
                ret = self._createNameList()
                self.mediator.Invoke('setNameList', uiUtils.array2GfxAarry(ret, True))
            return

    def onTrueSendMailS(self, cipher, roleName, gbId, subject, content, payment, income, itemIds, itemCnts, pages, poses, postage, moneyType):
        self.popConfirmPostage(roleName, gbId, subject, content, payment, income, itemIds, itemCnts, pages, poses, postage, cipher, moneyType)

    def onTrueSendMail(self, cipher, roleName, gbId, subject, content, payment, income, itemIds, itemCnts, pages, poses, postage, moneyType):
        msg = uiUtils.getTextFromGMD(GMDD.data.MAIL_ATTACH_ITEM_AND_MONEY, gameStrings.TEXT_MAILPROXY_732)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.popConfirmPostage, roleName, gbId, subject, content, payment, income, itemIds, itemCnts, pages, poses, postage, cipher, moneyType))

    def gotoConfirmSendMail(self, roleName, gbId, subject, content, payment, income, itemIds, itemCnts, pages, poses, cipher = '', moneyType = const.MONEY_TYPE_CASH):
        p = BigWorld.player()
        postage = self._getMailFee()
        if moneyType == const.MONEY_TYPE_CASH:
            if uiUtils.checkBindCashEnough(postage, p.bindCash, p.cash, Functor(self.confirmSendMail, roleName, gbId, subject, content, payment, income, itemIds, itemCnts, pages, poses, cipher, moneyType)):
                self.confirmSendMail(roleName, gbId, subject, content, payment, income, itemIds, itemCnts, pages, poses, cipher, moneyType)
        else:
            self.confirmSendMail(roleName, gbId, subject, content, payment, income, itemIds, itemCnts, pages, poses, cipher, moneyType)

    def popConfirmPostage(self, roleName, gbId, subject, content, payment, income, itemIds, itemCnts, pages, poses, postage, cipher = '', moneyType = const.MONEY_TYPE_CASH):
        msg = uiUtils.getTextFromGMD(GMDD.data.MAIL_CONFIRM_POSTAGE, gameStrings.TEXT_MAILPROXY_745) % postage
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.gotoConfirmSendMail, roleName, gbId, subject, content, payment, income, itemIds, itemCnts, pages, poses, cipher, moneyType))

    def confirmSendMail(self, roleName, gbId, subject, content, payment, income, itemIds, itemCnts, pages, poses, cipher, moneyType):
        e = self._getEntity(True)
        if e:
            e.cell.sendMail(roleName, gbId, subject, content, payment, moneyType, income, itemIds, itemCnts, pages, poses, cipher)

    def _getMailFee(self):
        p = BigWorld.player()
        if not p:
            return 0
        itemSlotCount = 0
        for key, val in self.bindingData.items():
            if key.find('mail0') != -1 and val:
                it, pg, ps = p.inv.findItemByUUID(val.uuid)
                if it != const.CONT_EMPTY_VAL:
                    itemSlotCount += 1

        fvars = {'n': p.dailySentMailCount + 1,
         'c': itemSlotCount}
        return commcalc._calcFormulaById(gametypes.FORMULA_ID_MAIL_FEE, fvars) + self.calcTax(self.cash)

    def onGetPostage(self, *arg):
        ret = self._getMailFee()
        return GfxValue(ret)

    def setPostage(self, value = None):
        if value == None:
            value = self._getMailFee()
        if self.mediator:
            self.mediator.Invoke('setPostage', GfxValue(value))

    def onGetNameList(self, *arg):
        ret = self._createNameList()
        return uiUtils.array2GfxAarry(ret, True)

    def onOpenInventory(self, *arg):
        if not gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.show()

    def onGetMailContent(self, *arg):
        ret = self._createMailContent()
        return uiUtils.array2GfxAarry(ret, True)

    def onCloseMail(self, *arg):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MAIL_PURCHASE)

    def closePurchase(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MAIL_PURCHASE)

    def onReplyMail(self, *arg):
        e = self._getEntity(True)
        if not e:
            return
        else:
            self.clearMail()
            self.mailBody = ''
            if self.mediator != None:
                self.mediator.Invoke('setPanel', GfxValue(TYPE_SEND))
                self.curTab = TYPE_SEND
                fromRole = ''
                replyTitle = ''
                if self.mailContent:
                    fromRole = self.mailContent['fromRole']
                    replyTitle = self.mailContent['subject']
                self.mediator.Invoke('setReceiver', GfxValue(gbk2unicode(fromRole)))
                self.mediator.Invoke('setReplyTitle', GfxValue(gbk2unicode(replyTitle)))
            return

    def onRejectMail(self, *arg):
        e = self._getEntity(True)
        if e:
            e.cell.rejectMail(self.curMailId)

    def onPayMail(self, *arg):
        if self.mailContent:
            e = self._getEntity(True)
            if e:
                if self.mailContent['payment'] > 0:
                    self.showPurchasePanel(0)
                elif self.mailContent['income'] > 0:
                    if self._checkBatchFetch():
                        e.cell.withdrawMailIncome(self.curMailId)

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        if self.bindingData.has_key(key) and self.bindingData[key]:
            return gameglobal.rds.ui.inventory.GfxToolTip(self.bindingData[key])
        else:
            return GfxValue('')

    def onGetAttachments(self, *arg):
        mids = arg[3][0].GetString().split(',')
        mids = [ int(mid) for mid in mids ]
        self.startBatchFetch(mids)

    def onGetSingleAttachment(self, *arg):
        if self.curMailId:
            key = arg[3][0].GetString()
            _, index = self.getSlotID(key)
            e = self._getEntity(True)
            itemCount = self.getAttachItemCount()
            if e:
                if itemCount == 1 and self.mailContent['payment'] > 0 and not self.mailContent['paid']:
                    self.getSingleItemIndex = index
                    self.showPurchasePanel(1)
                elif self._checkBatchFetch():
                    e.cell.fetchMailItem(self.curMailId, index)

    def onGetSingleMailAttachments(self, *arg):
        e = self._getEntity(True)
        if e and self.curMailId:
            mailObj = self.findMailObj(self.curMailId)
            if mailObj:
                self.getSingleMailAttachments()

    def getSingleMailAttachments(self):
        if self.curMailId:
            mailObj = self.findMailObj(self.curMailId)
            if mailObj:
                if mailObj['items'] and len(mailObj['items']) and (not mailObj['payment'] or mailObj['paid']):
                    self._getEntity(True).cell.fetchMailItems(self.curMailId)

    def onGetMoney(self, *arg):
        e = self._getEntity(True)
        if e:
            if self._checkBatchFetch():
                e.cell.withdrawMailIncome(self.curMailId)

    def onRemoveItem(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        self.removeItem(bar, slot)

    def refreshMails(self, resetFilter = True, useCurPage = False):
        self.curPage = useCurPage and self.curPage or 1
        if resetFilter:
            self.setMailTypeIndex(0)
            self.filterOption = gametypes.MAIL_FILTER_OPTION_ALL
            self.isInit = True
        self.isInit = self.curPage == 1
        e = self._getEntity()
        if e:
            e.cell.fetchMails(self.curPage, self.filterOption, self.curPage > 1)

    def onGetMailListByType(self, *arg):
        filterOption = int(arg[3][0].GetNumber())
        if filterOption != self.filterOption:
            self.filterOption = filterOption
            self.isInit = True
            e = self._getEntity()
            if e:
                e.cell.fetchMails(1, self.filterOption, False)

    def onChangeTab(self, *arg):
        type = int(arg[3][0].GetNumber())
        if self.curTab != type:
            self.cash = 0
        self.curTab = type
        self.clearItem()

    def onGetTab(self, *arg):
        return GfxValue(self.curTab)

    def onGetFriendNames(self, *arg):
        name = unicode2gbk(arg[3][0].GetString().strip())
        ret = []
        p = BigWorld.player()
        for fVal in p.friend.values():
            if hasattr(fVal, 'name') and fVal.name.find(name) != -1:
                ret.append({'label': fVal.name})

        return uiUtils.array2GfxAarry(ret, True)

    def markAllAsRead(self):
        for mailObj in self.mails:
            mailObj['read'] = 1

        self.setMailList(self.curPage, self.pageTotal, self.totalMails, self.mails)

    def _getEntity(self, needCheckAbility = False):
        if self.npcId:
            e = BigWorld.entities.get(self.npcId)
            return e
        else:
            p = BigWorld.player()
            if needCheckAbility and utils.isAbilityOn() and not p.getAbilityData(gametypes.ABILITY_MAIL_REMOTE_ON):
                if not self.abilityLackMsgId:
                    msg = uiUtils.getTextFromGMD(GMDD.data.ABILITY_LACK_MAIL_MSG, gameStrings.TEXT_MAILPROXY_934)
                    self.abilityLackMsgId = gameglobal.rds.ui.messageBox.showMsgBox(msg, callback=self.abilityLackMsgBoxCallback)
                return None
            return p

    def gotoSendPanel(self, receiverName):
        if self.mediator:
            self.clearMail()
            self.mediator.Invoke('setTabState', uiUtils.array2GfxAarry([False, True]))
            self.mediator.Invoke('setPanel', GfxValue(TYPE_SEND))
            self.curTab = TYPE_SEND
            self.mediator.Invoke('setReceiver', GfxValue(gbk2unicode(receiverName)))
            self.mediator.Invoke('setPostage', self._getMailFee())

    def onGetSentMailList(self, *arg):
        self.curPage = int(arg[3][0].GetNumber())
        self.isInit = arg[3][1].GetBool()
        e = self._getEntity()
        if e:
            e.cell.fetchSentMails(self.curPage)

    def setSentMailList(self, pageNo, pageTotal, totalSize, mails):
        if not self.mediator or self.curTab != TYPE_RETREAT:
            return
        if pageNo == 1 and self.filterOption == gametypes.MAIL_FILTER_OPTION_ALL:
            self.totalSentMails = totalSize
        self._setMailList(pageNo, pageTotal, mails)

    def _getMailType(self, mail):
        mailKind = 0
        if mail['kind'] == gametypes.MAIL_TYPE_USER:
            if mail['payment'] > 0:
                mailKind = uiConst.MAIL_TYPE_PAY
            elif mail['items'] and len(mail['items']) > 0:
                mailKind = uiConst.MAIL_TYPE_ATTACH
            else:
                mailKind = uiConst.MAIL_TYPE_NORMAL
        elif mail['kind'] in gametypes.MAIL_TYPE_SYS_FILTER:
            mailKind = uiConst.MAIL_TYPE_SYSTEM
        elif mail['kind'] == gametypes.MAIL_TYPE_CONSIGN:
            mailKind = uiConst.MAIL_TYPE_CONSIGN
        elif mail['kind'] == gametypes.MAIL_TYPE_SCENARIO:
            mailKind = uiConst.MAIL_TYPE_SCENARIO
        elif mail['kind'] == gametypes.MAIL_TYPE_MALL:
            mailKind = uiConst.MAIL_TYPE_MALL
        elif mail['kind'] == gametypes.MAIL_TYPE_GM_RETURN:
            mailKind = uiConst.MAIL_TYPE_SYSTEM
        return mailKind

    def setTitle(self, item, num):
        titleStr = '%s*%s' % (item.name, num)
        if self.mediator:
            self.mediator.Invoke('setTitle', GfxValue(gbk2unicode(titleStr)))

    def onRetreatMail(self, *arg):
        self.midToReturn = int(arg[3][0].GetString())
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(GMD.data.get(GMDD.data.MAIL_RETURN_CONFIRM, {}).get('text'), self._doRetreatMail)

    def _doRetreatMail(self):
        p = BigWorld.player()
        p.cell.returnMail(self.midToReturn)

    def onGetReceiverName(self, *arg):
        ret = self.receiverName
        self.receiverName = ''
        return GfxValue(gbk2unicode(ret))

    def _createMailCount(self, count):
        if self.curTab == TYPE_RECEIVE:
            self.unreadMailCnt = 0
            for mail in self.mails:
                if not self.isMailRead(mail):
                    self.unreadMailCnt += 1

        ret = ['(%d)' % self.unreadMailCnt, '(%d)' % count[1]]
        return ret

    def onGetMailCount(self, *arg):
        BigWorld.player().cell.getMailCount(gametypes.MAIL_FILTER_OPTION_ALL)
        return uiUtils.array2GfxAarry(self._createMailCount([self.totalMails, self.totalSentMails]))

    def setMailCount(self):
        if self.mediator:
            self.mediator.Invoke('setMailCount', uiUtils.array2GfxAarry(self._createMailCount([self.totalMails, self.totalSentMails])))

    def updateNewMailCount(self, count):
        self.newMailCount = count
        gameglobal.rds.ui.topBar.onNewMailNotice(count)

    def onReturnMail(self, mid):
        e = self._getEntity(True)
        if e:
            e.cell.fetchSentMails(1)

    def onRecordMailBody(self, *arg):
        self.mailBody = arg[3][0].GetString()

    def onGetMailBody(self, *arg):
        return GfxValue(gbk2unicode(self.mailBody))

    def onOpenHelp(self, *arg):
        gameglobal.rds.ui.help.show(gameStrings.TEXT_GAMECONST_1213)

    def updateMailCount(self, total, sentTotal):
        self.totalMails = total
        self.totalSentMails = sentTotal
        self.setMailCount()

    def onProsecute(self, *arg):
        name = unicode2gbk(arg[3][0].GetString().strip())
        if self.mailContent is None:
            return
        else:
            extra = {'msg': self.mailContent['msg'],
             'timeStamp': self.mailContent['tWhen'],
             'fromRole': self.mailContent['fromRole']}
            gameglobal.rds.ui.prosecute.show(name, uiConst.MENU_CHAT)
            gameglobal.rds.ui.prosecute.setMailProsecuteArg(extra)
            return

    def isMailHandled(self, mailObj):
        if mailObj['read'] == 0 or mailObj['items'] and len(mailObj['items']) or mailObj['income'] and not mailObj['withdrew'] or mailObj['payment'] and not mailObj['paid']:
            return False
        return True

    def checkMailIncomeOrItems(self, mailObj):
        return mailObj['items'] and len(mailObj['items']) or mailObj['income'] and not mailObj['withdrew']

    def isMailRead(self, mailObj):
        if mailObj['read'] == 0:
            return False
        return True

    def onFetchMailItemsFailed(self):
        if self.fetchFailedCallback:
            BigWorld.cancelCallback(self.fetchFailedCallback)
            self.fetchFailedCallback = 0
        self.fetchItemMids = []
        self.withdrawMids = []
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.MAIL_BATCH_FETCH_FAILED, ())
        if self.mediator:
            self.mediator.Invoke('updateFetchProgress', (GfxValue(False), GfxValue(0), GfxValue(self.totalLen)))

    def onWithdrawMailIncomeFailed(self):
        if self.fetchFailedCallback:
            BigWorld.cancelCallback(self.fetchFailedCallback)
            self.fetchFailedCallback = 0
        self.fetchItemMids = []
        self.withdrawMids = []
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.MAIL_BATCH_FETCH_FAILED, ())

    def _checkBatchFetch(self):
        if self.fetchItemMids or self.withdrawMids:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.MAIL_BATCH_FETCH_RUNNING, ())
            return False
        return True

    def startBatchFetch(self, mids):
        e = self._getEntity(True)
        if not e:
            return
        if not self._checkBatchFetch():
            return
        self.fetchItemMids = []
        self.withdrawMids = []
        for mid in mids:
            mailObj = self.findMailObj(mid)
            if mailObj:
                if mailObj['items'] and len(mailObj['items']) and (not mailObj['payment'] or mailObj['paid']):
                    self.fetchItemMids.append(mid)
                if mailObj['income'] and not mailObj['withdrew']:
                    self.withdrawMids.append(mid)

        if not self.fetchItemMids and not self.withdrawMids:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.MAIL_BATCH_FETCH_NOT_NECESSARY, ())
            return
        self.totalLen = len(self.fetchItemMids)
        if self.mediator:
            self.mediator.Invoke('updateFetchProgress', (GfxValue(True), GfxValue(len(self.fetchItemMids)), GfxValue(self.totalLen)))
        self.nextBatchFetch()

    def nextBatchFetch(self, instant = False):
        p = BigWorld.player()
        if not self.fetchItemMids and not self.withdrawMids:
            p.showGameMsg(GMDD.data.MAIL_BATCH_FETCH_FINISHED, ())
            if self.mediator:
                self.mediator.Invoke('updateFetchProgress', (GfxValue(False), GfxValue(0), GfxValue(self.totalLen)))
            if self.fetchFailedCallback:
                BigWorld.cancelCallback(self.fetchFailedCallback)
                self.fetchFailedCallback = 0
                p.cell.checkNewMail()
            return
        if instant:
            self._doNextBatchFetch()
        else:
            BigWorld.callback(1, Functor(self._doNextBatchFetch))

    def _doNextBatchFetch(self):
        p = BigWorld.player()
        if not self.fetchItemMids and not self.withdrawMids:
            p.showGameMsg(GMDD.data.MAIL_BATCH_FETCH_FINISHED, ())
            if self.mediator:
                self.mediator.Invoke('updateFetchProgress', (GfxValue(False), GfxValue(len(self.fetchItemMids)), GfxValue(self.totalLen)))
            if self.fetchFailedCallback:
                BigWorld.cancelCallback(self.fetchFailedCallback)
                self.fetchFailedCallback = 0
                p.cell.checkNewMail()
            return
        if self.fetchFailedCallback:
            BigWorld.cancelCallback(self.fetchFailedCallback)
        self.fetchFailedCallback = BigWorld.callback(5, Functor(self.onFetchMailItemsFailed))
        e = self._getEntity()
        if self.fetchItemMids:
            if e:
                e.cell.fetchMailItems(self.fetchItemMids[0])
        elif e:
            e.cell.withdrawMailIncome(self.withdrawMids[0])
        if e and self.mediator:
            self.mediator.Invoke('updateFetchProgress', (GfxValue(True), GfxValue(len(self.fetchItemMids)), GfxValue(self.totalLen)))

    def _addQueuedRead(self, mid):
        e = self._getEntity()
        if not e:
            return
        e.cell.markMailAsRead(mid)

    def onCashChange(self, *arg):
        txt = arg[3][0].GetString()
        self.cash = txt and int(txt) or 0
        self.setPostage()
        yunbi = BigWorld.player().cash
        notEngough = False
        if self.cash > yunbi:
            notEngough = True
        if self.mediator:
            self.mediator.Invoke('updateCashInputState', GfxValue(notEngough))

    def calcTax(self, cash):
        if not cash:
            return 0
        if self.taxMode == 1:
            tax = 0
        else:
            tax = max(int(cash * MCD.data.get('taxRate', const.MAIL_TAX_RATE)), 1)
        return tax

    def onSetCashTaxMode(self, *arg):
        if arg[3][0] is not None:
            self.taxMode = int(arg[3][0].GetNumber())
            self.setPostage()

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            for mailKey, item in self.posMap.items():
                if [page, pos] == item:
                    return self.isFill(mailKey[0], mailKey[1])

    def refreshFriendList(self):
        self.flNeedRefresh = True

    def onGetFriendList(self, *arg):
        if self.flNeedRefresh:
            self._updateFriendListData()
            self.flNeedRefresh = False
        return uiUtils.array2GfxAarry(self.friendList, True)

    def _updateFriendListData(self):
        p = BigWorld.player()
        friend = p.friend
        self.friendList = []
        gmap = {}
        gdataIndex = 2
        groups = [gametypes.FRIEND_GROUP_FRIEND]
        if gametypes.FRIEND_GROUP_FRIEND in groups:
            for id in friend.groups.iterkeys():
                if friend.isCustomGroup(id):
                    groups.append(id)

        if not groups:
            return
        for id in groups:
            name = friend.groups[id]
            gdata = [name,
             '',
             [],
             id,
             0,
             0]
            gmap[id] = len(self.friendList)
            self.friendList.append(gdata)

        for fVal in friend.itervalues():
            if fVal.group in groups and fVal.group > 0:
                groupIndex = gmap[fVal.group]
                self.friendList[groupIndex][gdataIndex].append(fVal.name)
            if gametypes.FRIEND_GROUP_TEMP in groups and fVal.temp:
                groupIndex = gmap[gametypes.FRIEND_GROUP_TEMP]
                self.friendList[groupIndex][gdataIndex].append(fVal.name)
            if gametypes.FRIEND_GROUP_RECENT in groups and fVal.recent:
                groupIndex = gmap[gametypes.FRIEND_GROUP_RECENT]
                self.friendList[groupIndex][gdataIndex].append(fVal.name)

    @ui.uiEvent(uiConst.WIDGET_MAIL_BOX, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onMailItemClick(self, event):
        if self.curTab != 1:
            return
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        p = BigWorld.player()
        pos = self.findFirstEmptyPos()
        if i:
            if i.isRuneHasRuneData():
                p.showGameMsg(GMDD.data.ITEM_MAIL_RUNE_EQUIP, ())
                return
            if i.isForeverBind():
                p.showGameMsg(GMDD.data.MAIL_ITEM_BIND, (i.name,))
                return
            if i.isItemNoMail():
                p.showGameMsg(GMDD.data.MAIL_ITEM_NOMAIL, (i.name,))
                return
            if i.hasLatch():
                p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                return
            if i.cwrap > 1:
                gameglobal.rds.ui.inventory.showNumberInputWidget(uiConst.NUMBER_WIDGET_ITEM_MAIL, nPage, nItem, pos)
            else:
                self.setItem(nPage, nItem, 0, pos, i, i.cwrap)

    def getToolTip(self, key):
        if self.bindingData.has_key(key) and self.bindingData[key]:
            return gameglobal.rds.ui.inventory.GfxToolTip(self.bindingData[key])
        else:
            return GfxValue('')

    def onGetMailTotalSize(self, *arg):
        return GfxValue(self.totalMails)

    def onGetTaxRate(self, *arg):
        taxRate = MCD.data.get('taxRate') * 100
        return GfxValue(taxRate)

    def onGetTianBiTaxRate(self, *args):
        taxRate = MCD.data.get('coinTaxRate', 0.02) * 100
        return GfxValue(taxRate)

    def onCheckAbility(self, *arg):
        e = self._getEntity(True)
        if e:
            return GfxValue(True)
        return GfxValue(False)

    def onIsInCrossServer(self, *args):
        return GfxValue(BigWorld.player()._isSoul())
