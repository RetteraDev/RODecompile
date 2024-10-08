#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\tzlocal/win32.o
try:
    import _winreg as winreg
except ImportError:
    import winreg

from tzlocal.windows_tz import win_tz
import pytz
_cache_tz = None

def valuestodict(key):
    """Convert a registry key's values to a dictionary."""
    dict = {}
    size = winreg.QueryInfoKey(key)[1]
    for i in range(size):
        data = winreg.EnumValue(key, i)
        dict[data[0]] = data[1]

    return dict


def get_localzone_name():
    handle = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    TZLOCALKEYNAME = 'SYSTEM\\CurrentControlSet\\Control\\TimeZoneInformation'
    localtz = winreg.OpenKey(handle, TZLOCALKEYNAME)
    keyvalues = valuestodict(localtz)
    localtz.Close()
    if 'TimeZoneKeyName' in keyvalues:
        tzkeyname = keyvalues['TimeZoneKeyName'].split(' ', 1)[0]
    else:
        tzwin = keyvalues['StandardName']
        TZKEYNAME = 'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Time Zones'
        tzkey = winreg.OpenKey(handle, TZKEYNAME)
        tzkeyname = None
        for i in range(winreg.QueryInfoKey(tzkey)[0]):
            subkey = winreg.EnumKey(tzkey, i)
            sub = winreg.OpenKey(tzkey, subkey)
            data = valuestodict(sub)
            sub.Close()
            try:
                if data['Std'] == tzwin:
                    tzkeyname = subkey
                    break
            except KeyError:
                pass

        tzkey.Close()
        handle.Close()
    if tzkeyname is None:
        raise LookupError('Can not find Windows timezone configuration')
    timezone = win_tz.get(tzkeyname)
    if timezone is None:
        timezone = win_tz.get(tzkeyname + ' Standard Time')
    if timezone is None:
        raise pytz.UnknownTimeZoneError('Can not find timezone ' + tzkeyname)
    return timezone


def get_localzone():
    """Returns the zoneinfo-based tzinfo object that matches the Windows-configured timezone."""
    global _cache_tz
    if _cache_tz is None:
        _cache_tz = pytz.timezone(get_localzone_name())
    return _cache_tz


def reload_localzone():
    """Reload the cached localzone. You need to call this if the timezone has changed."""
    global _cache_tz
    _cache_tz = pytz.timezone(get_localzone_name())
