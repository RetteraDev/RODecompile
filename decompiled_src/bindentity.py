#Embedded file name: /WORKSPACE/data/entities/client/helpers/bindentity.o
import BigWorld
import gamelog
import clientUtils
DUMMY_MODEL_PATH = 'char/39999/39999.model'
entityIDs = {}

def _update():
    global entityIDs
    for entityID in entityIDs:
        entry = entityIDs[entityID]
        entry[0].filter.position = entry[2].position

    if len(entityIDs) != 0:
        BigWorld.callback(0, _update)


def bindEntityToNode(entity, model, nodeName):
    gamelog.debug('yuguo: bindEntityToNode', entity.id, nodeName)
    if entityIDs.has_key(entity.id):
        removeBinding(entity.id)
    entity.filter = BigWorld.ClientFilter()
    node = model.node(nodeName)
    if node is None:
        gamelog.error("yuguo: can\'t find node %s on such model!" % nodeName)
        return
    dummy = clientUtils.model(DUMMY_MODEL_PATH)
    dummy.visible = False
    node.attach(dummy)
    entityIDs[entity.id] = (entity, node, dummy)
    if len(entityIDs) == 1:
        _update()


def removeBinding(entity):
    gamelog.debug('yuguo: removeBinding: ', entity)
    id = None
    if type(entity) == int:
        id = entity
    else:
        id = entity.id
    entityIDs[id][1].detach(entityIDs[id][2])
    del entityIDs[id]


def _loadDummyModel(entity):
    entity.fashion.loadSinglePartModel(DUMMY_MODEL_PATH)


def createDummyEntityAt(entityType, spaceID, model, nodeName):
    id = BigWorld.createEntity(entityType, spaceID, 0, (0, 0, 0), (0, 0, 1), {})
    entity = BigWorld.entity(id)
    bindEntityToNode(entity, model, nodeName)
    BigWorld.callback(2, lambda : _loadDummyModel(entity))
    return id
