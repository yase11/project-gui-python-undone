import pyaudio
import socket
from threading import Thread
import wave
import struct
from multiprocessing import Process
from PyQt5.QtCore import QObject, pyqtSignal
from pydub import AudioSegment

pausing = False

class Client_wave(QObject):
    done = True
    def __init__(self, ip, port, source):
        super(Client_wave, self).__init__()
        self.resume_play()
        self.done = False
        self.ip = ip
        if port is not None:
            self.port = int(port)
        self.port = 50931
        self.port_1 = 50932
        self.server_address = (self.ip, self.port)
        self.server_address_1 = (self.ip, self.port_1)
        self.frames = []
        self.source = source

        self.destination = "_sample_wav.wav"

        self.chunks = 1024
        self.Audio = pyaudio.PyAudio()
        self.operator_wav()

    def operator_wav(self):
        if self.source is not None and self.destination is not None:
            # process_1 = Process(target=self.converter, daemon=True)
            # process_1.start()
            # process_1.join()
            self.converter(self.source, self.destination)
        else:
            raise print("provide source")

        print("done converting")
        wf = wave.open(self.destination, 'rb')
        sample_width = wf.getsampwidth()
        print(f"Sample width: {sample_width}")
        sample_rate = wf.getframerate()
        print(f"Sample rate: {sample_rate}")
        channels = wf.getnchannels()
        print(f"Channels: {channels}")
        pyaudio_format = self.Audio.get_format_from_width(sample_width)
        print(f"Format: {pyaudio_format}")
        self.send_info(pyaudio_format, sample_rate, channels)
        nu_frames = wf.getnframes()
        print(f"No. of frames : {nu_frames}")
        wf.close()
        # process_2 = Process(target=self.processing_init, daemon=True)
        # process_2.start()
        # process_2.join()
        self.processing_init()
        print("done processing")



    def processing_init(self):
        # Initialize Threads
        udpThread = Thread(target=self.udpStream, daemon=True)
        AudioThread = Thread(target=self.record, daemon=True)
        udpThread.start()
        AudioThread.start()
        AudioThread.join()
        udpThread.join()

    def converter(self, src, dst):
        sound = AudioSegment.from_file(src)
        sound = sound.set_frame_rate(24000)
        sound = sound.set_sample_width(2)
        sound = sound.set_channels(1)
        sound.export(dst, format="wav")

    def udpStream(self):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            if pausing:
                break
            if len(self.frames) > 0:
                z = self.frames.pop(0)
                if z == b'':
                    self.done = True
                    break
                else:
                    udp.sendto(z, self.server_address_1)
        print("closing socket")
        udp.close()

    def record(self):
        with wave.open(self.destination, 'rb') as wf:
            data = wf.readframes(self.chunks)
            while True:
                if pausing:
                    break
                if self.done:
                    break
                self.frames.append(data)
                data = wf.readframes(self.chunks)
        print("done reading wav")
        wf.close()


    def send_info(self, format_py, sample_rate, channels):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(self.server_address)
        file_info = struct.pack(">iii", format_py, sample_rate, channels)
        sock.send(file_info)
        print("format is send!")
        sock.close()

    def stop_play(self):
        global pausing
        pausing = True

    def resume_play(self):
        global pausing
        pausing = False

# if __name__ == "__main__":
