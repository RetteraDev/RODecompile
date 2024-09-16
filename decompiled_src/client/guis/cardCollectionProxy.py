#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cardCollectionProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import events
import uiUtils
import uiConst
import const
from asObject import ASObject
from gamestrings import gameStrings
from callbackHelper import Functor
from uiProxy import UIProxy
from asObject import ASObject
from asObject import ASUtils
from data import card_atlas_data as CAD
from data import prop_ref_data as PRD
from data import prop_data as PD
CUR_ACTIVATE_PROP = 1
CUR_ATLAS_PROP = 2
ALL_ACTIVATE_PROP = 3
ALL_ATLAS_PROP = 4
CUR_ATLAS = 5
DETAIL_CARD_X = 53
DETAIL_CARD_Y = 105
TAB_INDEX_CARD_MAKE = 1
PASSIVE_SKILL_COLOR = '#e59545'
PASSIVE_SKILL_GRAY_COLOR = '#676767'

class CardCollectionProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CardCollectionProxy, self).__init__(uiAdapter)
        self.widget = None
        self.showCardEquip = True
        self.reset()

    def reset(self):
        self.curActivatePropList = []
        self.allActivatePropList = []
        self.curAtlasPropList = []
        self.allAtlasPropList = []
        self.propListDict = {}
        self.propDataDict = {}
        self.cardOverview = None
        self.overviewCardId = 0

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def unRegisterPanel(self):
        if self.cardOverview:
            if self.cardOverview.parent:
                self.cardOverview.parent.removeChild(self.cardOverview)
        self.widget = None
        self.reset()

    def initUI(self):
        self.uiAdapter.cardSystem.setMenuComm()
        self.widget.cardList.column = 3
        self.widget.cardList.itemHeight = 230
        self.widget.cardList.itemWidth = 168
        self.widget.cardList.itemRenderer = 'CardSystem_CardContainer'
        self.uiAdapter.cardSystem.setAllCardList()
        self.cardOverview = self.widget.getInstByClsName('CardSystem_CardOverview')
        if self.cardOverview:
            self.widget.addChild(self.cardOverview)
            self.cardOverview.x = DETAIL_CARD_X
            self.cardOverview.y = DETAIL_CARD_Y
            self.cardOverview.visible = False
            self.cardOverview.addEventListener(events.BUTTON_CLICK, self.handleGotoMakeClick, False, 0, True)
        self.widget.littleBlackBg.visible = False
        self.widget.allActivateTab.groupName = 'all'
        self.widget.allActivateTab.data = ALL_ACTIVATE_PROP
        self.widget.allAtlasTab.groupName = 'all'
        self.widget.allAtlasTab.data = ALL_ATLAS_PROP
        self.widget.activateMc.curPropList.itemRenderer = 'CardSystem_PropertyItemMultiline'
        self.widget.activateMc.curPropList.labelFunction = self.propListFunction
        self.widget.activateMc.curPropList.itemHeightFunction = self.propListItemHeightFunction
        self.widget.activateMc.curPropList.dataArray = []
        self.widget.atlasMc.atlasPropList.itemRenderer = 'CardSystem_PropertyItem'
        self.widget.atlasMc.atlasPropList.labelFunction = self.propListFunction
        self.widget.atlasMc.atlasPropList.dataArray = []
        self.widget.atlasMc.atlasList.itemHeight = 39
        self.widget.atlasMc.atlasList.itemRenderer = 'CardCollection_tucetaojian'
        self.widget.atlasMc.atlasList.labelFunction = self.atlasListFunction
        self.widget.atlasMc.atlasList.dataArray = []
        activedNum = 0
        conMax = 0
        for k, v in CAD.data.iteritems():
            activedNum += self.uiAdapter.cardSystem.getAtlasActivedNumData(k)
            conMax += self.uiAdapter.cardSystem.getAtlasConMax(k)

        numStr = uiUtils.convertNumStr(activedNum, conMax, enoughColor='', notEnoughColor='')
        self.widget.activateProgressTxt.htmlText = gameStrings.CARD_ACTIVATE_NUM_PROGRESS % (numStr,)
        self.widget.allActivateTab.selected = True
        self.refreshPropTxtList()
        self.refreshScore()
        self.widget.activateMc.showActivateBox.addEventListener(events.EVENT_SELECT, self.handleShowActivateSelected, False, 0, True)
        self.widget.allActivateTab.addEventListener(events.BUTTON_CLICK, self.handleAllBtnClick, False, 0, True)
        self.widget.allAtlasTab.addEventListener(events.BUTTON_CLICK, self.handleAllBtnClick, False, 0, True)
        self.widget.checkAtlasBtn.addEventListener(events.BUTTON_CLICK, self.handleAtlasBtnClick, False, 0, True)
        self.widget.rewardBtn.addEventListener(events.BUTTON_CLICK, self.handleRewardBtnClick, False, 0, True)
        self.refreshRewardPoint()
        self.setTemplateState()

    def refreshInfo(self):
        if not self.hasBaseData():
            return

    def setTemplateState(self):
        p = BigWorld.player()
        if p.isUsingTemp():
            self.widget.rewardBtn.visible = False
            self.widget.rewardRedPoint.visible = False
            self.widget.checkAtlasBtn.visible = False

    def refreshCardList(self):
        if not self.hasBaseData():
            return
        self.uiAdapter.cardSystem.setAllCardList()
        self.refreshPropTxtList()

    def refreshPropTxtList(self):
        if not self.hasBaseData():
            return
        self.genPropListData()
        listType = self.widget.allAtlasTab.group.selectedButton.data
        if listType == ALL_ACTIVATE_PROP:
            self.widget.activateMc.visible = True
            self.widget.atlasMc.visible = False
        elif listType == ALL_ATLAS_PROP:
            self.widget.activateMc.visible = False
            self.widget.atlasMc.visible = True
        else:
            self.widget.activateMc.visible = False
            self.widget.atlasMc.visible = False
        propDataType = CUR_ACTIVATE_PROP if self.widget.activateMc.showActivateBox.selected else ALL_ACTIVATE_PROP
        self.widget.activateMc.curPropList.dataArray = self.propDataDict.get(propDataType, [])
        self.widget.atlasMc.atlasPropList.dataArray = self.propDataDict.get(ALL_ATLAS_PROP, [])
        aData = []
        for verId in CAD.data.keys():
            info = {'verId': verId}
            aData.append(info)

        self.widget.atlasMc.atlasList.dataArray = aData

    def propListItemHeightFunction(self, *arg):
        if self.hasBaseData():
            info = ASObject(arg[3][0])
            itemMc = self.widget.getInstByClsName('CardSystem_PropertyItemMultiline')
            itemMc.contentTxt.htmlText = info.txt
            return GfxValue(itemMc.contentTxt.textHeight + 1)

    def propListFunction(self, *arg):
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if itemMc and info:
            itemMc.contentTxt.htmlText = info.txt

    def atlasListFunction(self, *arg):
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if itemMc and info:
            cData = CAD.data.get(info.verId, {})
            activedNum = self.uiAdapter.cardSystem.getAtlasActivedNumData(info.verId)
            conMax = self.uiAdapter.cardSystem.getAtlasConMax(info.verId)
            name = cData.get('version', '')
            numStr = uiUtils.convertNumStr(activedNum, conMax, enoughColor='', notEnoughColor='')
            itemMc.labels = [name, numStr]
            ASUtils.setHitTestDisable(itemMc, True)

    def refreshScore(self):
        if not self.hasBaseData():
            return False
        p = BigWorld.player()
        activedScore = self.uiAdapter.cardSystem.getAllActivedScore() + self.uiAdapter.cardSystem.getAllAtlasScore()
        self.widget.scoreTxt.text = int(activedScore)

    def handlePropMenuSel(self, *args):
        self.refreshPropTxtList()

    def handleVersionMenuSel(self, *args):
        self.refreshPropTxtList()

    def handleTypeMenuSel(self, *args):
        pass

    def onSelectedCard(self, cardItem, inital = False, oldCardId = 0):
        if not cardItem:
            return
        p = BigWorld.player()
        if p.isUsingTemp():
            return
        if not inital:
            self.showCardOverview(cardItem.cardId)

    def hasBaseData(self):
        if not self.widget:
            return False
        return True

    def showCardOverview(self, cardId):
        if not self.hasBaseData():
            return
        if not self.cardOverview:
            return
        p = BigWorld.player()
        self.widget.littleBlackBg.visible = True
        self.cardOverview.visible = True
        cardObj = p.getCard(cardId, True)
        self.cardOverview.gotoAndStop('jin' if cardObj.isBreakRank else ('putong' if cardObj.actived else 'puhui'))
        overviewCardItem = self.cardOverview.goldFront if cardObj.isBreakRank else self.cardOverview.normalFront
        self.uiAdapter.cardSystem.setCardMc(overviewCardItem, cardObj)
        self.cardOverview.back.cardDescTxt.htmlText = cardObj.getConfigData().get('cardDesc', '')
        if cardObj.noFixToSlot:
            self.cardOverview.tipMc.tipTxt.text = gameStrings.CARD_PROP_VALID_ALL_MAP_TXT
        else:
            self.cardOverview.tipMc.tipTxt.text = gameStrings.CARD_PROP_VALID_TXT
        self.widget.removeEventListener(events.MOUSE_CLICK, self.handleHideCardOverview)
        self.widget.addEventListener(events.MOUSE_CLICK, self.handleHideCardOverview, False, 0, True)
        gameglobal.rds.sound.playSound(480)
        self.overviewCardId = cardId

    def handleHideCardOverview(self, *args):
        if not self.hasBaseData():
            return
        self.widget.littleBlackBg.visible = False
        self.cardOverview.visible = False
        self.widget.removeEventListener(events.MOUSE_CLICK, self.handleHideCardOverview)
        gameglobal.rds.sound.playSound(481)

    def genPropListData(self):
        p = BigWorld.player()
        totalPropertyDict = {}
        curVerTotalPropertyDict = {}
        propType, ver, cType, keyword = self.uiAdapter.cardSystem.getMenuSelectedData()
        totalActiveSkills = []
        curActiveSkills = []
        for _, cardObj in p.cardBag['cardDict'].items():
            if not cardObj.actived:
                continue
            if cardObj.notValid:
                continue
            properties = cardObj.activeProps
            cItemData = cardObj.getConfigData()
            versionId = cardObj.version
            pType = cardObj.propType
            for propId, propVal in properties:
                if propId in totalPropertyDict:
                    totalPropertyDict[propId] += propVal
                else:
                    totalPropertyDict[propId] = propVal
                if ver and versionId != ver:
                    continue
                if propType and pType != propType:
                    continue
                if propId in curVerTotalPropertyDict:
                    curVerTotalPropertyDict[propId] += propVal
                else:
                    curVerTotalPropertyDict[propId] = propVal

            aSkills = self.uiAdapter.cardSystem.getCardSkillInfo(cardObj, False, fType=uiConst.CARD_SKILL_FORMAT_TYPE_DIAN)
            if aSkills:
                totalActiveSkills.append((aSkills, cardObj))
                if ver and versionId != ver:
                    continue
                if propType and pType != propType:
                    continue
                curActiveSkills.append((aSkills, cardObj))

        self.allActivatePropList = self.getPropertyListByDict(totalPropertyDict)
        self.curActivatePropList = self.getPropertyListByDict(curVerTotalPropertyDict)
        self.appendActiveSkill(totalActiveSkills, self.allActivatePropList)
        self.appendActiveSkill(curActiveSkills, self.curActivatePropList)
        curAtlasPropDict = {}
        allAtlasPropDict = {}
        vaData = self.uiAdapter.cardSystem.getVersionAtlasData()
        allAtlasPropDict, curAtlasPropDict = self.uiAdapter.cardSystem.getAllAtlasProp(propType=propType, ver=ver)
        self.allAtlasPropList = self.getPropertyListByDict(allAtlasPropDict)
        self.curAtlasPropList = self.getPropertyListByDict(curAtlasPropDict)
        self.propDataDict = {CUR_ACTIVATE_PROP: self.curActivatePropList,
         CUR_ATLAS_PROP: self.curAtlasPropList,
         ALL_ACTIVATE_PROP: self.allActivatePropList,
         ALL_ATLAS_PROP: self.allAtlasPropList}

    def appendActiveSkill(self, activeSkillsInfo, propList):
        for activeSkills, cardObj in activeSkillsInfo:
            for skillTitle, skillDesc, openLv in activeSkills:
                if skillTitle:
                    if cardObj.advanceLvEx < openLv:
                        continue
                    color = PASSIVE_SKILL_COLOR
                    skillTitle = uiUtils.toHtml(skillTitle, color)
                    info = {'txt': skillTitle}
                    propList.append(info)

    def getPropertyListByDict(self, propertyDict):
        propertyList = []
        for propId, propVal in propertyDict.items():
            propertyName, propVal = self.uiAdapter.cardSystem.transPropVal(propId, propVal)
            info = {'txt': self.uiAdapter.cardSystem.formatPropStr(propertyName, propVal, titleColor=uiConst.CARD_PROP_PRE_COLOR, valColor=uiConst.CARD_PROP_SUF_COLOR)}
            propertyList.append(info)

        return propertyList

    def handleCurBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        t.selected = True
        self.refreshPropTxtList()

    def handleAllBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        t.selected = True
        self.refreshPropTxtList()

    def handleShowActivateSelected(self, *arg):
        if not self.hasBaseData():
            return
        self.refreshPropTxtList()

    def handleAtlasBtnClick(self, *arg):
        self.uiAdapter.cardAtlas.show()

    def handleRewardBtnClick(self, *arg):
        self.uiAdapter.cardRankReward.show()

    def refreshRewardPoint(self):
        if not self.hasBaseData():
            return
        self.widget.rewardRedPoint.visible = False
        rewardInfo = self.uiAdapter.cardRankReward.getHasRewardInfo()
        for k, v in rewardInfo.iteritems():
            if v:
                self.widget.rewardRedPoint.visible = True
                break

    def handleGotoMakeClick(self, *arg):
        if not self.hasBaseData():
            return
        if self.overviewCardId:
            self.uiAdapter.cardSystem.show(tabIndex=TAB_INDEX_CARD_MAKE, selectedCardId=self.overviewCardId)
