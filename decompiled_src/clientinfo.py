#Embedded file name: /WORKSPACE/data/entities/common/clientinfo.o
from userSoleType import UserSoleType
from userType import MemberProxy

class DummyClientInfo(object):
    pass


class ClientInfo(UserSoleType):
    harddisk = MemberProxy('harddisk')
    os_info = MemberProxy('os_info')
    cpu_info = MemberProxy('cpu_info')
    cpu_hz = MemberProxy('cpu_hz')
    cpu_num = MemberProxy('cpu_num')
    ram = MemberProxy('ram')
    gpu_info = MemberProxy('gpu_info')
    gpu_ram = MemberProxy('gpu_ram')
    mac_info = MemberProxy('mac_info')
    netdelay = MemberProxy('netdelay')
    ckey = MemberProxy('ckey')
    cpu_serial = MemberProxy('cpu_serial')
    proxy = MemberProxy('proxy')
    net_vendor = MemberProxy('net_vendor')
    ctype = MemberProxy('ctype')
    cengine = MemberProxy('cengine')
    exe64 = MemberProxy('exe64')

    def __init__(self, dict):
        super(ClientInfo, self).__init__()
        if not dict.has_key('harddisk'):
            dict['harddisk'] = ''
        if not dict.has_key('os_info'):
            dict['os_info'] = ''
        if not dict.has_key('cpu_info'):
            dict['cpu_info'] = ''
        if not dict.has_key('cpu_hz'):
            dict['cpu_hz'] = 0
        if not dict.has_key('cpu_num'):
            dict['cpu_num'] = 0
        if not dict.has_key('ram'):
            dict['ram'] = 0
        if not dict.has_key('gpu_info'):
            dict['gpu_info'] = ''
        if not dict.has_key('gpu_ram'):
            dict['gpu_ram'] = 0
        if not dict.has_key('mac_info'):
            dict['mac_info'] = ''
        if not dict.has_key('netdelay'):
            dict['netdelay'] = 0.0
        if not dict.has_key('ckey'):
            dict['ckey'] = ''
        if not dict.has_key('cpu_serial'):
            dict['cpu_serial'] = ''
        if not dict.has_key('proxy'):
            dict['proxy'] = False
        if not dict.has_key('net_vendor'):
            dict['net_vendor'] = 0
        if not dict.has_key('ctype'):
            dict['ctype'] = 0
        if not dict.has_key('cengine'):
            dict['cengine'] = ''
        if not dict.has_key('exe64'):
            dict['exe64'] = 0
        self.fixedDict = dict

    def deepcopy(self):
        return {'harddisk': self.harddisk,
         'os_info': self.os_info,
         'cpu_info': self.cpu_info,
         'cpu_hz': self.cpu_hz,
         'cpu_num': self.cpu_num,
         'ram': self.ram,
         'gpu_info': self.gpu_info,
         'gpu_ram': self.gpu_ram,
         'mac_info': self.mac_info,
         'netdelay': self.netdelay,
         'ckey': self.ckey,
         'cpu_serial': self.cpu_serial,
         'proxy': self.proxy,
         'net_vendor': self.net_vendor,
         'ctype': self.ctype,
         'cengine': self.cengine,
         'exe64': self.exe64}

    def PyFixedDict(self):
        d = DummyClientInfo()
        d.harddisk = self.fixedDict['harddisk']
        d.os_info = self.fixedDict['os_info']
        d.cpu_info = self.fixedDict['cpu_info']
        d.cpu_hz = self.fixedDict['cpu_hz']
        d.cpu_num = self.fixedDict['cpu_num']
        d.ram = self.fixedDict['ram']
        d.gpu_info = self.fixedDict['gpu_info']
        d.gpu_ram = self.fixedDict['gpu_ram']
        d.mac_info = self.fixedDict['mac_info']
        d.netdelay = self.fixedDict['netdelay']
        d.ckey = self.fixedDict['ckey']
        d.cpu_serial = self.fixedDict['cpu_serial']
        d.proxy = self.fixedDict['proxy']
        d.net_vendor = self.fixedDict['net_vendor']
        d.ctype = self.fixedDict['ctype']
        d.cengine = self.fixedDict['cengine']
        d.exe64 = self.fixedDict['exe64']
        return d
