import pyaudio
import socket
from threading import Thread

frames = []

def udpStream(CHUNK):

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(("127.0.0.1", 12345))

    while True:
        soundData, addr = udp.recvfrom(CHUNK*CHANNELS*2)
        frames.append(soundData)
        if len(frames) > 0 :
            print("there is a signal")
    stop1 = udp.close()

def play(stream, CHUNK):
    BUFFER = 10
    while True:
            if len(frames) == BUFFER:
                while True:
                    try:
                        stream.write(frames.pop(0),CHUNK,)

                    except:
                        break
                 
if __name__ == "__main__":
    FORMAT = pyaudio.paInt16
    CHUNK = 1024
    CHANNELS = 2
    RATE = 44100

    Audio = pyaudio.PyAudio()

    stream = Audio.open(format=FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    output = True,
                    frames_per_buffer = CHUNK,
                    )

    udpThread  = Thread(target = udpStream, args=(CHUNK,))
    AudioThread  = Thread(target = play, args=(stream, CHUNK,))
    udpThread .start()
    AudioThread.start()
    udpThread .join()
    AudioThread.join()
