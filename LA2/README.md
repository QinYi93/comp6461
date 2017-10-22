# COMP6461 LA2

#   Demo
*   python httpc.py get -v -p 8080 "http://localhost/"
*   python httpc.py get -v -p 8080 "http://localhost/foo"
*   python httpc.py post -v -p 8080 -head Content-Type:application/json -d "{\"Assignment\":\"2\"}" "http://localhost/bar"
#   Test Case
*   python httpfstest.py
*   python multitest.py

# Reference
* HTTP 1.0 Protocol
[HTTP 1.0](https://www.w3.org/Protocols/HTTP/1.0/spec.html)


# Requirements
* Python 3.5.1
* IDE: PyCharm
