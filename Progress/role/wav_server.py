import struct
import time

import pyaudio
import socket
from threading import Thread


class Server_wave(object):
    def __init__(self, ip, port):
        super(Server_wave, self).__init__()
        self.frames = []
        self.chunks = 4098
        self.ip = ip
        if port is not None:
            self.port = int(port)
        self.port = 50931
        self.port_1 = 50932
        self.address = (self.ip, self.port)
        self.address_1 = (self.ip, self.port_1)
        self.done = False
        self.Audio = pyaudio.PyAudio()
        self.start_wave()

    def start_wave(self):
        self.sock = socket.socket()
        print("binding")
        self.sock.bind(self.address)
        self.recv_msg()

    def recv_msg(self):
        print("listening")
        self.sock.listen(5)
        print("receiving ")
        try:
            conn1, addr = self.sock.accept()
            data = conn1.recv(12)
            if data:
                addr1 = conn1.getpeername()
                print(f"Connected to : {addr1}")
                print("closing socket1")
                conn1.close()
                self.sock.close()
                self.running_data(conn1, data)
        except Exception as e:
            print(e)

    def running_data(self, conn, data):
        if data:
            data = struct.unpack(">iii", data)
            print(f"Pyaudio format: {data[0]}")
            print(f"Pyaudio sample rate: {data[1]}")
            print(f"Pyaudio channel: {data[2]}")
            data_1 = data[0]
            data_2 = data[1]
            data_3 = data[2]
            self.chn = data_3
            if data_1 and data_2 and data_3:

                self.stream = self.Audio.open(format=data_1,
                                              channels=data_3,
                                              rate=data_2,
                                              output=True)
                udpThread = Thread(target=self.udpStream, daemon=True)
                AudioThread = Thread(target=self.play, daemon=True)
                print("starting all")
                udpThread.start()
                AudioThread.start()
                udpThread.join()
                AudioThread.join()
            else:
                print("Invalid Data! ")

    def udpStream(self):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.bind(self.address_1)
        print("done binding udp")
        print("binding @: ", self.address_1)
        while True:
            try:
                udp.settimeout(5)
                soundData, addr = udp.recvfrom(self.chunks * self.chn * 2)
                if soundData is not b"":
                    self.frames.append(soundData)
                else:
                    print("not the data")
            except Exception as e:
                print("error: " + str(e))
                self.done = True
                self.frames.clear()
                break
        print("closing socket2")
        udp.close()

    def play(self):
        while True:
            if len(self.frames) == 0 and self.done:
                time.sleep(5)
                self.stream.stop_stream()
                if self.stream.is_stopped():
                    break
            if len(self.frames) > 0:
                while True:
                    try:
                        self.stream.write(self.frames.pop(0))
                    except:
                        break
        print("closing streaming")
        self.stream.close()
        self.Audio.terminate()

# if __name__ == "__main__":
