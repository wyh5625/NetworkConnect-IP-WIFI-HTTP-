import subprocess
import sys
# for windows
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
        ip, mask = get_ip_and_mask_win()
    elif 'linux' in platform:
        ip, mask = get_ip_and_mask_linux()
    subnet = subnet_cal(mask)
    print(ip)
    print(subnet)
