#Embedded file name: /WORKSPACE/data/entities/client/helpers/walklineeditor.o
import csv
import struct
import operator
import Math
import BigWorld
import GUI
import ResMgr
import gameglobal
import gamelog
import navigator
import clientUtils
from gameclass import Singleton
from guis import ui
INDICATOR_MODEL = 'char/50008/50008.model'
layoutPoints = None

class PointData(object):
    __slots__ = ['pos',
     'type',
     'connects',
     'num',
     'isFloat']
    AIRPOINT = 0
    AIRPORT = 1

    def __init__(self, type, pos, num, connectPoint = None):
        self.pos = pos
        self.type = type
        self.connects = []
        self.num = num
        self.isFloat = None
        self.addConnect(connectPoint)

    def distance(self, point):
        return (point.pos - self.pos).length

    def connectwith(self, point):
        return point in self.connects

    def updateType(self):
        self.isFloat = False
        if len(self.connects) != 2:
            self.type = self.__class__.AIRPORT
        else:
            self.type = self.__class__.AIRPOINT

    def addConnect(self, point = None):
        if point:
            if point not in self.connects:
                self.connects.append(point)
                point.addConnect(self)

    def delConnect(self, point = None):
        if point:
            if point in self.connects:
                self.connects.remove(point)
                point.delConnect(self)

    def delSelf(self):
        canSelect = -1
        tCon1, tCon2 = (None, None)
        type1, type2 = (0, 0)
        if self.type == self.__class__.AIRPOINT:
            if len(self.connects) == 2:
                tCon1, tCon2 = self.connects
                type1, type2 = tCon1.type, tCon2.type
        while len(self.connects):
            point = self.connects[0]
            canSelect = point.num
            point.delConnect(self)

        if tCon1 and tCon2:
            tCon1.type = type1
            tCon2.type = type2
            tCon1.addConnect(tCon2)
        return canSelect


class pointData(object):

    def __init__(self, num, last = None, dis = 0):
        self.num = num
        self.last = last
        self.dis = dis


points = {}
edges = {}
bestPath = {}

def findBestWay(p1, p2):
    global points
    global edges
    data = {}
    used = [p1]
    for p in points.keys():
        if p == p1:
            data[p] = pointData(p)
        else:
            data[p] = pointData(p, None, 999999)

    cur = p1
    cnt = 0
    while len(used) < len(data) and cnt < 100:
        predis = data[cur].dis != 999999 and data[cur].dis or 0
        for i in data.keys():
            w = edges.get((min(cur, i), max(cur, i)), None)
            if w is not None:
                w = w[0]
                if data[i].dis == -1 or data[i].dis > w[1] + predis:
                    data[i].last = cur
                    data[i].dis = w[1] + predis

        tdata = list(data.items())
        tdata.sort(cmp=lambda x, y: cmp(x[1].dis, y[1].dis))
        idx = 0
        while idx < len(tdata):
            if tdata[idx][0] in used:
                idx += 1
                continue
            if tdata[idx][1].dis != 999999:
                used.append(tdata[idx][0])
                cur = tdata[idx][0]
                break
            idx += 1

        cnt += 1

    cur = p2
    path = []
    while cur != p1:
        path.append(cur)
        if data[cur].last:
            cur = data[cur].last
        else:
            return

    path.append(p1)
    path.reverse()
    return path


paths = {}

def findAllPath(points, edges, senceNo, senceTotal, spaceNo):
    adj_matrix = {}
    best_path = {}
    best_dist = {}
    for k, v in edges.iteritems():
        adj_matrix[k] = v[0][1]
        best_dist[k] = v[0][1]
        best_path[k] = list(k)

    best_dist = adj_matrix
    gamelog.debug('findAllPath', best_dist, len(best_dist.keys()))
    t_plength = len(points)
    pointIdx = points.keys()
    for k in xrange(t_plength):
        for i in xrange(t_plength):
            for j in xrange(t_plength):
                if i == j or j == k or i == k:
                    continue
                key1 = (min(pointIdx[i], pointIdx[j]), max(pointIdx[i], pointIdx[j]))
                key2 = (min(pointIdx[i], pointIdx[k]), max(pointIdx[i], pointIdx[k]))
                key3 = (min(pointIdx[j], pointIdx[k]), max(pointIdx[j], pointIdx[k]))
                dist1 = best_dist.get(key1, None)
                dist2 = best_dist.get(key2, None)
                dist3 = best_dist.get(key3, None)
                if dist2 is not None and dist3 is not None:
                    if dist1 is None or best_dist[key1] > dist2 + dist3:
                        if key2[0] in key1:
                            ridNum = key2[1]
                        else:
                            ridNum = key2[0]
                        best_dist[key1] = dist2 + dist3
                        path2 = best_path[key2]
                        path3 = best_path[key3]
                        if ridNum != path2[-1]:
                            path2.reverse()
                        if ridNum != path3[0]:
                            path3.reverse()
                        path1 = path2 + path3[1:]
                        if path1[0] > path1[-1]:
                            path1.reverse()
                        best_path[key1] = path1

    return (best_dist, best_path)


def doSaveGraphic(sect, pointsdata, callback):
    t_pointdata = pointsdata
    for spaceNo in t_pointdata.keys():
        if len(t_pointdata[spaceNo]) == 0:
            continue
        curSpaceSect = sect.createSection('spaceNo_%d' % spaceNo)
        curSpaceSect.writeInt('spaceNo', spaceNo)
        pointSect = curSpaceSect.createSection('points')
        for k, v in t_pointdata[spaceNo].iteritems():
            psect = pointSect.createSection('point')
            psect.writeVector3('pos', v.pos)
            psect.writeInt('type', v.type)
            psect.writeString('connects', str([ x.num for x in v.connects ]))
            psect.writeInt('num', v.num)

    sect.save()
    if callback:
        callback()


def doSaveStoneWays(stonedata):
    stoneWayFile = open(PYPATH4, 'w')
    stoneWayFile.write('# -*- coding: GBK -*-\n')
    stoneWayFile.write('#stonenum:((pointnum, length), (pointnum, length), ...)\n')
    stoneWayFile.write('data = {\n')
    for _, data in stonedata.iteritems():
        if len(data) == 0:
            continue
        for stonenum, waydata in data.iteritems():
            stoneWayFile.write(str(stonenum) + ':(')
            for pointnum, dist in waydata.iteritems():
                if pointnum != -1 and dist != -1:
                    stoneWayFile.write('(' + str(pointnum) + ', ' + str(dist) + '), ')

            stoneWayFile.write('),\n')

    stoneWayFile.write('}\n')
    stoneWayFile.write("from utils import convertToConst\ndata = convertToConst(data, name=__name__.split(\'.\')[-1], ktype=\'int\', vtype=\'tuple\')")
    stoneWayFile.close()


CSVPATH1 = '../res/way/寻路主干道路点表.csv'
CSVPATH2 = '../res/way/寻路主干道路线表.csv'
CSVPATH3 = '../res/way/寻路主干道最短路径表.csv'
PYPATH1 = '../res/way/land_points_data.py'
PYPATH2 = '../res/way/land_lines_data.py'
PYPATH3 = '../res/way/land_paths_data_%d.py'
PYPATH4 = '../res/way/stones_waypoint_data.py'
PYPATH5 = '../res/way/flypoints_data.py'

def doExportFlyPoints(pointsdata):
    gamelog.debug('JJ: doExportPoints', pointsdata)
    t_pointsdata = pointsdata
    gamelog.debug('JJ: 需要处理主干道数据的场景编号: ', t_pointsdata.keys())
    cnt = 0
    flyData = {}
    for spaceNo in t_pointsdata.keys():
        cnt += 1
        if len(t_pointsdata) == 0:
            continue
        curpoint = t_pointsdata[spaceNo]
        vPoints = {}
        vEdges = {}
        for num, point in curpoint.items():
            if point.type == PointData.AIRPORT:
                gamelog.debug('bgf:vPoints', num, point.type, point.num, point.connects)
                vPoints[num] = point

        for num, point in vPoints.items():
            for connect in point.connects:
                edge = [point]
                tpoints = [point.num]
                weights = []
                curPoint = connect
                weight = int(point.distance(curPoint))
                weights.append(weight)
                success = True
                while curPoint.type != PointData.AIRPORT:
                    nextPoint = None
                    edge.append(curPoint)
                    tpoints.append(curPoint.num)
                    if len(curPoint.connects):
                        for p in curPoint.connects:
                            if p not in edge:
                                nextPoint = p
                                break

                    else:
                        success = False
                        break
                    if nextPoint:
                        weight += int(curPoint.distance(nextPoint))
                        weights.append(int(curPoint.distance(nextPoint)))
                        curPoint = nextPoint
                    else:
                        success = False
                        break

                if success and curPoint.type == PointData.AIRPORT:
                    edge.append(curPoint)
                    tpoints.append(curPoint.num)
                    if tpoints[0] < tpoints[-1]:
                        key = (min(point.num, curPoint.num), max(point.num, curPoint.num))
                        if not vEdges.has_key(key):
                            vEdges[key] = []
                        vEdges[key].append((edge,
                         weight,
                         weights,
                         tpoints))
                        vEdges[key].sort(key=operator.itemgetter(2))
                else:
                    BigWorld.player().showTopMsg('无法完成操作，请联系程序')
                    return

        best_dist, best_path = findAllPath(vPoints, vEdges, cnt, len(t_pointsdata), spaceNo)
        flyData[spaceNo] = (curpoint, vEdges, best_path)

    saveFlyDataToPy(PYPATH5, flyData)


def doExportPoints(pointsdata):
    global points
    global edges
    global bestPath
    gamelog.debug('JJ: doExportPoints', pointsdata)
    t_pointsdata = pointsdata
    gamelog.debug('JJ: 需要处理主干道数据的场景编号: ', t_pointsdata.keys())
    cnt = 0
    pointDict = {}
    lineDict = {}
    for spaceNo in t_pointsdata.keys():
        cnt += 1
        if len(t_pointsdata) == 0:
            continue
        curpoint = t_pointsdata[spaceNo]
        vPoints = {}
        vEdges = {}
        for num, point in curpoint.items():
            if point.type == PointData.AIRPORT:
                gamelog.debug('bgf:vPoints', num, point.type, point.num, point.connects)
                vPoints[num] = point

        for num, point in vPoints.items():
            for connect in point.connects:
                edge = [point]
                tpoints = [point.num]
                weights = []
                curPoint = connect
                weight = int(point.distance(curPoint))
                weights.append(weight)
                success = True
                while curPoint.type != PointData.AIRPORT:
                    nextPoint = None
                    edge.append(curPoint)
                    tpoints.append(curPoint.num)
                    if len(curPoint.connects):
                        for p in curPoint.connects:
                            if p not in edge:
                                nextPoint = p
                                break

                    else:
                        success = False
                        break
                    if nextPoint:
                        weight += int(curPoint.distance(nextPoint))
                        weights.append(int(curPoint.distance(nextPoint)))
                        curPoint = nextPoint
                    else:
                        success = False
                        break

                if success and curPoint.type == PointData.AIRPORT:
                    edge.append(curPoint)
                    tpoints.append(curPoint.num)
                    if tpoints[0] < tpoints[-1]:
                        key = (min(point.num, curPoint.num), max(point.num, curPoint.num))
                        if not vEdges.has_key(key):
                            vEdges[key] = []
                        vEdges[key].append((edge,
                         weight,
                         weights,
                         tpoints))
                        vEdges[key].sort(key=operator.itemgetter(2))
                else:
                    BigWorld.player().showTopMsg('无法完成操作，请联系程序')
                    return

        points = vPoints
        edges = vEdges
        best_dist = best_path = {}
        bestPath = best_dist
        pointsCache = {}
        for k, v in edges.iteritems():
            for tv in v:
                tdata = []
                tdata.append(tuple(tv[3]))
                tdata.append(tuple(tv[2]))
                tdata.append(tv[1])
                for p in tv[0]:
                    if p.num not in pointsCache:
                        pointsCache[p.num] = [p, []]
                    if k not in pointsCache[p.num][1]:
                        pointsCache[p.num][1].append(k)

                lineDict[k] = tuple(tdata)

        for num, (point, lidx) in pointsCache.items():
            tdata = []
            tdata.append(round(point.pos[0], 4))
            tdata.append(round(point.pos[1], 4))
            tdata.append(round(point.pos[2], 4))
            tdata.append(spaceNo)
            pointDict[point.num] = tuple(tdata)

        bestDict = {}
        gamelog.debug('bestDict', len(best_dist.keys()))
        for k, v in best_dist.iteritems():
            tdata = []
            tdata.append(str(k))
            tdata.append(str(v))
            tdata.append(str(tuple(best_path[k])))
            bestDict[k] = (v,) + tuple(best_path[k])

        pathFileName3 = PYPATH3 % spaceNo
        saveBestPathToPy(pathFileName3, bestDict)

    saveDictToPy(PYPATH1, pointDict, PYPATH2, lineDict)
    gamelog.debug('JJ: 所有场景主干道数据处理完毕')


def _getNum(num):
    return num % 10000


def saveFlyDataToPy(pathName, flyData):
    file = open(pathName, 'w')
    file.write('# -*- coding: GBK -*-\n')
    file.write('data = {\n')
    for spaceNo in flyData:
        points, lines, bestWay = flyData[spaceNo]
        excludePoints = []
        file.write('%d:{\n' % spaceNo)
        file.write("\'ports\':{")
        for key, value in points.iteritems():
            if value.type == PointData.AIRPOINT:
                excludePoints.append(key)
            file.write('%d:(%.4f, %.4f, %.4f),\n' % (key,
             value.pos[0],
             value.pos[1],
             value.pos[2]))

        file.write('},\n')
        if excludePoints:
            file.write("\'exclude_ports\':")
            file.write(str(tuple(excludePoints)))
            file.write(',\n')
        file.write("\'airlines\':{")
        for key, value in lines.iteritems():
            ret = '(%d, %d):(' % key
            for num in value[0][-1]:
                pos = points[num].pos
                ret += '(%.4f, %.4f, %.4f), ' % (pos[0], pos[1], pos[2])

            ret += '),\n'
            file.write(ret)

        file.write('},\n')
        file.write("\'paths\':{")
        for key in bestWay.keys():
            file.write('(%d, %d):(%d, %d),\n' % (key[0],
             key[1],
             key[0],
             key[1]))

        file.write('},\n')
        file.write('},\n')

    file.write('}\n')
    file.write("from utils import convertToConst\ndata = convertToConst(data, name=__name__.split(\'.\')[-1], ktype=\'int\', vtype=\'dict\')")


def saveBestPathToPy2(spaceNo, bestDict):
    file = open(spaceNo, 'w')
    file.write('# -*- coding: GBK -*-\n')
    file.write('#(port1, port2):(length, ports)\n')
    file.write('data = {\n')
    for key, value in bestDict.iteritems():
        aKey = tuple(map(_getNum, key))
        aValue = map(_getNum, value[1:])
        bValue = (value[0],) + tuple(aValue)
        file.write(str(aKey) + ':' + str(bValue))
        file.write(',\n')

    file.write('}\n')
    file.write("from utils import convertToConst\ndata = convertToConst(data, name=__name__.split(\'.\')[-1], ktype=\'tuple\', vtype=\'dict\')")


def saveBestPathToPy(pathName, bestDict):
    file = open(pathName, 'w')
    file.write('# -*- coding: GBK -*-\n')
    file.write('#(port1, port2):(length, ports)\n')
    file.write('data = {\n')
    for key, value in bestDict.iteritems():
        aKey = map(_getNum, key)
        aValue = map(_getNum, value[1:])
        bValue = (value[0],) + tuple(aValue)
        file.write(repr(struct.pack('<2H', *aKey)) + ':' + repr(struct.pack(('<%dH' % len(bValue)), *bValue)))
        file.write(',\n')

    file.write('}\n')
    file.write("from utils import convertToConst\ndata = convertToConst(data, name=__name__.split(\'.\')[-1], ktype=\'str\', vtype=\'str\')")


def saveDictToPy(pathName1, pointDict, pathName2, lineDict):
    pointFile = open(pathName1, 'w')
    pointFile.write('# -*- coding: GBK -*-\n')
    pointFile.write('#pointnum:(x, y, z, spaceNo, (line1, line2,...))\n')
    pointFile.write('data = {\n')
    for key, value in pointDict.iteritems():
        pointFile.write(str(key) + ':' + str(value))
        pointFile.write(',\n')

    pointFile.write('}\n')
    pointFile.write("from utils import convertToConst\ndata = convertToConst(data, name=__name__.split(\'.\')[-1], ktype=\'int\', vtype=\'tuple\')")
    lineFile = open(pathName2, 'w')
    lineFile.write('# -*- coding: GBK -*-\n')
    lineFile.write('#(port1, port2):((points, weights, length),...)\n')
    lineFile.write('data = {\n')
    for key, value in lineDict.iteritems():
        lineFile.write(str(key) + ':(' + str(value) + ',),\n')

    lineFile.write('}\n')
    lineFile.write("from utils import convertToConst\ndata = convertToConst(data, name=__name__.split(\'.\')[-1], ktype=\'tuple\', vtype=\'tuple\')")
    pointFile.close()
    lineFile.close()


class WalkLineEditor(object):
    __metaclass__ = Singleton
    SAVE_PATH = 'way/'

    def __init__(self):
        super(WalkLineEditor, self).__init__()
        self.indicators = {}
        self.lines = {}
        self.points = {}
        self.curSelect = -1
        self.lastSelect = -1
        self.processedPoint = []
        self.numIndex = []
        self.isBgRunning = False
        self.isRunning = False
        self.vPoints = []
        self.vEdges = []

    def dispPorts(self):
        self.compilePoints()
        curpoint = self.points.get(BigWorld.player().spaceNo, None)
        if curpoint is None:
            BigWorld.player().showTopMsg('当前场景没有需要显示的路点')
            return
        pos_list = []
        for i in curpoint.values():
            if i.type == PointData.AIRPORT:
                pos_list.append((i.pos.x,
                 i.pos.y,
                 i.pos.z,
                 BigWorld.player().spaceNo))

    def recoverFromData(self):
        LPD = navigator.getLandPointDataM()
        LLD = navigator.getLandLineDataM()
        if LPD is None or LLD is None:
            BigWorld.player().showTopMsg('缺少路线数据信息')
            return False
        tPointData = {}
        ports = {}
        airlines = {}
        paths = {}
        spaceNo_list = set([])
        for k, v in LLD.data.iteritems():
            spaceNo = int(k[0] / 10000)
            spaceNo_list.add(spaceNo)
            if not tPointData.has_key(spaceNo):
                tPointData[spaceNo] = {}
            if not airlines.has_key(spaceNo):
                airlines[spaceNo] = {}
            if not airlines[spaceNo].has_key(k):
                airlines[spaceNo][k] = []
                for i in v:
                    airlines[spaceNo][k].append(i[0])

            if not ports.has_key(spaceNo):
                ports[spaceNo] = {}
            if not paths.has_key(spaceNo):
                paths[spaceNo] = {}
            if not ports[spaceNo].has_key(k[0]):
                ports[spaceNo][k[0]] = (LPD.data[k[0]][0], LPD.data[k[0]][1], LPD.data[k[0]][2])
            if not ports[spaceNo].has_key(k[1]):
                ports[spaceNo][k[1]] = (LPD.data[k[1]][0], LPD.data[k[1]][1], LPD.data[k[1]][2])

        for spaceNo in spaceNo_list:
            LPATHD = navigator.getLandPathsDataM()
            if LPATHD:
                for k, v in LPATHD.data.iteritems():
                    k = struct.unpack('<2H', k)
                    k = (k[0] + spaceNo * 10000, k[1] + spaceNo * 10000)
                    if not paths[spaceNo].has_key(k):
                        paths[spaceNo][k] = v

        for spaceNo in tPointData.keys():
            tPointData[spaceNo]['ports'] = ports[spaceNo]
            tPointData[spaceNo]['airlines'] = airlines[spaceNo]
            tPointData[spaceNo]['paths'] = paths[spaceNo]

        for k, v in tPointData.iteritems():
            tpoints = v.get('ports', None)
            tedges = v.get('airlines', None)
            tpaths = v.get('paths', None)
            if tpoints is None or tedges is None or tpaths is None:
                return False
            self.points[k] = {}
            for idx, pos in tpoints.iteritems():
                self.points[k][idx] = PointData(0, Math.Vector3(pos), idx)

            for (sp, dp), edge in tedges.iteritems():
                for e in edge:
                    curpoint = self.points[k][sp].pos == Math.Vector3(LPD.data[e[0]][0], LPD.data[e[0]][1], LPD.data[e[0]][2]) and self.points[k][sp] or self.points[k][dp]
                    endpoint = self.points[k][dp].pos == Math.Vector3(LPD.data[e[-1]][0], LPD.data[e[-1]][1], LPD.data[e[-1]][2]) and self.points[k][dp] or self.points[k][sp]
                    for i in xrange(1, len(e) - 1):
                        curpoint = PointData(0, Math.Vector3(LPD.data[e[i]][:3]), e[i], curpoint)
                        self.points[k][e[i]] = curpoint

                    endpoint.addConnect(curpoint)

        self.compilePoints()
        return True

    def savePoints(self, filename):
        tfilename = filename.lower()
        if not tfilename.endswith('.xml'):
            BigWorld.player().showTopMsg('文件名必须以.xml为扩展名')
            return False
        ResMgr.purge(self.SAVE_PATH + filename)
        sect = ResMgr.root.createSection(self.SAVE_PATH + filename)
        self.saveGraphic(sect)
        return True

    def savePointAsCSV(self, fileName):
        csvfile = open('../res/way/' + fileName, 'w')
        o = csv.writer(csvfile)
        out_data = ['路点编号', '坐标']
        o.writerow(out_data)
        tcurpoint = self.points.get(BigWorld.player().spaceNo, None)
        if tcurpoint:
            for key, value in tcurpoint.iteritems():
                array = [key, '%f, %f, %f' % (value.pos[0], value.pos[1], value.pos[2])]
                o.writerow(array)

        csvfile.close()

    def saveGraphic(self, sect):
        self.compilePoints()
        doSaveGraphic(sect, self.points, None)

    def compilePoints(self):
        for space, points in self.points.iteritems():
            for i in points.values():
                i.updateType()

        tcurpoint = self.points.get(BigWorld.player().spaceNo, None)
        gamelog.debug('JJ: tcurpoint', tcurpoint)
        if tcurpoint is not None:
            for i in tcurpoint.values():
                self.placeIndicator(i)
                self.processedPoint.append(i.num)

    def connectPoints(self):
        tcurpoint = self.points.get(BigWorld.player().spaceNo, None)
        if tcurpoint is None:
            BigWorld.player().showTopMsg('当前场景没有路点1')
            return
        curPoint = tcurpoint.get(self.curSelect, None)
        lastPoint = tcurpoint.get(self.lastSelect, None)
        if curPoint is None or lastPoint is None:
            BigWorld.player().showTopMsg('当前选中点或上次选中点不存在，无法连接')
            return
        if curPoint.num == lastPoint.num:
            BigWorld.player().showTopMsg('同一个点无法建立连接')
            return
        if curPoint.connectwith(lastPoint):
            BigWorld.player().showTopMsg('两点之间已有连接')
            return
        curPoint.addConnect(lastPoint)
        self.delLayout(curPoint)
        self.delLayout(lastPoint)
        self.addLayout(curPoint, False)
        self.addLayout(lastPoint, False)
        self.updateCurrent()
        self.updateLast()

    def dconnectPoints(self):
        tcurpoint = self.points.get(BigWorld.player().spaceNo, None)
        if tcurpoint is None:
            BigWorld.player().showTopMsg('当前场景没有路点2')
            return
        curPoint = tcurpoint.get(self.curSelect, None)
        lastPoint = tcurpoint.get(self.lastSelect, None)
        if curPoint is None or lastPoint is None:
            BigWorld.player().showTopMsg('当前选中点或上次选中点不存在，无法删除连接')
            return
        if curPoint.num == lastPoint.num:
            BigWorld.player().showTopMsg('同一个点无法删除连接')
            return
        if not curPoint.connectwith(lastPoint):
            BigWorld.player().showTopMsg('两点之间没有连接')
            return
        curPoint.delConnect(lastPoint)
        self.delLayout(curPoint)
        self.delLayout(lastPoint)
        self.addLayout(curPoint, False)
        self.addLayout(lastPoint, False)
        self.updateCurrent()
        self.updateLast()

    def goToSelect(self):
        tcurpoint = self.points.get(BigWorld.player().spaceNo, None)
        if tcurpoint is None:
            BigWorld.player().showTopMsg('当前场景没有路点3')
            return
        if self.curSelect not in tcurpoint.keys():
            self.curSelect = -1
            return
        pos = tcurpoint[self.curSelect].pos
        if gameglobal.rds.isSinglePlayer:
            BigWorld.player().physics.teleport(pos)
        else:
            command = '$teleport %f %f %f %d' % (pos[0],
             pos[1],
             pos[2],
             BigWorld.player().spaceNo)
            BigWorld.player().handleConsoleInput(command, command)

    def pfToSelect(self):
        tcurpoint = self.points.get(BigWorld.player().spaceNo, None)
        if tcurpoint is None:
            BigWorld.player().showTopMsg('当前场景没有路点3')
            return
        if self.curSelect not in tcurpoint.keys():
            self.curSelect = -1
            return
        pos = tcurpoint[self.curSelect].pos
        p = BigWorld.player()
        p.physics.teleport((pos[0], pos[1], pos[2]))

    def clearModelState(self):
        for i in self.indicators.values():
            m = i[0]
            if len(m.queue) > 0:
                pos = m.position
                yaw = m.yaw
                BigWorld.player().delModel(m)
                BigWorld.player().addModel(m)
                m.position = pos
                m.yaw = yaw
                m.scale = (2.0, 2.0, 2.0)

    def updateLast(self):
        self.clearModelState()
        tcurpoint = self.points.get(BigWorld.player().spaceNo, None)
        if tcurpoint is None or self.lastSelect not in tcurpoint.keys():
            self.lastSelect = -1
            return
        self.indicators[self.lastSelect][0].scale = (6.0, 6.0, 6.0)

    def updateCurrent(self):
        self.clearModelState()
        tcurpoint = self.points.get(BigWorld.player().spaceNo, None)
        if tcurpoint is None or self.curSelect not in tcurpoint.keys():
            self.lastSelect = -1
            return
        self.indicators[self.curSelect][0].scale = (6.0, 6.0, 6.0)

    def addLayout(self, point, needSelect = True):
        self.placeIndicator(point)
        self.processedPoint.append(point.num)
        self.numIndex.append(point.num)
        if needSelect:
            self.updateCurrent()
            self.updateLast()
        self.processedPoint = []

    def delLayout(self, point):
        if self.indicators.has_key(point.num):
            i = self.indicators[point.num]
            BigWorld.player().delModel(i[0])
            GUI.delRoot(i[1])
            del self.indicators[point.num]
        if self.lines.has_key(point.num):
            lines = self.lines.get(point.num, [])
            for i in lines:
                GUI.delRoot(i)

            del self.lines[point.num]

    def placeIndicator(self, point):
        model = clientUtils.model(INDICATOR_MODEL)
        BigWorld.player().addModel(model)
        model.position = point.pos
        model.scale = (2.0, 2.0, 2.0)
        i = GUI.WorldLabelGUI('', ui.font18)
        i.source = model.matrix
        i.biasPos = Math.Vector3(0, 1, 0)
        dispstr = ''
        if point.type == PointData.AIRPORT:
            dispstr = ''.join((dispstr, str(point.num), ' (端点)'))
        elif point.type == PointData.AIRPOINT:
            dispstr = ''.join((dispstr, str(point.num)))
        if point.isFloat is None:
            dispstr = dispstr
        elif point.isFloat:
            dispstr = ''.join((dispstr, ' - 浮空'))
        else:
            dispstr = ''.join((dispstr, ' - 地表'))
        i.text = dispstr
        i.visible = True
        i.maxDistance = 200
        i.colour = Math.Vector4(0, 255, 0, 254)
        self.indicators[point.num] = (model, i)
        GUI.addRoot(i)
        if len(point.connects):
            for p in point.connects:
                if p.num in self.processedPoint:
                    continue
                line = GUI.WorldDebugGUI()
                GUI.addRoot(line)
                line.startPos = point.pos
                line.endPos = p.pos
                if point.type == PointData.AIRPORT or p.type == PointData.AIRPORT:
                    line.colour = Math.Vector4(190, 0, 0, 254)
                else:
                    line.colour = Math.Vector4(0, 190, 0, 254)
                line.radius = 0.02
                l1 = self.lines.setdefault(point.num, [])
                l2 = self.lines.setdefault(p.num, [])
                l1.append(line)
                l2.append(line)

    def clearIndicators(self):
        for i in self.indicators.values():
            if i[0].inWorld:
                BigWorld.player().delModel(i[0])
            GUI.delRoot(i[1])

        self.indicators = {}
        for lines in self.lines.itervalues():
            for i in lines:
                GUI.delRoot(i)

        self.lines = {}
        self.processedPoint = []

    def delPoint(self):
        tcurpoint = self.points.get(BigWorld.player().spaceNo, None)
        if tcurpoint is None:
            BigWorld.player().showTopMsg('当前场景没有路点7')
            return
        if self.curSelect not in tcurpoint.keys():
            return
        point = tcurpoint.get(self.curSelect, None)
        connects = point.connects + []
        if point:
            sel = point.delSelf()
        del tcurpoint[self.curSelect]
        if sel == -1 and len(tcurpoint):
            self.curSelect = tcurpoint.keys()[0]
        else:
            self.curSelect = sel
        self.delLayout(point)
        for point in connects:
            self.delLayout(point)

        for point in connects:
            self.addLayout(point, False)

        self.updateLast()
        self.updateCurrent()

    def addPoint(self, type = PointData.AIRPOINT):
        p = BigWorld.player()
        if not self.points.has_key(p.spaceNo):
            self.points[p.spaceNo] = {}
        num = p.spaceNo * 10000 + len(self.points[p.spaceNo]) + 1
        while num in self.points[p.spaceNo].keys():
            num += 1

        srcPoint = self.points[p.spaceNo].get(self.curSelect, None)
        newPoint = PointData(type, p.position, num, srcPoint)
        self.points[p.spaceNo][newPoint.num] = newPoint
        self.lastSelect = self.curSelect
        self.curSelect = newPoint.num
        self.placeIndicator(newPoint)
        self.updateLast()
        self.updateCurrent()

    def clearCurSpace(self):
        tcurpoint = self.points.get(BigWorld.player().spaceNo, None)
        if tcurpoint is None:
            BigWorld.player().showTopMsg('当前场景没有路点9')
            return
        self.points[BigWorld.player().spaceNo] = {}
        self.clearIndicators()

    def readPoints(self, filename):
        sect = ResMgr.openSection(filename)
        if sect == None:
            BigWorld.player().showTopMsg('导入文件 %s 失败 ' % filename)
            return False
        try:
            for space in sect.items():
                spaceNo = int(space[0].split('_')[-1])
                self.points[spaceNo] = {}
                for element in space[1].items():
                    if element[0] == 'spaceNo':
                        continue
                    elif element[0] == 'points':
                        for p in element[1].items():
                            pd = PointData(0, None, 0)
                            pd.pos = p[1].readVector3('pos')
                            pd.type = p[1].readInt('type')
                            pd.num = p[1].readInt('num')
                            tconnects = eval(p[1].readString('connects'))
                            for tp in tconnects:
                                if self.points[spaceNo].has_key(tp):
                                    if self.points[spaceNo][tp].__class__.__name__ == 'PointData':
                                        pd.addConnect(self.points[spaceNo][tp])
                                    elif self.points[spaceNo][tp].__class__.__name__ == 'list':
                                        self.points[spaceNo][tp].append(pd)
                                else:
                                    self.points[spaceNo][tp] = [pd]

                            if self.points[spaceNo].has_key(pd.num):
                                if self.points[spaceNo][pd.num].__class__.__name__ == 'list':
                                    for tpoint in self.points[spaceNo][pd.num]:
                                        tpoint.addConnect(pd)

                                    self.points[spaceNo][pd.num] = pd
                                else:
                                    self.points[spaceNo][pd.num] = pd
                            else:
                                self.points[spaceNo][pd.num] = pd

            self.compilePoints()
            BigWorld.player().showTopMsg('导入路点成功')
            return True
        except:
            import traceback
            traceback.print_exc()
            BigWorld.player().showTopMsg('导入文件 %s 失败 ' % filename)
            return False

    def getPoint(self, num):
        p = BigWorld.player()
        if num == None or not self.points.has_key(p.spaceNo) or not self.points[p.spaceNo].has_key(num):
            return
        return self.points[p.spaceNo][num]

    def getPoints(self, spaceNo = None):
        p = BigWorld.player()
        num = spaceNo
        if not spaceNo:
            num = p.spaceNo
        gamelog.debug('bgf:getPoints', num)
        if not self.points.has_key(num):
            return {}
        return self.points[num]

    def getCurrentPoint(self):
        return self.getPoint(self.curSelect)

    def getLastPoint(self):
        return self.getPoint(self.lastSelect)

    def setCurrent(self, num):
        self.lastSelect = self.curSelect
        self.curSelect = num

    def exportPoints(self):
        self.compilePoints()
        doExportPoints(self.points)

    def exportFlyPoints(self):
        self.compilePoints()
        doExportFlyPoints(self.points)

    def starCalStone(self):
        if self.isRunning:
            gamelog.debug('b.e.:starCalStone isRunning')
            return
        gamelog.debug('b.e.:starCalStone start')
        self.isRunning = True
        self.stone_dict = {}
        self.spaceNo_list = set([])
        BigWorld.player().isPathfinding = True
        for k in navigator.stoneInfo.iterkeys():
            self.spaceNo_list.add(k)

        self.doCalStone(None, None, True)

    def doCalStone(self, spaceNo, res, isFirst = False):
        if not isFirst:
            self.stone_dict[spaceNo] = res
        if self.spaceNo_list:
            spaceNo = self.spaceNo_list.pop()
            navigator.getNav().calstonepoints(spaceNo, self.doCalStone, 0)
        else:
            self.isRunning = False
            BigWorld.player().isPathfinding = False
            for k, v in self.stone_dict.iteritems():
                gamelog.debug('b.e.: stone_dict:', k, v)

            gamelog.debug('b.e.: doCalStone end!')
            doSaveStoneWays(self.stone_dict)

    def dropPoint(self):
        self.clearIndicators()
        tcurpoint = self.points.get(BigWorld.player().spaceNo, None)
        if tcurpoint:
            p = BigWorld.player()
            for key, value in tcurpoint.iteritems():
                pos = value.pos
                pos = BigWorld.findDropPoint(p.spaceID, Math.Vector3(pos[0], pos[1] + 10, pos[2]))
                if pos:
                    tcurpoint[key].pos = pos[0]

        self.compilePoints()
