import socketserver

class DNSRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        (data, socket) = self.request
        print("[+] RECV'd {data}".format(data=data))
