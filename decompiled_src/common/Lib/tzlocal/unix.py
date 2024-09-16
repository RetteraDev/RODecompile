#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\tzlocal/unix.o
from __future__ import with_statement
import os
import re
import pytz
_cache_tz = None

def _tz_from_env(tzenv):
    if tzenv[0] == ':':
        tzenv = tzenv[1:]
    if os.path.exists(tzenv):
        with open(tzenv, 'rb') as tzfile:
            return pytz.tzfile.build_tzinfo('local', tzfile)
    try:
        tz = pytz.timezone(tzenv)
        return tz
    except pytz.UnknownTimeZoneError:
        raise pytz.UnknownTimeZoneError('tzlocal() does not support non-zoneinfo timezones like %s. \nPlease use a timezone in the form of Continent/City')


def _get_localzone(_root = '/'):
    """Tries to find the local timezone configuration.
    
    This method prefers finding the timezone name and passing that to pytz,
    over passing in the localtime file, as in the later case the zoneinfo
    name is unknown.
    
    The parameter _root makes the function look for files like /etc/localtime
    beneath the _root directory. This is primarily used by the tests.
    In normal usage you call the function without parameters."""
    tzenv = os.environ.get('TZ')
    if tzenv:
        try:
            return _tz_from_env(tzenv)
        except pytz.UnknownTimeZoneError:
            pass

    for configfile in ('etc/timezone', 'var/db/zoneinfo'):
        tzpath = os.path.join(_root, configfile)
        if os.path.exists(tzpath):
            tzfile = os.open(tzpath, os.O_RDONLY)
            data = os.read(tzfile, 1024)
            os.close(tzfile)
            if data[:5] != 'TZif2':
                etctz = data.strip().decode()
                if ' ' in etctz:
                    etctz, dummy = etctz.split(' ', 1)
                if '#' in etctz:
                    etctz, dummy = etctz.split('#', 1)
                return pytz.timezone(etctz.replace(' ', '_'))

    zone_re = re.compile('\\s*ZONE\\s*=\\s*\"')
    timezone_re = re.compile('\\s*TIMEZONE\\s*=\\s*\"')
    end_re = re.compile('\"')
    for filename in ('etc/sysconfig/clock', 'etc/conf.d/clock'):
        tzpath = os.path.join(_root, filename)
        if not os.path.exists(tzpath):
            continue
        with open(tzpath, 'rt') as tzfile:
            data = tzfile.readlines()
        for line in data:
            match = zone_re.match(line)
            if match is None:
                match = timezone_re.match(line)
            if match is not None:
                line = line[match.end():]
                etctz = line[:end_re.search(line).start()]
                return pytz.timezone(etctz.replace(' ', '_'))

    tzpath = os.path.join(_root, 'etc/localtime')
    if os.path.exists(tzpath) and os.path.islink(tzpath):
        tzpath = os.path.realpath(tzpath)
        start = tzpath.find('/') + 1
        while start is not 0:
            tzpath = tzpath[start:]
            try:
                return pytz.timezone(tzpath)
            except pytz.UnknownTimeZoneError:
                pass

            start = tzpath.find('/') + 1

    for filename in ('etc/localtime', 'usr/local/etc/localtime'):
        tzpath = os.path.join(_root, filename)
        if not os.path.exists(tzpath):
            continue
        with open(tzpath, 'rb') as tzfile:
            return pytz.tzfile.build_tzinfo('local', tzfile)

    raise pytz.UnknownTimeZoneError('Can not find any timezone configuration')


def get_localzone():
    """Get the computers configured local timezone, if any."""
    global _cache_tz
    if _cache_tz is None:
        _cache_tz = _get_localzone()
    return _cache_tz


def reload_localzone():
    """Reload the cached localzone. You need to call this if the timezone has changed."""
    global _cache_tz
    _cache_tz = _get_localzone()
    return _cache_tz
