# COMP6461 LA2

#   Demo
*   python .\LA2\httpfs.py -v -p 8080 -d .
*
*   python LA1\httpc.py get -v -p 8080 "http://localhost/"
*   python LA1\httpc.py get -v -p 8080 "http://localhost/foo"
*   python LA1\httpc.py get -v -p 8080 -head Content-disposition:inline "http://localhost/foo"
*   python LA1\httpc.py get -v -p 8080 -head Content-disposition:attachment "http://localhost/foo"
*   python LA1\httpc.py post -v -p 8080 -head Content-Type:application/json -d "{\"Assignment\":\"2\"}" "http://localhost/bar"
#   Test Case
*   python LA2\httpfstest.py
*   python LA2\multitest.py

# Reference
* HTTP 1.0 Protocol
[HTTP 1.0](https://www.w3.org/Protocols/HTTP/1.0/spec.html)


# Requirements
* Python 3.5.1
* IDE: PyCharm
