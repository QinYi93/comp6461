# COMP6461 LA1

#   Demo
*   python httpc.py get -h
*   python httpc.py post -h
*   python httpc.py get -v 'http://httpbin.org/get?course=networking&assignment=1'
*   python httpc.py post -v -head Content-Type:application/json -d '{"Assignment":"1"}' -o 'output.txt' 'http://httpbin.org/post'
*   python httpc.py post -v -head Content-Type:application/json -f 'file.json' -o 'output.txt' 'http://httpbin.org/post'
*   python httpc.py get -v 'http://httpbin.org/redirect/5'
#   Test Case
*   python httptest.py -v

# Reference
* HTTP 1.0 Protocol
[HTTP 1.0](https://www.w3.org/Protocols/HTTP/1.0/spec.html)