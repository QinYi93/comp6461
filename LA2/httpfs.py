import socket
import threading
import argparse
import os
import json
import pathlib
from lockfile import LockFile
from http import http

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
    if args.debugging:
        print('Handle New client from', addr)
    try:
        while True:
            data = conn.recv(2048)
            data = data.decode("utf-8")
            if not data:
                break
            (method, path, body, headers) = parseRequest(data)
            if args.debugging:
                print(method, path, body, headers)
            if ".." in path:
                if args.debugging:
                    print("Access Denied", path)
                r = http(400, "Access Denied")
            else:
                if not dir.endswith("/"):
                    dir = dir + "/"
                if not dir.startswith("./"):
                    dir = "./" + dir
                path = (dir + path).replace("//", "/")
                # print(path)
                if method == "GET":
                    if path.endswith("/"):
                        if args.debugging:
                            print("GET Directory", path)
                        files = os.listdir(path)
                        # print(files)
                        r = http(200, json.dumps(files))
                        r.addHeader("Content-Type", "application/json")
                    else:
                        if args.debugging:
                            print("GET File", path)
                        if os.path.exists(path):
                            with open(path, 'r') as f:
                                content = f.read()
                            r = http(200, content)
                        else:
                            r = http(404, "")
                elif method == "POST":
                    try:
                        if args.debugging:
                            print("POST File", path)
                        pathlib.Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
                        lock = LockFile(path)
                        lock.acquire()
                        print(os.path.basename(path), " Content", body)
                        with open(path, 'a+') as f:
                            f.write(body+"\n")
                        lock.release()
                        r = http(200, "")
                    except OSError as e:
                        if args.debugging:
                            print(e)
                        r = http(400, e.strerror)
                else:
                    r = http(400, "")
            if args.debugging:
                print(r.toString())
            conn.sendall(r.toString().encode('ascii'))
            break

    finally:
        conn.close()

def parseRequest(data):
    (head, body) = data.split("\r\n\r\n")
    headArray = head.split("\r\n")
    line1 = headArray.pop(0).split()
    # if line1[1] == '200':
    method = line1[0]
    path = line1[1]
    protocol = line1[2]
    # print("\n====>Status:" + " ".join(line1[2:]) + "  Code:" + line1[1])
    headMap = {}
    for key in headArray:
        keyValue = key.split(":")
        headMap[keyValue[0]] = keyValue[1].strip()

    return method, path, body, headMap

parser = argparse.ArgumentParser(description='Socket based HTTP fileserver')
parser.add_argument("-p", action="store", dest="port", help="Set server port", type=int, default=8080)
parser.add_argument("-v", action="store_true", dest="debugging", help="Echo debugging mesages", default=False)
parser.add_argument("-d", action="store", dest="directory", help="Set directory path", default='./')

args = parser.parse_args()

run_server('', args.port, args.directory)