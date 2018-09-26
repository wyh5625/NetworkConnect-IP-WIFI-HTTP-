import ipcalc
import httplib
import socket
import subprocess
import sys
import ssl

port = 44300

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
    # context = ssl.create_default_context()
    for x in ipcalc.Network(first_ip+'/'+str(subnet)):
        conn = httplib.HTTPConnection(str(x), port, timeout=0.01)
        if conn is not None:
            try:
                conn.request("GET", "/")
                r1 = conn.getresponse()
                print(x, r1.status, r1.reason)
                data = r1.read()
                print(data)
            except httplib.HTTPException as e:
                print(x, e)
            except socket.timeout as e:
                print(x, e)
            except socket.error as e:
                print(x, e)
