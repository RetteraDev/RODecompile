#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/spaceLabelSettingProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gamelog
import gameglobal
import const
from cdata import game_msg_def_data as GMDD
from guis.uiProxy import DataProxy
from guis import uiConst
from guis import uiUtils
from data import personal_zone_tag_data as PZTD
LABELTYPE = {1: gameStrings.TEXT_SPACELABELSETTINGPROXY_16,
 2: gameStrings.TEXT_SPACELABELSETTINGPROXY_17,
 3: gameStrings.TEXT_SPACELABELSETTINGPROXY_18,
 4: gameStrings.TEXT_SPACELABELSETTINGPROXY_19,
 5: gameStrings.TEXT_SPACELABELSETTINGPROXY_20}

class SpaceLabelSettingProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(SpaceLabelSettingProxy, self).__init__(uiAdapter)
        self.bindType = 'spaceLabelSetting'
        self.modelMap = {'getTagInfo': self.onGetTagInfo,
         'getLabelInfo': self.onGetLabelInfo,
         'addPersonTag': self.onAddPersonTag,
         'getPersonTag': self.onGetPersonTag,
         'removePersonTag': self.onRemovePersonTag,
         'confirmSetting': self.onConfirmSetting,
         'getLabelNum': self.onGetLabelNum,
         'showLimitMsg': self.onShowLimitMsg}
        self.mediator = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SPACELABEL_SETTING, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SPACELABEL_SETTING:
            self.mediator = mediator

    def onConfirmSetting(self, *arg):
        p = BigWorld.player()
        tempOpType = []
        for key in self.willRemoveTag:
            tempOpType.append(const.PERSONAL_ZONE_TAG_OP_REMOVE)

        for key in self.willAddTag:
            tempOpType.append(const.PERSONAL_ZONE_TAG_OP_ADD)

        gamelog.debug(self.willAddTag)
        gamelog.debug(self.willRemoveTag)
        p.base.setPersonalZoneTag(self.willRemoveTag + self.willAddTag, tempOpType)
        self.hide()

    def onShowLimitMsg(self, *arg):
        limitNum = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.SETLABEL_LIMIT_NUM, ())

    def onGetPersonTag(self, *arg):
        tagInfos = []
        tagInfos = self.getPersonTag()
        return uiUtils.array2GfxAarry(tagInfos, True)

    def onGetLabelNum(self, *arg):
        return GfxValue(len(self.personTags))

    def getPersonTag(self, tagDict = None):
        tmpInfo = tagDict if tagDict else self.personTags
        tagInfos = []
        _index = 0
        for tagId in tmpInfo:
            _info = {}
            _info = self.getTagInfoFormat(tagId, _index)
            _index += 1
            tagInfos.append(_info)

        return tagInfos

    def onRemovePersonTag(self, *arg):
        tagId = int(arg[3][0].GetNumber())
        if tagId in self.personTags:
            self.personTags.remove(tagId)
        if tagId in self.willAddTag:
            self.willAddTag.remove(tagId)
        if self.personTagsSrc.get(tagId, False) and tagId not in self.willRemoveTag:
            self.willRemoveTag.append(tagId)

    def onGetLabelInfo(self, *arg):
        labelData = []
        for key in LABELTYPE:
            tempItem = {'labelName': LABELTYPE[key],
             'tags': []}
            labelData.append(tempItem)

        for key in PZTD.data:
            _type = PZTD.data[key]['type'] - 1
            bSelected = False
            if key in self.personTags:
                bSelected = True
            labelItem = {'tagId': key,
             'name': PZTD.data[key]['name'],
             'bSelected': bSelected}
            labelData[_type]['tags'].append(labelItem)

        dictData = {}
        dictData['formatData'] = labelData
        return uiUtils.dict2GfxDict(dictData, True)

    def onGetTagInfo(self, *arg):
        tagId = int(arg[3][0].GetNumber())
        return PZTD.data.get(tagId, {})

    def getTagInfoFormat(self, tagId, _index = None):
        tmpData = {}
        tmpData['tagId'] = tagId
        tmpData['tagData'] = PZTD.data.get(tagId, {})
        tmpData['index'] = _index if _index is not None else len(self.personTags) - 1
        return uiUtils.dict2GfxDict(tmpData, True)

    def onAddPersonTag(self, *arg):
        tagId = int(arg[3][0].GetNumber())
        if tagId not in self.personTags:
            self.personTags.append(tagId)
        if tagId in self.willRemoveTag:
            self.willRemoveTag.remove(tagId)
        if not self.personTagsSrc.get(tagId, False) and tagId not in self.willAddTag:
            self.willAddTag.append(tagId)
        return self.getTagInfoFormat(tagId)

    def getValue(self, key):
        if key == '':
            return uiUtils.array2GfxAarry([], True)

    def show(self, selfTags = None):
        self.personTagsSrc = selfTags
        self.personTags = []
        for key in selfTags:
            self.personTags.append(key)

        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SPACELABEL_SETTING)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SPACELABEL_SETTING)

    def reset(self):
        self.personTagsSrc = {}
        self.personTags = []
        self.willAddTag = []
        self.willRemoveTag = []
