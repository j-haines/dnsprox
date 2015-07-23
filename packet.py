import struct

class DNSPacket(object):
    identifier = 0
    flags = int.from_bytes(b'\x81\x80', byteorder='big')
    rranswers = int.from_bytes(b'\x00\x01', byteorder='big')
    rrauthority = int.from_bytes(b'\x00\x00', byteorder='big')
    rradditional = int.from_bytes(b'\x00\x00', byteorder='big')

    @property
    def qr(self):
        return (self.flags >> 0xf) & 0x1

    @property
    def opcode(self):
        return (self.flags >> 0xb) & 0xf

    @property
    def aa(self):
        return (self.flags >> 0xa) & 0x1

    @property
    def tc(self):
        return (self.flags >> 0x9) & 0x1

    @property
    def rd(self):
        return (self.flags >> 0x8) & 0x1

    @property
    def ra(self):
        return (self.flags >> 0x7) & 0x1

    @property
    def rcode(self):
        return self.flags & 0xf

    def pack(self):
        return struct.pack('!HHHH', self.identifier, self.flags)