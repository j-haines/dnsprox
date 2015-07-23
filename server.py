import socket
import socketserver

from handler import DNSRequestHandler


class DNSServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    def __init__(self, opts, *args, **kwargs):
        self.opts = opts

        bind = (opts.bind_addr, opts.bind_port)
        use_ipv6 = opts.use_ipv6

        print('[+] Starting dnsproxy on {0}:{1}...'.format(*bind))
        self.address_family = socket.AF_INET6 if use_ipv6 else socket.AF_INET
        super().__init__(bind, DNSRequestHandler, *args, **kwargs)
