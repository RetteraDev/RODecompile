#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/npcRelationshipOverViewProxy.o
import BigWorld
import const
import commNpcFavor
from gamestrings import gameStrings
import formula
from guis import uiConst
from guis import events
from guis.asObject import ASObject
from guis import uiUtils
from guis.asObject import TipManager
from uiProxy import UIProxy
SELECTED_TYPE_ALL = 0
SELECTED_TYPE_LV2 = 2
SELECTED_TYPE_LV3 = 3
SELECTED_TYPE_LV4 = 4
NOT_ADD_FRIEND_ICON_PATH = 'npcHeadIcon/-1.dds'
from cdata import game_msg_def_data as GMDD
from data import nf_npc_data as NND
from data import seeker_data as SD
from data import sys_config_data as SCD

class NpcRelationshipOverViewProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NpcRelationshipOverViewProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def get_SelectedNpcId(self):
        return self.uiAdapter.npcRelationship.npcId

    def set_SelectedNpcId(self, value):
        self.uiAdapter.npcRelationship.npcId = int(value)

    selectedNpcId = property(get_SelectedNpcId, set_SelectedNpcId)

    def reset(self):
        self.selectedType = SELECTED_TYPE_ALL
        self.selectedMc = None

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_NEW)

    def initUI(self):
        self.widget.lv2Btn.groupName = 'npcRelationshipOverView'
        self.widget.lv2Btn.data = SELECTED_TYPE_LV2
        self.widget.lv3Btn.groupName = 'npcRelationshipOverView'
        self.widget.lv3Btn.data = SELECTED_TYPE_LV3
        self.widget.lv4Btn.groupName = 'npcRelationshipOverView'
        self.widget.lv4Btn.data = SELECTED_TYPE_LV4
        self.widget.allBtn.groupName = 'npcRelationshipOverView'
        self.widget.allBtn.data = SELECTED_TYPE_ALL
        self.widget.allBtn.selected = True
        self.widget.lv2Btn.addEventListener(events.EVENT_SELECT, self.handleTypeBtnClick, False, 0, True)
        self.widget.lv3Btn.addEventListener(events.EVENT_SELECT, self.handleTypeBtnClick, False, 0, True)
        self.widget.lv4Btn.addEventListener(events.EVENT_SELECT, self.handleTypeBtnClick, False, 0, True)
        self.widget.allBtn.addEventListener(events.EVENT_SELECT, self.handleTypeBtnClick, False, 0, True)
        self.widget.selectedIcon.fitSize = True
        self.widget.npcList.column = 3
        self.widget.npcList.itemWidth = 123
        self.widget.npcList.itemHeight = 140
        self.widget.npcList.itemRenderer = 'npcRelationshipOverView_ItemRender'
        self.widget.npcList.labelFunction = self.labelFunction
        self.widget.npcList.dataArray = []
        self.widget.naviBtn.addEventListener(events.BUTTON_CLICK, self.handleNaviBtnClick, False, 0, True)
        self.widget.haoganBtn.addEventListener(events.BUTTON_CLICK, self.handleHanganBtnClick, False, 0, True)
        self.widget.guanxiBtn.addEventListener(events.BUTTON_CLICK, self.handleGuanxiBtnClick, False, 0, True)
        self.widget.questBtn.visible = False
        self.widget.questBtn.addEventListener(events.BUTTON_CLICK, self.handleQuestBtnClick, False, 0, True)

    def handleHanganBtnClick(self, *args):
        self.uiAdapter.npcRelationship.widget.setTabIndex(uiConst.NPC_RELATIONSHIP_TAB_HAOGAN)

    def handleGuanxiBtnClick(self, *args):
        self.uiAdapter.npcRelationship.widget.setTabIndex(uiConst.NPC_RELATIONSHIP_TAB_GUANXI)

    def handleNaviBtnClick(self, *args):
        e = ASObject(args[3][0])
        seedId = int(e.currentTarget.data)
        uiUtils.findPosById(seedId)

    def labelFunction(self, *args):
        npcId = int(args[3][0].GetNumber())
        itemMc = ASObject(args[3][1])
        p = BigWorld.player()
        name = NND.data.get(npcId, {}).get('name', '')
        if p.friend.has_key(npcId):
            headIcon = uiUtils.getPNpcIcon(npcId)
            _, friendlvVal = p.npcFavor.getPlayerRelationLvAndVal(npcId)
            if npcId == p.npcFavor.todayFavor[0]:
                tips = gameStrings.NPC_OVER_VIEW_FAVOR_TIP % friendlvVal + '\n' + gameStrings.NPC_OVER_VIEW_DAILY_FAVOR % p.npcFavor.npcFavorValueDaily.get(npcId, 0)
            else:
                tips = gameStrings.NPC_OVER_VIEW_FAVOR_TIP % friendlvVal
            TipManager.addTip(itemMc, tips)
        else:
            headIcon = NOT_ADD_FRIEND_ICON_PATH
            TipManager.removeTip(itemMc)
        itemMc.npcIcon.fitSize = True
        itemMc.npcIcon.loadImage(headIcon)
        itemMc.label = name
        itemMc.groupName = 'npcIcon'
        itemMc.data = npcId
        if self.selectedNpcId == npcId:
            if self.selectedMc:
                self.selectedMc.selected = False
            self.selectedMc = itemMc
            itemMc.selected = True
        else:
            itemMc.selected = False
        itemMc.isFavorNpc.visible = npcId == p.npcFavor.todayFavor[0]
        itemMc.addEventListener(events.BUTTON_CLICK, self.handleItemClick, False, 0, True)

    def handleQuestBtnClick(self, *args):
        p = BigWorld.player()
        npcId = p.npcFavor.todayFavor[0]
        if not p.npcFavor.todayFavor[1]:
            if self.uiAdapter.chatToFriend.isOpened(str(-npcId)):
                med = ASObject(self.uiAdapter.chatToFriend.friendMeds[str(-npcId)])
                med.swapPanelToFront()
            else:
                self.uiAdapter.friend.beginChat(const.FRIEND_NPC_ID, npcId)
        else:
            questNpcPId, questId = p.npcFavor.todayFavor
            questItemInfo = commNpcFavor.getQuestItemInfo(questId)
            questItemGId, questItemCnt = questItemInfo if questItemInfo else ((), 0)
            p.showGameMsg(GMDD.data.NF_NPC_FAVOR_DOING if p.npcFavor.questItemCnt < questItemCnt else GMDD.data.NPC_FAVOR_COMPLETED, {})

    def handleItemClick(self, *args):
        e = ASObject(args[3][0])
        npcId = int(e.currentTarget.data)
        p = BigWorld.player()
        if npcId == self.selectedNpcId:
            return
        if self.selectedMc:
            self.selectedMc.selected = False
        self.selectedMc = e.currentTarget
        self.selectedMc.selected = True
        e.currentTarget.selected = True
        self.selectedNpcId = npcId
        self.refreshDetail()

    def handleTypeBtnClick(self, *args):
        e = ASObject(args[3][0])
        selectedType = int(e.currentTarget.data)
        if selectedType == self.selectedType:
            return
        self.selectedNpcId = 0
        self.selectedType = selectedType
        self.refreshInfo()

    def getNpcList(self):
        npcList = []
        for npcId, data in NND.data.iteritems():
            npcLv = data.get('npcLv', 0)
            if not data.get('isGift', 0):
                continue
            if self.selectedType != SELECTED_TYPE_ALL and npcLv != self.selectedType:
                continue
            npcList.append(npcId)

        npcList.sort(cmp=self.cmpNpc, reverse=True)
        return npcList

    def cmpNpc(self, idA, idB):
        p = BigWorld.player()
        isAddFriendFlagA = 1 if p.friend.has_key(idA) else -1
        isAddFriendFlagB = 1 if p.friend.has_key(idB) else -1
        npcLvA = NND.data.get(idA, {}).get('npcLv', 0)
        npcLvB = NND.data.get(idB, {}).get('npcLv', 0)
        return cmp((isAddFriendFlagA, npcLvA, idB), (isAddFriendFlagB, npcLvB, idA))

    def refreshInfo(self):
        if not self.widget:
            return
        npcList = self.getNpcList()
        if not self.selectedNpcId:
            self.selectedNpcId = npcList[0]
        self.widget.npcList.dataArray = npcList
        self.refreshDetail()
        unlockCnt = len(set(npcList) & set(BigWorld.player().friend.keys()))
        self.widget.txtUnlock.text = gameStrings.NPC_UNLOCK_TXT % (unlockCnt, len(npcList))

    def refreshDetail(self):
        p = BigWorld.player()
        if self.selectedNpcId == p.npcFavor.todayFavor[0]:
            self.widget.questBtn.visible = True
        else:
            self.widget.questBtn.visible = False
        if not p.friend.has_key(self.selectedNpcId):
            self.widget.selectedIcon.loadImage(NOT_ADD_FRIEND_ICON_PATH)
            self.widget.txtName.text = NND.data.get(self.selectedNpcId, {}).get('name', '')
            self.widget.quality.gotoAndStop('level%d' % (commNpcFavor.getNpcLv(self.selectedNpcId) - 1))
            self.widget.friendlyLv.gotoAndStop('level0')
            for i in xrange(self.widget.friendlyLv.numChildren):
                mc = self.widget.friendlyLv.getChildAt(i)
                if mc.text:
                    mc.text = gameStrings.NOT_ADD_FRIEND_TXT
                    break

            seekId = NND.data.get(self.selectedNpcId, {}).get('seekId', 0)
            spaceNo = SD.data.get(seekId, {}).get('spaceNo', 0)
            x, y, z = SD.data.get(seekId, {}).get('xpos', 0), SD.data.get(seekId, {}).get('ypos', 0), SD.data.get(seekId, {}).get('zpos', 0)
            spaceName = formula.whatSpaceName(spaceNo, False)
            self.widget.txtPos.htmlText = gameStrings.NPC_NAVI_POS % (spaceNo,
             x,
             y,
             z,
             spaceName)
            self.widget.naviBtn.data = seekId
            self.widget.txtBorn.text = gameStrings.NOT_ADD_FRIEND_TXT
            self.widget.txtDesc.text = gameStrings.NOT_ADD_FRIEND_TXT
            self.widget.txtNews.text = gameStrings.NOT_ADD_FRIEND_TXT
        else:
            self.widget.selectedIcon.loadImage(uiUtils.getPNpcIcon(self.selectedNpcId))
            self.widget.txtName.text = NND.data.get(self.selectedNpcId, {}).get('name', '')
            self.widget.quality.gotoAndStop('level3')
            self.widget.quality.gotoAndStop('level%d' % (commNpcFavor.getNpcLv(self.selectedNpcId) - 1))
            friendlyLv, _ = p.npcFavor.getPlayerRelationLvAndVal(self.selectedNpcId)
            self.widget.friendlyLv.gotoAndStop('level%d' % friendlyLv)
            seekId = NND.data.get(self.selectedNpcId, {}).get('seekId', 0)
            spaceNo = SD.data.get(seekId, {}).get('spaceNo', 0)
            x, y, z = SD.data.get(seekId, {}).get('xpos', 0), SD.data.get(seekId, {}).get('ypos', 0), SD.data.get(seekId, {}).get('zpos', 0)
            spaceName = formula.whatSpaceName(spaceNo, False)
            self.widget.txtPos.htmlText = gameStrings.NPC_NAVI_POS % (spaceNo,
             x,
             y,
             z,
             spaceName)
            self.widget.naviBtn.data = seekId
            cfgData = NND.data.get(self.selectedNpcId, {})
            self.widget.txtBorn.text = cfgData.get('birthday', 'birthday')
            self.widget.txtDesc.text = cfgData.get('txtDesc', 'desc')
            self.widget.txtNews.text = self.uiAdapter.friend.getNpcTxtNews(self.selectedNpcId)
