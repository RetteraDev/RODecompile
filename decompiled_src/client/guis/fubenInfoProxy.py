#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fubenInfoProxy.o
from Scaleform import GfxValue
import BigWorld
import gameglobal
from guis.uiProxy import UIProxy
from guis import uiConst, uiUtils
from guis import tipUtils
from guis import ui
from guis.ui import gbk2unicode
from data import fb_ui_data as FUD
from data import monster_data as MD
from data import wg_ui_align_data as WUAD
from data import wg_ui_icon_data as WUID

class FubenInfoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FubenInfoProxy, self).__init__(uiAdapter)
        self.modelMap = {'getTooltip': self.onGetTooltip,
         'clickBuff': self.onClickBuff}
        self.fbMonsterInfo = None
        self.fbItemData = {}
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_WUGU_FB_INFO:
            self.med = mediator
            self.refreshFBInfo()
        elif widgetId == uiConst.WIDGET_WUGU_BUFF_INFO:
            self.buffMed = mediator
            self.refreshFBInfo()

    def reset(self):
        self.med = None
        self.buffMed = None
        self.fbId = None
        self.uiParams = {}

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WUGU_FB_INFO)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WUGU_BUFF_INFO)

    def onEnterFuben(self, fbId):
        self.fbId = fbId
        for fbUiInfo in FUD.data.values():
            if fbUiInfo.get('fubenId') == fbId:
                self.uiParams[fbUiInfo.get('uiId')] = fbUiInfo.get('uiParam')

    def refreshFubenItem(self, fbItemData):
        self.fbItemData = fbItemData
        self.refreshFBInfo()

    def refreshFbMonsterInfo(self, fbMonsterInfo):
        self.fbMonsterInfo = fbMonsterInfo
        self.refreshFBInfo()

    def refreshFBInfo(self):
        if self.med:
            obj = self.uiAdapter.movie.CreateObject()
            name = ''
            hp = 0
            maxHp = 0
            if self.fbMonsterInfo and self.fbMonsterInfo[0]:
                name = MD.data.get(self.fbMonsterInfo[0].get('charType')).get('name')
                hp = self.fbMonsterInfo[0].get('hp')
                maxHp = self.fbMonsterInfo[0].get('mhp')
                obj.SetMember('shouhuName', GfxValue(gbk2unicode(name)))
                obj.SetMember('shouhuHp', GfxValue(hp))
                obj.SetMember('shouhuMaxHp', GfxValue(maxHp))
                itemNums = []
                paths = []
                fbuiParam = self.uiParams.get(uiConst.WIDGET_WUGU_FB_INFO)
                if fbuiParam:
                    fbItemIds = fbuiParam[0:len(fbuiParam) - 1]
                    paths = [ uiUtils.getItemIconFile64(id) for id in fbItemIds ]
                    obj.SetMember('fbItemId', uiUtils.array2GfxAarry(fbItemIds))
                    if self.fbItemData:
                        itemNums = [ self.fbItemData.get(id, 0) for id in fbItemIds ]
                    else:
                        itemNums = [ 0 for id in fbItemIds ]
                obj.SetMember('fbItemPath', uiUtils.array2GfxAarry(paths, True))
                obj.SetMember('fbItemNum', uiUtils.array2GfxAarry(itemNums))
                self.med.Invoke('setWuguInfo', obj)
                self.med.Invoke('setVisible', GfxValue(True))
            else:
                self.med.Invoke('setVisible', GfxValue(False))
        if self.buffMed:
            if self.fbMonsterInfo and self.fbMonsterInfo[0]:
                name = MD.data.get(self.fbMonsterInfo[0].get('charType', ''), {}).get('name', '')
                hp = self.fbMonsterInfo[0].get('hp', '0')
                maxHp = self.fbMonsterInfo[0].get('mhp', '0')
                buffRows = []
                data = {'shouhuName': name,
                 'shouhuHp': hp,
                 'shouhuMaxHp': maxHp,
                 'buffRows': buffRows}
                fbuiParam = self.uiParams.get(uiConst.WIDGET_WUGU_BUFF_INFO)
                if fbuiParam:
                    wgUiId = fbuiParam[0]
                    wgData = WUAD.data.get(wgUiId, {})
                    if wgData:
                        rowIndex = 0
                        for name, itemId, buffIds, costNum in wgData.get('rows', ()):
                            buffs = []
                            buffRowData = {'buffName': name,
                             'fbItemId': itemId,
                             'fbItemPath': uiUtils.getItemIconFile40(itemId),
                             'fbItemCnt': 'x%s' % self.fbItemData.get(itemId, 0),
                             'buffs': buffs}
                            buffRows.append(buffRowData)
                            coloumIndex = 0
                            for buffId in buffIds:
                                iconData = WUID.data.get(buffId, {})
                                if iconData:
                                    buffData = {'index': '%s_%s' % (rowIndex, coloumIndex),
                                     'iconPath': 'state/icon/%s.dds' % iconData.get('icon', 'notFound'),
                                     'name': iconData.get('name', ''),
                                     'type': iconData.get('type', ''),
                                     'desc1': iconData.get('describe', ''),
                                     'desc2': iconData.get('sub_describe', ''),
                                     'iconCnt': uiUtils.convertNumStr(self.fbItemData.get(itemId, 0), costNum)}
                                    buffs.append(buffData)
                                coloumIndex += 1

                            rowIndex += 1

                if not self.uiAdapter.quest.isShow and not gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
                    self.buffMed.Invoke('setVisible', GfxValue(True))
                self.buffMed.Invoke('setWuguInfo', uiUtils.dict2GfxDict(data, True))
            else:
                self.buffMed.Invoke('setVisible', GfxValue(False))

    def onGetTooltip(self, *arg):
        index = int(arg[3][0].GetString())
        return tipUtils.getItemTipById(index)

    @ui.callFilter(2)
    def onClickBuff(self, *args):
        indexs = args[3][0].GetString().split('_')
        if len(indexs) == 2:
            BigWorld.player().cell.triggerFubenAIByUI((int(indexs[0]), int(indexs[1])))
