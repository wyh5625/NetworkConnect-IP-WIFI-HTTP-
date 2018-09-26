import socket
import sys

ip_prefix = "192.168.1."
port = 44300
# Create a TCP/IP socket

for ad in range(1, 256):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(0.1)
    ip = ip_prefix + str(ad)
    address = (ip, port)
    try:
        client.connect(address)
        print("successfully connect to: " + str(address))
        client.close()
    except socket.error:
        print("can't connect to " + ip + ":" + str(port))

