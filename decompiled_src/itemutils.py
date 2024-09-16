#Embedded file name: /WORKSPACE/data/entities/common/itemutils.o
import BigWorld
import const
import utils
from item import Item
if BigWorld.component in ('base', 'cell'):
    import gameengine
    import gamelog
    import mail
from data import item_data as ID
from data import log_src_def_data as LSDD
from data import sys_config_data as SCD
from cdata import guanyin_data as GD
from cdata import guanyin_book_data as GBD

def getGuanYinAllBooks(gbId, it):
    if BigWorld.component not in ('base', 'cell'):
        return []
    if not it.isGuanYin():
        return []
    bookIdList = []
    now = utils.getNow()
    for slot, info in enumerate(it.guanYinInfo):
        for part, bookId in enumerate(info):
            if not bookId:
                continue
            bd = GBD.data.get(bookId)
            if not bd:
                gameengine.reportCritical('@xjw _getGuanYinAllBooks Not config! %d %d %d %d', gbId, slot, part, bookId)
                continue
            if it.guanYinExtraInfo[slot][part]:
                extra = it.guanYinExtraInfo[slot][part]
                if extra.has_key('expireTime') and now > extra['expireTime']:
                    gameengine.reportCritical('@xjw _transGuanYinToNewPhase Expired(expireTime) %d %d %d %d %d', gbId, slot, part, bookId, extra['expireTime'])
                    continue
                if extra.has_key('commonExpireTime') and now > extra['commonExpireTime']:
                    gameengine.reportCritical('@xjw _transGuanYinToNewPhase Expired(commonExpireTime) %d %d %d %d %d', gbId, slot, part, bookId, extra['commonExpireTime'])
                    continue
            info[part] = None
            bookIdList.append(bookId)

        it.guanYinStat[slot] = None

    return bookIdList


def sendGuanYinBook(gbId, bookIdList):
    if BigWorld.component not in ('base', 'cell'):
        return
    if gbId < const.GBID_BASE:
        gamelog.info('xjw## sendGuanYinBook, is puppet, not send!', gbId, bookIdList)
        return
    gamelog.info('xjw## sendGuanYinBook', gbId, bookIdList)
    mailTemplateId = SCD.data.get('guanYinRetMailTemplate', 0)
    if mailTemplateId and gbId:
        while bookIdList:
            books = bookIdList[:6]
            bookIdList = bookIdList[6:]
            items = []
            for bookId in books:
                item = Item(bookId, 1)
                item.srcType = LSDD.data.LOG_SRC_GUANYIN_RET
                item.bindItem()
                items.append(item)

            mailFrom, subject, content = mail.getTemplateWithFrom(mailTemplateId)
            mail.sendSysMail('', gbId, content, subject, 0, 0, items, fromRole=mailFrom, templateId=mailTemplateId)


def checkGuanYinHasSkill(it):
    if not it or not it.isGuanYin():
        return False
    if not getattr(it, 'guanYinInfo', False):
        return False
    for slot, info in enumerate(it.guanYinInfo):
        for part, bookId in enumerate(info):
            if bookId and bookId > 0:
                return True

    return False


def checkGuanYinHasSuperSkill(it):
    if not it or not it.isGuanYin():
        return False
    return getattr(it, 'guanYinSuperBookId', False)


def getGuanYinLv(itemId):
    return GD.data.get(itemId, {}).get('lv', 0)


def getItemRare(itemId):
    return ID.data.get(itemId, {}).get('isRare', False)
