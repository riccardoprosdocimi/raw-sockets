# Rohit

from binascii import hexlify
import socket
import struct

from IP import IPPacket

ip_proto = socket.htons(0x0800)
sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, ip_proto)

def start():
    while True:
        pkt = sock.recvfrom(4096)[0]

        raw_ip_header = pkt[14:35]

        total_length_raw = raw_ip_header[2:4]
        (total_length,) = struct.unpack("!h", total_length_raw)
        data = pkt[35 : 35 + total_length - 20]  # header length = 20

        pkt_id_raw = raw_ip_header[5:7]
        (pkt_id,) = struct.unpack("!h", pkt_id_raw)

        ttl_raw = raw_ip_header[9:10]
        (ttl,) = struct.unpack("!c", ttl_raw)
        ttl = int(hexlify(ttl), base=16)

        protocol_raw = raw_ip_header[10:11]
        (protocol,) = struct.unpack("!c", protocol_raw)
        protocol = int(hexlify(protocol), base=16)

        checksum_raw = raw_ip_header[11:13]
        (checksum,) = struct.unpack("!h", checksum_raw)

        src_ip_raw = raw_ip_header[13:17]
        src_ip = socket.inet_ntoa(src_ip_raw)

        dst_ip_raw = raw_ip_header[17:21]
        dst_ip = socket.inet_ntoa(dst_ip_raw)

        ip_packet = IPPacket(src_ip, dst_ip, data)
        ip_packet.identification = pkt_id
        ip_packet.ttl = ttl
        ip_packet.protocol = protocol
        ip_packet.checksum = checksum