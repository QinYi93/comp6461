# import socket
import threading
import ipaddress
import argparse
from packet import *
import packet
import rsocket as socket

def deliver_msg(recv_list):
    message = list()
    for recv in recv_list:
        message.extend(recv.payload)
    print(len(message))
    print(bytes(message).decode("utf-8"))

def handle_client(peer_ip, peer_port, route):
    print("create a new thread")
    # peer_ip = ipaddress.ip_address(socket.gethostbyname(addr[0]))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(packet.control_package(packet.SYN_ACK, peer_ip, peer_port).to_bytes(), route)
    print("send SYN-ACK")
    # sock.sendto("SYNACK".encode("ascii"), addr)
    sock.settimeout(15)
    data, route = sock.recvfrom(1024)  # buffer size is 1024 bytes
    p = packet.Packet.from_bytes(data)

    recv_list = list()
    if p.packet_type == packet.ACK:
        print("receive ACK, sequence #:"+ str(p.seq_num))
        print("Router: ", route)
        print("Packet: ", p)
        print("Payload: ", p.payload.decode("utf-8"))
        while True:
            data, route = sock.recvfrom(1024)  # buffer size is 1024 bytes
            p = packet.Packet.from_bytes(data)
            print("Router: ", route)
            print("Packet: ", p)
            # print("Payload: ", p.payload.decode("utf-8"))
            if p.seq_num % 5 == 0:
                sock.sendto(packet.control_package(packet.ACK, peer_ip, peer_port, p.seq_num).to_bytes(), route)
            else:
                sock.sendto(packet.control_package(packet.ACK, peer_ip, peer_port, p.seq_num).to_bytes(), route)
            recv_list.append(p)
            if len(p.payload) == 0:
                deliver_msg(recv_list)

def run_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind(('', port))
    while True:
        data, route = sock.recvfrom(1024)  # buffer size is 1024 bytes

        p = packet.Packet.from_bytes(data)
        print("Router: ", route)
        print("Packet: ", p)
        print("Payload: ", p.payload.decode("utf-8"))


        # print("received message:" + data.decode("utf-8") + " addr:"+str(addr))
        if p.packet_type == packet.SYN:
            print("receive SYN")
            threading.Thread(target=handle_client, args=(p.peer_ip_addr, p.peer_port, route)).start()

def handle_real_client_bak(conn, addr):
    print("create a new thread")
    recv_list = list()
    while True:
        data = conn.recvall(1024)  # buffer size is 1024 bytes
        p = packet.Packet.from_bytes(data)
        # print("Router: ", route)
        print("Packet: ", p)
        # print("Payload: ", p.payload.decode("utf-8"))
        if p.seq_num % 5 == 0:
            conn.conn.sendto(packet.control_package(packet.ACK, addr[0], addr[1], p.seq_num).to_bytes(), conn.router)
        else:
            conn.conn.sendto(packet.control_package(packet.ACK, addr[0], addr[1], p.seq_num).to_bytes(), conn.router)
        recv_list.append(p)
        if len(p.payload) == 0:
            deliver_msg(recv_list)

def handle_real_client(conn, addr):
    print("create a new thread")
    recvlist = bytearray()
    data = conn.recvall()
    recvlist.extend(data)
    # while True:
    #     data = conn.recvall()
    #     if len(data) == 0:
    #         break
    #     else:
    #         recvlist.extend(data)
    print(recvlist.decode("utf-8"))

def run_real_server(host, port):
    listener = socket.rsocket()
    try:
        listener.bind((host, port))
        listener.listen(10)
        # if args.debugging:
        print('Echo server is listening at', port)
        while True:
            conn, addr = listener.accept()
            if conn and addr:
                threading.Thread(target=handle_real_client, args=(conn, addr)).start()
    finally:
        listener.close()

parser = argparse.ArgumentParser()
parser.add_argument("--port", help="echo server port", type=int, default=8007)
args = parser.parse_args()
# run_server(args.port)
run_real_server('', args.port)