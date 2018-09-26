from wifi import Cell, Scheme

ROBOT = "Sophia"
SSID = "sophia wifi"
PASSWORD = "wifi pwd"

def connect_wifi(robot, ssid, password):
    scheme = Scheme.find('wlan0', robot)
    if scheme == None:
        cell = (c for c in Cell.all('wlan0') if c.ssid == ssid).next()
        scheme = Scheme.for_cell('wlan0', robot, cell, password)
        scheme.save()
    scheme.activate()
