import json
import multiprocessing
import selectors
import socket
import struct
from threading import Thread

from Progress.roleclient.wav_client import Client_wave
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

mysel = selectors.DefaultSelector()
keep_running = True


class Client2_Send(QObject):
    finished = pyqtSignal()
    finished_1 = pyqtSignal()

    def __init__(self, ip=None, port=None, ip2=None, port2=None, ip3=None, port3=None, source=None):
        super(Client2_Send, self).__init__()

        self.success_connect_1 = True
        self.success_connect_2 = True
        self.success_connect_3 = True

        self.source = source
        print(self.source)

        if ip is not None and port is not None:
            self.ip = ip
            self.port = int(port)
            self.server_address = (self.ip, self.port)
        else:
            self.server_address = None
        if ip2 is not None and port2 is not None:
            self.ip2 = ip2
            self.port2 = int(port2)
            self.server_address_2 = (self.ip2, self.port2)
        else:
            self.server_address_2 = None
        if ip3 is not None and port3 is not None:
            self.ip3 = ip3
            self.port3 = int(port3)
            self.server_address_3 = (self.ip3, self.port3)
        else:
            self.server_address_3 = None

    @pyqtSlot()
    def running_all(self):
        process_1 = Thread(target=self.server1_operate, daemon=True)
        process_2 = Thread(target=self.server2_operate, daemon=True)
        process_3 = Thread(target=self.server3_operate, daemon=True)
        process_1.start()
        process_2.start()
        process_3.start()

    def server1_operate(self):
        print('connecting to {} port {}'.format(*self.server_address))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(self.server_address)
        except Exception as e:
            print(f'error--1: {e}')
            self.success_connect_1 = False
        else:
            self.success_connect_1 = True
            print("Successfully connect to 1")
        if self.success_connect_1:
            sock.setblocking(False)

            # Set up the selector to watch for when the socket is ready
            # to send data as well as when there is data to read.
            mysel.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, )
            # =========>
            # =========//////////
            self.main_operation()

    def server2_operate(self):
        try:
            print('connecting to {} port {}'.format(*self.server_address_2))
        except TypeError as e:
            pass
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock2.connect(self.server_address_2)
        except Exception as e:
            print(f'error--2: {e}')
            self.success_connect_2 = False
        else:
            self.success_connect_2 = True

        if self.success_connect_2:
            sock2.setblocking(False)
            print("Successfully connect to 2")
            # Set up the selector to watch for when the socket is ready
            # to send data as well as when there is data to read.
            mysel.register(sock2, selectors.EVENT_READ | selectors.EVENT_WRITE, )
            # =========>
            # =========//////////
            self.main_operation()

    def server3_operate(self):
        try:
            print('connecting to {} port {}'.format(*self.server_address_3))
        except:
            pass
        sock3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock3.connect(self.server_address_3)
        except Exception as e:
            print(f'error--3: {e}')
            self.success_connect_3 = False
        else:
            self.success_connect_3 = True

        if self.success_connect_3:
            sock3.setblocking(False)
            print("Successfully connect to 3")
            # Set up the selector to watch for when the socket is ready
            # to send data as well as when there is data to read.
            mysel.register(sock3, selectors.EVENT_READ | selectors.EVENT_WRITE, data=None)
            # =========>
            # =========//////////
            self.main_operation()

    def main_operation(self):
        if keep_running:
            print('waiting for I/O')
            for key, mask in mysel.select(timeout=1):
                connection = key.fileobj
                self.client_address = connection.getpeername()
                print('client({})'.format(self.client_address))
                if mask & selectors.EVENT_WRITE:
                    self.service_operate(connection)

    def service_operate(self, conn):
        data = b"xboxlive2020operate"
        pack_data = struct.pack(">i19si", 4020, data, 202304)
        conn.sendall(pack_data)
        if pack_data:
            address_1 = conn.getpeername()
            ip_add = address_1[0]
            port_add = address_1[1]
            source = self.source
            print("sending data")
            w = Client_wave(ip_add, port_add, source)
            #w.operator_wav()
            mysel.unregister(conn)
            conn.close()
            self.finished.emit()

# if __name__=='__main__':
#     Client_Send()
