import socket
import threading
import argparse
import os
import json
import pathlib
from lockfile import LockFile
from http import http
import magic

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
            (method, path, query, body, headers) = parseRequest(data)
            if args.debugging:
                print(method, path, body, headers)
            if ".." in path:
                if args.debugging:
                    print("Access Denied", path)
                r = http(400, "Access Denied".encode("ascii"))
            else:
                if not dir.endswith("/"):
                    dir = dir + "/"
                # if not dir.startswith("./"):
                #     dir = "./" + dir
                path = (dir + path).replace("//", "/")
                # print(path)
                if method == "GET":
                    try:
                        if path.endswith("/"):
                            if args.debugging:
                                print("GET Directory", path)
                            files = os.listdir(path)
                            # print(files)
                            r = http(200, json.dumps(files).encode("ascii"))
                            r.addHeader("Content-Type", "application/json")
                        else:
                            if os.path.exists(path):
                                if args.debugging:
                                    print("FIND File", path)
                                r = http(200, "")

                                kind = magic.from_file(path, mime=True)
                                r.addHeader("Content-Type", kind)
                                if "text" in kind:
                                    with open(path, 'r') as f:
                                        content = f.read()
                                        r.setContent(content.encode("ascii"))
                                else:
                                    with open(path, 'rb') as f:
                                        content = f.read()
                                        r.setContent(content)

                                if "Content-disposition" in headers:
                                    r.addHeader("Content-disposition", headers["Content-disposition"])
                                elif "inline" in query:
                                    r.addHeader("Content-disposition", "inline")
                                else:
                                    r.addHeader("Content-disposition", "attachment")
                            else:
                                r = http(404, "".encode("ascii"))
                    except OSError as e:
                        if args.debugging:
                            print(e)
                        r = http(400, e.strerror)
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
                        r = http(200, "".encode("ascii"))
                    except OSError as e:
                        if args.debugging:
                            print(e)
                        r = http(400, e.strerror)
                else:
                    r = http(400, "")
            if args.debugging:
                print(r.headToString())
            conn.sendall(r.headToString().encode("ascii"))
            conn.sendall(r.getBody())
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
    query = ""
    if "?" in path:
        path, query = path.split("?")
    elif "&" in path:
        path, query = path.split("&")

    protocol = line1[2]
    # print("\n====>Status:" + " ".join(line1[2:]) + "  Code:" + line1[1])
    headMap = {}
    for key in headArray:
        keyValue = key.split(":")
        headMap[keyValue[0]] = keyValue[1].strip()

    return method, path, query, body, headMap

parser = argparse.ArgumentParser(description='Socket based HTTP fileserver')
parser.add_argument("-p", action="store", dest="port", help="Set server port", type=int, default=8080)
parser.add_argument("-v", action="store_true", dest="debugging", help="Echo debugging mesages", default=False)
parser.add_argument("-d", action="store", dest="directory", help="Set directory path", default='./')

args = parser.parse_args()

run_server('', args.port, args.directory)