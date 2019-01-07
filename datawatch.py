#!/usr/bin/env python3
"""
This is the data aquisition & collection program for
my homedata
"""
# import numpy as np
import socketserver
import time
import piplates.DAQCplate as DAQC
import Adafruit_DHT as dht


def temp_raw(addr):
    temp_sensor = "/sys/bus/w1/devices/{}/w1_slave".format(addr)
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines


def readPress():
    v = DAQC.getADC(0, 0)
    vs = DAQC.getADC(0, 8)
    return (v/vs+0.095)/0.009


def readDSB(addr):
    lines = temp_raw(addr)
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        lines = temp_raw(addr)
    temp_out = lines[1].find("t=")
    if temp_out != -1:
        temp_str = lines[1].strip()[temp_out+2:]
        return float(temp_str)/1000.0


def getValues():
    """ Read som values """
    dsb1 = "28-000005b45569"
    dsb2 = "28-000005b48527"
    dsb3 = "28-000005b49e58"
    ret_frm = "InTemp:{},InHD:{},DSB1:{},DSB2:{},DSB3:{},Press:{}"
    inhd, intemp = dht.read_retry(dht.DHT22, 16)
    return ret_frm.format(intemp,
                          inhd,
                          readDSB(dsb1),
                          readDSB(dsb2),
                          readDSB(dsb3),
                          readPress())


class DummyDAQ(socketserver.BaseRequestHandler):
    """ This is a dummy data server for programming and testing purpous """
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        cmd, *arg = self.data.decode().split()
        if cmd == 'GetTemp':
            if arg[0].lower() == 'all':
                self.request.sendall("InTemp:19.2,OutTemp:-2.1".encode())
            elif arg[0].lower() == 'in':
                self.request.sendall("InTemp:19.1".encode())
        elif cmd == 'GetPress':
            if arg[0].lower() == 'all':
                self.request.sendall("OutPress:986".encode())
        elif cmd == 'Update':
            ret_dat = getValues()
            self.request.sendall(ret_dat.encode())


if __name__ == '__main__':
    ip_port = '192.168.0.104', 9994

    server = socketserver.TCPServer(ip_port, DummyDAQ)
    server.serve_forever()
