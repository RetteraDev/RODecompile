#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/npcRelationshipXindongProxy.o
import BigWorld
import gameglobal
from callbackHelper import Functor
import gamelog
import gametypes
import const
from guis import events
from guis import uiConst
from guis import uiUtils
from guis.asObject import ASObject
from guis.asObject import MenuManager
import utils
from gamestrings import gameStrings
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD
from data import nf_npc_data as NND
from data import sys_config_data as SCD
RANK_NPC_CNT = 5

class NpcRelationshipXindongProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NpcRelationshipXindongProxy, self).__init__(uiAdapter)
        self.widget = None
        self.version = 0
        self.rankData = {}
        self.reset()

    def reset(self):
        self.npcArray = []
        self.playerArray = []
        self.selectedNpcIdx = -1
        self.lastSelectedMc = None
        self.rankData = {}
        self.lastQueryTime = 0

    def getSelectedNpcId(self):
        if self.selectedNpcIdx >= 0 and self.selectedNpcIdx < len(self.npcArray):
            return self.npcArray[self.selectedNpcIdx].get('npcId', 0)
        return 0

    def getPlayerList(self):
        if self.selectedNpcIdx >= 0 and self.selectedNpcIdx < len(self.npcArray):
            return self.npcArray[self.selectedNpcIdx].get('playerList', [])
        return []

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.refreshInfo()
        gamelog.info('jbx:queryTopUniversal', gametypes.TOP_TYPE_NPC_FAVOR, self.version, '0')
        BigWorld.player().base.queryTopUniversal(gametypes.TOP_TYPE_NPC_FAVOR, self.version, '0')
        self.lastQueryTime = utils.getNow()

    def checkQuery(self):
        if utils.getNow(False) - self.lastQueryTime > 1.1:
            return True
        else:
            gameglobal.rds.ui.systemTips.show(gameStrings.NPC_RANK_QUERY_CD)
            return False

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def updateRankData(self, data):
        gamelog.info('jbx:updateRankData', data)
        topId = data.get(gametypes.TOP_UNIVERSAL_TOP_ID, 0)
        if not topId or not topId == gametypes.TOP_TYPE_NPC_FAVOR:
            return
        else:
            key = data.get(gametypes.TOP_UNIVERSAL_KEY, None)
            self.rankData[key] = data
            self.refreshInfo()
            return

    def initUI(self):
        self.widget.npcList.labelFunction = self.npcLabelFunction
        self.widget.npcList.itemRenderer = 'NpcRelationshipXindong_NpcItemRender'
        self.widget.playerList.labelFunction = self.playerLabelFunction
        self.widget.playerList.itemRenderer = 'NpcRelationshipXindong_PlayerItemRender'
        self.widget.refreshBtn.addEventListener(events.BUTTON_CLICK, self.handleRefreshBtnClick, False, 0, True)
        self.widget.rewardBtn.addEventListener(events.BUTTON_CLICK, self.handleRewardBtnClick, False, 0, True)
        self.widget.txtRules.htmlText = SCD.data.get('npcRankRefreshRules', 'SCD.data.npcRankRefreshRules')

    def refreshInfo(self):
        if not self.widget:
            return
        oldNpcId = self.getSelectedNpcId()
        if not oldNpcId:
            oldNpcId = self.uiAdapter.npcRelationship.npcId
        self.npcArray = []
        p = BigWorld.player()
        idList = [ id for id, info in NND.data.items() if info.get('isGift', 0) ]
        idList.sort()
        for i, rankInfo in enumerate(self.rankData.get('0', {}).get(gametypes.TOP_UNIVERSAL_DATA_LIST, [])):
            dataInfo = {}
            npcId = rankInfo.get(gametypes.TOP_UNIVERSAL_GBID)
            dataInfo['npcId'] = npcId
            idList.remove(npcId)
            dataInfo['npcName'] = rankInfo.get(gametypes.TOP_UNIVERSAL_ROLE_NAME, '')
            dataInfo['iconPath'] = uiUtils.getPNpcIcon(npcId)
            dataInfo['value'] = rankInfo.get(gametypes.TOP_UNIVERSAL_VALUE, 0)
            dataInfo['timeStamp'] = rankInfo.get(gametypes.TOP_UNIVERSAL_VALUE_TIMESTAMP, 0)
            playerList = []
            for j, pRankInfo in enumerate(self.rankData.get(str(npcId), {}).get(gametypes.TOP_UNIVERSAL_DATA_LIST, [])):
                playInfo = {}
                playInfo['gbId'] = pRankInfo.get(gametypes.TOP_UNIVERSAL_GBID)
                school = pRankInfo.get(gametypes.TOP_UNIVERSAL_SCHOOL, p.school)
                sex = pRankInfo.get(gametypes.TOP_UNIVERSAL_SEX, p.school)
                photo = pRankInfo.get(gametypes.TOP_UNIVERSAL_PHOTO, '')
                if utils.isDownloadImage(photo):
                    playInfo['playerIcon'] = photo
                    playInfo['isNOS'] = True
                else:
                    playInfo['playerIcon'] = 'headIcon/%s.dds' % str(school * 10 + sex)
                    playInfo['isNOS'] = False
                playInfo['playerName'] = pRankInfo.get(gametypes.TOP_UNIVERSAL_ROLE_NAME, '')
                playInfo['value'] = pRankInfo.get(gametypes.TOP_UNIVERSAL_VALUE, 0)
                playInfo['timeStamp'] = pRankInfo.get(gametypes.TOP_UNIVERSAL_VALUE_TIMESTAMP, 0)
                borderId = pRankInfo.get(gametypes.TOP_UNIVERSAL_PHOTO_BORDER, 1)
                borderId = borderId if borderId else 1
                playInfo['borderImg'] = p.getPhotoBorderIcon(borderId, uiConst.PHOTO_BORDER_ICON_SIZE40)
                playerList.append(playInfo)

            dataInfo['playerList'] = playerList
            playerList.sort(cmp=self.cmpRankData)
            self.npcArray.append(dataInfo)

        self.npcArray.sort(cmp=self.cmpRankData)
        while len(self.npcArray) < RANK_NPC_CNT:
            npcId = idList.pop(0)
            dataInfo = {}
            dataInfo['npcId'] = npcId
            dataInfo['npcName'] = NND.data.get(npcId, {}).get('name', '')
            dataInfo['iconPath'] = uiUtils.getPNpcIcon(npcId)
            dataInfo['value'] = 0
            dataInfo['timeStamp'] = utils.getNow()
            dataInfo['playerList'] = []
            self.npcArray.append(dataInfo)

        for itemMc in self.widget.npcList.items:
            itemMc.selectedMc.visible = False

        self.selectedNpcIdx = 0
        for index, info in enumerate(self.npcArray):
            if info['npcId'] == oldNpcId:
                self.selectedNpcIdx = index
                break

        self.widget.npcList.dataArray = range(len(self.npcArray))
        self.playerArray = self.getPlayerList()
        self.widget.playerList.dataArray = range(len(self.playerArray))

    def cmpRankData(self, rankInfoA, rankInfoB):
        return cmp((rankInfoB['value'], rankInfoA['timeStamp']), (rankInfoA['value'], rankInfoB['timeStamp']))

    def npcLabelFunction(self, *args):
        rankIdx = int(args[3][0].GetNumber())
        itemMc = ASObject(args[3][1])
        itemMc.addEventListener(events.MOUSE_CLICK, self.handleNpcItemClick, False, 0, True)
        if rankIdx >= len(self.npcArray):
            return
        if self.selectedNpcIdx == rankIdx:
            if self.lastSelectedMc:
                self.lastSelectedMc.selectedMc.visible = False
            self.lastSelectedMc = itemMc
            itemMc.selectedMc.visible = True
            if not self.rankData.has_key(str(self.getSelectedNpcId())) and utils.getNow(False) > self.lastQueryTime:
                BigWorld.callback(1.1, Functor(BigWorld.player().base.queryTopUniversal, gametypes.TOP_TYPE_NPC_FAVOR, self.version, str(self.getSelectedNpcId())))
                self.lastQueryTime = utils.getNow(False) + 1.1
        else:
            itemMc.selectedMc.visible = False
        dataInfo = self.npcArray[rankIdx]
        itemMc.rankIdx = rankIdx
        itemMc.rank.text = str(rankIdx + 1)
        if rankIdx < 3:
            itemMc.top3Icon.visible = True
            itemMc.top3Icon.gotoAndStop('top%d' % (rankIdx + 1))
        else:
            itemMc.top3Icon.visible = False
        itemMc.headIcon.icon.fitSize = True
        itemMc.headIcon.icon.loadImage(dataInfo['iconPath'])
        itemMc.txtName.text = dataInfo['npcName']
        itemMc.txtValue.text = dataInfo['value']
        npcId = dataInfo['npcId']
        p = BigWorld.player()
        if p.friend.has_key(npcId):
            itemMc.nextBtn.visible = False
        else:
            itemMc.nextBtn.visible = True
            itemMc.nextBtn.data = npcId
            itemMc.nextBtn.addEventListener(events.BUTTON_CLICK, self.handleNextBtnClick, False, 0, True)

    def handleNextBtnClick(self, *args):
        e = ASObject(args[3][0])
        npcId = int(e.currentTarget.data)
        if not BigWorld.player().friend.has_key(npcId):
            BigWorld.player().base.addContactNF(npcId)
        else:
            BigWorld.player().showGameMsg(GMDD.data.ALREAD_ADD_NPC_FRIEND, ())

    def playerLabelFunction(self, *args):
        playerRankIdx = int(args[3][0].GetNumber())
        if playerRankIdx >= len(self.playerArray):
            return
        itemMc = ASObject(args[3][1])
        itemMc.rankIdx = playerRankIdx
        itemMc.rank.text = str(playerRankIdx + 1)
        if playerRankIdx < 3:
            itemMc.top3Icon.visible = True
            itemMc.top3Icon.gotoAndStop('top%d' % (playerRankIdx + 1))
        else:
            itemMc.top3Icon.visible = False
        dataInfo = self.playerArray[playerRankIdx]
        itemMc.headIcon.icon.fitSize = True
        if dataInfo['isNOS']:
            itemMc.headIcon.icon.imgType = uiConst.IMG_TYPE_NOS_FILE
            itemMc.headIcon.icon.url = dataInfo['playerIcon']
        else:
            itemMc.headIcon.icon.loadImage(dataInfo['playerIcon'])
        itemMc.headIcon.borderImg.fitSize = True
        itemMc.headIcon.borderImg.loadImage(dataInfo['borderImg'])
        itemMc.txtName.text = dataInfo['playerName']
        itemMc.txtValue.text = dataInfo['value']
        MenuManager.getInstance().registerMenuById(itemMc.headIcon, uiConst.MENU_CHAT, {'roleName': dataInfo['playerName'],
         'gbId': dataInfo['gbId']})

    def handleNpcItemClick(self, *args):
        if not self.checkQuery():
            return False
        e = ASObject(args[3][0])
        rankIdx = e.currentTarget.rankIdx
        if rankIdx == self.selectedNpcIdx:
            return
        if self.lastSelectedMc:
            self.lastSelectedMc.selectedMc.visible = False
        self.lastSelectedMc = e.currentTarget
        self.lastSelectedMc.selectedMc.visible = True
        self.selectedNpcIdx = rankIdx
        self.playerArray = self.getPlayerList()
        self.widget.playerList.dataArray = range(len(self.playerArray))
        BigWorld.player().base.queryTopUniversal(gametypes.TOP_TYPE_NPC_FAVOR, self.version, str(self.getSelectedNpcId()))
        self.lastQueryTime = utils.getNow(False)

    def handleRefreshBtnClick(self, *args):
        if not self.checkQuery():
            return False
        if self.getSelectedNpcId():
            gamelog.info('jbx:queryTopUniversal', gametypes.TOP_TYPE_NPC_FAVOR, self.version, str(self.getSelectedNpcId()))
            BigWorld.player().base.queryTopUniversal(gametypes.TOP_TYPE_NPC_FAVOR, self.version, '0')
            BigWorld.callback(1.1, Functor(BigWorld.player().base.queryTopUniversal, gametypes.TOP_TYPE_NPC_FAVOR, self.version, str(self.getSelectedNpcId())))
            self.lastQueryTime = utils.getNow(False) + 1.1
        else:
            gamelog.info('jbx:queryTopUniversal', gametypes.TOP_TYPE_NPC_FAVOR, self.version, '0')
            BigWorld.player().base.queryTopUniversal(gametypes.TOP_TYPE_NPC_FAVOR, self.version, '0')
            self.lastQueryTime = utils.getNow(False)

    def handleRewardBtnClick(self, *args):
        if not self.getSelectedNpcId():
            return
        gamelog.info('jbx:openRewardPanel', gametypes.TOP_TYPE_NPC_FAVOR, self.getSelectedNpcId())
        self.uiAdapter.ranking.openRewardPanel(const.PROXY_KEY_NPC_FAVOR, self.getSelectedNpcId(), useNewAwardPanel=True)
