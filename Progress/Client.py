import json
import multiprocessing
import selectors
import socket
import struct
from threading import Thread

from Progress.roleclient.live_client import Live_Client
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

mysel = selectors.DefaultSelector()
keep_running = True


class Client_Send(QObject):
    finished1 = pyqtSignal()

    def __init__(self, ip=None, port=None, ip2=None, port2=None, ip3=None, port3=None):
        super(Client_Send, self).__init__()

        self.success_connect_1 = True
        self.success_connect_2 = True
        self.success_connect_3 = True

        if ip != None and port != None:
            self.ip = ip
            self.port = int(port)
            self.server_address = (self.ip, self.port)
        else:
            self.server_address = None
        if ip2 != None and port2 != None:
            self.ip2 = ip2
            self.port2 = int(port2)
            self.server_address_2 = (self.ip2, self.port2)
        else:
            self.server_address_2 = None
        if ip3 != None and port3 != None:
            self.ip3 = ip3
            self.port3 = int(port3)
            self.server_address_3 = (self.ip3, self.port3)
        else:
            self.server_address_3 = None

    @pyqtSlot()
    def running_all(self):
        thread_1 = Thread(target=self.server1_operate, daemon=True)
        thread_2 = Thread(target=self.server2_operate, daemon=True)
        thread_3 = Thread(target=self.server3_operate, daemon=True)
        thread_1.start()
        thread_2.start()
        thread_3.start()

        # self.server1_operate()
        # self.server2_operate()
        # self.server3_operate()

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
            mysel.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, data=None)
            # =========>
            # =========//////////
            self.main_operation()

    def server2_operate(self):
        print('connecting to {} port {}'.format(*self.server_address_2))
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
            mysel.register(sock2, selectors.EVENT_READ | selectors.EVENT_WRITE, data=self.service_bluff)
            # =========>
            # =========//////////
            self.main_operation_bluff()

    def server3_operate(self):
        print('connecting to {} port {}'.format(*self.server_address_3))
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
            mysel.register(sock3, selectors.EVENT_READ | selectors.EVENT_WRITE, data=self.service_bluff)
            # =========>
            # =========//////////
            self.main_operation_bluff()

    def main_operation(self):
        if keep_running:
            print('waiting for I/O')
            for key, mask in mysel.select(timeout=1):
                connection = key.fileobj
                self.client_address = connection.getpeername()
                print('client({})'.format(self.client_address))
                if mask & selectors.EVENT_WRITE:
                    self.service_operate(connection)

    def main_operation_bluff(self):
        if keep_running:
            print('waiting for I/O')
            for key, mask in mysel.select(timeout=1):
                callback = key.data
                callback(key.fileobj, mask)

    def service_bluff(self, key, mask):
        sock = key
        if mask & selectors.EVENT_WRITE:
            self.service_operate_bluff(sock)
        # print('shutting down')
        # mysel.unregister(connection)
        # connection.close()
        # mysel.close()

    def service_operate(self, conn):
        data = b'logarithmic'
        pack_data = struct.pack(">ii11s", 32, 2319, data)
        conn.sendall(pack_data)
        if pack_data:
            json_ser1 = json.dumps(self.server_address)
            json_ser2 = json.dumps(self.server_address_2)
            json_ser3 = json.dumps(self.server_address_3)
            Live_Client(json_ser1, json_ser2, json_ser3)
            mysel.unregister(conn)
            conn.close()
            self.finished1.emit()

    def service_operate_bluff(self, conn):
        data = b'logarithmic'
        pack_data = struct.pack(">ii11s", 32, 2319, data)
        conn.sendall(pack_data)
        if pack_data:
            print("done123")
            mysel.unregister(conn)
            conn.close()
            # self.finished1.emit()

# if __name__=='__main__':
#     Client_Send()
