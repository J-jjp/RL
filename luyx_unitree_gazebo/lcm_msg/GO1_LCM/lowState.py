"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class lowState(object):
    __slots__ = ["timecount", "jpFB", "jvFB", "jtFB", "jCmd", "rpy", "angularV", "linearV", "twistCmd", "footForce", "contactFlag"]

    __typenames__ = ["int64_t", "float", "float", "float", "float", "float", "float", "float", "float", "int16_t", "boolean"]

    __dimensions__ = [None, [12], [12], [12], [12], [3], [3], [3], [3], [4], [4]]

    def __init__(self):
        self.timecount = 0
        self.jpFB = [ 0.0 for dim0 in range(12) ]
        self.jvFB = [ 0.0 for dim0 in range(12) ]
        self.jtFB = [ 0.0 for dim0 in range(12) ]
        self.jCmd = [ 0.0 for dim0 in range(12) ]
        self.rpy = [ 0.0 for dim0 in range(3) ]
        self.angularV = [ 0.0 for dim0 in range(3) ]
        self.linearV = [ 0.0 for dim0 in range(3) ]
        self.twistCmd = [ 0.0 for dim0 in range(3) ]
        self.footForce = [ 0 for dim0 in range(4) ]
        self.contactFlag = [ False for dim0 in range(4) ]

    def encode(self):
        buf = BytesIO()
        buf.write(lowState._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">q", self.timecount))
        buf.write(struct.pack('>12f', *self.jpFB[:12]))
        buf.write(struct.pack('>12f', *self.jvFB[:12]))
        buf.write(struct.pack('>12f', *self.jtFB[:12]))
        buf.write(struct.pack('>12f', *self.jCmd[:12]))
        buf.write(struct.pack('>3f', *self.rpy[:3]))
        buf.write(struct.pack('>3f', *self.angularV[:3]))
        buf.write(struct.pack('>3f', *self.linearV[:3]))
        buf.write(struct.pack('>3f', *self.twistCmd[:3]))
        buf.write(struct.pack('>4h', *self.footForce[:4]))
        buf.write(struct.pack('>4b', *self.contactFlag[:4]))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != lowState._get_packed_fingerprint():
            raise ValueError("Decode error")
        return lowState._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = lowState()
        self.timecount = struct.unpack(">q", buf.read(8))[0]
        self.jpFB = struct.unpack('>12f', buf.read(48))
        self.jvFB = struct.unpack('>12f', buf.read(48))
        self.jtFB = struct.unpack('>12f', buf.read(48))
        self.jCmd = struct.unpack('>12f', buf.read(48))
        self.rpy = struct.unpack('>3f', buf.read(12))
        self.angularV = struct.unpack('>3f', buf.read(12))
        self.linearV = struct.unpack('>3f', buf.read(12))
        self.twistCmd = struct.unpack('>3f', buf.read(12))
        self.footForce = struct.unpack('>4h', buf.read(8))
        self.contactFlag = map(bool, struct.unpack('>4b', buf.read(4)))
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if lowState in parents: return 0
        tmphash = (0x2a8a6efad61242a9) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if lowState._packed_fingerprint is None:
            lowState._packed_fingerprint = struct.pack(">Q", lowState._get_hash_recursive([]))
        return lowState._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

