import selectors
import socket
import struct
import types
from threading import Thread

sel = selectors.DefaultSelector()

from Progress.role.Speaker_live import Speaker_Live
from Progress.role.wav_server import Server_wave

on_data = True

class Server_Operation(object):
    def __init__(self, host, port):
        super(Server_Operation, self).__init__()
        self.host = host
        self.port = port

    def create_server(self):
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.setblocking(False)
        lsock.bind((self.host, self.port))
        lsock.listen(5)
        print('listening on', (self.host, self.port))
        sel.register(lsock, selectors.EVENT_READ, data=self.accept_connection)
        thread_run = Thread(target=self.run_program, daemon=True)
        thread_run.start()
        thread_run.join()
        #self.run_program()

    def accept_connection(self,sock, mask):
        conn, self.addr = sock.accept()  # Should be ready to read
        print(f"Connection established from:  {self.addr}")
        conn.setblocking(False)
        select_events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, select_events, data=self.service_connection)

    def service_connection(self, key, mask):
        sock = key
        if mask & selectors.EVENT_READ:
            self.read_handler(sock)
        #if mask & selectors.EVENT_WRITE:
            #self.write_handler(sock)

    def run_program(self):
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                callback = key.data
                callback(key.fileobj,mask)

    def read_handler(self, sock):
        global on_data
        try:
            recv_data = sock.recv(1024)
            if len(recv_data) > 0:
                on_data =True
        except Exception as e:
            sel.unregister(sock)
            sock.close()
            on_data =False
        if on_data:
            data_len = len(recv_data)
            if data_len == 27:
                try:
                    un_pack = struct.unpack(">i19si" ,recv_data)
                    data_1 = un_pack[0]
                    data_1 = int(data_1)
                    data_2 = un_pack[2]
                    data_2 = int(data_2)
                    data_3 = un_pack[1].decode()
                    if data_1 == 4020 and data_2 == 202304 and data_3[9:17] == "020opera":
                        print("Connected at 2")
                        w2 = Server_wave(self.host, self.port)
                        sel.unregister(sock)
                        sock.close()
                except Exception as e:
                    print(f"the message is wrong 2: {e}")
                    sel.unregister(sock)
                    sock.close()
            elif data_len == 19:
                try:
                    un_pack = struct.unpack(">ii11s" ,recv_data)
                    data_1 = un_pack[0]
                    data_1 = int(data_1)
                    data_2 = un_pack[1]
                    data_2 = int(data_2)
                    data_3 = un_pack[2].decode()
                    if data_1 == 32 and data_2 == 2319 and data_3[4:9]=="rithm":
                        print('Connected at 1')
                        #print(ip_port)
                        #ip_add = ip_port[0]
                        #port_add = ip_port[1]
                        w1 = Speaker_Live(self.host, self.port)
                        sel.unregister(sock)
                        sock.close()
                except Exception as e:
                    print(f"the message is wrong: {e}")
                    sel.unregister(sock)
                    sock.close()

        # else:
        #     print('closing connection')
        #     sel.unregister(sock)
        #     sock.close()



if __name__ == "__main__":

    host = "127.0.0.1"
    port = 59302
    # HOST = "127.0.0.1"
    # PORT = 12345
    # CHUNK = 1024

    server = Server_Operation(host, port)
    server.create_server()
