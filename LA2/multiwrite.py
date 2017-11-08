import sys
sys.path.extend(["../"])
sys.path.extend(["."])
from threading import Thread

from LA1.http import http


def test_post_request_multi(file, index):
    body = str(index)
    h = http("http://localhost/"+file, 8080)
    h.setType('post')
    h.setData(body)
    h.addHeader("Content-Type", "application/json")
    h.addHeader("Content-Length", str(len(body)))
    h.constructContent()
    reply = h.send()

for i in range(0, 10):
    Thread(target=test_post_request_multi, args=("bar", i)).start()
    # Thread(target=test_post_request_multi, args=("bar1", i)).start()
    # Thread(target=test_post_request_multi, args=("bar2", i)).start()
    # Thread(target=test_post_request_multi, args=("bar3", i)).start()