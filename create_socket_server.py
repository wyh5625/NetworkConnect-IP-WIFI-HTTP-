import socket
import time
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "192.168.1.74"
port = 44300
address = (ip, port)
server.bind(address)
server.listen(1)
client, address = server.accept()


print("connect client successfully")
print("client addr: " + str(address))

while True:
    time.sleep(2)
    client.send("hello client")