#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/npcRelationshipGuanxiProxy.o
import BigWorld
import commNpcFavor
import uiConst
from guis.asObject import ASObject
from guis.asObject import MenuManager
from guis import events
from guis import uiUtils
from uiProxy import UIProxy
from data import nf_npc_data as NND
from data import nf_npc_friendly_level_data as NNFLD
from data import sys_config_data as SCD
SUB_TAB_FRIEND = 0
SUB_TAB_ENEMY = 1
SUB_TAB_FAMILY = 2
FRIEND_MAX_CNT = 6
NOT_ADD_FRIEND_ICON_PATH = 'npcHeadIcon/-1.dds'

class NpcRelationshipGuanxiProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NpcRelationshipGuanxiProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.subTabIdx = SUB_TAB_FRIEND

    def initPanel(self, widget):
        self.npcId = self.uiAdapter.npcRelationship.npcId
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initUI(self):
        self.widget.friendBtn.addEventListener(events.BUTTON_CLICK, self.handleFriendBtnClick, False, 0, True)
        self.widget.enemyBtn.addEventListener(events.BUTTON_CLICK, self.handleEnemyBtnClick, False, 0, True)
        self.widget.familyBtn.addEventListener(events.BUTTON_CLICK, self.handleFamilyBtnClick, False, 0, True)

    def handleFriendBtnClick(self, *args):
        self.subTabIdx = SUB_TAB_FRIEND
        self.refreshInfo()

    def handleEnemyBtnClick(self, *args):
        self.subTabIdx = SUB_TAB_ENEMY
        self.refreshInfo()

    def handleFamilyBtnClick(self, *args):
        self.subTabIdx = SUB_TAB_FAMILY
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.friendBtn.selected = self.subTabIdx == SUB_TAB_FRIEND
        self.widget.enemyBtn.selected = self.subTabIdx == SUB_TAB_ENEMY
        self.widget.familyBtn.selected = self.subTabIdx == SUB_TAB_FAMILY
        self.widget.friend.visible = self.subTabIdx in (SUB_TAB_FRIEND, SUB_TAB_ENEMY)
        self.widget.family.visible = self.subTabIdx == SUB_TAB_FAMILY
        self.subTabIdx == SUB_TAB_FRIEND and self.refreshFriend()
        self.subTabIdx == SUB_TAB_ENEMY and self.refreshEnemy()
        self.subTabIdx == SUB_TAB_FAMILY and self.refreshFamily()

    def refreshFriend(self):
        if not self.widget:
            return
        else:
            self.widget.friend.npc.headIcon.fitSize = True
            if not BigWorld.player().npcFavor.isShowNpcDetail(self.npcId):
                self.widget.friend.npc.headIcon.loadImage(NOT_ADD_FRIEND_ICON_PATH)
            else:
                self.widget.friend.npc.headIcon.loadImage(uiUtils.getPNpcIcon(self.npcId))
            self.widget.friend.txtNpcName.txt.text = NND.data.get(self.npcId, {}).get('name', '')
            friend = NND.data.get(self.npcId, {}).get('friend', None) if BigWorld.player().friend.has_key(self.npcId) else []
            for index in xrange(FRIEND_MAX_CNT):
                friendMc = self.widget.friend.getChildByName('friend%d' % index)
                if not friend or index >= len(friend):
                    friendMc.visible = False
                else:
                    friendMc.visible = True
                    npcId, friendLv = friend[index]
                    npcLv = NND.data.get(self.npcId, {}).get('npcLv', 0)
                    friendMc.level.gotoAndStop('level%d' % friendLv)
                    friendMc.level.txtLevel.text = NNFLD.data.get((npcLv, friendLv), {}).get('friendlyName', '')
                    friendMc.friend.icon.headIcon.fitSize = True
                    friendMc.friend.icon.headIcon.loadImage(uiUtils.getPNpcIcon(npcId))
                    friendMc.txtFriend.txt.text = NND.data.get(npcId, {}).get('name', '')

            return

    def refreshEnemy(self):
        if not self.widget:
            return
        else:
            self.widget.friend.npc.headIcon.fitSize = True
            if not BigWorld.player().npcFavor.isShowNpcDetail(self.npcId):
                self.widget.friend.npc.headIcon.loadImage(NOT_ADD_FRIEND_ICON_PATH)
            else:
                self.widget.friend.npc.headIcon.loadImage(uiUtils.getPNpcIcon(self.npcId))
            self.widget.friend.txtNpcName.txt.text = NND.data.get(self.npcId, {}).get('name', '')
            enemy = NND.data.get(self.npcId, {}).get('enemy', None) if BigWorld.player().friend.has_key(self.npcId) else []
            for index in xrange(FRIEND_MAX_CNT):
                friendMc = self.widget.friend.getChildByName('friend%d' % index)
                if not enemy or index >= len(enemy):
                    friendMc.visible = False
                else:
                    friendMc.visible = True
                    npcId, friendLv = enemy[index]
                    npcLv = NND.data.get(self.npcId, {}).get('npcLv', 0)
                    friendMc.level.gotoAndStop('level%d' % friendLv)
                    friendMc.level.txtLevel.text = NNFLD.data.get((npcLv, friendLv), {}).get('friendlyName', '')
                    friendMc.friend.icon.headIcon.fitSize = True
                    friendMc.friend.icon.headIcon.loadImage(uiUtils.getPNpcIcon(npcId))
                    friendMc.txtFriend.txt.text = NND.data.get(npcId, {}).get('name', '')

            return

    def getNpcInfo(self, npcId):
        if npcId == 0:
            return ('', 'npcHeadIcon/-1.dds')
        configData = NND.data.get(npcId, {})
        name = configData.get('name', '')
        photoIcon = uiUtils.getPNpcIcon(npcId)
        return (name, photoIcon)

    def setNpcRelationMc(self, cfgName, mcName):
        configData = NND.data.get(self.npcId, {}).get(cfgName, (0, 0)) if BigWorld.player().npcFavor.isShowNpcDetail(self.npcId) else [-1, -1]
        relationMc = self.widget.family.getChildByName(mcName)
        if configData and type(configData) not in (tuple, list):
            configData = (configData,)
        if list(configData) == [-1, -1]:
            relationMc.visible = False
            return
        relationMc.visible = True
        txtMcName = 'txt' + mcName[0].upper() + mcName[1:]
        firstMc = relationMc.getChildByName(mcName)
        firstTxtMc = relationMc.getChildByName(txtMcName)
        if configData[0] == -1:
            firstMc.gotoAndStop('noPlayer')
            firstTxtMc.txt.text = ''
        else:
            npcName, icon = self.getNpcInfo(configData[0])
            firstMc.gotoAndStop('player')
            firstMc.icon.headIcon.fitSize = True
            firstMc.icon.headIcon.loadImage(icon)
            firstTxtMc.txt.text = npcName
        anotherMc = relationMc.getChildByName(mcName + '2')
        secondMc = anotherMc.getChildByName(mcName + '2')
        secondTxtMc = anotherMc.getChildByName(txtMcName + '2')
        if len(configData) < 2:
            anotherMc.visible = False
            return
        anotherMc.visible = True
        if configData[1] == -1:
            secondMc.gotoAndStop('noPlayer')
            secondTxtMc.txt.text = ''
        else:
            secondMc.visible = True
            npcName, icon = self.getNpcInfo(configData[1])
            secondMc.gotoAndStop('player')
            secondMc.icon.headIcon.fitSize = True
            secondMc.icon.headIcon.loadImage(icon)
            secondTxtMc.txt.text = npcName

    def refreshFamily(self):
        if not self.widget:
            return
        npcName, icon = self.getNpcInfo(self.npcId)
        self.widget.family.txtNpcName.txt.text = npcName
        self.widget.family.npc.headIcon.fitSize = True
        if not BigWorld.player().npcFavor.isShowNpcDetail(self.npcId):
            self.widget.family.npc.headIcon.loadImage(NOT_ADD_FRIEND_ICON_PATH)
        else:
            self.widget.family.npc.headIcon.loadImage(icon)
        self.setNpcRelationMc('teacher', 'teacher')
        self.setNpcRelationMc('parent', 'parentMc')
        if not self.widget.family.teacher.visible and not self.widget.family.parentMc.visible:
            self.widget.family.top.visible = False
        else:
            self.widget.family.top.visible = True
        self.setNpcRelationMc('brother', 'friend')
        self.setNpcRelationMc('couple', 'couple')
        self.setNpcRelationMc('disciple', 'disciple')
        self.setNpcRelationMc('child', 'child')
        if not self.widget.family.disciple.visible and not self.widget.family.child.visible:
            self.widget.family.bottom.visible = False
        else:
            self.widget.family.bottom.visible = True
