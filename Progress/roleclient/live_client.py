import json
import pyaudio
import socket
from threading import Thread



pausing = False

class Live_Client(object):
    def __init__(self, ip, ip2, ip3=None):
        super(Live_Client, self).__init__()
        self.ip = ip
        self.frames = []
        self.ip = json.loads(self.ip)
        self.ip2 = ip2
        self.ip3 = ip3
        self.ip2 = json.loads(self.ip2)
        self.ip3 = json.loads(self.ip3)
        self.addresses = (self.ip[0], self.ip[1])
        self.addresses2 = (self.ip2[0], self.ip2[1])
        self.addresses3 = (self.ip3[0], self.ip3[1])
        self.resume_playing()
        FORMAT = pyaudio.paInt16
        CHUNK = 1024
        self.chunk = CHUNK
        CHANNELS = 2
        RATE = 44100
        self.Audio = pyaudio.PyAudio()
        self.stream = self.Audio.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK,
                            )
        self.AudioThread = Thread(target=self.record,daemon=True)
        self.udpThread = Thread(target=self.udpStream, daemon=True)

        self.AudioThread.start()
        self.udpThread.start()

        #AudioThread.join()
        #udpThread.join()


    def udpStream(self):
        print("were live now!")
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.z1 = udp
        while True:
            if pausing:
                break
            while True:
                if pausing:
                    break
                if len(self.frames) > 0:
                    frames_mod = self.frames.pop(0)
                    self.z1.sendto(frames_mod, self.addresses)
                    self.z1.sendto(frames_mod, self.addresses2)
                    self.z1.sendto(frames_mod, self.addresses3)
        print("closing socket")
        udp.close()
        print(f'udp: {self.udpThread.is_alive()}')

    def record(self):
        while True:
            if pausing:
                break
            self.frames.append(self.stream.read(self.chunk))
        print("closing recording")
        self.stream.stop_stream()
        self.stream.close()
        self.Audio.terminate()
        print(f'audio: {self.AudioThread.is_alive()}')


    def stop_playing(self):
        global pausing
        pausing = True
        print("pausing")

    def resume_playing(self):
        global pausing
        pausing = False




