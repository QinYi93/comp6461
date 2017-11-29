import argparse
import math
import sys
sys.path.extend(["./"])
import LA3.rsocket as socket
from numpy import uint32



def run_client(router_addr, router_port, server_addr, server_port):
    content = """accept() -> (socket object, address info)
        我爱北京天安门，天安门上太阳升
        Wait for an incoming connection.  Return a new socket
        representing the connection, and the address of the client.
        For IP sockets, the address info is a pair (hostaddr, port)
        """
    conn = socket.rsocket((router_addr, router_port), 4294967295-8)
    conn.connect((server_addr, server_port))
    conn.sendall(content.encode("utf-8"))
    # conn.sendall(content)

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
