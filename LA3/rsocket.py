import unittest
import argparse
import sys
import socket
import time
import math
import logging
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

WINDOW = 10
FRAME_SIZE = 1024
RECV_TIME_OUT = 2
HANDSHAKE_TIME_OUT = 15
SLIDE_TIME = 0.1

log = logging.getLogger('ARQ')

fh = logging.FileHandler('debug.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s] >> %(message)s << %(funcName)s() %(asctime)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
log.setLevel(logging.DEBUG)
log.addHandler(fh)
log.addHandler(ch)


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
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.remote = None
        self.data = list()
        self.control = list()
        self.client_list = list()

    def handshaking(self, address, sequence):
        peer_ip = ipaddress.ip_address(socket.gethostbyname(address[0]))
        log.debug(peer_ip)
        try:
            # conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.conn.connect(self.router)
            self.conn.sendall(packet.control_package(packet.SYN, peer_ip, address[1], sequence).to_bytes())
            self.conn.settimeout(HANDSHAKE_TIME_OUT)
            data, route = self.conn.recvfrom(FRAME_SIZE)
            p = packet.Packet.from_bytes(data)
            log.debug("Router:{}".format(route))
            log.debug("Packet:{}".format(p))
            log.debug("Payload:{}".format(p.payload.decode("utf-8")))

            # conn.sendto(control_package(packet.ACK, p.peer_ip_addr, p.peer_port, sequence), self.router)

            self.conn.sendall(packet.control_package(packet.ACK, p.peer_ip_addr, p.peer_port, sequence).to_bytes())
            return (p.peer_ip_addr, p.peer_port)

        except Exception as e:
            log.error(e)
            raise HandShakeException("Hand Shaking " + e.__str__())

    def connect(self, address):

        try:
            self.remote = self.handshaking(address, self.sequence)
            self.sequence = packet.grow_sequence(self.sequence, 1)
        except HandShakeException as e:
            log.error(e)
            raise e

    def findIndex(self, window, se):
        for i in range(0, len(window)):
            if window[i] == se:
                return i

    def sendall(self, data):
        index = 0
        timer = None
        # mapping = {}
        log.debug("init send sequence#:{}".format(self.sequence))
        window = [-i for i in range(1, WINDOW+1)]
        for i in range(0, WINDOW):
            window[i] = -int(packet.grow_sequence(self.sequence, i))
        package, self.sequence = packet.data_package(self.remote[0], self.remote[1], data, self.sequence)
        # for pack in package:
        #     self.conn.sendall(pack.to_bytes())
        # compare_window = window.copy()
        timeout = [False, False]
        log.debug("init widow:{}".format(window))
        while len(package) != 0:
            log.debug("plus stop package, {} package waiting for send:".format(len(package)))
            #send new package
            for i in range(0, len(window)):
                if window[i] < 0: # new window slot
                    if (i - index + WINDOW) % WINDOW < len(package):
                        p = package[(i - index + WINDOW) % WINDOW]
                        # if not window[i] + p.seq_num == 0:
                        #     print(window, p.seq_num)
                        #     print(compare_window)
                        #     raise Exception("sequence number wrong!")
                        log.debug("send {} slot, slot value is {}, package #{}".format(i, window[i], p.seq_num))
                        if window[i] + p.seq_num == 0:
                            window[i] = -window[i]
                            # mapping[window[i]] = i
                            self.conn.sendall(p.to_bytes())
                            log.debug("sending new package:{}".format(p))
                        else:
                            log.debug("skip slot {} belongs to future".format(i))
            compare_window = window.copy()
            # self.conn.settimeout(RECV_TIME_OUT)
            def out(timeout):
                log.debug("receive time out")
                # print(timeout)
                timeout[0] = True
                timeout[1] = False
                # print(timeout)

            if not timeout[1]:
                timer = Timer(RECV_TIME_OUT, out, [timeout])
                timer.start()
                timeout[1] = True
            log.debug("\nafter send, widow:{}".format(window))
            log.debug("receive from remote")
            while True:
                self.conn.settimeout(SLIDE_TIME)
                # compare_window = window.copy()
                try:
                    data, route = self.conn.recvfrom(1024)  # buffer size is 1024 bytes
                    p = packet.Packet.from_bytes(data)
                    log.debug("Recv:{}".format(p))
                    if p.packet_type == packet.DATA:
                        log.debug("cache data package")
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
                        if p.seq_num in window:#mapping.keys():
                            window_index = self.findIndex(window, p.seq_num)#mapping.pop(p.seq_num)
                            log.debug("recv ACK {} for slot {}".format(p.seq_num, window_index))
                            if not window[window_index] - p.seq_num == 0:
                                raise Exception("sequence number wrong! slot {} expect {}, but got {}".format(window_index, window[window_index], p.seq_num))
                            log.debug("old window:{}".format(window))
                            window[window_index] = -int(packet.grow_sequence(p.seq_num, WINDOW))
                            log.debug("new window:{}".format(window))
                        else:
                            log.debug("recv ACK {} but not belongs any window slot, drop!".format(p.seq_num))
                    elif p.packet_type == packet.NAK:
                        if p.seq_num in window:#mapping.keys():
                            window_index = self.findIndex(window, p.seq_num)#mapping.pop(p.seq_num)
                            log.debug("recv NAK {} for lot {}".format(p.seq_num, window_index))
                            if not window[window_index] - p.seq_num == 0:
                                raise Exception(
                                    "sequence number wrong! slot {} expect {}, but got {}".format(window_index,
                                                                                                  window[window_index],
                                                                                                  p.seq_num))
                            log.debug("old window:{}".format(window))
                            window[window_index] = -int(p.seq_num)
                            log.debug("new window:{}".format(window))
                        else:
                            log.debug("recv NAK {} but not belongs any window slot, drop!".format(p.seq_num))
                    else:
                        print("UFO")
                except socket.timeout:
                    log.debug("slide window")
                    break

            index, package, window = self.slide_window(compare_window, package, window)
            if not timeout[0]:
                continue
            if(len(package) != 0):
                for i in range(0, len(window)):
                    if window[i] > 0:
                        if (i - index + WINDOW) % WINDOW < len(package):
                            p = package[(i - index + WINDOW) % WINDOW]
                            log.debug("resend {} slot, slot value is {}, package #{}".format(i, window[i], p.seq_num))
                            # if not window[i] == p.seq_num:
                            #     print(window, p.seq_num)
                            #     raise Exception("sequence number wrong!")
                            # window[i] = -window[i]
                            if window[i] == p.seq_num:
                                p = package[(i - index + WINDOW) % WINDOW]
                                self.conn.sendall(p.to_bytes())
                                log.debug("sending new package:{}".format(p))
                            else:
                                log.debug("skip slot {} belongs to future".format(i))
                # print(window)
            else:
                log.debug("All the package send out!")

        timer.cancel()
    def slide_window(self, compare_window, package, window):
        log.debug("\ncompare with original window")
        log.debug("NEW:{}".format(window))
        log.debug("ORI:{}".format(compare_window))
        log.debug("start slide window")
        new_window = window.copy()
        index = WINDOW
        for i in range(0, len(window)):
            if window[i] + compare_window[i] == 0 or window[i] == compare_window[i]:
                index = i
                log.debug("find the most old slot {}".format(i))
                break
            else:
                log.debug("slot {} send success, slide one".format(i))
                new_window.append(new_window.pop(0))
        # print(index)
        log.debug("total package length:{}".format(len(package)))
        if not index == 0:
            package = package[index:]
        log.debug("rest package length:{}".format(len(package)))
        # move window
        # print(new_window)
        window = new_window
        log.debug("new window:{}".format(window))
        index = 0
        # assert ()
        if index + 1 == WINDOW:
            index = (index + 1) % WINDOW
        # if index == WINDOW -1:
        #     index = -1
        return index, package, window

    def recv_data_package(self, packet):
        index = 0
        timer = None
        # mapping = {}
        # log.debug("init recv sequence#:{}".format(self.sequence))
        # window = [-i for i in range(1, WINDOW + 1)]
        # for i in range(0, WINDOW):
        #     window[i] = -int(packet.grow_sequence(self.sequence, i))

    def recv_control_package(self, packet):
        self.control.append(packet)

    def recvall(self):#, buffersize):
        index = 0
        timer = None
        # mapping = {}
        cache = bytearray()
        log.debug("init recv sequence#:{}".format(self.sequence))
        window = [-i for i in range(1, WINDOW + 1)]
        for i in range(0, WINDOW):
            window[i] = int(packet.grow_sequence(self.sequence, i))

        while True:
            while (isinstance(window[0], packet.Packet)):
                peek = window[0]
                if len(peek.payload) == 0:
                    log.debug("pop terminate packet, se#{}".format(peek.seq_num))
                    self.sequence = packet.grow_sequence(p.seq_num, 1)
                    return cache
                p = window.pop(0)
                self.sequence = packet.grow_sequence(p.seq_num, 1)
                log.debug("pop first slot, se#{}".format(p.seq_num))
                last = window[len(window) - 1]
                if isinstance(last, packet.Packet):
                    window.append(packet.grow_sequence(last.seq_num, 1))
                else:
                    window.append(packet.grow_sequence(last, 1))
                cache.extend(p.payload)

                # if len(cache) >= buffersize:
                #     data = cache[:buffersize]
                #     cache = cache[buffersize:]
                #     return data
            if len(cache) > 0:
                return cache
            data = self.conn.recv(FRAME_SIZE)
            p = packet.Packet.from_bytes(data)
            # print("Router: ", route)
            log.debug("Packet: {}".format(p))
            # print("Payload: ", p.payload.decode("utf-8"))

            # print("received message:" + data.decode("utf-8") + " addr:"+str(addr))
            if not (p.peer_ip_addr == self.remote[0] and p.peer_port == self.remote[1]):
                log.debug("recv bad data from {}:{}".format(p.peer_ip_addr, p.peer_port))
                continue
            if not p.packet_type == packet.DATA:
                log.debug("recv control packet, cache")
                self.recv_control_package(p)
            else:
                if p.seq_num in window:
                    window_index = self.findIndex(window, p.seq_num)
                    window[window_index] = p
                    log.debug("slot {} recv data se#{}".format(window_index, p.seq_num))
                    self.conn.sendall(packet.control_package(packet.ACK, self.remote[0], self.remote[1], p.seq_num).to_bytes())

                else:
                    # if not possible to recv future expect se#
                    log.debug("recv out of expect se#{}".format(p.seq_num))
                    self.conn.sendall(packet.control_package(packet.ACK, self.remote[0], self.remote[1], p.seq_num).to_bytes())
        # return self.conn.recv(buffersize)

    def bind(self, address):
        self.conn.bind(address)

    def listen(self, max):
        # self.conn.listen(max)
        self.MAX = max

    def accept(self):
        try:
            data, route = self.conn.recvfrom(1024)  # buffer size is 1024 bytes

            p = packet.Packet.from_bytes(data)
            print("Router: ", route)
            print("Packet: ", p)
            print("Payload: ", p.payload.decode("utf-8"))
            if len(self.client_list) > self.MAX:
                return None, None
            if p.packet_type == packet.SYN:
                return self.accept_client(p)
        except socket.timeout as e:
            log.error(e)
            return None, None

    def accept_client(self, p):
        print("create a new thread")
        # peer_ip = ipaddress.ip_address(socket.gethostbyname(addr[0]))
        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock = rsocket()
        sock.conn.sendto(packet.control_package(packet.SYN_ACK, p.peer_ip_addr, p.peer_port, p.seq_num).to_bytes(), self.router)
        print("send SYN-ACK")
        # sock.sendto("SYNACK".encode("ascii"), addr)
        # sock.settimeout(15)
        data = sock.conn.recv(1024)  # buffer size is 1024 bytes
        p = packet.Packet.from_bytes(data)

        recv_list = list()
        if p.packet_type == packet.ACK:
            sock.sequence = packet.grow_sequence(p.seq_num, 1)
            sock.remote = (p.peer_ip_addr, p.peer_port)
            sock.conn.connect(self.router)
            print("receive ACK, sequence #:" + str(p.seq_num))
            # print("Router: ", route)
            print("Packet: ", p)
            print("Payload: ", p.payload.decode("utf-8"))
            return sock, (p.peer_ip_addr, p.peer_port)
        return None, None
            # while True:
            #     data, route = sock.recvfrom(1024)  # buffer size is 1024 bytes
            #     p = Packet.from_bytes(data)
            #     print("Router: ", route)
            #     print("Packet: ", p)
            #     # print("Payload: ", p.payload.decode("utf-8"))
            #     if p.seq_num % 5 == 0:
            #         sock.sendto(packet.control_package(packet.ACK, peer_ip, peer_port, p.seq_num).to_bytes(), route)
            #     else:
            #         sock.sendto(packet.control_package(packet.ACK, peer_ip, peer_port, p.seq_num).to_bytes(), route)
            #     recv_list.append(p)
            #     if len(p.payload) == 0:
            #         deliver_msg(recv_list)

    def close(self):  # real signature unknown; restored from __doc__
        """
        close()

        Close the socket.  It cannot be used after this call.
        """
        self.conn.close()
        for c in self.client_list:
            c.close()

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

if __name__ == '__main__':
    unittest.main()