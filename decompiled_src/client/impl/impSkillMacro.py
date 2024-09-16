#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impSkillMacro.o
import BigWorld
import gameglobal
import utils
import gametypes
from guis import uiConst
from skillMacro import *
from cdata import game_msg_def_data as GMDD

class ImpSkillMacro(object):

    def onQueryMySkillMacros(self, mySkillMacroInfo, useSkillMacroToday):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe6\x88\x91\xe7\x9a\x84\xe6\x8a\x80\xe8\x83\xbd\xe5\xae\x8f\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param mySkillMacroInfo:
        :param useSkillMacroToday: \xe4\xbb\x8a\xe5\xa4\xa9\xe6\x98\xaf\xe5\x90\xa6\xe4\xbd\xbf\xe7\x94\xa8\xe8\xbf\x87\xe6\x8a\x80\xe8\x83\xbd\xe5\xae\x8f
        :return:
        """
        self.useSkillMacroToday = useSkillMacroToday
        self.mySkillMacroInfo = mySkillMacroInfo
        for macroId, macro in mySkillMacroInfo.iteritems():
            SkillMacroCondition.getInstance().buildBuffer(macro.macroList)

        gameglobal.rds.ui.skillMacroOverview.openOverviewPanel()
        gameglobal.rds.ui.actionbar.refreshActionbar()
        gameglobal.rds.ui.actionbar.refreshAllItembar()

    def onAddMySkillMacro(self, macroId, page, slot, iconType, iconPath, name, macroList):
        """
        \xe6\x96\xb0\xe5\x8a\xa0\xe4\xb8\x80\xe4\xb8\xaa\xe6\x8a\x80\xe8\x83\xbd\xe5\xae\x8f\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param macroId: \xe6\x96\xb0\xe5\x8a\xa0\xe5\xae\x8f\xe7\x9a\x84id
        :param page: \xe6\x96\xb0\xe5\x8a\xa0\xe5\xae\x8f\xe7\x9a\x84page
        :param slot: \xe6\x96\xb0\xe5\x8a\xa0\xe5\xae\x8f\xe7\x9a\x84slot
        :param iconType: \xe5\xae\x8f\xe7\x9a\x84\xe5\x9b\xbe\xe6\xa0\x87\xe7\xb1\xbb\xe5\x9e\x8b
        :param iconPath: \xe6\x96\xb0\xe5\x8a\xa0\xe5\xae\x8f\xe7\x9a\x84iconPath
        :param name: \xe6\x96\xb0\xe5\x8a\xa0\xe5\xae\x8f\xe7\x9a\x84\xe5\x90\x8d\xe7\xa7\xb0
        :param macroList: \xe6\x96\xb0\xe5\x8a\xa0\xe5\xae\x8f\xe7\x9a\x84\xe8\xaf\xad\xe5\x8f\xa5\xe5\x88\x97\xe8\xa1\xa8
        :return:
        """
        self.showGameMsg(GMDD.data.SKILL_MACRO_SAVE_SUCCESS, ())
        if not hasattr(self, 'mySkillMacroInfo'):
            return
        gameglobal.rds.ui.skillMacroOverview.isSaving = False
        self.mySkillMacroInfo[macroId] = SkillMacroVal(macroId, page, slot, iconType, iconPath, name, macroList)
        SkillMacroCondition.getInstance().buildBuffer(macroList)
        gameglobal.rds.ui.skillMacroOverview.refreshMySkillMacroArea()
        gameglobal.rds.ui.skillMacroOverview.setSelectedMacroId(macroId)

    def onModifyMySkillMacro(self, macroId, page, slot, iconType, iconPath, name, macroList):
        """
        \xe4\xbf\xae\xe6\x94\xb9\xe4\xb8\x80\xe4\xb8\xaa\xe6\x8a\x80\xe8\x83\xbd\xe5\xae\x8f\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param macroId: \xe8\xa6\x81\xe4\xbf\xae\xe6\x94\xb9\xe7\x9a\x84\xe5\xae\x8fid
        :param page: \xe4\xbf\xae\xe6\x94\xb9\xe5\x90\x8e\xe5\xae\x8f\xe7\x9a\x84page
        :param slot: \xe4\xbf\xae\xe6\x94\xb9\xe5\x90\x8e\xe5\xae\x8f\xe7\x9a\x84slot
        :param iconType: \xe5\xae\x8f\xe7\x9a\x84\xe5\x9b\xbe\xe6\xa0\x87\xe7\xb1\xbb\xe5\x9e\x8b
        :param iconPath: \xe4\xbf\xae\xe6\x94\xb9\xe5\x90\x8e\xe5\xae\x8f\xe7\x9a\x84iconPath
        :param name: \xe4\xbf\xae\xe6\x94\xb9\xe5\x90\x8e\xe5\xae\x8f\xe7\x9a\x84\xe5\x90\x8d\xe7\xa7\xb0
        :param macroList: \xe4\xbf\xae\xe6\x94\xb9\xe5\x90\x8e\xe5\xae\x8f\xe7\x9a\x84\xe8\xaf\xad\xe5\x8f\xa5\xe5\x88\x97\xe8\xa1\xa8
        :return:
        """
        if gameglobal.rds.ui.skillMacroOverview.isSaving:
            self.showGameMsg(GMDD.data.SKILL_MACRO_SAVE_SUCCESS, ())
            gameglobal.rds.ui.skillMacroOverview.isSaving = False
        info = self.mySkillMacroInfo.get(macroId, {})
        info.slot = slot
        info.iconType = iconType
        info.iconPath = iconPath
        info.name = name
        info.macroList = macroList
        SkillMacroCondition.getInstance().buildBuffer(macroList)
        self.mySkillMacroInfo[macroId] = info
        gameglobal.rds.ui.skillMacroOverview.refreshMySkillMacroArea()
        gameglobal.rds.ui.actionbar.modifyItemByMacroId(long(macroId))

    def onExchangeMySkillMacro(self, exchangeMacroInfo):
        """
        \xe4\xba\xa4\xe6\x8d\xa2\xe5\x90\x8e\xe7\x9a\x84\xe4\xb8\xa4\xe4\xb8\xaa\xe5\xae\x8f\xe4\xbf\xa1\xe6\x81\xaf
        :param exchangeMacroInfo: key\xe4\xb8\xba\xe5\xae\x8fid, value\xe4\xb8\xbaSkillMacroVal
        :return:
        """
        for macroId, info in exchangeMacroInfo.iteritems():
            self.mySkillMacroInfo[macroId] = info

        gameglobal.rds.ui.skillMacroOverview.refreshMySkillMacroArea()

    def onDelMySkillMacro(self, macroId):
        """
        \xe5\x88\xa0\xe9\x99\xa4\xe4\xb8\x80\xe4\xb8\xaa\xe6\x8a\x80\xe8\x83\xbd\xe5\xae\x8f\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param macroId: \xe8\xa6\x81\xe5\x88\xa0\xe9\x99\xa4\xe6\x8a\x80\xe8\x83\xbd\xe5\xae\x8f\xe7\x9a\x84\xe5\xae\x8fid
        :return:
        """
        del self.mySkillMacroInfo[macroId]
        gameglobal.rds.ui.skillMacroOverview.refreshMySkillMacroArea()
        gameglobal.rds.ui.skillMacroOverview.setRightPanel()
        gameglobal.rds.ui.skillMacroOverview.removeRightMenu()
        gameglobal.rds.ui.actionbar.removeItemByMacroId(long(macroId))

    def onShareSkillMacroToChat(self):
        """
        \xe5\x88\x86\xe4\xba\xab\xe6\x8a\x80\xe8\x83\xbd\xe5\xae\x8f\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :return:
        """
        gameglobal.rds.ui.skillMacroOverview.shareMacroLink()

    def onShareSkillMacroToChatFromGM(self, gbId, macroId, shareTime, macroName, school, roleName):
        """
        \xe7\xbd\x91\xe9\xa1\xb5\xe4\xb8\x8a\xe5\x88\x86\xe4\xba\xab\xe5\x88\xb0\xe8\x81\x8a\xe5\xa4\xa9\xe6\xa1\x86\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83\xe4\xbf\xa1\xe6\x81\xaf
        :param gbId:
        :param macroId:
        :param shareTime:
        :param macroName:
        :param school:
        :param roleName:
        :return:
        """
        gameglobal.rds.ui.skillMacroOverview.shareWebMacroLink(gbId, macroId, shareTime, macroName, school, roleName)

    def onGetSkillMacroFromChat(self, macroInfo):
        """
        \xe7\x82\xb9\xe5\x87\xbb\xe6\xb8\xb8\xe6\x88\x8f\xe5\x86\x85\xe6\x8a\x80\xe8\x83\xbd\xe5\xae\x8f\xe5\x88\x86\xe4\xba\xab\xe7\x9a\x84\xe9\x93\xbe\xe6\x8e\xa5\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param macroInfo:
        :return:
        """
        if gameglobal.rds.ui.skillMacroOverview.checkMacroFull():
            return
        gameglobal.rds.ui.skillMacroOverview.isSaving = True
        gameglobal.rds.ui.skillMacroOverview.editMode = uiConst.NO_EDIT
        self.base.addMySkillMacro(macroInfo.iconType, macroInfo.iconPath, macroInfo.name, macroInfo.macroList, gametypes.SKILL_MACRO_ADD_FROM_SHARE)

    def getMacroInfoById(self, macroId):
        if hasattr(self, 'mySkillMacroInfo'):
            return self.mySkillMacroInfo.get(macroId, None)
        else:
            self.base.queryMySkillMacros()
            return None

    def getIconNameFromRawIcon(self, rawIcon):
        splitResult = rawIcon.split('_')
        return splitResult[-1]

    def onQueryWebSkillMacros(self, page, queryType, webSkillMacroList):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe5\xae\x98\xe7\xbd\x91\xe6\x8a\x80\xe8\x83\xbd\xe5\xae\x8f\xe5\x88\x97\xe8\xa1\xa8\xe5\x9b\x9e\xe8\xb0\x83
        :param page:
        :param queryType: \xe6\x9f\xa5\xe8\xaf\xa2\xe7\xb1\xbb\xe5\x9e\x8b 1\xef\xbc\x9a\xe6\x9c\x80\xe6\x96\xb0\xef\xbc\x8c2\xef\xbc\x9a\xe6\x8e\x92\xe8\xa1\x8c
        :param webSkillMacroList: \xe5\xae\x8f\xe5\x88\x97\xe8\xa1\xa8
        :return:
        """
        self.webSkillMacroList = webSkillMacroList
        gameglobal.rds.ui.skillMacroOverview.refreshWebArea(webSkillMacroList, page)

    def dealWithRawWebSkillMacroList(self, webSkillMacroList):
        newWebList = {}
        for key, value in webSkillMacroList.iteritems():
            if not value:
                continue
            newKey = key.encode(utils.defaultEncoding())
            newValue = []
            for item in value:
                newItem = {}
                for valueKey, v in item.iteritems():
                    newValueKey = valueKey.encode(utils.defaultEncoding())
                    if newValueKey == 'macrosContent':
                        if v.encode(utils.defaultEncoding()) == 'null':
                            v = {}
                        else:
                            v = eval(v.encode(utils.defaultEncoding()))
                    newItem[newValueKey] = v

                newValue.append(newItem)

            newWebList[newKey] = newValue

        return newWebList

    def onApplyWebSkillMacro(self, skillMacroWebId, result):
        """
        \xe5\xba\x94\xe7\x94\xa8\xe6\x8a\x80\xe8\x83\xbd\xe5\xae\x8f\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param skillMacroWebId: \xe5\xba\x94\xe7\x94\xa8\xe7\x9a\x84\xe5\xae\x8fid
        :param result: \xe7\xbb\x93\xe6\x9e\x9c\xe5\x8f\x8a\xe6\x9c\x80\xe6\x96\xb0\xe7\x9a\x84\xe5\xae\x8f\xe4\xbf\xa1\xe6\x81\xaf
        :return:
        """
        voteCount = result['skillmacros']['voteCount']
        gameglobal.rds.ui.skillMacroOverview.updateWebApplyNum(skillMacroWebId, voteCount)
        self.showGameMsg(GMDD.data.SKILL_MACRO_WEB_APPLY_SUCCESS, ())

    def onPublishWebSkillMacro(self, macroId, result):
        """
        \xe5\x8f\x91\xe5\xb8\x83\xe6\x8a\x80\xe8\x83\xbd\xe5\xae\x8f\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param macroId: \xe5\x8f\x91\xe5\xb8\x83\xe7\x9a\x84\xe6\x8a\x80\xe8\x83\xbd\xe5\xae\x8fid
        :param result: \xe5\x8f\x91\xe5\xb8\x83\xe7\xbb\x93\xe6\x9e\x9c
        :return:
        """
        if result.get('resCode', 0):
            self.showGameMsg(GMDD.data.SKILL_MACRO_PUBLISH_FAIL, ())
        else:
            token = result.get('token', '').encode(utils.defaultEncoding())
            gameglobal.rds.ui.skillMacroOverview.openWebPanel(token=token, webType=gametypes.SKILL_MACRO_PUT_OUT_WEB_TYPE, id=result.get('id', 0))
            self.showGameMsg(GMDD.data.SKILL_MACRO_PUBLISH_SUCCESS, ())

    def onQueryWebSkillDetail(self, webSkillMacroId, result):
        token = result.get('token', '').encode(utils.defaultEncoding())
        gameglobal.rds.ui.skillMacroOverview.openWebPanel(token=token, webType=gametypes.SKILL_MACRO_QUERY_WEB_TYPE)

    def onApplyWebSkillMacroFromGM(self, webSkillMacroId, macroContent):
        """
        \xe7\xbd\x91\xe9\xa1\xb5\xe4\xb8\x8a\xe7\x82\xb9\xe5\x87\xbb\xe4\xb8\x80\xe9\x94\xae\xe5\xba\x94\xe7\x94\xa8\xe7\x9a\x84\xe6\x95\xb0\xe6\x8d\xae\xe5\x9b\x9e\xe8\xb0\x83
        :param webSkillMacroId:
        :param macroContent:
        :return:
        """
        iconType = macroContent.get('iconType', 0)
        iconPath = macroContent.get('iconPath', '').encode(utils.defaultEncoding())
        name = macroContent.get('name', 0).encode(utils.defaultEncoding())
        macroList = []
        unicodeMacroList = macroContent.get('macroList', 0)
        for item in unicodeMacroList:
            macroList.append(item.encode(utils.defaultEncoding()))

        self.base.addMySkillMacro(iconType, iconPath, name, macroList, gametypes.SKILL_MACRO_ADD_FROM_APPLY)
