import socket
import socketserver

from dnslib import DNSRecord, DNSError

from rules import RulesManager


class DNSRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        record = None
        (data, socket) = self.request
        try:
            record = self._parse_data(data)
        except DNSError:
            print("[e] Failed to parse packet -- skipping")
            return
        label = record.get_q().get_qname()
        domain = '.'.join([p.decode('ascii') for p in label.label])
        zones = RulesManager.match(label)

        reply = record.reply()

        if not zones:
            print("[i] No matching rule for {domain}".format(domain=domain))
            reply = self._forward_request(reply)
        else:
            print("[i] Found matching rule for {domain}".format(domain=domain))
            for zone in zones:
                reply.add_answer(zone)

        socket.sendto(reply.pack(), self.client_address)

    def _forward_request(self, reply):
        data = self.request[0]
        dns_host = self.server.opts.dns_server
        dns_port = self.server.opts.dns_port

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(30)
        s.sendto(data, (dns_host, dns_port))
        resp = s.recv(1024)
        s.close()

        try:
            record = self._parse_data(resp)
        except DNSError:
            print("[e] Failed to parse response")

        for answer in record.rr:
            reply.add_answer(answer)

        return reply

    def _parse_data(self, data):
        return DNSRecord.parse(data)
