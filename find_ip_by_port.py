import sys
import ipcalc
import socket
import subprocess
import ssl

if sys.version_info > (3,0):
    import http.client as client
else:
    import httplib as client


port = 44301

def get_ip_and_mask_win():
    proc = subprocess.Popen('ipconfig',stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if 'IPv4' in str(line):
            ip = str(line).split(' ')[-1].strip("'").strip("\\n").strip("\\r")
            break

    mask = proc.stdout.readline().rstrip().split(b':')[-1].replace(b' ',b'').decode()
    return ip, mask

def get_ip_and_mask_linux():
    proc = subprocess.Popen('ifconfig',stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if 'wlan0'.encode() in line:
            break
    line = proc.stdout.readline().rstrip().split()
    ip = str(line[1])
    mask = str(line[3])
    return ip, mask

def subnet_cal(mask):
    return sum([bin(int(x)).count('1') for x in '255.255.255.0'.split('.')])

if __name__ == '__main__':
    platform = sys.platform
    if 'win' in platform:
        first_ip, mask = get_ip_and_mask_win()
    elif 'linux' in platform:
        first_ip, mask = get_ip_and_mask_linux()
    subnet = subnet_cal(mask)
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    for x in ipcalc.Network(first_ip+'/'+str(subnet)):
        conn = client.HTTPSConnection(str(x), port, timeout=0.1, context=context)
        if conn is not None:
            try:
                conn.request("GET", "/")
                r1 = conn.getresponse()
                print(x, r1.status, r1.reason)
                data = r1.read()
                print(data)
            except client.HTTPException as e:
                print(x, e)
            except socket.timeout as e:
                print(x, e)
            except socket.error as e:
                print(x, e)
