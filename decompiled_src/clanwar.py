#Embedded file name: /WORKSPACE/data/entities/client/helpers/clanwar.o
import BigWorld
import copy
import utils
from data import region_server_config_data as RSCD

class FortVal(object):

    def __init__(self, fortId = 0, ownerGuildNUID = 0, ownerGuildName = '', ownerGuildFlag = 0, ownerClanNUID = 0, fromHostId = 0):
        self.fortId = fortId
        self.updateOwner(ownerGuildNUID, ownerGuildName, ownerGuildFlag, ownerClanNUID, fromHostId)

    def updateOwner(self, ownerGuildNUID = 0, ownerGuildName = '', ownerGuildFlag = 0, ownerClanNUID = 0, fromHostId = 0):
        p = BigWorld.player()
        if ownerGuildName and fromHostId != utils.getHostId():
            ownerGuildName += '-' + RSCD.data.get(fromHostId, {}).get('serverName', '')
        self.ownerGuildNUID = ownerGuildNUID
        self.ownerGuildName = ownerGuildName
        self.ownerGuildFlag = ownerGuildFlag
        self.ownerClanNUID = ownerClanNUID
        self.fromHostId = fromHostId

    def checkOwner(self, ownerGuildNUID, ownerClanNUID):
        return self.ownerGuildNUID == ownerGuildNUID

    def checkOwnerEx(self, ownerGuildNUID, ownerClanNUID):
        return self.ownerGuildNUID == ownerGuildNUID or self.ownerClanNUID and self.ownerClanNUID == ownerClanNUID


class ReliveBoardVal(object):

    def __init__(self, nuid = 0, lv = 0, pos = None):
        self.nuid = nuid
        self.lv = lv
        self.pos = pos


class BuildingVal(object):

    def __init__(self, nuid = 0, buildingType = 0, buildingId = 0, cmarkerId = 0, pos = None):
        self.nuid = nuid
        self.buildingType = buildingType
        self.buildingId = buildingId
        self.cmarkerId = cmarkerId
        self.pos = pos


class ClanWar:

    def __init__(self, fort = {}, reliveBoard = {}, building = {}, cmarker = {}):
        self.fort = copy.deepcopy(fort)
        self.reliveBoard = copy.deepcopy(reliveBoard)
        self.building = copy.deepcopy(building)
        self.cmarker = copy.deepcopy(cmarker)

    def getFort(self, fortId):
        fort = self.fort.get(fortId)
        if not fort:
            fort = FortVal(fortId=fortId)
            self.fort[fortId] = fort
        return fort
