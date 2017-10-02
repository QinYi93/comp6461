import unittest
from http import http

class TestHTTPMethods(unittest.TestCase):

    def test_get(self):
        h = http("http://httpbin.org/get?course=networking&assignment=1")
        h.setType('get')
        h.constructContent()
        reply = h.send()
        self.assertEqual(reply.state, '200')

    def test_post_request(self):
        body = '{"Assignment":"1"}'
        h = http("http://httpbin.org/post")
        h.setType('post')
        h.setData(body)
        h.addHeader("Content-Type", "application/json")
        h.addHeader("Content-Length",str(len(body)))
        h.constructContent()
        reply = h.send()
        print(reply.headMap)
        print(reply.body)
        self.assertEqual(reply.state, '200')
    
    def test_redirect(self):
        h = http("http://httpbin.org/redirect/5")
        h.setType('get')
        h.constructContent()
        reply = h.send()
        self.assertEqual(reply.state, '200')

        
if __name__ == '__main__':
    unittest.main()