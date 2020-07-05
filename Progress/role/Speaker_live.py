import socket

import pyaudio
#import socket
from threading import Thread

not_operating = False

class Speaker_Live(object):
    def __init__(self,ip = None, port = None):
        super(Speaker_Live, self).__init__()
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        chunks =1024
        self.format = FORMAT
        self.rate = RATE
        self.channels = CHANNELS
        self.chunks = chunks
        self.frames = []
        print("Speaker is ready to live!")
        self.ip = ip
        if port is not None:
            self.port = int(port)

        self.address = (self.ip, self.port)
        print(f"Live at : {self.address}")
        self.resuming()
        self.initialize_speaker()



    def initialize_speaker(self):
        self.Audio = pyaudio.PyAudio()

        stream = self.Audio.open(format=self.format,
                            channels=self.channels,
                            rate=self.rate,
                            output=True,
                            frames_per_buffer=self.chunks,
                            )

        self.udpThread = Thread(target=self.udpStream, daemon=True)
        self.AudioThread = Thread(target=self.play, args=(stream,), daemon=True)
        self.udpThread.start()
        self.AudioThread.start()
        self.udpThread.join()
        self.AudioThread.join()


    def udpStream(self):
        global not_operating
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            udp.bind(self.address)
        except:
            print("error")
        udp.settimeout(5)
        while True:
            try:
                soundData ,addr = udp.recvfrom(self.chunks*self.channels*2)
                self.frames.append(soundData)
                if soundData !=b'':
                    self.resuming()
                    #print("data")
                    pass
                    #print(self.AudioThread.is_alive())
                else:
                    print('no data')
            except Exception as e:
                print(f"error9: {e}")
                not_operating = True
                break
        print("closing connection")
        udp.close()


    def play(self,stream):
        BUFFER = 10
        while True:
            if not_operating:
                break
            if len(self.frames) == BUFFER:
                while True:
                    try:
                        print('writing')
                        stream.write(self.frames.pop(0), self.chunks)
                    except:
                        break

        print("stop streaming")
        stream.stop_stream()
        stream.close()
        self.Audio.terminate()


    def resuming(self):
        global not_operating
        not_operating = False
# if __name__ == "__main__":
#
#     HOST = "127.0.0.1"
#     PORT = 59302
#     CHUNK = 1024
#
#     speaker = Speaker_Live(HOST, PORT,CHUNK)


    # Audio = pyaudio.PyAudio()
    #
    # stream = Audio.open(format=FORMAT,
    #                 channels = CHANNELS,
    #                 rate = RATE,
    #                 output = True,
    #                 frames_per_buffer = CHUNK,
    #                 )
    #
    # udpThread  = Thread(target = udpStream, args=(CHUNK,))
    # AudioThread  = Thread(target = play, args=(stream, CHUNK,))
    # udpThread .start()
    # AudioThread.start()
    # udpThread .join()
    # AudioThread.join()
