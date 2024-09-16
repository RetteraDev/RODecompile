#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wishMadeViewProxy.o
import BigWorld
import gameglobal
import gametypes
import const
import formula
import utils
from callbackHelper import Functor
from guis import uiUtils, uiConst
from Scaleform import GfxValue
from uiProxy import UIProxy
from ui import unicode2gbk
from ui import gbk2unicode
from data import wish_config_data as WCD
from data import mail_template_data as MTD
from data import bonus_data as BD
from data import item_data as ID
from cdata import game_msg_def_data as GMDD

class WishMadeViewProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WishMadeViewProxy, self).__init__(uiAdapter)
        self.modelMap = {'getWishDataByType': self.onGetWishDataByType,
         'getRankList': self.onGetRankList,
         'clickFavorBtn': self.onClickFavorBtn,
         'notifyUpdateWish': self.onNotifyUpdateWish,
         'getMyNewWish': self.onGetMyNewWish,
         'notifyAwardList': self.onNotifyAwardList,
         'getFriendWish': self.onGetFriendWish,
         'closeFriendWish': self.onCloseFrendWish,
         'addFriendWish': self.onAddFriendWish,
         'getRoleName': self.onGetRoleName}
        uiAdapter.registerEscFunc(uiConst.WIDGET_WISHMADE_VIEW, self.hide)
        uiAdapter.registerEscFunc(uiConst.WIDGET_FESTIVAL_WISH_MADE, self.hide)
        self.hotData = []
        self.nowData = []
        self.recordData = []
        self.hotVersion = 0
        self.nowVersion = 0
        self.rewardVersion = 0
        self.mineVersion = 0
        self.friendWish = {}
        self.fMediator = None
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_WISHMADE_VIEW:
            self.mediator = mediator
            p = BigWorld.player()
            BigWorld.callback(1, Functor(p.cell.queryMyWish, self.mineVersion))
        elif widgetId == uiConst.WIDGET_FESTIVAL_WISH_MADE:
            self.mediator = mediator
            p = BigWorld.player()
            BigWorld.callback(1, Functor(p.cell.queryMyWish, self.mineVersion))
        else:
            self.fMediator = mediator

    def clearWidget(self, *arg):
        gameglobal.rds.ui.funcNpc.close()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FESTIVAL_WISH_MADE)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WISHMADE_VIEW)

    def reset(self):
        self.mediator = None

    def closeFriendWish(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FRIEND_WISH)
        self.fMediator = None

    def show(self):
        if gameglobal.rds.configData.get('enableFestivalWishMadeView', True):
            self.uiAdapter.loadWidget(uiConst.WIDGET_FESTIVAL_WISH_MADE)
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WISHMADE_VIEW)

    def showFriendWish(self, info):
        if info:
            gbId = info['tgtGbId']
            fval = BigWorld.player().getFValByGbId(gbId)
            if fval:
                info['roleName'] = fval.name
                self.friendWish = info
                self.uiAdapter.loadWidget(uiConst.WIDGET_FRIEND_WISH)
        else:
            BigWorld.player().showGameMsg(GMDD.data.WISH_FRIEND_NO_WISH, ())

    def onGetWishDataByType(self, *arg):
        tId = arg[3][0].GetNumber()
        ret = self.getDataByType(tId)
        return uiUtils.array2GfxAarry(ret)

    def getDataByType(self, tId):
        if tId == uiConst.WISH_HOT:
            ret = self.hotData
        elif tId == uiConst.WISH_NOW:
            ret = self.nowData
        return ret

    def setDataByType(self, tId, data):
        if tId == uiConst.WISH_HOT:
            self.hotData = data
        elif tId == uiConst.WISH_NOW:
            self.nowData = data

    def setWishVersion(self, tId, version):
        if tId == uiConst.WISH_HOT:
            self.hotVersion = version
        elif tId == uiConst.WISH_NOW:
            self.nowVersion = version

    def updateWishData(self, tId, data, version):
        if self.mediator:
            if data != self.getDataByType(tId):
                self.setWishVersion(tId, version)
                self.setDataByType(tId, data)
                self.mediator.Invoke('updateBoard', (uiUtils.array2GfxAarry(data, True), GfxValue(tId)))

    def onGetRankList(self, *arg):
        return uiUtils.array2GfxAarry(self.recordData, True)

    def onGetFriendWish(self, *arg):
        return uiUtils.dict2GfxDict(self.friendWish, True)

    def onClickFavorBtn(self, *arg):
        dbId = arg[3][0].GetNumber()
        p = BigWorld.player()
        p.base.upvoteWish(dbId)

    def onCloseFrendWish(self, *arg):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FRIEND_WISH)

    def onNotifyUpdateWish(self, *arg):
        tId = arg[3][0].GetNumber()
        data = self.getDataByType(tId)
        if self.mediator:
            self.mediator.Invoke('updateBoard', (uiUtils.array2GfxAarry(data, True), GfxValue(tId)))
        if tId == uiConst.WISH_HOT:
            BigWorld.player().cell.queryHotestWish(self.hotVersion)
        else:
            BigWorld.player().cell.queryLatestWish(self.nowVersion)

    def onNotifyAwardList(self, *arg):
        if self.mediator:
            self.mediator.Invoke('setRankList', uiUtils.array2GfxAarry(self.recordData, True))
        BigWorld.player().cell.queryWishAwardRecord(self.rewardVersion)

    def updateVote(self, dbId, count):
        p = BigWorld.player()
        if self.mediator:
            self.mediator.Invoke('updateVote', (GfxValue(dbId), GfxValue(count)))
            if p.myWishMsg and p.myWishMsg[2] == dbId:
                p.myWishMsg[0] = count
                self.updateMyWish(p.myWishMsg)
            self.updateLocalData(dbId, count)
        if self.fMediator and self.friendWish and self.friendWish['dbId'] == dbId:
            self.fMediator.Invoke('updateFavorCnt', GfxValue(count))

    def updateLocalData(self, dbId, count):
        for hotItem in self.hotData:
            if hotItem['dbId'] == dbId:
                hotItem['cnt'] = count

        for nowItem in self.nowData:
            if nowItem['dbId'] == dbId:
                nowItem['cnt'] = count

    def updateMyWish(self, msg, version = None):
        if self.mediator:
            if version is not None:
                self.mineVersion = version
            self.mediator.Invoke('setMyNewWish', uiUtils.array2GfxAarry(msg, True))

    def updateAwardRecord(self, data, version):
        if self.mediator:
            if data != self.recordData:
                self.rewardVersion = version
                self.setAwardRecord(data)
                self.mediator.Invoke('setRankList', uiUtils.array2GfxAarry(self.recordData, True))

    def setAwardRecord(self, data):
        ret = []
        for item in data:
            itemInfo = {}
            itemInfo['msg'] = self.getDescByItem(item)
            itemInfo['time'] = formula.toYearDesc(item['timestamp'], 1)
            ret.append(itemInfo)

        self.recordData = ret

    def getDescByItem(self, item):
        ret = ''
        mailId = item['val']
        bonusId = MTD.data.get(mailId, {}).get('bonusId')
        fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', ())
        fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        if fixedBonus:
            itemId = fixedBonus[0][1]
        else:
            itemId = 0
        itemName = ID.data.get(itemId, {}).get('name', '')
        if item['aType'] == gametypes.WISH_LUCKY_TYPE_COUPLE:
            formatStr = WCD.data.get('WISH_DECT_COUPLE_TEXT', '')
            ret = formatStr % (item['roleName'], item['tgtRoleName'], itemName)
        else:
            formatStr = WCD.data.get('WISH_DESC_TEXT', '')
            ret = formatStr % (item['roleName'], itemName)
        return ret

    def onGetMyNewWish(self, *args):
        p = BigWorld.player()
        return uiUtils.array2GfxAarry(p.myWishMsg, True)

    def onAddFriendWish(self, *arg):
        roleName = unicode2gbk(arg[3][0].GetString())
        p = BigWorld.player()
        if roleName:
            if not p.friend.findByRole(roleName):
                p.base.addContact(str(roleName), gametypes.FRIEND_GROUP_FRIEND, const.FRIEND_SRC_WISH)
            else:
                p.showGameMsg(GMDD.data.HAS_FRIEND, ())
        else:
            p.showGameMsg(GMDD.data.ANONYMITY_FRIEND, ())

    def onGetRoleName(self, *arg):
        p = BigWorld.player()
        ret = p.roleName
        return GfxValue(gbk2unicode(ret))
