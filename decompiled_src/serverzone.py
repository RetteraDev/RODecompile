#Embedded file name: /WORKSPACE/data/entities/client/serverzone.o
import BigWorld
import gamelog
from data import sys_config_data as SCD

class ServerEntry(object):

    def __init__(self):
        self.busy = 0
        self.locale = 0
        self.name = ''
        self.title = ''
        self.mode = 0
        self.ip = ['', '', '']
        self.charNum = 0


NET_MAPPING = {'tel': 1,
 'cnc': 2,
 'cer': 3}

class ServerZone(object):

    def __init__(self):
        self._server_cache = {}
        self._service_cache = {}
        self._zone_map = {}
        self.item = {}
        self.keys = []
        self.service = 0
        self.firstZone = ''
        self.firstMachine = ''
        self.serversInfo = None
        self.serverName = SCD.data.get('serverSortNames', ['岩锤烽烟',
         '梦回苏澜',
         '星茸花语',
         '月满汐湾',
         '玉木仙缘',
         '内部测试'])

    def load(self):
        try:
            f = open('../serverlist.ini')
        except IOError:
            try:
                f = open('../game/server.lst')
            except IOError:
                BigWorld.msgBox('找不到服务器列表!')
                BigWorld.quit()
                return False

        try:
            content = f.readlines()
            f.close()
            self._parseServerList(content)
        except:
            BigWorld.msgBox('服务器列表出错，请用tystart.exe运行游戏!')
            BigWorld.quit()
            return False

        return True

    def refreshServerList(self, content):
        self._server_cache = {}
        self._service_cache = {}
        self._zone_map = {}
        self.item = {}
        self.keys = []
        self.firstZone = ''
        self.firstMachine = ''
        self._parseServerList(content)
        if self.serversInfo:
            self.updateCharNum(self.serversInfo)

    def _parseServerList(self, content):
        try:
            for line in content:
                line = line.strip()
                if line == '':
                    continue
                if line.startswith('#'):
                    network = line.split('=')[1]
                    network = network.strip()
                    gamelog.debug('chaos: network ', network)
                    self.service = NET_MAPPING.get(network, 0)
                    continue
                item = line.split(' ')
                if len(item) != 9:
                    raise ValueError
                key = str(item[0])
                if self.item.get(key, None) == None:
                    self.item[key] = []
                    self.keys.append(key)
                entry = ServerEntry()
                entry.name = item[4]
                entry.title = item[5]
                entry.mode = item[3]
                entry.locale = item[2]
                entry.busy = item[1]
                entry.ip[0] = item[6]
                entry.ip[1] = item[7]
                entry.ip[2] = item[8]
                entry.bgp = int(entry.locale) == 3
                entry.isEduNet = entry.bgp == True and entry.ip[1] != entry.ip[2]
                self._server_cache.setdefault(item[4], []).append(entry)
                self._zone_map.setdefault(item[4], []).append(key)
                self.item[key].append(entry)
                if self.firstZone == '':
                    self.firstZone = item[0]
                if self.firstMachine == '' and int(entry.mode) != 3:
                    self.firstMachine = entry.name

            for key, entrys in self.item.items():
                entrys.sort(lambda x, y: cmp(self.serverName.index(x.name) if x.name in self.serverName else len(self.serverName), self.serverName.index(y.name) if y.name in self.serverName else len(self.serverName)))

        except Exception as e:
            gamelog.debug('@zhp parseSeverlist Error', e)

    def findByIp(self, ip):
        for key, item in self.item.iteritems():
            for i, entry in enumerate(item):
                if ip in entry.ip:
                    return (key, i)

    def findByName(self, name):
        for key, item in self.item.iteritems():
            for i, entry in enumerate(item):
                if name == entry.name:
                    return (key, i)

    def findByNameExcludeHide(self, name):
        for key, item in self.item.iteritems():
            i, j = (0, 0)
            for entry in item:
                j += 1
                if int(entry.mode) == 3:
                    continue
                if name == entry.name:
                    return (key, i, j - 1)
                i += 1

    def updateCharNum(self, serversInfo):
        self.serversInfo = serversInfo
        self._service_cache.clear()
        for items in self._server_cache.values():
            for item in items:
                item.charNum = 0

        if serversInfo:
            for replyVal in serversInfo:
                server, num = replyVal.server, replyVal.usernum
                entrys = self._server_cache.get(server, None)
                if entrys:
                    for entry in entrys:
                        entry.charNum = num

                services = self._zone_map.get(server, '')
                if services:
                    for service in services:
                        self._service_cache.setdefault(service, 0)
                        self._service_cache[service] += num

    def getCharNumByZone(self, zone):
        return self._service_cache.get(zone, 0)

    def getEntry(self, zone, serverIdx):
        servers = self.item.get(zone, [])
        if len(servers) > serverIdx:
            return servers[serverIdx]

    def findNoviceServers(self):
        results = []
        for key, item in self.item.iteritems():
            i, j = (0, 0)
            for entry in item:
                j += 1
                if int(entry.mode) == 5:
                    results.append((key, i, j - 1))
                i += 1

        return results
