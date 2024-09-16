#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\gt/gtDispatcher.o
import asyncore
import socket
import ssl
import select
from StringIO import StringIO

class dispatcher(asyncore.dispatcher):
    RECV_BUFFER = 4096
    ST_INIT = 0
    ST_ESTABLISHED = 1
    ST_HANDSHAKE = 2

    def __init__(self, channel_interface_obj, accept_connection = None):
        print 'dispatcher.__init__'
        if accept_connection:
            asyncore.dispatcher.__init__(self, accept_connection)
            self.status = dispatcher.ST_ESTABLISHED
        else:
            asyncore.dispatcher.__init__(self)
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.status = dispatcher.ST_INIT
        print 'dispatcher.__init__ set SO_KEEPALIVE'
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.socket.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
        if hasattr(socket, 'TCP_KEEPCNT') and hasattr(socket, 'TCP_KEEPIDLE') and hasattr(socket, 'TCP_KEEPINTVL'):
            print 'dispatcher.__init__ set TCP_KEEPCNT'
            self.socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 3)
            print 'dispatcher.__init__ set TCP_KEEPIDLE'
            self.socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 60)
            print 'dispatcher.__init__ set TCP_KEEPINTVL'
            self.socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 60)
        self.recv_buffer_size = self.RECV_BUFFER
        self.w_buffer = StringIO()
        self.channel_interface_obj = channel_interface_obj

    def set_buffer(self, size):
        self.recv_buffer_size = size

    def set_socket_buffer(self, recv_buffer_size, send_buffer_size):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buffer_size)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, send_buffer_size)

    def disconnect(self):
        self.close()
        self.w_buffer = StringIO()
        self.status = dispatcher.ST_INIT
        if self.channel_interface_obj:
            self.channel_interface_obj.on_disconnected()
        self.channel_interface_obj = None

    def handle_connect(self):
        print 'dispatcher.handle_connect'
        self.status = dispatcher.ST_ESTABLISHED
        if self.channel_interface_obj:
            self.channel_interface_obj.on_connected()

    def handle_close(self):
        print 'dispatcher.handle_close'
        self.disconnect()

    def handle_expt(self):
        print 'dispatcher.handle_expt'
        self.disconnect()

    def handle_error(self):
        print 'dispatcher.handle_error'
        asyncore.dispatcher.handle_error(self)
        self.disconnect()

    def handle_read(self):
        data = self.recv(self.recv_buffer_size)
        if data:
            rc = self.channel_interface_obj.input_data(data)
            if rc == 2:
                return
            elif rc == 0:
                self.disconnect()
                return
            else:
                assert 0
                self.disconnect()
                return

    def handle_write(self):
        buff = self.w_buffer.getvalue()
        if buff:
            sent = self.send(buff)
            self.w_buffer = StringIO(buff[sent:])
            self.w_buffer.seek(0, 2)

    def send_data(self, data):
        self.w_buffer.write(data)

    def writable(self):
        return self.w_buffer.getvalue() or self.status == dispatcher.ST_INIT


class dispatcher_ssl(dispatcher):

    def __init__(self, certfile, channel_interface_obj, accept_connection = None):
        print 'dispatcher_ssl.__init__'
        dispatcher.__init__(self, channel_interface_obj, accept_connection=accept_connection)
        self.handshake_count = 0
        self.handshake_status = 0
        self.certfile = certfile

    def disconnect(self):
        self.close()
        self.w_buffer = StringIO()
        self.status = dispatcher.ST_INIT
        if self.channel_interface_obj:
            self.channel_interface_obj.on_disconnected()
        self.channel_interface_obj = None
        self.handshake_count = 0
        self.handshake_status = 0

    def handle_connect(self):
        print 'dispatcher_ssl.handle_connect'
        self.socket = ssl.wrap_socket(self.socket, ca_certs=self.certfile, cert_reqs=ssl.CERT_REQUIRED, do_handshake_on_connect=False)
        self.status = dispatcher.ST_HANDSHAKE
        self._handshake()

    def _handshake(self):
        try:
            self.handshake_count += 1
            self.socket.do_handshake()
            self.handshake_status = 0
            self.on_handshaked()
        except ssl.SSLError as err:
            if err.args[0] == ssl.SSL_ERROR_WANT_READ:
                self.handshake_status = ssl.SSL_ERROR_WANT_READ
            elif err.args[0] == ssl.SSL_ERROR_WANT_WRITE:
                self.handshake_status = ssl.SSL_ERROR_WANT_WRITE
            else:
                raise

    def handle_handshake(self):
        if self.handshake_status == ssl.SSL_ERROR_WANT_READ:
            select.select([self.socket], [], [], 0)
        elif self.handshake_status == ssl.SSL_ERROR_WANT_WRITE:
            select.select([], [self.socket], [], 0)
        else:
            raise RuntimeError('bad handshake_status')
        self._handshake()

    def on_handshaked(self):
        print 'dispatcher_ssl.on_handshaked', self.handshake_count
        if self.channel_interface_obj:
            self.channel_interface_obj.on_handshaked()
        self.status = dispatcher.ST_ESTABLISHED

    def readable(self):
        if self.status == dispatcher.ST_HANDSHAKE:
            self.handle_handshake()
            return False
        if isinstance(self.socket, ssl.SSLSocket):
            while self.socket.pending() > 0:
                self.handle_read_event()

        return True
