#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zmjSpriteRewardProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gamelog
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis.asObject import ASObject
from guis.asObject import MenuManager
from data import zmj_fuben_config_data as ZFCD

class ZmjSpriteRewardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ZmjSpriteRewardProxy, self).__init__(uiAdapter)
        self.notTake = []
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ZMJ_SPRITE_REWARD, self.hide)

    def reset(self):
        super(ZmjSpriteRewardProxy, self).reset()
        self.rewardInfoDict = {}
        self.widget = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ZMJ_SPRITE_REWARD:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        super(ZmjSpriteRewardProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ZMJ_SPRITE_REWARD)

    def show(self):
        if not gameglobal.rds.configData.get('enableZMJAssist', False):
            return
        if self.widget:
            self.widget.swapPanelToFront()
            self.refreshInfo()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ZMJ_SPRITE_REWARD)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.confirmBtn.disabled = not self.notTake
        self.widget.mainMc.scrollWndList.itemRenderer = 'ZmjSpriteReward_ScrollWndListItem'
        self.widget.mainMc.scrollWndList.dataArray = []
        self.widget.mainMc.scrollWndList.lableFunction = self.itemFunction
        self.widget.mainMc.scrollWndList.itemHeight = 37
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleClickConfirmBtn, False, 0, True)
        self.widget.helpIcon.helpKey = ZFCD.data.get('zmjSpriteRewardHelpKey', 0)
        self.queryInfo()
        self.refreshInfo()

    def queryInfo(self):
        p = BigWorld.player()
        p.base.getZMJAssistAwardInfo()

    def setAwardInfo(self, notTake, took):
        self.rewardInfoDict = {}
        self.notTake = notTake
        index = 0
        for rewardInfo in notTake:
            self.rewardInfoDict[index] = {'gbId': rewardInfo[0],
             'name': rewardInfo[1],
             'school': rewardInfo[2],
             'fame': rewardInfo[3],
             'timeStamp': rewardInfo[4],
             'canRecieve': True}
            index += 1

        for rewardInfo in took:
            self.rewardInfoDict[index] = {'gbId': rewardInfo[0],
             'name': rewardInfo[1],
             'school': rewardInfo[2],
             'fame': rewardInfo[3],
             'timeStamp': rewardInfo[4],
             'canRecieve': False}
            index += 1

        gameglobal.rds.ui.zmjLittleBossPanel.setAssitAwardFlag(notTake)
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        if self.widget:
            self.widget.confirmBtn.disabled = not notTake
            self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        rewardList = []
        for gbId, itemDetail in self.rewardInfoDict.iteritems():
            rewardList.append({'gbId': gbId,
             'school': itemDetail.get('school', 0),
             'name': itemDetail.get('name', ' '),
             'fame': itemDetail.get('fame', 0),
             'timeStamp': itemDetail.get('timeStamp', 0),
             'canRecieve': itemDetail.get('canRecieve', False)})

        rewardList.sort(cmp=self.sort_reward)
        self.widget.mainMc.scrollWndList.dataArray = rewardList
        self.widget.mainMc.scrollWndList.validateNow()
        self.widget.mainMc.emptyHint.text = gameStrings.ZMJ_SPRITE_REWARD_EMPTY_TXT
        self.widget.mainMc.emptyHint.visible = len(rewardList) == 0

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        if not itemData:
            itemMc.visible = False
            return
        itemMc.visible = True
        if itemData.canRecieve:
            itemMc.gotoAndStop('online')
            itemMc.canReceive.text = gameStrings.ZMJ_SPRITE_REWARD_CAN_RECEIVE
        else:
            itemMc.gotoAndStop('offline')
            itemMc.canReceive.text = gameStrings.ZMJ_SPRITE_REWARD_RECEIVED
        itemMc.overMc.visible = False
        itemMc.schoolIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(itemData.school))
        itemMc.playerName.text = itemData.name
        itemMc.fightScore.text = itemData.fame
        itemMc.rewardScore.text = itemData.fame
        itemMc.gbId = itemData.gbId
        itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleOverItem, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleOutItem, False, 0, True)
        menuParam = {'roleName': itemData.name,
         'gbId': itemData.gbId}
        MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_CHAT, menuParam)

    def handleClickConfirmBtn(self, *args):
        BigWorld.player().base.takeAllZMJAssistAward()

    def handleOverItem(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.overMc.visible = True

    def handleOutItem(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.overMc.visible = False

    def sort_reward(self, a, b):
        if a['canRecieve'] > b['canRecieve']:
            return -1
        if a['canRecieve'] < b['canRecieve']:
            return 1
        if a['timeStamp'] > b['timeStamp']:
            return -1
        if a['timeStamp'] < b['timeStamp']:
            return 1
        return 0
