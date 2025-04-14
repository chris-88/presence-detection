import socket
import struct
import network

AP_IP = "192.168.4.1"

def start_dns_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', 53))
    print('DNS server listening on UDP 53')

    while True:
        try:
            data, addr = s.recvfrom(512)
            if data:
                # Build DNS response
                transaction_id = data[:2]
                flags = b'\x81\x80'
                qdcount = data[4:6]
                ancount = qdcount
                nscount = b'\x00\x00'
                arcount = b'\x00\x00'
                dns_header = transaction_id + flags + qdcount + ancount + nscount + arcount
                dns_question = data[12:]
                dns_answer = b'\xc0\x0c' + b'\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'
                dns_answer += socket.inet_aton(AP_IP)
                response = dns_header + dns_question + dns_answer
                s.sendto(response, addr)
        except Exception as e:
            print('DNS server error:', e)
