#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/richTextUtils.o
from gamestrings import gameStrings
import re
import sys
import math
import random
import BigWorld
import uiUtils
import utils
import const
import uiConst
import gameglobal
import formula
import gametypes
import gamelog
import itemToolTipUtils
import wingWorldUtils
from gamestrings import gameStrings
from data import item_data as ID
from data import seeker_data as SD
from data import chunk_mapping_data as CMD
from data import map_config_data as MCD
from data import jingjie_data as JD
from data import arena_score_desc_data as ASDD
from data import qumo_lv_data as QLD
from data import junjie_config_data as JCD
from data import mingpai_data as MPD
from data import world_war_army_data as WWAD
from data import wing_world_army_data as WWDAD
from data import prop_ref_data as PRD
from data import equip_prefix_prop_data as EPPD
from data import chat_channel_data as CCD
OP_CODE_PRO = 'CH'
OP_CODE_RANDOM = 'RND'
ALL_OP_CODE = (OP_CODE_PRO, OP_CODE_RANDOM)
HIDE_QUES = '@@H_ques'
PLAYER_PRO = '@@((%s)_[^@]+)' % '|'.join(ALL_OP_CODE)
transTextField = None

def linkFun(match):
    itemId = match.group(1)
    color = match.group(2)
    if color:
        color = '#' + color[2:]
    else:
        color = '#00FF00'
    itemName = ID.data.get(int(itemId), {}).get('name', '')
    return "<u><font color=\'%s\'><a href=\'event:item:%s\'>%s</a></font></u>" % (color, itemId, itemName)


def imgAnswerFun(match):
    img = match.group(1)
    secAsk = match.group(2)
    size = match.group(3)
    if not img.startswith('http'):
        return ''
    return '[img %s->sec_ask:%s@size_%s]' % (img, secAsk, size)


def answerFun(match):
    answer = match.group(1)
    if '@@IMG_' in answer:
        return '<answer %s>' % answer
    hideQues = False
    rHideQues = re.findall(HIDE_QUES, answer, re.DOTALL)
    if rHideQues and len(rHideQues):
        hideQues = True
        answer = re.sub(HIDE_QUES, '', answer, 0, re.DOTALL)
    rPlayerPro = re.findall(PLAYER_PRO, answer, re.DOTALL)
    if rPlayerPro and len(rPlayerPro):
        answer = re.sub(PLAYER_PRO, '', answer, 0, re.DOTALL)
    if answer.find('@') >= 0:
        arr = answer.split('@')
        show = arr[0]
        link = arr[1]
    else:
        show = answer
        link = re.sub('\\#c[A-Fa-f0-9]{,6}', '', answer, 0, re.DOTALL)
    if rPlayerPro:
        opCode = [ x[0] for x in rPlayerPro ]
        link += '@@' + '@@'.join(opCode)
    if hideQues:
        return "<font color=\'#DDFFFF\'><a href=\'event:sec_ask:%s@@H_ques\'><u>%s</u></a></font>" % (link, show)
    else:
        return "<font color=\'#DDFFFF\'><a href=\'event:sec_ask:%s\'><u>%s</u></a></font>" % (link, show)


def uiActionFun(match):
    txt = match.group(1)
    actions = match.group(2)
    return uiUtils.toHtml(txt, linkEventTxt='uiShow:' + actions)


def webImgFun(match):
    code = match.group(1)
    imgUrl = match.group(2)
    linkTo = match.group(3)
    if code == 'uiShow':
        linkTo = 'uiShow:' + linkTo
    size = match.group(4)
    return '[img %s->%s@size_%s]' % (imgUrl, linkTo, size)


def ieImgFun(match):
    code = match.group(1)
    imgUrl = match.group(2)
    linkTo = match.group(3)
    uiSize = match.group(5)
    imgSize = match.group(6)
    if uiSize:
        width, height = uiSize.split('_')
        linkTo = 'uiShow:innerIE.show(%s, %s, %s, %s)' % (linkTo,
         code,
         width,
         height)
    else:
        linkTo = 'uiShow:innerIE.show(%s, %s)' % (linkTo, code)
    return '[img %s->%s@size_%s]' % (imgUrl, linkTo, imgSize)


def ieTextFun(match):
    code = match.group(1)
    text = match.group(2)
    linkTo = match.group(3)
    uiSize = match.group(5)
    if uiSize:
        if uiSize:
            width, height = uiSize.split('_')
            linkTo = 'uiShow:innerIE.show(%s, %s, %s, %s)' % (linkTo,
             code,
             width,
             height)
    else:
        linkTo = 'uiShow:innerIE.show(%s, %s)' % (linkTo, code)
    return uiUtils.toHtml(text, linkEventTxt=linkTo)


def webFun(match):
    txt = match.group(1)
    webSite = match.group(2)
    return uiUtils.toHtml(txt, linkEventTxt=webSite)


def findSeekFun(match):
    seekId = match.group(1)
    seekData = SD.data.get(int(seekId), {})
    spaceNo = seekData.get('spaceNo', const.SPACE_NO_BIG_WORLD)
    if spaceNo == const.SPACE_NO_BIG_WORLD:
        chunkName = uiUtils.getChunkName(seekData.get('xpos', 0), seekData.get('zpos', 0))
        secenName = CMD.data.get(chunkName, {}).get('chunkNameZhongwen', '')
    else:
        secenName = MCD.data.get(spaceNo, {}).get('name', '')
    if secenName:
        secenName = secenName + ','
    content = '%s(%s%s,%s,%s)' % (seekData.get('name', ''),
     secenName,
     int(seekData.get('xpos', 0)),
     int(seekData.get('zpos', 0)),
     int(seekData.get('ypos', 0)))
    return "<u><font color=\'#00FF00\'><a href=\'event:seek:%s\'>%s</a></font></u>" % (seekId, content)


def findPosFun(match):
    pos = match.group(1).split(',')
    if len(pos) == 5:
        return "<u><font color=\'#00FF00\'><a href=\'event:findPos:%s\'>(%s,%s,%s,%s)</a></font></u>" % (match.group(1),
         pos[4],
         pos[1],
         pos[3],
         pos[2])
    return "<u><font color=\'#00FF00\'><a href=\'event:findPos:%s\'>(%s,%s,%s)</a></font></u>" % (match.group(1),
     pos[1],
     pos[3],
     pos[2])


def colorFun(match):
    color = match.group(1)
    content = match.group(2)
    end = match.group(3)
    if len(end) > 1:
        end = ''
    return "<font color=\'#%s\'>%s</font>" % (color, content) + end


def colorFun2(match):
    color = match.group(1)
    content = match.group(2)
    return "<font color=\'#%s\'>%s</font>" % (color, content)


def replaceFun(match):
    content = match.group(1)
    return '[%s]' % content


def getOpFun(match):
    if not utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
        return ''
    else:
        content = match.group(1).lower()
        result = ''
        try:
            if content.startswith(OP_CODE_PRO.lower()):
                content = content[len(OP_CODE_PRO) + 1:]
                if '|' in content:
                    proCode = content.split('|')
                else:
                    proCode = [content]
                for code in proCode:
                    funcName = 'get' + code[0].upper() + code[1:]
                    func = getattr(sys.modules[__name__], funcName, None)
                    if func:
                        result += ' %s=%s' % (code, func(BigWorld.player()))

            elif content.startswith(OP_CODE_RANDOM.lower()):
                content = content[len(OP_CODE_RANDOM) + 1:]
                if '-' in content:
                    rnds = content.split('-')
                if len(rnds) == 2:
                    start, end = rnds
                    if start < end:
                        result += ' %s' % random.randrange(int(start), int(end))
        except:
            gamelog.error('@zhp parse RichText Error:%s' % content)

        return result


def cgtTxtFun(match):
    txt = match.group(1)
    link = match.group(2)
    if '@@IMG_' in link:
        link, size = link.split('@@IMG_')
        if not txt.startswith('http'):
            return ''
        return '[img %s->qustionTxt:%s@size_%s]' % (txt, link, size)
    else:
        return "<u><a href=\'event:qustionTxt:%s\'>%s</a></u>" % (link, txt)


def addFriendFun(match):
    txt = match.group(1)
    link = match.group(2)
    if '@@IMG_' in link:
        link, size = link.split('@@IMG_')
        if not txt.startswith('http'):
            return ''
        return '[img %s->addFriend:%s@size_%s]' % (txt, link, size)
    else:
        return "<u><a href=\'event:addFriend:%s\'>%s</a></u>" % (link, txt)


def userLinkFun(match):
    txt = match.group(1)
    return "<a href=\'event:role%s$\'><u>%s</u></a>" % (txt, txt)


def msgUserlinkFun(match):
    p = BigWorld.player()
    field, data = match.group(1).split('=')
    roleName, gbId = data.split(',')
    gbId = long(gbId)
    p = BigWorld.player()
    if p.gbId == gbId:
        ret = gameStrings.SELF_FIELD
    elif gbId not in p.members:
        ret = "<a href = \'event:privateChat:%s,%d\'><u>%s</u></a>" % (roleName, gbId, roleName)
    elif p.groupType == gametypes.GROUP_TYPE_TEAM_GROUP:
        color = CCD.data.get(const.CHAT_CHANNEL_TEAM, {}).get('color')
        ret = "%s<a href = \'event:privateChat:%s,%d\'><u>%s</u></a>" % (gameStrings.TEAM_MEMBER_FIELD,
         roleName,
         gbId,
         uiUtils.toHtml(roleName, color))
    elif p.groupType == gametypes.GROUP_TYPE_RAID_GROUP:
        color = CCD.data.get(const.CHAT_CHANNEL_GROUP, {}).get('color')
        ret = "%s<a href = \'event:privateChat:%s,%d\'><u>%s</u></a>" % (gameStrings.GROUP_MEMBER_FIELD,
         roleName,
         gbId,
         uiUtils.toHtml(roleName, color))
    else:
        ret = "<a href = \'event:privateChat:%s,%d\'><u>%s</u></a>" % (roleName, gbId, roleName)
    return ret


def msgEndlinkFun(match):
    p = BigWorld.player()
    field, data = match.group(1).split('=')
    gbId = long(data)
    if gbId not in p.members or gbId == p.gbId:
        return ''
    return gameStrings.TEXT_RICHTEXTUTILS_285 % (gbId, gbId)


SPRITE_RICH_TEXT_PATERNS = [['<noEvaluate/>', ''],
 [uiConst.NO_ERROR_CORRECT, ''],
 ['\\sdesc.*?>', '>'],
 ['</?tuijiandaoju.*?>', ''],
 ['<(item[0-9]+|skill[0-9]+|img.*?)>', replaceFun],
 ['<answer\\s?(.*?)>', answerFun],
 ['<answer\\s?(.*?)@(.*?)@@IMG_(.*?)>', imgAnswerFun],
 ['<interface\\s?(.*?)@(.*?)>', uiActionFun],
 ['<cgt\\s?(.*?)@(.*?)>', cgtTxtFun],
 ['<AddF\\s(.*?)@(.*?)>', addFriendFun],
 ['<(web|uiShow)\\s?(.*?)@(.*?)@@IMG_(.*?)>', webImgFun],
 ['<uiShow\\s?(.*?)@(.*?)>', uiActionFun],
 ['<web\\s?(.*?)@(.*?)>', webFun],
 ['<link.*?item.*?=.*?([0-9]+)(\\#c.*?)?>', linkFun],
 ['<find\\s?seekId.*?=(.*?)>', findSeekFun],
 ['<find\\s?=(.*?)>', findPosFun],
 ['<Iecall_(0|2|3)\\s?(.*?)@(.*?)(@@UI_(.*?))?@@IMG_(.*?)>', ieImgFun],
 ['<Iecall_(0|2|3)\\s?(.*?)@(.*?)(@@UI_(.*?))?>', ieTextFun],
 ['\\#c([A-Fa-f0-9]{,6})\\s?(.*?)(\\#n|<|@|>)', colorFun],
 ['\\#c([A-Fa-f0-9]{,6})([^(#c|#r|<)]+)', colorFun2],
 ['\\#r', '<br>']]
SYS_RICH_TEXT_PATERNS = [['<userlink(.*?)>', userLinkFun], ['<msgUserlink(.*?)>', msgUserlinkFun], ['<msgEndlink(.*?)>', msgEndlinkFun]]

def parseRichText(txt):
    for item in SPRITE_RICH_TEXT_PATERNS:
        try:
            txt = re.sub(item[0], item[1], txt, 0, re.DOTALL | re.IGNORECASE | re.VERBOSE)
        except:
            pass

    return txt


def parseSysTxt(txt):
    for item in SYS_RICH_TEXT_PATERNS:
        try:
            txt = re.sub(item[0], item[1], txt, 0, re.DOTALL | re.IGNORECASE | re.VERBOSE)
        except:
            pass

    return txt


def getOpCodeFullText(txt):
    opFullText = re.sub(PLAYER_PRO, getOpFun, txt, 0, re.DOTALL | re.IGNORECASE | re.VERBOSE)
    viewText = re.sub(PLAYER_PRO, '', txt, 0, re.DOTALL | re.IGNORECASE | re.VERBOSE)
    return (viewText, opFullText)


def getSrv(p):
    return gameglobal.rds.g_serverid


def getHost(p):
    title = gameglobal.rds.loginManager.titleName()
    if title:
        return title
    return '0'


def getGbid(p):
    return p.gbId


def getUid(p):
    return p.clientDBID


def getName(p):
    return p.realRoleName


def getLv(p):
    return p.lv


def getUrs(p):
    return gameglobal.rds.ui.loginWin.userName


def getVip(p):
    return utils.getVipGrade(p)


def getCzfw(p):
    ret = int(uiUtils.hasVipBasic())
    if ret:
        d = math.ceil((p.vipBasicPackage.get('tExpire', 0) - p.getServerTime()) / const.TIME_INTERVAL_DAY)
        return '%d.%d' % (ret, d)
    else:
        return ret


def getSxzz(p):
    vipPackage = p.vipAddedPackage.get(10011, {})
    ret = int(vipPackage.get('tExpire', 0) > p.getServerTime())
    if ret:
        d = math.ceil((vipPackage.get('tExpire', 0) - p.getServerTime()) / const.TIME_INTERVAL_DAY)
        return '%d.%d' % (ret, d)
    else:
        return ret


def getZdzz(p):
    vipPackage = p.vipAddedPackage.get(10013, {})
    ret = int(vipPackage.get('tExpire', 0) > p.getServerTime())
    if ret:
        d = math.ceil((vipPackage.get('tExpire', 0) - p.getServerTime()) / const.TIME_INTERVAL_DAY)
        return '%d.%d' % (ret, d)
    else:
        return ret


def getXxzz(p):
    vipPackage = p.vipAddedPackage.get(10012, {})
    ret = int(vipPackage.get('tExpire', 0) > p.getServerTime())
    if ret:
        d = math.ceil((vipPackage.get('tExpire', 0) - p.getServerTime()) / const.TIME_INTERVAL_DAY)
        return '%d.%d' % (ret, d)
    else:
        return ret


def getXb(p):
    return const.SEX_NAME.get(p.physique.sex, '')


def getZy(p):
    return const.SCHOOL_DICT.get(p.school, '')


def getTx(p):
    csd = gameglobal.rds.loginScene.getCharShowData(p.school, p.physique.sex, p.physique.bodyType)
    return const.BODY_TYPE_DESC.get(csd.get('icon', 'hao'), gameStrings.TEXT_RICHTEXTUTILS_420)


def getRealm(p):
    return JD.data.get(p.jingJie, {}).get('name', '')


def getIz(p):
    chunckName = BigWorld.ChunkInfoAt(p.position)
    return formula.whatLocationName(p.spaceNo, chunckName)


def getGh(p):
    if p.guildName:
        return p.guildName
    return 0


def getGhzw(p):
    if p.guild and p.guild.member.has_key(p.gbId):
        return gametypes.GUILD_ROLE_DICT[p.guild.member[p.gbId].roleId]
    return 0


def getZp(p):
    return p.equipment.calcAllEquipScore(p.suitsCache)


def getZl(p):
    return utils.calcArenaCombatPower(p.arenaInfo)


def getZj(p):
    return JCD.data.get(p.junJieLv, {}).get('name', '')


def getQm(p):
    if p.qumoLv == 0:
        return '0'
    return QLD.data.get(p.qumoLv, {}).get('name', '0')


def getJjdw(p):
    tmpASDD = ASDD.data.keys()
    tmpASDD.sort()
    for minS, maxS in tmpASDD:
        if p.arenaInfo.arenaScore >= minS and p.arenaInfo.arenaScore <= maxS:
            return ASDD.data[minS, maxS].get('desc', gameStrings.TEXT_ARENAPROXY_321)

    return gameStrings.TEXT_RICHTEXTUTILS_467


def getZswq(p):
    equip = p.equipment[gametypes.EQU_PART_WEAPON_ZHUSHOU]
    return createItemInfoStr(equip)


def getFswq(p):
    equip = p.equipment[gametypes.EQU_PART_WEAPON_FUSHOU]
    return createItemInfoStr(equip)


def getMz(p):
    equip = p.equipment[gametypes.EQU_PART_HEAD]
    return createItemInfoStr(equip)


def getYf(p):
    equip = p.equipment[gametypes.EQU_PART_BODY]
    return createItemInfoStr(equip)


def getKz(p):
    equip = p.equipment[gametypes.EQU_PART_LEG]
    return createItemInfoStr(equip)


def getSt(p):
    equip = p.equipment[gametypes.EQU_PART_HAND]
    return createItemInfoStr(equip)


def getXz(p):
    equip = p.equipment[gametypes.EQU_PART_SHOE]
    return createItemInfoStr(equip)


def getXl(p):
    equip = p.equipment[gametypes.EQU_PART_NECKLACE]
    return createItemInfoStr(equip)


def getEhs(p):
    equip = p.equipment[gametypes.EQU_PART_EARRING1]
    return createItemInfoStr(equip)


def getEhx(p):
    equip = p.equipment[gametypes.EQU_PART_EARRING2]
    return createItemInfoStr(equip)


def getJzs(p):
    equip = p.equipment[gametypes.EQU_PART_RING1]
    return createItemInfoStr(equip)


def getJzx(p):
    equip = p.equipment[gametypes.EQU_PART_RING2]
    return createItemInfoStr(equip)


def createItemInfoStr(item):
    if not item:
        return ''
    itemStr = ''
    if hasattr(item, 'name'):
        itemStr = item.name
        if hasattr(item, 'prefixInfo'):
            for prefixItem in EPPD.data.get(item.prefixInfo[0], []):
                if prefixItem['id'] == item.prefixInfo[1]:
                    itemStr = '%s %s' % (prefixItem['name'], itemStr)
                    break

        enhJuexingData = getattr(item, 'enhJuexingData', {})
        if enhJuexingData:
            enhJueXingList = [ [key, val] for key, val in enhJuexingData.items() ]
            enhJueXingList.sort(key=lambda k: k[0])
            for key in enhJueXingList:
                if not key[1]:
                    continue
                for pId, pType, propNum in key[1]:
                    if pId in itemToolTipUtils.PROPS_SHOW_SHRINK:
                        propNum = round(propNum / 100.0, 1)
                    prdData = PRD.data.get(pId, {})
                    itemStr += ' %s%s' % (prdData.get('name', ''), uiUtils.formatProp(propNum, pType, prdData.get('showType', 0)))

    return itemStr


def itemRichText(itemId):
    return ['item%d'] % itemId


def mingPaiRichText(mpId, w = 0, h = 0):
    if not gameglobal.rds.configData.get('enableMingpai', False):
        return ''
    if mpId > 0 and MPD.data.has_key(mpId):
        return '[mingpai%s@%s_%s]' % (mpId, w, h)
    return ''


def wwArmyPostRichText(postId, camp = 0):
    if gameglobal.rds.configData.get('enableWorldWarArmy', False) and WWAD.data.has_key(postId):
        if WWAD.data.get(postId).get('icon'):
            w, h = WWAD.data.get(postId, {}).get('size', (120, 16))
            return '[wwArmyPost%s@%s_%s]' % (postId, w, h)
    if gameglobal.rds.configData.get('enableWingWorld', False) and wingWorldUtils.getWingArmyData().has_key(postId):
        p = BigWorld.player()
        if p.isWingWorldCampArmy():
            if wingWorldUtils.getWingArmyData().get(postId).get('icon1', '') and wingWorldUtils.getWingArmyData().get(postId).get('icon2', ''):
                w, h = wingWorldUtils.getWingArmyData().get(postId, {}).get('size', (120, 16))
                if not camp:
                    camp = p.wingWorldCamp
                if not camp:
                    w, h = (0, 0)
                postId = '%s-%s' % (postId, camp)
                return '[wwArmyPost%s@%s_%s]' % (postId, w, h)
        elif wingWorldUtils.getWingArmyData().get(postId).get('icon'):
            w, h = wingWorldUtils.getWingArmyData().get(postId, {}).get('size', (120, 16))
            return '[wwArmyPost%s@%s_%s]' % (postId, w, h)
    return ''


def voiceRichText(id):
    if id:
        return '[voice.%s]' % id
    return ''


def isVoice(msg, retMatch = False):
    match = None
    if msg:
        match = re.search('\\[voice.*?\\]', msg, re.DOTALL | re.IGNORECASE | re.VERBOSE)
    if retMatch:
        return match
    elif match:
        return True
    else:
        return False


def isSoundRecord(msg):
    if msg:
        if re.search('\\[sound.*?\\]', msg, re.DOTALL | re.IGNORECASE | re.VERBOSE):
            return True
    return False


def isRedPacket(msg):
    if msg:
        if re.search('\\[redPacket.*?\\]', msg, re.DOTALL | re.IGNORECASE | re.VERBOSE):
            return True
    return False


def isMingPai(msg):
    if msg:
        if re.search('\\[mingpai.*?\\]', msg, re.DOTALL | re.IGNORECASE | re.VERBOSE):
            return True
    return False


def isWwArmyPost(msg):
    if msg:
        if re.search('\\[wwArmyPost.*?\\]', msg, re.DOTALL | re.IGNORECASE | re.VERBOSE):
            return True
    return False


def isSysRichTxt(msg):
    return isMingPai(msg) or isRedPacket(msg) or isWwArmyPost(msg) or isSoundRecord(msg)


def htmlToPlaneText(msg):
    global transTextField
    if not transTextField:
        import asObject
        transTextField = asObject.ASUtils.getClsByClsName('flash.text.TextField')
    transTextField.htmlText = msg
    transTextField.htmlText = transTextField.text
    return transTextField.text


def parseFriendChatMsg(msg):
    if isSoundRecord(msg):
        return gameStrings.FRIEND_CHAT_VOICEMSG_SHOW
    if isRedPacket(msg):
        return gameStrings.FRIEND_CHAT_REDPACKETMSG_SHOW
    result = re.sub('!\\$(17[0-8]|1[0-6][0-9]|0[0-9][0-9]){1}', gameStrings.FRIEND_CHAT_FACEMSG_SHOW, msg, re.DOTALL | re.IGNORECASE | re.VERBOSE)
    return result
