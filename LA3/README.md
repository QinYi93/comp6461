# COMP6461 LA3
*   pip install lockfile, pathlib, python-magic
*   brew install libmagic

#   Demo
##  Start router
*   .\router_x64.exe --port=3000 --drop-rate=0.2 --max-delay=100ms --seed 2387230234324

##  Start File Server
*   python ./LA2/httpfs.py -v -p 8080 -d .

##  Run Client
*   python LA1/httpc.py get -v -p 8080 "http://localhost/"
*   python LA1/httpc.py get -v -p 8080 "http://localhost/foo"
*   python LA1/httpc.py post -v -p 8080 -head Content-Type:application/json -d "{\"Assignment\":\"2\"}" "http://localhost/bar"

#   Bonus
*   python LA1/httpc.py get -v -p 8080 -head Content-disposition:inline "http://localhost/foo"
*   python LA1/httpc.py get -v -p 8080 -head Content-disposition:attachment "http://localhost/foo"
*   http://localhost:8080/foo
*   http://localhost:8080/foo?inline
*   http://localhost:8080/python
*   http://localhost:8080/python?inline

#   Test Case
*   python LA2/httpfstest.py
*   python LA2/multiwrite.py
*   python LA2/multiread.py
*   python LA2/readwrite.py

# Reference
* HTTP 1.0 Protocol
[HTTP 1.0](https://www.w3.org/Protocols/HTTP/1.0/spec.html)


# Requirements
* Python 3.6.2
* IDE: PyCharm
