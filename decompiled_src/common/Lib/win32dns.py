#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib/win32dns.o
"""
 $Id: win32dns.py,v 1.3.2.1 2007/05/22 20:26:49 customdesigned Exp $

 Extract a list of TCP/IP name servers from the registry 0.1
    0.1 Strobl 2001-07-19
 Usage:
    RegistryResolve() returns a list of ip numbers (dotted quads), by
    scouring the registry for addresses of name servers

 Tested on Windows NT4 Server SP6a, Windows 2000 Pro SP2 and
 Whistler Pro (XP) Build 2462 and Windows ME
 ... all having a different registry layout wrt name servers :-/

 Todo:

   Program doesn't check whether an interface is up or down

 (c) 2001 Copyright by Wolfgang Strobl ws@mystrobl.de,
          License analog to the current Python license
"""
import string, re
import _winreg

def binipdisplay(s):
    """convert a binary array of ip adresses to a python list"""
    if len(s) % 4 != 0:
        raise EnvironmentError
    ol = []
    for i in range(len(s) / 4):
        s1 = s[:4]
        s = s[4:]
        ip = []
        for j in s1:
            ip.append(str(ord(j)))

        ol.append(string.join(ip, '.'))

    return ol


def stringdisplay(s):
    """convert "d.d.d.d,d.d.d.d" to ["d.d.d.d","d.d.d.d"].
       also handle u'd.d.d.d d.d.d.d', as reporting on SF 
    """
    import re
    return map(str, re.split('[ ,]', s))


def RegistryResolve():
    nameservers = []
    x = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
    try:
        y = _winreg.OpenKey(x, 'SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters')
    except EnvironmentError:
        try:
            y = _winreg.OpenKey(x, 'SYSTEM\\CurrentControlSet\\Services\\VxD\\MSTCP')
            nameserver, dummytype = _winreg.QueryValueEx(y, 'NameServer')
            if nameserver and nameserver not in nameservers:
                nameservers.extend(stringdisplay(nameserver))
        except EnvironmentError:
            pass

        return nameservers

    try:
        nameserver = _winreg.QueryValueEx(y, 'DhcpNameServer')[0].split()
    except:
        nameserver = _winreg.QueryValueEx(y, 'NameServer')[0].split()

    if nameserver:
        nameservers = nameserver
    nameserver = _winreg.QueryValueEx(y, 'NameServer')[0]
    _winreg.CloseKey(y)
    try:
        y = _winreg.OpenKey(x, 'SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\DNSRegisteredAdapters')
        for i in range(1000):
            try:
                n = _winreg.EnumKey(y, i)
                z = _winreg.OpenKey(y, n)
                dnscount, dnscounttype = _winreg.QueryValueEx(z, 'DNSServerAddressCount')
                dnsvalues, dnsvaluestype = _winreg.QueryValueEx(z, 'DNSServerAddresses')
                nameservers.extend(binipdisplay(dnsvalues))
                _winreg.CloseKey(z)
            except EnvironmentError:
                break

        _winreg.CloseKey(y)
    except EnvironmentError:
        pass

    try:
        y = _winreg.OpenKey(x, 'SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces')
        for i in range(1000):
            try:
                n = _winreg.EnumKey(y, i)
                z = _winreg.OpenKey(y, n)
                try:
                    nameserver, dummytype = _winreg.QueryValueEx(z, 'NameServer')
                    if nameserver and nameserver not in nameservers:
                        nameservers.extend(stringdisplay(nameserver))
                except EnvironmentError:
                    pass

                _winreg.CloseKey(z)
            except EnvironmentError:
                break

        _winreg.CloseKey(y)
    except EnvironmentError:
        pass

    _winreg.CloseKey(x)
    return nameservers


if __name__ == '__main__':
    print 'Name servers:', RegistryResolve()
