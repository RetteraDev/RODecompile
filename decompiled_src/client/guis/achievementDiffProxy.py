#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/achievementDiffProxy.o
import time
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import const
import gametypes
import clientUtils
from uiProxy import UIProxy
from ui import gbk2unicode
from data import achievement_class_data as ACD
from data import achievement_data as AD
from data import achieve_target_data as ATD
from data import item_data as ID
from data import title_data as TD
from cdata import font_config_data as FCD
ICON_IMAGE_RES = 'achieve/'

class AchievementDiffProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AchievementDiffProxy, self).__init__(uiAdapter)
        self.mediator = None
        self.modelMap = {'clickClose': self.onClickClose,
         'initData': self.onInitData,
         'clickClassItem': self.onClickClassItem,
         'sendAchievement': self.onSendAchievement}
        self.achieveTargets = {}
        self.lastAchieves = []
        self.achieves = {}
        self.initAchieve()
        self.otherName = ''
        uiAdapter.registerEscFunc(uiConst.WIDGET_ACHIEVEMENT_DIFF, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ACHIEVEMENT_DIFF:
            self.mediator = mediator

    def initAchieve(self):
        self.initAchieveTargetArray = {}
        self.achieveMax = {}
        self.achieveCount = {}
        self.achieveMax['gongji'] = 0
        self.achieveCount['gongji'] = 0
        self.achieveMax['sum'] = 0
        self.achieveCount['sum'] = 0
        for achievementId in ACD.data:
            for subAchievementId in ACD.data[achievementId].get('value', {}):
                self.achieveMax[subAchievementId] = 0
                self.achieveCount[subAchievementId] = 0
                self.initAchieveTargetArray[subAchievementId] = []

        for id in AD.data:
            isHide = AD.data.get(id, {}).get('hideUI', 0)
            if isHide == uiConst.ACHIEVE_HIDE_ALL or isHide == uiConst.ACHIEVE_HIDE_NOTDONE and id not in self.achieves:
                continue
            achieveClass = AD.data[id].get('class', None)
            if achieveClass and achieveClass in self.achieveMax:
                self.achieveMax[achieveClass] += 1
                self.initAchieveTargetArray[achieveClass].append(id)
                self.achieveMax['sum'] += 1
                self.achieveMax['gongji'] += AD.data[id].get('rewardPoint', 0)

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ACHIEVEMENT_DIFF)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ACHIEVEMENT_DIFF)

    def reset(self):
        super(self.__class__, self).reset()
        self.achieveTargets = {}
        self.lastAchieves = []
        self.achieves = {}
        for id in self.achieveCount:
            self.achieveCount[id] = 0

    def onClickClose(self, *arg):
        self.hide()

    def onInitData(self, *arg):
        self.initAchieve()
        gameglobal.rds.ui.achievement.initAchieve()
        movie = arg[0]
        for id in gameglobal.rds.ui.achievement.achieves:
            if id in AD.data:
                isHide = AD.data.get(id, {}).get('hideUI', 0)
                if isHide == uiConst.ACHIEVE_HIDE_ALL:
                    continue
                achieveClass = AD.data[id].get('class', None)
                if achieveClass:
                    gameglobal.rds.ui.achievement.achieveCount[achieveClass] += 1
                    gameglobal.rds.ui.achievement.achieveCount['sum'] += 1
                    gameglobal.rds.ui.achievement.achieveCount['gongji'] += AD.data[id].get('rewardPoint', 0)
                else:
                    msg = 'Achievement id %d no class' % id
                    BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_CRITICAL, [msg], 0, {})

        obj = movie.CreateObject()
        obj.SetMember('gongjiRatio', GfxValue(str(gameglobal.rds.ui.achievement.achieveCount['gongji']) + '/' + str(gameglobal.rds.ui.achievement.achieveMax['gongji'])))
        obj.SetMember('roleName', GfxValue(gbk2unicode(BigWorld.player().realRoleName)))
        obj.SetMember('achieveCount', GfxValue(gameglobal.rds.ui.achievement.achieveCount['sum']))
        obj.SetMember('achieveMax', GfxValue(gameglobal.rds.ui.achievement.achieveMax['sum']))
        for id in self.achieves:
            if id in AD.data:
                isHide = AD.data.get(id, {}).get('hideUI', 0)
                if isHide == uiConst.ACHIEVE_HIDE_ALL:
                    continue
                achieveClass = AD.data[id].get('class', None)
                if achieveClass:
                    self.achieveCount[achieveClass] += 1
                    self.achieveCount['sum'] += 1
                    self.achieveCount['gongji'] += AD.data[id].get('rewardPoint', 0)
                else:
                    msg = 'Achievement id %d no class' % id
                    BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_CRITICAL, [msg], 0, {})

        obj.SetMember('otherGongjiRatio', GfxValue(str(self.achieveCount['gongji']) + '/' + str(self.achieveMax['gongji'])))
        obj.SetMember('otherRoleName', GfxValue(gbk2unicode(self.otherName)))
        obj.SetMember('otherAchieveCount', GfxValue(self.achieveCount['sum']))
        obj.SetMember('otherAchieveMax', GfxValue(self.achieveMax['sum']))
        achievementArray = movie.CreateArray()
        lastAchievementObj = movie.CreateObject()
        lastAchievementObj.SetMember('titileName', GfxValue(gbk2unicode('最近获得成就')))
        lastAchievementObj.SetMember('imagePath', GfxValue(ICON_IMAGE_RES + '0.dds'))
        if gameglobal.rds.ui.achievement.achieveCount['sum'] >= const.ACHIEVE_LAST_NUM:
            lastAchievementObj.SetMember('achieveRatio', GfxValue(str(const.ACHIEVE_LAST_NUM) + '/' + str(const.ACHIEVE_LAST_NUM)))
        else:
            lastAchievementObj.SetMember('achieveRatio', GfxValue(str(gameglobal.rds.ui.achievement.achieveCount['sum']) + '/' + str(const.ACHIEVE_LAST_NUM)))
        lastAchievementObjData = movie.CreateObject()
        lastAchievementObjData.SetMember('classId', GfxValue(1))
        lastAchievementObjData.SetMember('subCount', GfxValue(1))
        lastAchievementObj.SetMember('data', lastAchievementObjData)
        achievementArray.SetElement(0, lastAchievementObj)
        for achievementId in ACD.data:
            achievementObjMax = 0
            achievementObjCount = 0
            achievementObj = movie.CreateObject()
            achievementObj.SetMember('titleName', GfxValue(gbk2unicode(ACD.data[achievementId].get('name', ''))))
            achievementObj.SetMember('imagePath', GfxValue(ICON_IMAGE_RES + str(ACD.data[achievementId].get('icon', 1)) + '.dds'))
            subAchievementArray = movie.CreateArray()
            nodeAchievementId = achievementId * 100 + 1
            achievementObjData = movie.CreateObject()
            achievementObjData.SetMember('classId', GfxValue(nodeAchievementId))
            achievementObjData.SetMember('subCount', GfxValue(len(ACD.data[achievementId]['value'])))
            achievementObjMax += self.achieveMax[nodeAchievementId]
            achievementObjCount += gameglobal.rds.ui.achievement.achieveCount[nodeAchievementId]
            achievementObj.SetMember('data', achievementObjData)
            i = 0
            for subAchievementId in ACD.data[achievementId].get('value', {}):
                if subAchievementId != nodeAchievementId:
                    subAchievementObj = movie.CreateObject()
                    subAchievementObj.SetMember('titleName', GfxValue(gbk2unicode(ACD.data[achievementId]['value'][subAchievementId])))
                    subAchievementObj.SetMember('achieveRatio', GfxValue(str(gameglobal.rds.ui.achievement.achieveCount[subAchievementId]) + '/' + str(self.achieveMax[subAchievementId])))
                    subAchievementObj.SetMember('classId', GfxValue(subAchievementId))
                    achievementObjMax += self.achieveMax[subAchievementId]
                    achievementObjCount += gameglobal.rds.ui.achievement.achieveCount[subAchievementId]
                    subAchievementArray.SetElement(i, subAchievementObj)
                    i += 1

            achievementObj.SetMember('achieveRatio', GfxValue(str(achievementObjCount) + '/' + str(achievementObjMax)))
            achievementObj.SetMember('subAchievementArray', subAchievementArray)
            achievementArray.SetElement(achievementId, achievementObj)

        la = gameglobal.rds.ui.achievement.lastAchieves
        achieveArray = movie.CreateArray()
        i = 0
        for id in la:
            isHide = AD.data.get(id, {}).get('hideUI', 0)
            if isHide == uiConst.ACHIEVE_HIDE_ALL or isHide == uiConst.ACHIEVE_HIDE_NOTDONE and id not in la:
                continue
            achieveObj = gameglobal.rds.ui.achievement.transformObj(id)
            achieveArray.SetElement(i, achieveObj)
            i = i + 1

        otherAchieveArray = movie.CreateArray()
        i = 0
        for id in la:
            isHide = AD.data.get(id, {}).get('hideUI', 0)
            if isHide == uiConst.ACHIEVE_HIDE_ALL or isHide == uiConst.ACHIEVE_HIDE_NOTDONE and id not in la:
                continue
            achieveObj = self.transformObj(id)
            otherAchieveArray.SetElement(i, achieveObj)
            i = i + 1

        obj.SetMember('achieveArray', achieveArray)
        obj.SetMember('otherAchieveArray', otherAchieveArray)
        obj.SetMember('achievementArray', achievementArray)
        return obj

    def transformObj(self, id):
        if id not in AD.data:
            return
        movie = gameglobal.rds.ui.movie
        achieveObj = movie.CreateObject()
        achieveObj.SetMember('isExpand', GfxValue(AD.data[id].get('isExpand', 0)))
        expandType = AD.data[id].get('expandType', 1)
        achieveObj.SetMember('expandType', GfxValue(expandType))
        achieveObj.SetMember('achieveId', GfxValue(id))
        rewardName = ''
        rewardTitleId = AD.data[id].get('rewardTitle', '')
        if rewardTitleId:
            titleData = TD.data.get(rewardTitleId, {})
            if id in self.achieves:
                color = FCD.data.get(('title', titleData.get('style', '')), {}).get('color', '#CCCCCC')
                rewardName += "<font color=\'#ff7f00\' size = \'14\' \\>" + '奖励称号:' + '</font> <br>' + "<font size = \'12\' color=\'" + color + "\'>" + '·' + titleData.get('name', '') + '</font> <br>'
            else:
                rewardName += "<font color=\'#ff7f00\' size = \'14\' \\>" + '奖励称号:' + '</font> <br>' + "<font size = \'12\' \\>" + '·' + titleData.get('name', '') + '</font> <br>'
        bonusId = AD.data[id].get('bonusId', 0)
        rewardItems = clientUtils.genItemBonus(bonusId)
        sign = True
        for i in range(len(rewardItems)):
            if rewardItems[i]:
                if rewardItems[i][0] in ID.data:
                    itemName = ID.data[rewardItems[i][0]].get('name', '')
                    if sign:
                        sign = False
                        if id in self.achieves:
                            quality = ID.data[rewardItems[i][0]].get('quality', '')
                            color = FCD.data.get(('item', quality), {}).get('color', '#CCCCCC')
                            rewardName += "<font color=\'#ff7f00\' size = \'14\' \\>" + '奖励物品:' + '</font> <br>' + "<font size = \'12\' color=\'" + color + "\'>" + '·' + itemName + '*' + str(rewardItems[i][1]) + '</font> <br>'
                        else:
                            rewardName += "<font color=\'#ff7f00\' size = \'14\' \\>" + '奖励物品:' + '</font> <br>' + "<font size = \'12\' \\>" + '·' + itemName + '*' + str(rewardItems[i][1]) + '</font> <br>'
                    elif id in self.achieves:
                        quality = ID.data[rewardItems[i][0]].get('quality', '')
                        color = FCD.data.get(('item', quality), {}).get('color', '#CCCCCC')
                        rewardName += "<font size = \'12\' color=\'" + color + "\'>" + '·' + itemName + '*' + str(rewardItems[i][1]) + '</font> <br>'
                    else:
                        rewardName += "<font size = \'12\' \\>" + '·' + itemName + '*' + str(rewardItems[i][1]) + '</font> <br>'

        achieveObj.SetMember('rewardName', GfxValue(gbk2unicode(rewardName)))
        if id in self.achieves:
            achieveObj.SetMember('isDone', GfxValue(True))
            achieveObj.SetMember('des', GfxValue(gbk2unicode(AD.data[id].get('desc', ' '))))
            localTime = time.localtime(self.achieves[id])
            achieveObj.SetMember('date', GfxValue(str(localTime[0]) + '/' + str(localTime[1]) + '/' + str(localTime[2])))
        else:
            achieveObj.SetMember('isDone', GfxValue(False))
            if AD.data[id].get('isShow', 0):
                achieveObj.SetMember('des', GfxValue(gbk2unicode(AD.data[id].get('desc', ' '))))
            else:
                achieveObj.SetMember('des', GfxValue('???'))
        achieveObj.SetMember('name', GfxValue(gbk2unicode(AD.data[id].get('name', ''))))
        achieveObj.SetMember('rewardPoint', GfxValue(AD.data[id].get('rewardPoint', 0)))
        if AD.data[id].get('isExpand', 0):
            if expandType == 1:
                achieveTargets = AD.data[id].get('achieveTargets', ())
                if achieveTargets:
                    targetId = achieveTargets[0]
                    targetMax = ATD.data.get(targetId, {}).get('varMax', 0)
                    if id in self.achieves:
                        targetCount = targetMax
                    elif targetId in self.achieveTargets:
                        var = ATD.data.get(targetId, {}).get('var', '')
                        if var:
                            targetCount = self.achieveTargets[targetId].get(var, 0)
                        else:
                            targetCount = 0
                        if targetCount > targetMax:
                            targetCount = targetMax
                    else:
                        targetCount = 0
                    achieveObj.SetMember('targetCount', GfxValue(targetCount))
                    achieveObj.SetMember('targetMax', GfxValue(targetMax))
            elif expandType == 2 or expandType == 3:
                achieveObj.SetMember('expandCount', GfxValue(AD.data[id].get('expandCount', 2)))
                targetArray = movie.CreateArray()
                for j, targetId in enumerate(AD.data[id]['achieveTargets']):
                    targetObj = movie.CreateObject()
                    targetObj.SetMember('targetName', GfxValue(gbk2unicode(ATD.data[targetId].get('name', ''))))
                    if targetId in self.achieveTargets and self.achieveTargets[targetId]['done']:
                        targetObj.SetMember('done', GfxValue(True))
                    else:
                        targetObj.SetMember('done', GfxValue(False))
                    targetArray.SetElement(j, targetObj)

                achieveObj.SetMember('targetArray', targetArray)
        return achieveObj

    def mergeAchievesObj(self, ids, sum, rewardPoint):
        movie = gameglobal.rds.ui.movie
        id = ids[-1]
        if id not in AD.data:
            return
        achieveObj = movie.CreateObject()
        achieveObj.SetMember('isExpand', GfxValue(1))
        achieveObj.SetMember('expandType', GfxValue(4))
        achieveObj.SetMember('achieveId', GfxValue(id))
        rewardName = ''
        rewardTitleId = AD.data[id].get('rewardTitle', '')
        if rewardTitleId:
            titleData = TD.data.get(rewardTitleId, {})
            color = FCD.data.get(('title', titleData.get('style', '')), {}).get('color', '#CCCCCC')
            rewardName = "<font color=\'#ff7f00\' size = \'14\' \\>" + '奖励称号:' + '</font> <br>' + '·' + "<font size = \'12\' color=\'" + color + "\'>" + titleData.get('name', '') + '   </font>'
        if AD.data[id].get('rewardItems', '') and not rewardTitleId:
            if AD.data[id]['rewardItems'][0][0] in ID.data:
                itemName = ID.data[AD.data[id]['rewardItems'][0][0]].get('name', '')
                quality = ID.data[AD.data[id]['rewardItems'][0][0]].get('quality', '')
                color = FCD.data['item', quality]['color']
                rewardName += "<font color=\'#ff7f00\' size = \'14\' \\>" + '奖励物品:' + '</font> <br>' + "<font size = \'12\' \\>" + '·' + itemName + '*' + str(AD.data[id]['rewardItems'][0][1]) + '</font>'
        achieveObj.SetMember('rewardName', GfxValue(gbk2unicode(rewardName)))
        achieveObj.SetMember('isDone', GfxValue(True))
        achieveObj.SetMember('des', GfxValue(gbk2unicode(AD.data[id].get('desc', ' '))))
        doneData = 0
        for achieveTargetId in AD.data[id].get('achieveTargets', {}):
            if doneData < self.achieveTargets[achieveTargetId]['date']:
                doneData = self.achieveTargets[achieveTargetId]['date']

        localTime = time.localtime(doneData)
        achieveObj.SetMember('date', GfxValue(str(localTime[0]) + '/' + str(localTime[1]) + '/' + str(localTime[2])))
        achieveObj.SetMember('name', GfxValue(gbk2unicode(AD.data[id].get('name', ''))))
        achieveObj.SetMember('rewardPoint', GfxValue(rewardPoint))
        achieveObj.SetMember('sum', GfxValue(sum))
        targetArray = movie.CreateArray()
        j = 0
        for idx in ids:
            ad = AD.data.get(idx, {})
            targetObj = movie.CreateObject()
            targetObj.SetMember('name', GfxValue(gbk2unicode(ad.get('name', ''))))
            targetObj.SetMember('rewardPoint', GfxValue(ad.get('rewardPoint', 0)))
            targetArray.SetElement(j, targetObj)
            j += 1

        achieveObj.SetMember('targetArray', targetArray)
        return achieveObj

    def onClickClassItem(self, *arg):
        classId = int(arg[3][0].GetNumber())
        movie = gameglobal.rds.ui.movie
        achieveArray, achieves = gameglobal.rds.ui.achievement.genUnMergeArray(movie, classId)
        otherAchieveArray = self.genUnMergeArray(movie, classId, achieves)
        if self.mediator:
            self.mediator.Invoke('updateOtherAchieve', (achieveArray, otherAchieveArray))

    def onSendAchievement(self, *arg):
        id = int(arg[3][0].GetNumber())
        achievementDate = 'id' + str(id)
        if id in gameglobal.rds.ui.achievement.achieves:
            localTime = time.localtime(gameglobal.rds.ui.achievement.achieves[id])
            achievementDate = achievementDate + ':time' + str(localTime[0]) + '/' + str(localTime[1]) + '/' + str(localTime[2]) + ':' + BigWorld.player().realRoleName
        elif AD.data[id].get('isExpand', 0) and AD.data[id].get('expandType', 1) != 1:
            for targetId in AD.data[id].get('achieveTargets', {}):
                if targetId in gameglobal.rds.ui.achievement.achieveTargets and gameglobal.rds.ui.achievement.achieveTargets[targetId]['done']:
                    achievementDate = achievementDate + ':' + str(targetId)

        color = FCD.data['achieve', 0]['color']
        msg = "<font color=\'%s\'>[<a href = \'event:achv%s\'><u>%s</u></a>]</font>" % (color, achievementDate, AD.data[id]['name'])
        gameglobal.rds.ui.sendLink(msg)

    def genUnMergeArray(self, movie, classId, otherAchieves):
        achieveArray = movie.CreateArray()
        if classId == 1:
            for i, id in enumerate(gameglobal.rds.ui.achievement.lastAchieves):
                achieveObj = self.transformObj(id)
                achieveArray.SetElement(i, achieveObj)

        else:
            achieves = []
            temp = []
            for id in self.initAchieveTargetArray[classId]:
                temp.append(id)

            for ach in otherAchieves:
                if ach in temp:
                    achieves.append(ach)

            j = 0
            for id in achieves:
                achieveObj = self.transformObj(id)
                achieveArray.SetElement(j, achieveObj)
                j += 1

        return achieveArray

    def _genArray(self, movie, classId, otherAchieves, selectId = None):
        achieveArray = movie.CreateArray()
        if classId == 1:
            i = 0
            for id in self.lastAchieves:
                isHide = AD.data.get(id, {}).get('hideUI', 0)
                if isHide == uiConst.ACHIEVE_HIDE_ALL or isHide == uiConst.ACHIEVE_HIDE_NOTDONE and id not in self.achieves:
                    continue
                achieveObj = self.transformObj(id)
                achieveArray.SetElement(i, achieveObj)
                i = i + 1

        else:
            doneAchieves = []
            undoneAchieves = []
            tempDoneAchieves = []
            tempUndoneAchieves = []
            for id in self.initAchieveTargetArray[classId]:
                isHide = AD.data.get(id, {}).get('hideUI', 0)
                if isHide == uiConst.ACHIEVE_HIDE_ALL:
                    continue
                if id in self.achieves:
                    doneAchieves.append(id)
                elif isHide != uiConst.ACHIEVE_HIDE_NOTDONE:
                    undoneAchieves.append(id)

            for ach in otherAchieves:
                if ach in doneAchieves:
                    tempDoneAchieves.append(ach)
                if ach in undoneAchieves:
                    tempUndoneAchieves.append(ach)

            j = 0
            doneAchievesGroup = {}
            undoneAchievesGroup = {}
            for id in tempDoneAchieves:
                if AD.data[id].get('group', ''):
                    groupId, sum = AD.data[id]['group'].split(':')
                    rewardPoint = AD.data[id].get('rewardPoint', 0)
                    if doneAchievesGroup.has_key(groupId):
                        if doneAchievesGroup[groupId][0] < sum:
                            doneAchievesGroup[groupId][1].append(id)
                            ids = doneAchievesGroup[groupId][1]
                            doneAchievesGroup[groupId] = (sum, ids, doneAchievesGroup[groupId][2] + rewardPoint)
                    else:
                        doneAchievesGroup[groupId] = (sum, [id], rewardPoint)
                else:
                    if selectId == id:
                        achieveObj = self.transformObj(id, True)
                    else:
                        achieveObj = self.transformObj(id)
                    achieveArray.SetElement(j, achieveObj)
                    j += 1

            for groupId in doneAchievesGroup:
                sum, ids, rewardPoint = doneAchievesGroup[groupId]
                if selectId in ids:
                    achieveObj = self.mergeAchievesObj(ids, sum, rewardPoint, True)
                else:
                    achieveObj = self.mergeAchievesObj(ids, sum, rewardPoint)
                achieveArray.SetElement(j, achieveObj)
                j += 1

            for id in tempUndoneAchieves:
                if AD.data[id].get('group', ''):
                    groupId, sum = AD.data[id]['group'].split(':')
                    if undoneAchievesGroup.has_key(groupId):
                        if undoneAchievesGroup[groupId][0] > sum:
                            undoneAchievesGroup[groupId] = (sum, id)
                    else:
                        undoneAchievesGroup[groupId] = (sum, id)
                else:
                    if selectId == id:
                        achieveObj = self.transformObj(id, True)
                    else:
                        achieveObj = self.transformObj(id)
                    achieveArray.SetElement(j, achieveObj)
                    j += 1

            for groupId in undoneAchievesGroup:
                sum, id = undoneAchievesGroup[groupId]
                if selectId == id:
                    achieveObj = self.transformObj(id, True)
                else:
                    achieveObj = self.transformObj(id)
                achieveArray.SetElement(j, achieveObj)
                j += 1

        return achieveArray
