#Embedded file name: I:/bag/tmp/tw2/res/entities\common/gamestrings.o
DEFAULT_LANGUAGE = 'zh_CN'
RUSSIA_LANGUAGE = 'ru'
EUROPE_LANGUAGE = 'eu'

def serverLanguage():
    import ResMgr
    import BigWorld
    if BigWorld.component in 'client':
        try:
            sec = ResMgr.openSection('../game/tianyu.xml')
            lan = sec.readString('language')
            if not lan:
                return DEFAULT_LANGUAGE
            return lan
        except:
            return DEFAULT_LANGUAGE

    else:
        try:
            return ResMgr.root['server']['bw.xml']['Game']['language'].asString
        except (KeyError, AttributeError):
            return DEFAULT_LANGUAGE


langModule = 'gamestrings_%s' % serverLanguage()
try:
    gameStrings = __import__(langModule).data
except:
    gameStrings = __import__('gamestrings_zh_CN').data

def reloadGameStrings():
    global gameStrings
    try:
        gameStrings = __import__(langModule).data
    except:
        gameStrings = __import__('gamestrings_zh_CN').data


def isInternationalLanguage():
    return serverLanguage() != DEFAULT_LANGUAGE


def isRussiaLanguage():
    return serverLanguage() == RUSSIA_LANGUAGE


def isEuropeLanguage():
    return serverLanguage() == EUROPE_LANGUAGE
