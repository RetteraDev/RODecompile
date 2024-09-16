#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impMail.o
import BigWorld
import gameglobal
import const
import npcConst
import gametypes
from guis import uiConst
from sfx import birdEffect
from data import npc_data as ND
from data import mail_config_data as MCD
from cdata import game_msg_def_data as GMDD

class ImpMail(object):

    def onOpenMail(self, id):
        if not BigWorld.entities.get(id):
            return
        else:
            npcId = BigWorld.entities.get(id).npcId
            npcData = ND.data.get(npcId, None)
            if npcData == None:
                return
            openType = npcData.get('full', 0)
            if openType:
                gameglobal.rds.ui.funcNpc.openDirectly(self.id, npcId, npcConst.NPC_FUNC_MAIL)
                gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)
            else:
                gameglobal.rds.ui.inventory.show(False)
            if gameglobal.rds.ui.mail.isShow():
                gameglobal.rds.ui.mail.closeMailBox()
            gameglobal.rds.ui.mail.show(id, uiConst.LAYOUT_NPC_FUNC)
            return

    def onNewMail(self, cnt):
        if gameglobal.rds.ui.mail.isShow() and gameglobal.rds.ui.mail.newMailCount < cnt:
            gameglobal.rds.ui.mail.refreshMails()
        gameglobal.rds.ui.mail.updateNewMailCount(cnt)
        gameglobal.rds.tutorial.onGetMail()

    def onReadMail(self, mid, params):
        tWhen, tEnd, fromGbId, fromRole, fromSchool, kind, msg, subject, payment, moneyType, income, bind, paid, withdrew, reject, items, read = params
        mailObj = {'mid': mid,
         'tWhen': tWhen,
         'tEnd': tEnd,
         'fromGbId': fromGbId,
         'fromRole': fromRole,
         'fromSchool': fromSchool,
         'kind': kind,
         'msg': msg,
         'subject': subject,
         'payment': payment,
         'moneyType': moneyType,
         'income': income,
         'bind': bind,
         'paid': paid,
         'withdrew': withdrew,
         'reject': reject,
         'items': items,
         'read': read}
        if gametypes.MAIL_FROM_REPLACE.has_key(kind):
            mailObj['fromRole'] = gametypes.MAIL_FROM_REPLACE.get(kind)
        gameglobal.rds.ui.mail.readMail(mid, mailObj)

    def onDeleteMails(self, mids):
        gameglobal.rds.ui.mail.isInit = True
        gameglobal.rds.ui.mail.refreshMails(resetFilter=False, useCurPage=True)
        BigWorld.player().showGameMsg(GMDD.data.MAIL_DELETE_SUCCESS, ())

    def onFetchMails(self, filterOption, pageNo, pageTotal, totalSize, mails):
        mailObjs = []
        for mail in mails:
            mid, tWhen, tEnd, fromGbId, fromRole, fromSchool, subject, payment, moneyType, income, paid, withdrew, read, items, msg, kind, bind, template = mail
            if kind == gametypes.MAIL_TYPE_PAY:
                if moneyType == const.MONEY_TYPE_CASH:
                    income -= max(int(income * MCD.data.get('taxRate', const.MAIL_TAX_RATE)), 1)
                elif moneyType == const.MONEY_TYPE_COIN:
                    income -= max(int(income * MCD.data.get('coinTaxRate', const.MAIL_COIN_TAX_RATE)), 1)
            mailObj = {'mid': mid,
             'tWhen': tWhen,
             'tEnd': tEnd,
             'fromGbId': fromGbId,
             'fromRole': fromRole,
             'fromSchool': fromSchool,
             'subject': subject,
             'payment': payment,
             'moneyType': moneyType,
             'income': income,
             'paid': paid,
             'withdrew': withdrew,
             'read': read,
             'hasAttach': not not items,
             'items': items,
             'msg': msg,
             'kind': kind,
             'bind': bind,
             'template': template}
            if gametypes.MAIL_FROM_REPLACE.has_key(kind):
                mailObj['fromRole'] = gametypes.MAIL_FROM_REPLACE.get(kind)
            mailObjs.append(mailObj)

        gameglobal.rds.ui.mail.setMailList(pageNo, pageTotal, totalSize, mailObjs)

    def onMailItemsFetched(self, mid, index):
        gameglobal.rds.ui.mail.onFetchMailItem(mid, index)
        gameglobal.rds.sound.playSound(gameglobal.SD_26)

    def onMailIncomeWithdrew(self, mid):
        gameglobal.rds.ui.mail.onWithdraw(mid)

    def onSendMailSuccess(self, toRole):
        self.showGameMsg(GMDD.data.MAIL_SEND_SUCCESS, (toRole,))
        gameglobal.rds.ui.mail.clearMail()

    def onMarkAllMailsAsRead(self):
        gameglobal.rds.ui.topBar.onNewMailNotice(0)
        gameglobal.rds.ui.mail.markAllAsRead()

    def onRejectMail(self, mid):
        self.showGameMsg(GMDD.data.MAIL_REJECT_SUCCESS, ())
        self.onDeleteMails([mid])

    def onPayMail(self, mid):
        self.showGameMsg(GMDD.data.MAIL_PAY_SUCCESS, ())
        gameglobal.rds.ui.mail.onPay(mid)

    def onShowMailEffect(self):
        birdEffect.showBirdEffect()

    def onFetchSentMails(self, pageNo, pageTotal, totalSize, mails):
        mailObjs = []
        for mail in mails:
            mid, tWhen, tEnd, fromGbId, fromRole, fromSchool, toRole, subject, payment, moneyType, income, paid, withdrew, read, items, msg, kind, template = mail
            mailObj = {'mid': mid,
             'tWhen': tWhen,
             'tEnd': tEnd,
             'fromGbId': fromGbId,
             'fromRole': toRole,
             'fromSchool': fromSchool,
             'subject': subject,
             'payment': payment,
             'income': income,
             'moneyType': moneyType,
             'paid': paid,
             'withdrew': withdrew,
             'read': read,
             'hasAttach': not not items,
             'items': items,
             'msg': msg,
             'kind': kind,
             'template': template}
            mailObjs.append(mailObj)

        gameglobal.rds.ui.mail.setSentMailList(pageNo, pageTotal, totalSize, mailObjs)

    def onReturnMail(self, mid):
        gameglobal.rds.ui.mail.onReturnMail(mid)
        self.showGameMsg(GMDD.data.MAIL_RETURN_SUCCESS, ())

    def set_dailySentMailCount(self, old):
        gameglobal.rds.ui.mail.setPostage()

    def onGetMailCount(self, filterOption, total, sentTotal):
        gameglobal.rds.ui.mail.updateMailCount(total, sentTotal)

    def onFetchMailItemsFailed(self):
        gameglobal.rds.ui.mail.onFetchMailItemsFailed()

    def onWithdrawMailIncomeFailed(self):
        gameglobal.rds.ui.mail.onWithdrawMailIncomeFailed()

    def OnFeedbackToBirdlet(self):
        gameglobal.rds.ui.birdLetHotLine.hide()
        self.showGameMsg(GMDD.data.BIRDLET_SEND_SUCCESS, ())

    def sendMailRecentReceivers(self, receivers):
        gameglobal.rds.ui.mail.nameList = receivers
