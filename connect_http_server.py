import http.client
import socket

ip_prefix = "192.168.1."
port = 44300

for i in range(1,255):
    conn = None
    ip = ip_prefix + str(i)
    conn = http.client.HTTPConnection(ip, port, timeout=0.01)

    if conn is not None:
        try:
            conn.request("GET", "/")
            r1 = conn.getresponse()
            print(ip, r1.status, r1.reason)
            data = r1.read()
            print(data)
        except http.client.HTTPException as e:
            print(ip, e)
        except socket.timeout as e:
            print(ip, e)

