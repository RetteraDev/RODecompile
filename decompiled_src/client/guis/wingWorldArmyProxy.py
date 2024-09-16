#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldArmyProxy.o
import BigWorld
import gameglobal
import events
import uiUtils
import const
import gametypes
import wingWorldUtils
from gameStrings import gameStrings
from uiProxy import UIProxy
from asObject import ASObject
from guis.asObject import MenuManager
from guis import uiConst
from guis.asObject import ASUtils
from data import wing_world_army_data as WWAD
from cdata import game_msg_def_data as GMDD
CAMP_POST_ITEM_HEIGHT = 38
IMAGE_PATH = 'wingWorld/wingWorldFlag/%d.dds'

class WingWorldArmyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldArmyProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.widget = None
        self.selectGeneralPostId = 0
        self.selectedPostId = 0

    def initPanel(self, widget):
        self.widget = widget
        p = BigWorld.player()
        p.cell.queryWingWorldArmy(p.wingWorld.armyVer, p.wingWorld.armyOnlineVer)
        self.initUI()
        self.refreshInfo()

    def unRegisterPanel(self):
        self.reset()

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if p.isWingWorldCampArmy():
            self.widget.armyTree.visible = False
            self.refreshNewWnd()
        else:
            self.widget.campArmyTree.visible = False

    def refreshNewWnd(self):
        self.widget.campArmyTree.itemRenderer = 'WingWorldArmy_CampPostItem'
        self.widget.campArmyTree.labelFunction = self.campPostLabelFunc
        self.widget.campArmyTree.itemHeight = CAMP_POST_ITEM_HEIGHT
        allGeneralList = gameglobal.rds.ui.wingWorld.getLeaderAndGeneralInfo()
        dataArray = []
        for general in allGeneralList:
            dataArray.append({'postId': general.postId,
             'name': general.name})

        self.widget.campArmyTree.dataArray = dataArray
        self.widget.campArmyTree.validateNow()
        self.widget.attr3.text = gameStrings.WIDG_WORLD_CAMP_WEEK_CONTIRB
        self.widget.attr4.text = gameStrings.WIDG_WORLD_CAMP_SEASON_CONTIRB

    def campPostLabelFunc(self, *args):
        p = BigWorld.player()
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.label = itemData.name
        itemMc.focusable = False
        itemMc.postId = itemData.postId
        itemMc.addEventListener(events.BUTTON_CLICK, self.onCampPostBtnClick)
        itemMc.icon.fitSize = True
        armyData = wingWorldUtils.getWingArmyData()
        iconName = armyData.get(itemData.postId, {}).get('armyIcon1', '') if p.wingWorldCamp == 1 else armyData.get(itemData.postId, {}).get('armyIcon2', '')
        if self.selectGeneralPostId == itemData.postId:
            itemMc.selected = True
        else:
            itemMc.selected = False
        if iconName:
            itemMc.icon.visible = True
            itemMc.icon.loadImage(IMAGE_PATH % iconName)
        else:
            itemMc.icon.visible = False

    def onCampPostBtnClick(self, *args):
        e = ASObject(args[3][0])
        self.selectGeneralPostId = e.currentTarget.postId
        self.widget.tipTextField.text = ''
        self.refreshMemberList(self.selectGeneralPostId)
        self.widget.campArmyTree.dataArray = self.widget.campArmyTree.dataArray

    def initUI(self):
        p = BigWorld.player()
        self.widget.tipTextField.text = gameStrings.WING_WORLD_ARMY_TIP_TEXT1
        armyState = p.wingWorld.armyState
        if p.isWingWorldCampArmy():
            self.widget.appointBtn.visible = p.wingWorld.isPlayerGeneral(p.gbId)
        else:
            self.widget.appointBtn.visible = p.wingWorld.isPlayerGeneral(p.gbId) and armyState == gametypes.WING_WORLD_ARMY_STATE_OPEN
        self.widget.appointBtn.addEventListener(events.MOUSE_CLICK, self.handleAppointClick, False, 0, True)
        self.widget.skillBtn.addEventListener(events.MOUSE_CLICK, self.handleSkillClick, False, 0, True)
        for i in xrange(3):
            btn = self.widget.armyTree.canvas.getChildByName('army%d' % i)
            btn.groupName = 'wingWorldArmyMgrsBtn'
            btn.index = i + 1
            btn.addEventListener(events.MOUSE_CLICK, self.handleArmyBtnClick)

        self.refreshMarshalPanel()

    def handleAppointClick(self, *args):
        if BigWorld.player()._isSoul():
            BigWorld.player().showGameMsg(GMDD.data.WING_WORLD_SOUL_FORBIDDEN, ())
            return
        gameglobal.rds.ui.wingWorldAppoint.show()

    def handleSkillClick(self, *args):
        p = BigWorld.player()
        gameglobal.rds.ui.wingWorldArmySkill.show()
        p.cell.queryWingWorldVolatile(p.wingWorld.volatileVer)

    def handleArmyBtnClick(self, *args):
        btn = ASObject(args[3][0]).target
        btn.selected = True
        selectedPostId = btn.index
        if selectedPostId == self.selectedPostId:
            selectedPostId = 0
        self.selectedPostId = selectedPostId
        self.refreshGeneralArmyTree(selectedPostId)

    def handleGeneralClick(self, *args):
        e = ASObject(args[3][0])
        if e.buttonIdx == uiConst.RIGHT_BUTTON:
            return
        btn = e.target
        self.selectGeneralPostId = btn.postId
        self.widget.tipTextField.text = ''
        self.refreshMemberList(self.selectGeneralPostId)

    def refreshOldMarshalPanel(self):
        if not self.widget:
            return
        armyMc = self.widget.armyMc.mainMc
        generalList = gameglobal.rds.ui.wingWorld.getArmyMgrInfo()
        p = BigWorld.player()
        for i in xrange(6):
            armyName = armyMc.getChildByName('army%dName' % i)
            btnName = self.widget.armyTree.canvas.getChildByName('army%d' % i)
            if armyName:
                armyName.text = gameStrings.WING_WORLD_NO_LEADER
            if btnName:
                btnName.label = wingWorldUtils.getWingArmyData().get(i + 1, {}).get('categoryName', '')

        if generalList:
            for general in generalList:
                index = general.postId - 1
                armyName = armyMc.getChildByName('army%dName' % index)
                armyIconMc = armyMc.getChildByName('army%dIcon' % index)
                armyIcon = armyIconMc.icon
                borderImg = armyIconMc.borderImg
                if armyName:
                    armyName.text = general.name
                photo = general.photo
                if uiUtils.isDownloadImage(photo):
                    BigWorld.player().downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, self.onDownloadOtherPhoto, (photo, armyIcon))
                else:
                    photo = 'headIcon/%s.dds' % str(general.school * 10 + general.sex)
                    armyIcon.fitSize = True
                    armyIcon.loadImage(photo)
                borderImg.fitSize = True
                borderImg.loadImage(p.getPhotoBorderIcon(general.borderId, uiConst.PHOTO_BORDER_ICON_SIZE40))
                ASUtils.setHitTestDisable(borderImg, True)
                MenuManager.getInstance().registerMenuById(armyIcon, uiConst.MENU_RANK, {'roleName': general.name,
                 'gbId': general.gbId})

    def refreshNewMarshalPanel(self):
        if not self.widget:
            return
        armyMc = self.widget.armyMc.mainMc
        generalList = gameglobal.rds.ui.wingWorld.getArmyMgrInfo()
        p = BigWorld.player()
        for i in xrange(5):
            armyName = armyMc.getChildByName('army%dName' % i)
            armyTitleMc = armyMc.getChildByName('army%dTitle' % i)
            if armyName:
                armyName.text = gameStrings.WING_WORLD_NO_LEADER
            if i == 0:
                armyTitleMc.gotoAndStop('c%d1' % p.wingWorldCamp)
            else:
                armyTitleMc.gotoAndStop('c%d2' % p.wingWorldCamp)

        if generalList:
            for general in generalList:
                index = general.postId - 1
                armyName = armyMc.getChildByName('army%dName' % index)
                armyIconMc = armyMc.getChildByName('army%dIcon' % index)
                armyIcon = armyIconMc.icon
                borderImg = armyIconMc.borderImg
                if armyName:
                    armyName.text = general.name
                photo = general.photo
                if uiUtils.isDownloadImage(photo):
                    if general.hostId == p.getOriginHostId():
                        BigWorld.player().downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, self.onDownloadOtherPhoto, (photo, armyIcon))
                    else:
                        BigWorld.player().downloadCrossNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, general.hostId, gametypes.NOS_FILE_PICTURE, self.onDownloadOtherPhoto, (photo, armyIcon))
                else:
                    photo = 'headIcon/%s.dds' % str(general.school * 10 + general.sex)
                    armyIcon.fitSize = True
                    armyIcon.loadImage(photo)
                borderImg.fitSize = True
                borderImg.loadImage(p.getPhotoBorderIcon(general.borderId, uiConst.PHOTO_BORDER_ICON_SIZE40))
                ASUtils.setHitTestDisable(borderImg, True)
                MenuManager.getInstance().registerMenuById(armyIcon, uiConst.MENU_RANK, {'roleName': general.name,
                 'gbId': general.gbId,
                 'hostId': general.hostId})

    def refreshMarshalPanel(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if p.isWingWorldCampArmy():
            self.widget.armyMc.gotoAndStop('new')
            armyMc = self.widget.armyMc.mainMc
            armyMc.gotoAndStop('camp%d' % p.wingWorldCamp)
            self.refreshNewMarshalPanel()
        else:
            self.widget.armyMc.gotoAndStop('old')
            self.refreshOldMarshalPanel()

    def onDownloadOtherPhoto(self, status, nosPath, armyIcon):
        if not self.widget:
            return
        photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + nosPath + '.dds'
        armyIcon.fitSize = True
        armyIcon.loadImage(photo)

    def refreshGeneralArmyTree(self, index):
        generalList = gameglobal.rds.ui.wingWorld.getSupportArmyInfo(index)
        p = BigWorld.player()
        lastBtn = self.widget.armyTree.canvas.army0
        for i in xrange(3):
            if i == 0:
                continue
            btn = self.widget.armyTree.canvas.getChildByName('army%d' % i)
            btn.y = lastBtn.y + 54
            if i == index:
                btn.y = btn.y + 39 * len(generalList) + 3
            lastBtn = btn

        lastBtn = self.widget.armyTree.canvas.getChildByName('army%d' % (index - 1))
        for i in xrange(13):
            generalBtn = self.widget.armyTree.canvas.getChildByName('general%d' % i)
            if i < len(generalList):
                if generalBtn == None:
                    generalBtn = self.widget.getInstByClsName('WingWorldArmy_wanjiamingzi')
                    generalBtn.name = 'general%d' % i
                generalBtn.visible = True
                generalBtn.label = generalList[i].name
                generalBtn.postId = generalList[i].postId
                generalBtn.addEventListener(events.MOUSE_CLICK, self.handleGeneralClick, False, 0, True)
                generalBtn.x = self.widget.armyTree.canvas.army0.x + 4
                general = generalList[i]
                if i == 0:
                    generalBtn.y = lastBtn.y + 54
                else:
                    generalBtn.y = lastBtn.y + 39
                lastBtn = generalBtn
                self.widget.armyTree.setContent(generalBtn)
                if p.isWingWorldCampArmy():
                    MenuManager.getInstance().registerMenuById(generalBtn, uiConst.MENU_RANK, {'roleName': general.name,
                     'gbId': general.gbId,
                     'hostId': general.hostId})
                else:
                    MenuManager.getInstance().registerMenuById(generalBtn, uiConst.MENU_RANK, {'roleName': general.name,
                     'gbId': general.gbId})
            elif generalBtn != None:
                generalBtn.visible = False

    def refreshMemberList(self, postId):
        armyList = gameglobal.rds.ui.wingWorld.getSupportSoldierInfo(postId)
        armyListArray = []
        armyData = wingWorldUtils.getWingArmyData()
        for player in armyList:
            armyListArray.append({'name': player.name,
             'postName': armyData.get(player.postId, {}).get('name', ()),
             'combatScore': player.combatScore,
             'zhanXun': player.weeklyZhanXun,
             'gbId': player.gbId,
             'rescueCnt': player.yabiaoRescue,
             'hostId': getattr(player, 'hostId', 0),
             'weekContrib': 0,
             'seasonContrib': 0})

        if armyListArray:
            self.widget.memberList.itemRenderer = 'WingWorldArmy_ListItemRenderer'
            self.widget.memberList.labelFunction = self.memberListItemFunction
            self.widget.memberList.itemHeight = 30
            self.widget.memberList.dataArray = armyListArray
        else:
            self.widget.memberList.dataArray = []
            self.widget.tipTextField.text = gameStrings.WING_WORLD_ARMY_TIP_TEXT2

    def memberListItemFunction(self, *arg):
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        p = BigWorld.player()
        if itemMc and info:
            itemMc.playerName.text = info.name
            itemMc.postName.text = info.postName
            itemMc.combatScore.text = int(info.combatScore)
            if p.isWingWorldCampArmy():
                itemMc.zhanXun.text = int(info.weekContrib)
                itemMc.txtRescueCnt.text = int(info.seasonContrib)
                MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_RANK, {'roleName': info.name,
                 'gbId': info.gbId,
                 'hostId': info.hostId})
            else:
                itemMc.zhanXun.text = int(info.zhanXun)
                itemMc.txtRescueCnt.text = int(info.rescueCnt)
                MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_RANK, {'roleName': info.name,
                 'gbId': info.gbId})
