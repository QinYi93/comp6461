import unittest
import sys
import _socket
from _socket import *

# sys.path.extend(["../"])

class TestSocketMethods(unittest.TestCase):
    def test_send(self):
        return

class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class socket(_socket.socket):
    def __init__(self):
        return

    def accept(self):
        """accept() -> (socket object, address info)

        Wait for an incoming connection.  Return a new socket
        representing the connection, and the address of the client.
        For IP sockets, the address info is a pair (hostaddr, port).
        """
        # fd, addr = self._accept()
        # # If our type has the SOCK_NONBLOCK flag, we shouldn't pass it onto the
        # # new socket. We do not currently allow passing SOCK_NONBLOCK to
        # # accept4, so the returned socket is always blocking.
        # type = self.type & ~globals().get("SOCK_NONBLOCK", 0)
        # sock = socket(self.family, type, self.proto, fileno=fd)
        # # Issue #7995: if no default timeout is set and the listening
        # # socket had a (non-zero) timeout, force the new socket in blocking
        # # mode to override platform-specific socket flags inheritance.
        # if getdefaulttimeout() is None and self.gettimeout():
        #     sock.setblocking(True)
        return #sock, addr

    def close(self):
        return

    def packageContent(self, type, sequence, ip, port, content):
        #  1        4       4     2        1013
        #------------------------------------------
        # type | sequence | ip | port | sub-content
        return []

class handshake():
    def SYNpackage(self, sequence):
        return

    def SYNACKpackage(self):
        return

    def ACKpackage(self):
        return

    def NAKpackage(self):
        return

if __name__ == '__main__':
    unittest.main()