import socket
import threading
import argparse

def run_server(host, port, dir):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((host, port))
        listener.listen(5)
        if args.debugging:
            print('Echo server is listening at', port)
        while True:
            conn, addr = listener.accept()
            threading.Thread(target=handle_client, args=(conn, addr, dir)).start()
    finally:
        listener.close()

def handle_client(conn, addr, dir):
    print(conn, addr, dir)

parser = argparse.ArgumentParser(description='Socket based HTTP fileserver')
parser.add_argument("-p", action="store", dest="port", help="Set server port", type=int, default=8080)
parser.add_argument("-v", action="store_true", dest="debugging", help="Echo debugging mesages", default=False)
parser.add_argument("-d", action="store", dest="directory", help="Set directory path", default='/')

args = parser.parse_args()

run_server('', args.port, args.directory)