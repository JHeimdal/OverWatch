#!/usr/bin/env python3
"""
This is the data aquisition & collection program for
my cleverhome
"""
import numpy as np
import socketserver

def getValues():
    """ Returns some random data to use as data for viewer """
    inTemp=20.
    outTemp=-2.
    inHD=67
    outHD=30
    outPress=998
    ret_frm="InTemp:{},OutTemp:{},InHD:{},OutHD:{},OutPress:{}"
    np.random.seed()
    return ret_frm.format(inTemp+3*(np.random.rand()-0.5),\
                          outTemp+5*(np.random.rand()-0.7),\
                          inHD+5*(np.random.rand()-0.5),\
                          outHD+2*(np.random.rand()-0.5),\
                          outPress+10*(np.random.rand()-0.5))

class DummyDAQ(socketserver.BaseRequestHandler):
    """ This is a dummy data server for programming and testing purpous """
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        cmd,*arg = self.data.decode().split()
        if cmd=='GetTemp':
            if arg[0].lower()=='all':
                self.request.sendall("InTemp:19.2,OutTemp:-2.1".encode())
            elif arg[0].lower()=='in':
                self.request.sendall("InTemp:19.1".encode())
        elif cmd=='GetPress':
            if arg[0].lower()=='all':
                self.request.sendall("OutPress:986".encode())
        elif cmd=='Update':
            ret_dat = getValues()
            self.request.sendall(ret_dat.encode())

if __name__ == '__main__':
    ip_port = '127.0.0.1',9995

    server = socketserver.TCPServer(ip_port, DummyDAQ)
    server.serve_forever()
