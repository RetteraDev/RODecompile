#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\helpers/tabooTool.o
import os
INPUT_FILE = 'tabooData.txt'
OUTPUT_FILE = 'tabooData.py'
TABOO_DICT = {'TABOO_PINGBI': 'originWordsA',
 'TABOO_TIHUAN': 'originWordsB',
 'TABOO_TIANXIA': 'originWordsBWorld',
 'TABOO_MIYU': 'originWordsBSingle',
 'TABOO_DIDENGJI': 'originWordsBNewbie',
 'TABOO_SANLEI': 'originWordsC',
 'TABOO_QUANDENGJI': 'originWordsBAllLv',
 'TABOO_MINGMING': 'originWordsName',
 'TABOO_CHECKPATHWG': 'checkPathWaiguaList',
 'TABOO_TUISONG': 'autoPushSystemWords'}

def _findTabooType(line):
    for key in TABOO_DICT.keys():
        if key in line:
            return key


def parseTabooData(fin, res, tabooType):
    while True:
        line = fin.readline()
        lenth = len(line)
        line = line.decode('mbcs')
        if len(line) == 0:
            return True
        t = _findTabooType(line)
        if t:
            if t != tabooType:
                fin.seek(-1 * (lenth + 1), os.SEEK_CUR)
            return False
        res[tabooType].append(line)

    return False


def writeRes(res):
    fout = open(OUTPUT_FILE, 'w')
    fout.write('# -*-coding: utf-8 -*-\n\n')
    for k in TABOO_DICT:
        if k not in res:
            res[k] = []

    for key, vals in res.items():
        fout.write(TABOO_DICT[key] + ' = (\n')
        for t in vals:
            t = t.strip('\n')
            if not t:
                continue
            t = t.encode('utf-8')
            fout.write("    \'" + t.strip('\n') + "\',\n")

        fout.write(')\n\n')

    fout.close()


def processTabooData():
    fin = open(INPUT_FILE, 'r')
    if not fin:
        return
    res = {}
    while True:
        line = fin.readline()
        if len(line) == 0:
            break
        line = line.decode('mbcs')
        tabooType = _findTabooType(line)
        if not tabooType:
            continue
        res[tabooType] = []
        if parseTabooData(fin, res, tabooType):
            break

    writeRes(res)
    fin.close()
    print 'processTabooData done'


if __name__ == '__main__':
    processTabooData()
