#Embedded file name: I:/bag/tmp/tw2/res/entities\client/BusinessItem.o
import BigWorld
import gamelog
import gameglobal
import utils
from guis import ui
from guis import cursor
from iClient import IClient
from iDisplay import IDisplay
from helpers import fashion
from helpers import modelServer
from data import business_config_data as BCD
from data import item_data as ID
from cdata import game_msg_def_data as GMDD

class BusinessItem(IClient, IDisplay):

    def __init__(self):
        super(BusinessItem, self).__init__()
        self.firstFetchFinished = False
        self.itemData = ID.data.get(BCD.data.get('BusinessItemId', 450001), {})
        self.isLeaveWorld = False
        self.trapId = None
        self.srcPosition = None

    def afterModelFinish(self):
        super(BusinessItem, self).afterModelFinish()
        self.setTargetCapsUse(True)

    def enterWorld(self):
        super(BusinessItem, self).enterWorld()
        self.fashion = fashion.Fashion(self.id)
        self.fashion.loadDummyModel()
        self.modelServer = modelServer.SimpleModelServer(self)
        self.trapId = BigWorld.addPot(self.matrix, cursor.TALK_DISTANCE, self.trapCallback)
        if hasattr(self, 'playerName') and self.playerName != '':
            self.roleName = '%s的特产包裹' % self.playerName
        else:
            self.roleName = '特产包裹'

    def leaveWorld(self):
        super(BusinessItem, self).leaveWorld()
        self.isLeaveWorld = True
        gameglobal.rds.ui.pickUp.hideById(self.id)
        self.businessItemTrapCallback()
        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None

    def trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        if enteredTrap == False:
            gameglobal.rds.ui.pickUp.hideById(self.id)
        self.businessItemTrapCallback()

    def businessItemTrapCallback(self):
        p = BigWorld.player()
        entities = BigWorld.entities.values()
        entities = filter(lambda entity: entity.__class__.__name__ == 'BusinessItem' and (entity.model.position - BigWorld.player().position).lengthSquared < cursor.TALK_DISTANCE * cursor.TALK_DISTANCE and entity.isLeaveWorld == False, entities)
        p.businessItemTrapCallback(entities)

    def getItemData(self):
        modelId = self.itemData.get('modelId', 0)
        if modelId == 0:
            return {'model': 30005,
             'dye': 'Default',
             'fullPath': 'item/model/30005/30005.model'}
        soundName = self.itemData.get('dropItemSound', None)
        return {'model': modelId,
         'dye': 'Default',
         'fullPath': 'item/model/%d/%d.model' % (modelId, modelId),
         'dropItemSound': soundName}

    def showTargetUnitFrame(self):
        return False

    def onTargetCursor(self, enter):
        if enter:
            if ui.get_cursor_state() == ui.NORMAL_STATE:
                ui.set_cursor_state(ui.TARGET_STATE)
                if (self.position - BigWorld.player().position).length > cursor.TALK_DISTANCE:
                    ui.set_cursor(cursor.usebox_dis)
                else:
                    ui.set_cursor(cursor.usebox)
                ui.lock_cursor()
        elif ui.get_cursor_state() == ui.TARGET_STATE:
            ui.reset_cursor()

    @ui.callFilter(1, False)
    def use(self):
        if not self.inWorld:
            return
        p = BigWorld.player()
        if utils.isInBusinessZaiju(p):
            if hasattr(self, 'ownerGbId') and self.ownerGbId != p.gbId and hasattr(self, 'birthTime') and self.birthTime + BCD.data.get('blackPickInterval', 0) > utils.getNow():
                p.showGameMsg(GMDD.data.GUILD_BUSINESS_ITEM_PICK_TIME_ERROR, ())
            else:
                self.cell.openBox()
        else:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_ITEM_PICK_NO_ZAIJU, ())

    def onOpenBox(self, isSuc):
        gamelog.info('@szh onOpenBox', self.id, isSuc)
        if not self.inWorld:
            return
        p = BigWorld.player()
        if not isSuc:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_ITEM_PICK_OPEN_ERROR, ())
            return
        if utils.isInBusinessZaiju(p):
            gameglobal.rds.ui.pickUp.show(self.id, self.items, True)
        else:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_ITEM_PICK_NO_ZAIJU, ())

    def onPickItems(self, isSuc):
        gamelog.info('@szh onPickItem', self.id, isSuc)
        if not self.inWorld or not isSuc:
            return
        p = BigWorld.player()
        if utils.isInBusinessZaiju(p):
            pass
        else:
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_ITEM_PICK_NO_ZAIJU, ())

    def set_items(self, oldValue):
        if gameglobal.rds.ui.pickUp.mediator:
            gameglobal.rds.ui.pickUp.show(self.id, self.items, True)
