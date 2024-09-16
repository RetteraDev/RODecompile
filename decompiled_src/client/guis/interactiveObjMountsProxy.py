#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/interactiveObjMountsProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from data import interactive_data as ID

class InteractiveObjMountsProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(InteractiveObjMountsProxy, self).__init__(uiAdapter)
        self.modelMap = {'getMountsInfo': self.onGetMountsInfo,
         'exitRideTogether': self.onExitRideTogether,
         'removeMember': self.onRemoveMember,
         'clickTarget': self.onClickTarget}
        self.mediator = None
        self.seatNum = 0
        self.uiPos = 0

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_INTERACTIVE_OBJ_MOUNTS:
            self.mediator = mediator

    def reset(self):
        self.mediator = None

    def show(self):
        if BigWorld.player().inInteractiveObj():
            objId = self.getInteractiveObjId()
            if objId != 0 and not ID.data.get(objId, {}).get('ignore', 0):
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_INTERACTIVE_OBJ_MOUNTS)
                self.refreshView()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_INTERACTIVE_OBJ_MOUNTS)

    def onGetMountsInfo(self, *arg):
        self.refreshView()

    def refreshView(self):
        objId = self.getInteractiveObjId()
        if objId == 0:
            return
        else:
            icon = ''
            self.uiPos = []
            data = ID.data.get(objId, {})
            if data != None:
                icon = data.get('pic', '')
                self.seatNum = data.get('canInteractiveCnt', 0)
                self.uiPos = data.get('uiPos', {})
            if not self.uiPos:
                return
            ret = {}
            ret['icon'] = icon
            ret['count'] = self.seatNum
            ret['players'] = self.getInteractiveRoles()
            if self.mediator:
                self.mediator.Invoke('setData', uiUtils.dict2GfxDict(ret, True))
            return

    def getInteractiveRoles(self):
        roleList = []
        p = BigWorld.player()
        isHost = False
        isInit = True
        for i in self.uiPos:
            ret = {}
            entityId = self.getIdByIdx(i)
            if entityId != 0 and entityId != None:
                ret['index'] = i
                ret['isEmpty'] = False
                ret['entityId'] = entityId
                ret['isEmpty'] = False
                entity = BigWorld.entities.get(int(entityId))
                if entity:
                    ret['name'] = entity.roleName
                else:
                    ret['name'] = ''
                ret['pos'] = self.uiPos[i]
                if isInit:
                    isHost = i == 0 and p.id == entityId
                    isInit = False
                ret['isHost'] = isHost
                ret['isSelf'] = entityId == p.id
            else:
                ret['isEmpty'] = True
                ret['pos'] = self.uiPos[i]
            roleList.append(ret)

        return uiUtils.array2GfxAarry(roleList, True)

    def onExitRideTogether(self, *arg):
        p = BigWorld.player()
        p.quitInteractiveObj()
        self.refreshView()

    def onRemoveMember(self, *arg):
        goAwayMember = int(arg[3][0].GetNumber())
        BigWorld.player().cell.kickoffInteractive(goAwayMember)

    def onClickTarget(self, *arg):
        entityId = arg[3][0].GetNumber()
        ent = BigWorld.entities.get(int(entityId))
        BigWorld.player().lockTarget(ent)

    def getIdByIdx(self, idx):
        obj = self.getInteractiveObj()
        if obj:
            for eId, index in obj.avatarMap.iteritems():
                if idx == index:
                    return eId

        return 0

    def getInteractiveObj(self):
        p = BigWorld.player()
        interObj = BigWorld.entities.get(p.interactiveObjectEntId)
        if interObj and interObj.inWorld:
            return interObj
        else:
            return None

    def getInteractiveObjId(self):
        obj = self.getInteractiveObj()
        if obj:
            return obj.objectId
        else:
            return None
