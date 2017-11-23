import unittest
import argparse
import sys
import socket
import time
import math
from numpy import uint32
import numpy as np
from threading import Timer

import ipaddress
# sys.path.extend(["."])
# from packet import *
import packet

# import __socket
# from _socket import *

# sys.path.extend(["../"])

WINDOW = 1

class TestSocketMethods(unittest.TestCase):
    def test_send(self):
        return

class HandShakeException(Exception):
    pass

class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class rsocket():#__socket.socket):

    def __init__(self, router=('localhost', 3000), sequence = 0):
        self.router = router
        self.sequence = uint32(sequence)
        self.conn = None
        self.remote = None
        self.data = None

    def handshaking(self, address, sequence):
        peer_ip = ipaddress.ip_address(socket.gethostbyname(address[0]))
        print(peer_ip)
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            conn.connect(self.router)
            conn.sendall(packet.control_package(packet.SYN, peer_ip, address[1], sequence).to_bytes())
            conn.settimeout(5)
            data, route = conn.recvfrom(1024)
            p = packet.Packet.from_bytes(data)
            print("Router: ", route)
            print("Packet: ", p)
            print("Payload: ", p.payload.decode("utf-8"))

            # conn.sendto(control_package(packet.ACK, p.peer_ip_addr, p.peer_port, sequence), self.router)

            conn.sendall(packet.control_package(packet.ACK, p.peer_ip_addr, p.peer_port, sequence).to_bytes())
            return conn, (p.peer_ip_addr, p.peer_port)

        except Exception as e:
            print(e)
            raise HandShakeException("Hand Shaking " + e.__str__())

    def connect(self, address):

        try:
            self.conn, self.remote = self.handshaking(address, self.sequence)
            self.sequence = packet.grow_sequence(self.sequence, 1)
        except HandShakeException as e:
            print(e)
            raise e


    def sendall(self, data):
        index = 0
        print(self.sequence)
        # window = np.array([-i for i in range(1, 11)], dtype='int64')
        window = [-i for i in range(1, WINDOW+1)]
        print(window)
        for i in range(0, WINDOW):
            window[i] = -int(packet.grow_sequence(self.sequence, i))
        # window = list()
        # window.extend([-i for i in range(self.sequence, self.sequence+WINDOW)])
        print(window)
        # assert()
        package, self.sequence = packet.data_package(self.remote[0], self.remote[1], data, self.sequence)
        # for pack in package:
        #     self.conn.sendall(pack.to_bytes())
        mapping = {}
        compare_window = window.copy()
        while len(package) != 0:
            print("package length:", len(package))
            timeout = [False]
            #send new package
            for i in range(0, len(window)):
                if window[i] < 0:
                    if (i - index + WINDOW) % WINDOW < len(package):
                        p = package[(i - index + WINDOW) % WINDOW]
                        # if not window[i] + p.seq_num == 0:
                        #     print(window, p.seq_num)
                        #     print(compare_window)
                        #     raise Exception("sequence number wrong!")
                        if window[i] + p.seq_num == 0:
                            window[i] = -window[i]
                            mapping[window[i]] = i
                            self.conn.sendall(p.to_bytes())
                            # if i <= index:
                            #     self.conn.sendall(package[WINDOW-1-index+i].to_bytes())
                            # else:
                            #     self.conn.sendall(package[i-1-index].to_bytes())
                            print("send package:{}".format(p))
            compare_window = window.copy()

            def out(timeout):
                print("receive time out")
                print(timeout)
                timeout[0] = True
                print(timeout)

            t = Timer(1, out, [timeout])
            # t.start()
            print(window)
            while not timeout[0]:
                print("receive NAK/ACK")
                try:
                    data, route = self.conn.recvfrom(1024)  # buffer size is 1024 bytes
                    p = packet.Packet.from_bytes(data)
                    print("Recv:{}".format(p))
                    if p.packet_type == packet.DATA:
                        self.data.append(p)
                    elif p.packet_type == packet.ACK:
                        # o_se = window[index]
                        # if index >= 0:
                        #     o_se = window[index]
                        # else:
                        #     o_se = window[0]
                        # print(o_se)
                        # window_index = p.seq_num - o_se
                        # print(window_index)
                        # window_index = (window_index+index) % WINDOW
                        # print(window_index)
                        if p.seq_num in mapping.keys():
                            window_index = mapping.pop(p.seq_num)
                            if not window[window_index] - p.seq_num == 0:
                                raise Exception("sequence number wrong!")
                            window[window_index] = -int(packet.grow_sequence(p.seq_num, WINDOW))
                    elif p.packet_type == packet.NAK:
                        if p.seq_num in mapping.keys():
                            window_index = mapping.pop(p.seq_num)
                            if not window[window_index] - p.seq_num == 0:
                                raise Exception("sequence number wrong!")
                            window[window_index] = -p.seq_num
                    else:
                        print("UFO")
                except socket.timeout:
                    timeout[0] = True
            print(window)
            print("compare_window")
            print(compare_window)
            for i in range(0, len(window)):
                if window[i] + compare_window[i] == 0:
                    index = i
                    break
            print(index)
            print(len(package))
            if not index == 0:
                package = package[index:]
            print(len(package))
                # assert ()
            if index+1 == WINDOW:
                index = (index + 1) % WINDOW
            # if index == WINDOW -1:
            #     index = -1
            if(len(package) != 0):
                for i in range(0, len(window)):
                    if window[i] > 0:
                        if (i - index + WINDOW) % WINDOW < len(package):
                            p = package[(i - index + WINDOW) % WINDOW]
                            # if not window[i] == p.seq_num:
                            #     print(window, p.seq_num)
                            #     raise Exception("sequence number wrong!")
                            # window[i] = -window[i]
                            if window[i] == p.seq_num:
                                p = package[(i - index + WINDOW) % WINDOW]
                                self.conn.sendall(p.to_bytes())
                                print("send package:{}".format(p))
                print(window)

    def bind(self, address):  # real signature unknown; restored from __doc__
        """
        bind(address)

        Bind the socket to a local address.  For IP sockets, the address is a
        pair (host, port); the host must refer to the local host. For raw packet
        sockets the address is a tuple (ifname, proto [,pkttype [,hatype]])
        """
        pass

    def listen(self, backlog=None):  # real signature unknown; restored from __doc__
        """
        listen([backlog])

        Enable a server to accept connections.  If backlog is specified, it must be
        at least 0 (if it is lower, it is set to 0); it specifies the number of
        unaccepted connections that the system will allow before refusing new
        connections. If not specified, a default reasonable value is chosen.
        """
        pass

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

    def close(self):  # real signature unknown; restored from __doc__
        """
        close()

        Close the socket.  It cannot be used after this call.
        """
        self.conn.close()

    def packageContent(self, type, sequence, ip, port, content):
        #  1        4       4     2        1013
        #------------------------------------------
        # type | sequence | ip | port | sub-content
        return []

class handshake():



    def ack_package(self):
        return "ACK".encode("ascii")

    def nak_package(self):
        return "NAK".encode("ascii")

def run_client(router_addr, router_port, server_addr, server_port):
    content = """accept() -> (socket object, address info)
        我爱北京天安门，天安门上太阳升
        Wait for an incoming connection.  Return a new socket
        representing the connection, and the address of the client.
        For IP sockets, the address info is a pair (hostaddr, port)
        """
    conn = rsocket((router_addr, router_port), 4294967295-8)
    conn.connect((server_addr, server_port))
    conn.sendall(content)

    se = uint32(4294967295)
    se = uint32(se) + uint32(1)
    print(se)


# Usage:
# python echoclient.py --routerhost localhost --routerport 3000 --serverhost localhost --serverport 8007

parser = argparse.ArgumentParser()
parser.add_argument("--routerhost", help="router host", default="localhost")
parser.add_argument("--routerport", help="router port", type=int, default=3000)

parser.add_argument("--serverhost", help="server host", default="localhost")
parser.add_argument("--serverport", help="server port", type=int, default=8007)

parser.add_argument("--windowsize", help="window size", type=int, default=10)
args = parser.parse_args()

if args.windowsize > math.pow(2, 31):
    raise Exception("window size too large")
WINDOW = args.windowsize

run_client(args.routerhost, args.routerport, args.serverhost, args.serverport)


if __name__ == '__main__':
    unittest.main()