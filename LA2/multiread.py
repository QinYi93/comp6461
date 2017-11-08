import sys
sys.path.extend(["../"])
sys.path.extend(["."])
from threading import Thread

from LA1.http import http

def test_get_file(file, self):
    h = http("http://localhost/"+file, 8080)
    h.setType('get')
    h.constructContent()
    reply = h.send()

for i in range(0, 10):
    Thread(target=test_get_file, args=("bar", i)).start()