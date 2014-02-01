"""
SocksiPy + urllib.request handler

version: 0.3
author: Andy Haden

original author (version 0.2): e<e@tr0ll.in> 

This module provides a Handler which you can use with urllib.request to allow it to tunnel your connection through a socks.sockssocket socket, with out monkey patching the original socket...
"""

import urllib.request
import http.client
import socks

class SocksiPyHTTPConnection(http.client.HTTPConnection):
    def __init__(self, *args, **kwargs):
        self.proxyargs = kwargs['proxyargs']
        del kwargs['proxyargs']

        http.client.HTTPConnection.__init__(self, *args, **kwargs)

    def connect(self):
        self.sock = socks.socksocket()
        self.sock.setproxy(**self.proxyargs)
        if type(self.timeout) in (int, float):
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))

class SocksiPyHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        self.proxyargs = kwargs['proxyargs']
        del kwargs['proxyargs']

        http.client.HTTPSConnection.__init__(self, *args, **kwargs)

    def connect(self):
        sock = socks.socksocket()
        sock.setproxy(**self.proxyargs)
        if type(self.timeout) in (int, float):
            sock.settimeout(self.timeout)
        sock.connect((self.host, self.port))
        self.sock = self._context.wrap_socket(sock)

class SocksiPyHTTPHandler(urllib.request.HTTPHandler):
    def __init__(self, proxyargs):
        self.proxyargs = proxyargs
        urllib.request.HTTPHandler.__init__(self)

    def http_open(self, req):
        return self.do_open(SocksiPyHTTPConnection, req, proxyargs=self.proxyargs)

class SocksiPyHTTPSHandler(urllib.request.HTTPSHandler):
    def __init__(self, proxyargs, *args, **kwargs):
        self.proxyargs = proxyargs
        self.args = args
        self.kwargs = kwargs
        urllib.request.HTTPSHandler.__init__(self, *args, **kwargs)

    def https_open(self, req):
        return self.do_open(SocksiPyHTTPSConnection, req, *self.args, proxyargs=self.proxyargs, **self.kwargs)

if __name__ == "__main__":
    proxyargs = {'proxy_type':socks.PROXY_TYPE_SOCKS4, 'addr':"127.0.0.1", 'port':9050}
    opener = urllib.request.build_opener(SocksiPyHTTPHandler(proxyargs),
                                         SocksiPyHTTPSHandler(proxyargs))
    req = urllib.request.Request("http://icanhazip.com/")
    print(opener.open(req).read())
