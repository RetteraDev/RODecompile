#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/npcRelationshipHaoganProxy.o
import BigWorld
import commNpcFavor
import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import MenuManager
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis.asObject import ASUtils
from data import nf_npc_level_data as NNLD
from data import nf_npc_data as NND
from data import nf_npc_friendly_level_data as NNFLD
LEVEL_CNT = 7
LITTLE_ICON_MAX_CNT = 8
TIP_CNT = 3

class NpcRelationshipHaoganProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NpcRelationshipHaoganProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.littleIconList = []

    @property
    def npcId(self):
        return self.uiAdapter.npcRelationship.npcId

    def reset(self):
        self.littleIconList = []
        super(NpcRelationshipHaoganProxy, self).reset()

    def initPanel(self, widget):
        BigWorld.player().base.queryTopPFriendlyWithLvNF(self.npcId)
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initUI(self):
        self.widget.tips.visible = False

    def getTopFriends(self):
        p = BigWorld.player()
        if not p.npcFavor.topFriend.has_key(self.npcId) or not p.npcFavor.isShowNpcDetail(self.npcId):
            return []
        topList = p.npcFavor.topFriend[self.npcId][:]
        topList.sort(cmp=p.npcFavor.cmpFriendVal)
        return topList

    def refreshLittleIcons(self):
        if not self.widget:
            return
        topFriends = self.getTopFriends()
        topFriends = topFriends[:LITTLE_ICON_MAX_CNT + 2]
        for level in xrange(LEVEL_CNT):
            for angle in xrange(LITTLE_ICON_MAX_CNT + 1):
                mc = self.widget.getChildByName('littleIcon%d%d' % (level, angle))
                if mc:
                    mc.visible = False

        angle = 0
        for idx, npcFriendVal in enumerate(topFriends):
            if angle == 4:
                angle += 1
            angle = angle % LITTLE_ICON_MAX_CNT
            pfVal = npcFriendVal.pfVal
            level = commNpcFavor.getPFriendlyLv(self.npcId, pfVal, BigWorld.player())
            mc = self.widget.getChildByName('littleIcon%d%d' % (level - 2, angle))
            gbId = npcFriendVal.gbId
            name = npcFriendVal.name
            school = npcFriendVal.school
            sex = npcFriendVal.sex
            if npcFriendVal.photo and uiUtils.isDownloadImage(npcFriendVal.photo):
                photo = npcFriendVal.photo
            else:
                photo = 'headIcon/%s.dds' % str(school * 10 + sex)
            mc.borderImg.fitSize = True
            mc.borderImg.loadImage(BigWorld.player().getPhotoBorderIcon(npcFriendVal.borderId, uiConst.PHOTO_BORDER_ICON_SIZE40))
            if mc:
                mc.visible = True
                mc.icon.fitSize = True
                if uiUtils.isDownloadImage(photo):
                    mc.icon.imgType = uiConst.IMG_TYPE_NOS_FILE
                    mc.icon.url = photo
                else:
                    mc.icon.loadImage(photo)
                MenuManager.getInstance().registerMenuById(mc, uiConst.MENU_CHAT, {'roleName': name,
                 'gbId': gbId})
                TipManager.addTip(mc, name)
            angle += 1

        for i in xrange(2, 9):
            textMc = self.widget.getChildByName('level%d' % i)
            textMc.selectable = False
            TipManager.addTipByFunc(textMc, self.showFriendLvTip, (textMc, i), False)

    def showFriendLvTip(self, *args):
        args = ASObject(args[3][0])
        mc = args[0]
        lv = args[1]
        friendLvTips = NNLD.data.get((self.npcId, lv), {}).get('friendLvTips', ())
        self.widget.tips.visible = True
        for i in xrange(TIP_CNT):
            tipsMc = self.widget.tips.getChildByName('tips%d' % i)
            if i < len(friendLvTips):
                tipsMc.visible = True
                title, content = friendLvTips[i]
                tipsMc.title.text = title
                tipsMc.content.text = content
            else:
                tipsMc.visible = False

        TipManager.showImediateTip(mc, self.widget.tips)
        if not friendLvTips:
            self.widget.tips.visible = False

    def refreshInfo(self):
        if not self.widget:
            return
        npcName = NND.data.get(self.npcId, {}).get('name', '')
        if not BigWorld.player().npcFavor.isShowNpcDetail(self.npcId):
            npcIcon = 'npcHeadIcon/-1.dds'
        else:
            npcIcon = uiUtils.getPNpcIcon(self.npcId)
        self.widget.txtPlayerName.text = npcName
        self.widget.npcIcon.headIcon.fitSize = True
        self.widget.npcIcon.headIcon.loadImage(npcIcon)
        p = BigWorld.player()
        level, pVal = p.npcFavor.getPlayerRelationLvAndVal(self.npcId)
        npcQuality = commNpcFavor.getNpcLv(self.npcId)
        if NNFLD.data.has_key((npcQuality, level + 1)):
            rewardId = NNFLD.data.get((npcQuality, level + 1), {}).get('rewardId', 0)
            self.widget.inventroySlot.visible = True
            self.widget.inventroySlot.setItemSlotData(uiUtils.getGfxItemById(rewardId, 1))
        else:
            rewardId = NNFLD.data.get((npcQuality, level), {}).get('rewardId', 0)
            self.widget.inventroySlot.visible = True
            self.widget.inventroySlot.setItemSlotData(uiUtils.getGfxItemById(rewardId, 1))
        self.refreshLittleIcons()
