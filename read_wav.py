import pyaudio
import wave
import sys
import simpleaudio as sa
CHUNK = 1024


# instantiate PyAudio (1)
p = pyaudio.PyAudio()

wf = wave.open("_sample_wav.wav", 'rb')

sample_width = wf.getsampwidth()
print(f"Sample width: {sample_width}")
sample_rate = wf.getframerate()
print(f"Sample rate: {sample_rate}")
channelss = wf.getnchannels()
print(f"Channels: {channelss}")
pyaud_format = p.get_format_from_width(sample_width)
print(f"Pyaudio format: {pyaud_format}")

# audio_data = wf.readframes(wf.getnframes())
# num_channels = wf.getnchannels()
# bytes_per_sample = wf.getsampwidth()
# sample_rate = wf.getframerate()
#
# play_obj = sa.play_buffer(audio_data, num_channels, bytes_per_sample, sample_rate)
# play_obj.wait_done()






# open stream (2)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# read data
data = wf.readframes(1024)
frames = []
length = wf.getnframes()
# play stream (3)
pos = wf.tell()
while len(data) > 0:
    data1 = stream.write(data)
    frames.append(data)
    data = wf.readframes(1024)
    print(pos)

print(frames)
print(len(frames))
print(length)
# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()
