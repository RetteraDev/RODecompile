#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wishMadeProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import const
import random
import gametypes
from Scaleform import GfxValue
import utils
import commcalc
from guis import ui
from callbackHelper import Functor
from uiProxy import SlotDataProxy
from guis import uiConst
from guis import uiUtils
from guis import events
from ui import gbk2unicode
from ui import unicode2gbk
from helpers import taboo
from data import wish_data as WD
from data import wish_config_data as WCD
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
from data import mail_template_data as MTD
from data import bonus_data as BD
EMOTE_SELF_WISH = 1
EMOTE_NOTICE_WISH = 2
LUCK_WISH = 3
WISH_MADE_CD_CALL = 60

class WishMadeProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(WishMadeProxy, self).__init__(uiAdapter)
        self.modelMap = {'makeSelfWish': self.onMakeSelfWish,
         'makeNoticeWish': self.onMakeNoticeWish,
         'makeLuckyWish': self.onMakeLuckyWish,
         'changePage': self.changeWishPage,
         'getSelfWishData': self.onGetSelfWishData,
         'getNoticeWishData': self.onGetNoticeWishData,
         'getLuckyWishData': self.onGetLuckyWishData,
         'getFriendList': self.onGetFriendList,
         'getRandomWish': self.onGetRandomWish,
         'removeItem': self.onRemoveItem,
         'getMsgLimit': self.onGetMsgLimit,
         'getTabsText': self.onGetTabsText}
        self.binding = {}
        self.type = 'wish'
        self.bindType = 'wish'
        self.mediator = None
        self.curPage = EMOTE_SELF_WISH
        self.recentfriend = []
        self.posMap = {}
        self.randomWishes = None
        self.selfStamp = None
        self.noticeStamp = None
        self.itemNum = {}
        self.curWishes = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_WISH_MADE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_WISH_MADE:
            self.mediator = mediator

    def show(self):
        if gameglobal.rds.configData.get('enableWish', False):
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WISH_MADE)
            BigWorld.player().cell.querySingleWishCnt()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        self.curPage = EMOTE_SELF_WISH
        self.mediator = None
        self.clearItem()
        self.randomWishes = None
        self.itemNum = {}
        gameglobal.rds.ui.funcNpc.close()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WISH_MADE)
        if gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[4:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'wish%d.slot%d' % (bar, slot)

    def onGetSelfWishData(self, *arg):
        ret = self._getSelfWishData()
        return uiUtils.dict2GfxDict(ret, True)

    def formatWishDesc(self):
        cnts = WCD.data.get('WISH_REWARD_CNT', (1001,))
        cnts = list(cnts)
        cnts.sort()
        wishCnt = cnts[-1]
        for c in cnts:
            if c >= self.curWishes:
                wishCnt = c
                break

        desc = WCD.data.get('WISH_REWARD_DESC', gameStrings.TEXT_WISHMADEPROXY_109) % (str(wishCnt), self.curWishes)
        return desc

    def _getSelfWishData(self):
        ret = {}
        configData = self._getWishConfigData(gametypes.WISH_TYPE_SINGLE)
        emoteConsumeItem = configData.get('consumeItemId', 331472)
        emoteConsumeItemCnt = configData.get('consumeItemCnt', 10)
        ownCnt = BigWorld.player().inv.countItemInPages(int(emoteConsumeItem), enableParentCheck=True)
        cntStr = uiUtils.convertNumStr(ownCnt, emoteConsumeItemCnt, enoughColor='#146622')
        itemName = ID.data.get(emoteConsumeItem, {}).get('name', '')
        ret['consume'] = gameStrings.TEXT_WISHMADEPROXY_120 % (itemName, cntStr)
        ret['cd'] = WISH_MADE_CD_CALL - (utils.getNow() - self.selfStamp) if self.selfStamp else 0
        ret['desc'] = self.formatWishDesc()
        return ret

    def onGetNoticeWishData(self, *arg):
        ret = self._getNoticeWishData()
        return uiUtils.dict2GfxDict(ret, True)

    def _getNoticeWishData(self):
        ret = {}
        configData = self._getWishConfigData(gametypes.WISH_TYPE_COUPLE)
        emoteConsumeItem = configData.get('consumeItemId', 331472)
        emoteConsumeItemCnt = configData.get('consumeItemCnt', 10)
        ownCnt = BigWorld.player().inv.countItemInPages(int(emoteConsumeItem), enableParentCheck=True)
        cntStr = uiUtils.convertNumStr(ownCnt, emoteConsumeItemCnt, enoughColor='#146622')
        itemName = ID.data.get(emoteConsumeItem, {}).get('name', '')
        ret['consume'] = gameStrings.TEXT_WISHMADEPROXY_120 % (itemName, cntStr)
        ret['cd'] = WISH_MADE_CD_CALL - (utils.getNow() - self.noticeStamp) if self.noticeStamp else 0
        return ret

    def onGetLuckyWishData(self, *arg):
        ret = {}
        configData = self._getWishConfigData(gametypes.WISH_TYPE_LUCKY)
        ret['wishCount'] = ''
        ret['wishMadeTime'] = gameStrings.TEXT_WISHMADEPROXY_145 % WCD.data.get('LUCKY_WISH_TIME', gameStrings.TEXT_WISHMADEPROXY_145_1)
        luckConsumeItem = configData.get('consumeItemId', 331472)
        luckConsumeItemCnt = configData.get('consumeItemCnt', 10)
        ownCnt = BigWorld.player().inv.countItemInPages(int(luckConsumeItem), enableParentCheck=True)
        cntStr = uiUtils.convertNumStr(ownCnt, luckConsumeItemCnt, enoughColor='#451602')
        itemName = ID.data.get(luckConsumeItem, {}).get('name', '')
        ret['consume'] = gameStrings.TEXT_WISHMADEPROXY_151 % (itemName, cntStr)
        ret['desc'] = configData.get('desc', gameStrings.TEXT_MONSTERCLANWARACTIVITYPROXY_348)
        ret['expEnable'] = True
        ret['moneyEnable'] = True
        ret['itemEnable'] = True
        ret['item0'] = self._genMailItem(WCD.data.get('LUCKY_EXP_MAIL_ID', 0))
        ret['item1'] = self._genMailItem(WCD.data.get('LUCKY_CASH_MAIL_ID', 0))
        ret['item2'] = self._genMailItem(WCD.data.get('LUCKY_ITEM_MAIL_ID', 0))
        ret['title0'] = WCD.data.get('LUCKY_TITLE1', gameStrings.TEXT_PLAYRECOMMLVUPPROXY_81)
        ret['title1'] = WCD.data.get('LUCKY_TITLE2', gameStrings.TEXT_WISHMADEPROXY_162)
        ret['title2'] = WCD.data.get('LUCKY_TITLE3', gameStrings.TEXT_WISHMADEPROXY_163)
        ret['tip0'] = WCD.data.get('LUCKY_TIP1', gameStrings.TEXT_WISHMADEPROXY_165)
        ret['tip1'] = WCD.data.get('LUCKY_TIP2', gameStrings.TEXT_WISHMADEPROXY_166)
        ret['tip2'] = WCD.data.get('LUCKY_TIP3', gameStrings.TEXT_WISHMADEPROXY_167)
        ret['makeBtn0'] = WCD.data.get('WISH_BUTTON_TEXT1', gameStrings.TEXT_WISHMADEPROXY_169)
        ret['makeBtn1'] = WCD.data.get('WISH_BUTTON_TEXT1', gameStrings.TEXT_WISHMADEPROXY_169)
        ret['makeBtn2'] = WCD.data.get('WISH_BUTTON_TEXT1', gameStrings.TEXT_WISHMADEPROXY_169)
        return uiUtils.dict2GfxDict(ret, True)

    def onGetTabsText(self, *arg):
        ret = {}
        ret['selfBtn'] = WCD.data.get('LUCKY_TAB1', gameStrings.TEXT_WISHMADEPROXY_179)
        ret['noticeBtn'] = WCD.data.get('LUCKY_TAB2', gameStrings.TEXT_WISHMADEPROXY_180)
        return uiUtils.dict2GfxDict(ret, True)

    def _genMailItem(self, mailId):
        bonusId = MTD.data.get(mailId, {}).get('bonusId', 0)
        fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', ())
        fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        if fixedBonus:
            itemId = fixedBonus[0][1]
        else:
            itemId = 0
        item = uiUtils.getGfxItemById(itemId)
        return item

    def onMakeSelfWish(self, *arg):
        wType = int(arg[3][0].GetNumber())
        content = arg[3][1].GetString().strip()
        p = BigWorld.player()
        if content:
            content = unicode2gbk(content)
            isNormal, content = taboo.checkPingBiWord(content, False)
            if not isNormal:
                p.showGameMsg(GMDD.data.CHAT_TABOO_WORD, ())
                return
            result, content = taboo.checkBSingle(content)
            if not result:
                p.showGameMsg(GMDD.data.CHAT_TABOO_WORD, ())
                return
            p = BigWorld.player()
            p.cell.makeSingleWish(wType, content)
            self.selfStamp = utils.getNow()
            self.clearPanelContent(wType)
        else:
            p.showGameMsg(GMDD.data.NONE_CONTENT_SUBMIT_FORBIDDEN, ())

    def onMakeNoticeWish(self, *arg):
        wType = int(arg[3][0].GetNumber())
        content = arg[3][1].GetString().strip()
        roleName = unicode2gbk(arg[3][2].GetString().strip())
        p = BigWorld.player()
        if roleName and roleName == p.roleName:
            p.showGameMsg(GMDD.data.CAN_NOT_MAKE_WISH_TO_SELF, ())
            return
        if content:
            content = unicode2gbk(content)
            isNormal, content = taboo.checkPingBiWord(content, False)
            if not isNormal:
                p.showGameMsg(GMDD.data.CHAT_TABOO_WORD, ())
                return
            result, content = taboo.checkBSingle(content)
            if not result:
                p.showGameMsg(GMDD.data.CHAT_TABOO_WORD, ())
                return
        if not roleName:
            p.showGameMsg(GMDD.data.NONE_TARGET_PLAYER_SUBMIT_FORBIDDEN, ())
            return
        itemIds = []
        itemCnts = []
        pages = []
        poses = []
        for key, val in self.bindingData.items():
            if key.find('wish0') != -1 and val:
                it, pg, ps = p.inv.findItemByUUID(val.uuid)
                if it != const.CONT_EMPTY_VAL:
                    itemIds.append(it.id)
                    pages.append(pg)
                    poses.append(ps)
                    itemCnts.append(self.itemNum.get(key, val.cwrap))

        subjuct = WCD.data.get('WISH_COUPLE_SUBJECT', gameStrings.TEXT_WISHMADEPROXY_257) % p.roleName
        self.popConfirmPostage(roleName, subjuct, content, itemIds, itemCnts, pages, poses, wType)

    def onMakeLuckyWish(self, *arg):
        wType = int(arg[3][0].GetNumber())
        BigWorld.player().cell.makeLuckyWish(wType)

    def changeWishPage(self, *arg):
        self.curPage = int(arg[3][0].GetNumber())

    def onGetFriendList(self, *arg):
        return uiUtils.array2GfxAarry(self.recentfriend, True)

    @ui.uiEvent(uiConst.WIDGET_WISH_MADE, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onWishItemClick(self, event):
        event.stop()
        if not self.curPage == EMOTE_NOTICE_WISH:
            return
        else:
            it = event.data['item']
            nPage = event.data['page']
            nItem = event.data['pos']
            if it == None:
                return
            if it:
                pos = self.findFirstEmptyPos()
                if it.isRuneHasRuneData():
                    p.showGameMsg(GMDD.data.ITEM_MAIL_RUNE_EQUIP, ())
                    return
                if it.isForeverBind():
                    p.showGameMsg(GMDD.data.MAIL_ITEM_BIND, (it.name,))
                    return
                if it.hasLatch():
                    p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                    return
                if it.cwrap > 1:
                    gameglobal.rds.ui.inventory.showNumberInputWidget(uiConst.NUMBER_WIDGET_WISH_MADE, nPage, nItem, pos)
                else:
                    self.setItem(nPage, nItem, 0, pos, it, it.cwrap)
            return

    def findFirstEmptyPos(self):
        for idx in xrange(6):
            key = self._getKey(0, idx)
            if not self.bindingData.has_key(key) or not self.bindingData[key]:
                return idx

        return -1

    def setItem(self, srcBar, srcSlot, destBar, destSlot, item, num):
        key = self._getKey(destBar, destSlot)
        if self.binding.has_key(key):
            self.bindingData[key] = item
            count = num
            self.itemNum[key] = count
            data = uiUtils.getGfxItem(item, appendInfo={'count': num})
            self.posMap[destBar, destSlot] = [srcBar, srcSlot]
            self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
            gameglobal.rds.ui.inventory.updateSlotState(srcBar, srcSlot)

    def isFill(self, page, pos):
        key = self._getKey(page, pos)
        if self.bindingData.get(key, None):
            return True
        else:
            return False

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            for wishKey, item in self.posMap.items():
                if [page, pos] == item:
                    return self.isFill(wishKey[0], wishKey[1])

    def onGetRandomWish(self, *arg):
        if not self.randomWishes:
            self.randomWishes = WCD.data.get('RANDOM_WISHES', [])
        if len(self.randomWishes) > 0:
            choice = random.choice(self.randomWishes)
        else:
            choice = ''
        return GfxValue(gbk2unicode(choice))

    def onRemoveItem(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        self.removeItem(bar, slot)

    def removeItem(self, bar, slot):
        key = self._getKey(bar, slot)
        if self.binding.has_key(key):
            self.bindingData[key] = None
            self.itemNum[key] = None
            data = GfxValue(0)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
            srcBar, srcSlot = self.posMap.get((bar, slot), (None, None))
            if srcBar != None:
                self.posMap.pop((bar, slot))
                gameglobal.rds.ui.inventory.updateSlotState(srcBar, srcSlot)

    def clearItem(self):
        for slot in range(6):
            self.removeItem(0, slot)

    def _getWishConfigData(self, stype):
        return WD.data.get(stype, {})

    def onGetMsgLimit(self, *arg):
        return GfxValue(const.MAX_WISH_MSG_LENGTH)

    def clearPanelContent(self, wType):
        if self.mediator:
            self.clearItem()
            self.itemNum = {}
            self.mediator.Invoke('clearPanelContent', GfxValue(wType))

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        if self.bindingData.has_key(key) and self.bindingData[key]:
            return gameglobal.rds.ui.inventory.GfxToolTip(self.bindingData[key])
        else:
            return GfxValue('')

    def _getWishMadeMailFee(self):
        p = BigWorld.player()
        if not p:
            return 0
        itemSlotCount = 0
        for key, val in self.bindingData.items():
            if key.find('wish0') != -1 and val:
                it, pg, ps = p.inv.findItemByUUID(val.uuid)
                if it != const.CONT_EMPTY_VAL:
                    itemSlotCount += 1

        fvars = {'n': p.dailySentMailCount + 1,
         'c': itemSlotCount}
        return commcalc._calcFormulaById(gametypes.FORMULA_ID_MAIL_FEE, fvars) + gameglobal.rds.ui.mail.calcTax(0)

    def popConfirmPostage(self, roleName, subjuct, content, itemIds, itemCnts, pages, poses, wType):
        postage = self._getWishMadeMailFee()
        msg = uiUtils.getTextFromGMD(GMDD.data.WISH_MADE_CONFIRM_POSTAGE, gameStrings.TEXT_WISHMADEPROXY_400) % postage
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.gotoConfirmSendMail, roleName, subjuct, content, itemIds, itemCnts, pages, poses, wType))

    def gotoConfirmSendMail(self, roleName, subjuct, content, itemIds, itemCnts, pages, poses, wType):
        p = BigWorld.player()
        postage = self._getWishMadeMailFee()
        if len(itemIds) == 0:
            func = Functor(self.sendWish, roleName, subjuct, content, itemIds, itemCnts, pages, poses, p.cipherOfPerson, wType)
        else:
            func = Functor(self.sendWishWithItems, roleName, subjuct, content, itemIds, itemCnts, pages, poses, p.cipherOfPerson, wType)
        if uiUtils.checkBindCashEnough(postage, p.bindCash, p.cash, func):
            func()

    def sendWish(self, roleName, subjuct, content, itemIds, itemCnts, pages, poses, cipher, wType):
        p = BigWorld.player()
        p.cell.makeCoupleWish(roleName, 0, subjuct, content, itemIds, itemCnts, pages, poses, cipher, wType)
        self.noticeStamp = utils.getNow()
        if roleName not in self.recentfriend:
            self.recentfriend.append({'label': roleName})
        self.clearPanelContent(wType)

    @ui.checkInventoryLock()
    def sendWishWithItems(self, roleName, subjuct, content, itemIds, itemCnts, pages, poses, cipher, wType):
        p = BigWorld.player()
        p.cell.makeCoupleWish(roleName, 0, subjuct, content, itemIds, itemCnts, pages, poses, p.cipherOfPerson, wType)
        self.noticeStamp = utils.getNow()
        if roleName not in self.recentfriend:
            self.recentfriend.append({'label': roleName})
        self.clearPanelContent(wType)

    def updateSpecialWish(self, curWishes):
        self.curWishes = curWishes
        if self.mediator:
            desc = self.formatWishDesc()
            self.mediator.Invoke('updateSpecialWish', GfxValue(gbk2unicode(desc)))
