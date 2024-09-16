#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldVote2ndProxy.o
import BigWorld
import uiConst
import events
from gamestrings import gameStrings
from uiProxy import UIProxy
import wingWorldUtils
from data import wing_world_army_data as WWAD

class WingWorldVote2ndProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldVote2ndProxy, self).__init__(uiAdapter)
        self.widget = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_VOTE_2ND, self.handleCancelBtnClick)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_VOTE_2ND:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def initUI(self):
        self.widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelBtnClick, False, 0, True)
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        self.widget.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelBtnClick, False, 0, True)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_VOTE_2ND)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_VOTE_2ND)

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        armyInfo = p.wingWorld.getArmyByGbId(p.wingWorldArmyVoteGbId)
        if armyInfo:
            self.widget.textField.text = gameStrings.WING_WORLD_VOTE_2ND_TEXTFIELD1 % armyInfo.name
        else:
            self.widget.textField.text = gameStrings.WING_WORLD_VOTE_2ND_TEXTFIELD2
        for i in range(1, 4):
            ckboxItem = self.widget.getChildByName('ckbox%d' % i)
            leaderInfo = p.wingWorld.getArmyByPostId(i)
            if leaderInfo:
                leaderName = leaderInfo.name
                leaderCate = wingWorldUtils.getWingArmyData().get(i).get('categoryName')
                ckboxItem.visible = True
                ckboxItem.label = gameStrings.WING_WORLD_VOTE_2ND_CHOICE % (leaderName, leaderCate)
                ckboxItem.gbId = leaderInfo.gbId
            else:
                ckboxItem.visible = False

    def handleConfirmBtnClick(self, *arg):
        p = BigWorld.player()
        for i in range(1, 4):
            ckboxItem = self.widget.getChildByName('ckbox%d' % i)
            if ckboxItem.selected:
                p.cell.comfirmWingWorldArmyCategory(long(ckboxItem.gbId))
                break

        self.hide()
        self.delPushMessage()

    def handleCancelBtnClick(self, *arg):
        self.hide()
        self.addPushMessage()

    def addPushMessage(self):
        if not self.uiAdapter.pushMessage.msgs.has_key(uiConst.MESSAGE_TYPE_WING_WORLD_ARMY_VOTE):
            callBackDict = {'click': self.show}
            self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WING_WORLD_ARMY_VOTE, callBackDict)
            self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_ARMY_VOTE)

    def delPushMessage(self):
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_ARMY_VOTE)
